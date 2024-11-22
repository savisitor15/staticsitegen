from enum import Enum
from htmlnode import HTMLNode
from textnode import TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code_block"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

class BlockNode(object):
    def __init__(self, children: list[TextNode], block_type:BlockType, weight = 0) -> "BlockNode":
        ### Weight is only really used for headings
        self._weight = weight
        ## Do some checking
        if block_type == BlockType.CODE:
            check_list = children.copy()
            for index, item in enumerate(check_list):
                if item.text_type == TextType.CODE:
                    ## Don't support nested code lines
                    children[index] = TextNode(item.text, TextType.TEXT, item.url)
        self.children = children
        self.block_type = block_type

    def __eq__(self, other:"BlockNode"):

        return self.children == other.children and self.block_type == other.block_type
    
    def __repr__(self) -> str:
        out = [str(x) for x in self.children]
        return f"BlockType({out}, {self.block_type})"

    def get_weight(self) -> int:
        return self._weight