from enum import Enum

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

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props)

    def to_html(self):
        if (self.value == None or self.value == "") and self.tag != "br":
            raise ValueError("LeafNodes must have a value!") # Except BR tags...
        if self.tag == None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
