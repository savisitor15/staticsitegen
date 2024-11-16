from textnode import TextType, TextNode

TextToTag = {
    TextType.TEXT : "",
    TextType.BOLD : "b",
    TextType.ITALIC : "i",
    TextType.LINK : "a",
    TextType.CODE : "code",
    TextType.IMAGE : "img"
}

class HTMLNode(object):
    def __init__(self, tag = None, value = None, props = None, children = None):
        self.tag = tag
        self.value = value
        self.props = props
        self.children = children

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        out = ""
        if self.props != None:
            for k,v in self.props.items():
                out += f' {k}="{v}"'
        return out
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, props={self.props}, children={self.children})"
    
    def __eq__(self, value: 'HTMLNode') -> bool:
        return self.tag == value.tag and self.children == value.children and self.props == value.props and self.value == value.value

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props)

    def to_html(self):
        if (self.value == None) and self.tag != "br":
            raise ValueError("LeafNodes must have a value!") # Except BR tags...
        if self.tag == None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, props=props, children=children)

    def _output_children_html(self, children):
        if len(children) == 0:
            return ""
        return f"{children[0].to_html()}{self._output_children_html(children[1:])}"

    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError("Parent - tag invalid")
        if self.children == None or len(self.children) == 0:
            raise ValueError("Parent - no children")
        return f"<{self.tag}>{self._output_children_html(self.children)}</{self.tag}>"

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

