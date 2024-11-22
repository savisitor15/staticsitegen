from blocknode import BlockType, BlockNode
from htmlnode import ParentNode, HTMLNode, LeafNode
from textcommon import text_node_to_html_node, text_to_textnodes
import re

def markdown_to_blocks(markdown: str) -> list[str]:
    """This routine splits a documents into identifyable blocks of markdown seperated by new lines"""
    if len(markdown) <= 0:
        raise ValueError("No document supplied!")
    orig_blocks = markdown.split("\n\n")
    blocks = list()
    for block in orig_blocks:
        if len(block.strip()) == 0:
            continue
        else:
            block = '\n'.join([x.strip() for x in block.split('\n')])
            blocks.append(block.strip() + "\n")
    return blocks

def block_to_block_type(input_doc: str, ) -> BlockType:
    """Assosciate a given string to block type"""
    # Patern dict
    patterns = {
        BlockType.HEADING : r"^#{1,6}\s(.*?)\n",
        BlockType.QUOTE : r"^>{1}\s?(.*?)\n",
        BlockType.ORDERED_LIST : r"^\d+.\s?(.*?)\n",
        BlockType.UNORDERED_LIST : r"^[*|-]\s?(.*?)\n",
        BlockType.CODE : r"^`{3}([\S\s]+?)\n?`{3}",
        }
    typ_list = list()
    for typ, pat in patterns.items():
        if len(re.findall(pat, input_doc)) > 0:
            typ_list.append(typ)
    if len(typ_list) > 1:
        print(typ_list)
        raise IndexError("Multiple types detected!")
    else:
        typ_list.append(BlockType.PARAGRAPH)
    return typ_list[0]

def text_to_blockChildren(markdown: str, block_type : BlockType):
    # Patern dict
    patterns = {
        BlockType.HEADING : r"(^#{1,6})\s(.*?)\n",
        BlockType.QUOTE : r"(^>{1})\s?(.*?)\n",
        BlockType.ORDERED_LIST : r"(^\d+.)\s?(.*?)\n",
        BlockType.UNORDERED_LIST : r"(^[*|-])\s?(.*?)\n",
        BlockType.CODE : r"^`{3}([\w]*)\n?([\S\s]+?)\n?`{3}",
        }
    weight = 0
    outputlist = []
    if block_type == BlockType.PARAGRAPH:
        return text_to_textnodes(markdown), weight
    matches = re.finditer(patterns[block_type],markdown, re.MULTILINE)
    for match in matches:
        ## Headings
        if block_type == BlockType.HEADING:
            weight = match.group(1).count("#",0,5)
        outputlist += text_to_textnodes(match.group(2))
    return outputlist, weight
    
    

def text_to_blocknodes(markdown: str) -> list[BlockNode]:
    raw : list =  [(x,block_to_block_type(x)) for x in markdown_to_blocks(markdown)]
    # Parse and create the nodes
    outlist = []
    for item in raw:
        children, weight = text_to_blockChildren(item[0], item[1])
        outlist.append(BlockNode(children, item[1], weight))
    return outlist

def extract_title(markdown):
    """Find the first 1 weight HEADING"""
    pat = r"(#)\s(.*?)\n"
    matches = re.finditer(pat, markdown)
    for match in matches:
        return match.group(2)
    return None



def block_to_htmlnode(block_node: BlockNode) -> HTMLNode:
    """Convert block nodes to their corrosponding html nodes"""
    children=[text_node_to_html_node(x) for x in block_node.children]
    match block_node.block_type:
        case BlockType.PARAGRAPH:
            return ParentNode("p", children)
        case BlockType.HEADING:
            return LeafNode(f"h{block_node.get_weight()}",block_node.children[0].text)
        case BlockType.CODE:
            return ParentNode("pre", [ParentNode("code", children)])
        case BlockType.QUOTE:
            return ParentNode("blockquote", children)
        case BlockType.UNORDERED_LIST:
            ## This one requires some manual work
            children = [ParentNode("li", [x]) for x in children]
            return ParentNode("ul", children)
        case BlockType.ORDERED_LIST:
            children = [ParentNode("li", [x]) for x in children]
            return ParentNode("ol", children)
        
def blocks_to_html(block_nodes: list[BlockNode]) -> ParentNode:
    return ParentNode("div", [block_to_htmlnode(x) for x in block_nodes])


