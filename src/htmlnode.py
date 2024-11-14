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
        for k,v in self.props.items():
            out += f' {k}="{v}"'
        return out
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, props={self.props}, children={self.children})"
