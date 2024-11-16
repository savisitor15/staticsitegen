from textnode import TextType, TextNode
from htmlnode import LeafNode

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
