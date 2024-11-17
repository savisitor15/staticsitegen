from textnode import TextType, TextNode, TEXT_DELIMITERS
from enum import Enum
from htmlnode import LeafNode


class NodeType(Enum):
    HTML = "html"
    LEAF = "leaf"
    TEXT = "text"

TextToTag = {
    TextType.TEXT : "",
    TextType.BOLD : "b",
    TextType.ITALIC : "i",
    TextType.LINK : "a",
    TextType.CODE : "code",
    TextType.IMAGE : "img"
}


def text_node_to_html_node(text_node: TextNode):
    """Convert Text node to LeafNode"""
    match text_node.text_type:
        case TextType.TEXT | TextType.BOLD | TextType.ITALIC | TextType.CODE:
            tag = TextToTag[text_node.text_type]
            value = text_node.text
            return LeafNode(tag, value)
        case TextType.IMAGE:
            tag = TextToTag[text_node.text_type]
            return LeafNode(tag, "", {"src": text_node.url, "alt": text_node.text})
        case TextType.LINK:
            tag = TextToTag[text_node.text_type]
            return LeafNode(tag, text_node.text, {"href": text_node.url})
        case _:
            raise ValueError(f"{text_node.text_type} Not supported!")


import re

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """Get the image tuple"""
    # images GROUP 1 = Alt Text GROUP 2 = URL
    regex_pat = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex_pat, text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """Get the link tuple list"""
    regex_pat = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex_pat, text)


def split_nodes_delimiter(old_nodes: list[TextNode], output_type: TextType,) -> list[TextNode]:
    """Split out delimited text from an original text node. Preserving order"""
    if type(old_nodes) is not list:
        raise TypeError("Old_nodes must be a list of TextNode!")
    match output_type:
        case TextType.BOLD:
            regex_pat = r"\*\*(.*?)\*\*"
        case TextType.ITALIC:
            regex_pat = r"\*(.*?)\*"
        case TextType.CODE:
            regex_pat = "\\`(.*?)\\`"
        case TextType.IMAGE:
            regex_pat = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
        case TextType.LINK:
            regex_pat = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
        case _:
            raise ValueError("Unknown Output Type!")
    # Extract the contained markup list
    output_list = list()
    for item in old_nodes:
        source_str = item.text
        matches = re.finditer(regex_pat, source_str)
        last_match_end = 0
        for match in matches:
            # extract the match from the source string
            if last_match_end < match.start():
                # This is a second match and there's source text between!
                output_list.append(TextNode(source_str[last_match_end:match.start()], item.text_type, item.url or None))
            # The extracted match
            if output_type == TextType.IMAGE or output_type == TextType.LINK:
                output_list.append(TextNode(match.group(1), output_type, match.group(2)))
                print(f"Testing! ->> {match.groups()}")
            else:
                output_list.append(TextNode(match.group(1), output_type))
            last_match_end = match.end()
        if last_match_end < len(source_str):
            output_list.append(TextNode(source_str[last_match_end:], item.text_type, item.url or None))
    return output_list

def split_text_nodes_nested(old_nodes: list[TextNode], )->list[TextNode]:
    """This routine calls split_nodes_delimiter in the correct order to safely expand all text nodes not Links and Images that may be nested.
    IMAGES -> LINKS -> BOLD -> ITALIC -> CODE
    """
    new_nodes = old_nodes.copy()
    order = [TextType.IMAGE, TextType.LINK, TextType.BOLD, TextType.ITALIC, TextType.CODE]
    for it in order:
        new_nodes = split_nodes_delimiter(new_nodes, it)
    return new_nodes

        

