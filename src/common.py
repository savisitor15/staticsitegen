from blockcommon import text_to_blocknodes, blocks_to_html, extract_title
from htmlnode import ParentNode, LeafNode
from textnode import TextNode
from blocknode import BlockNode

def markdown_to_html_node(markdown:str) -> ParentNode:
    """This will return a single string of HTML from a markdown structure"""
    # Convert the markdown to block and textnodes
    blocks = text_to_blocknodes(markdown)
    if len(blocks) > 0:
        # convert the blocks to HTML
        htmlnodes = blocks_to_html(blocks)
    else:
        raise Exception("Unable to create blocks!")
    if htmlnodes:
        return htmlnodes
    
def generate_page(from_path, template_path, dest_path):
    """
    from_path -> Markdown input path
    template_path -> HTML template to use
    dest_path -> Output directory
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    raw_markdown = ""
    with open(from_path, "r") as md_fp:
        raw_markdown = md_fp.read()
    raw_template = ""
    with open(template_path, "r") as temp_fp:
        raw_template = temp_fp.read()
    # Extract the title
    title = extract_title(raw_markdown)
    raw_template = raw_template.replace(" {{ Title }} ", title)
    output_html = markdown_to_html_node(raw_markdown).to_html()
    raw_template = raw_template.replace("{{ Content }}", output_html)
    with open(dest_path, "w") as fp:
        fp.write(raw_template)



