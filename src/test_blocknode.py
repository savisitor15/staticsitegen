import unittest
from textnode import TextNode, TextType
from textcommon import text_to_textnodes
from blocknode import BlockNode, BlockType

HEADING_TEXT = "# This is a 1 heading"
UPPER_MOST_HEADING_TEST = "###### This is a level 6 heading"
PARA_TEXT = "Here we have a standard paragraph\nMulti-lined for testing\nAnd showing support for entire doc_strings\n"


class TestBlockNode(unittest.TestCase):
    def test_blocknode(self):
        """Basic self test"""
        node = BlockNode(text_to_textnodes(PARA_TEXT), BlockType.PARAGRAPH)
        self.assertEqual(node.block_type, BlockType.PARAGRAPH)
        self.assertEqual(node.children, text_to_textnodes(PARA_TEXT))
                         
    def test_eq(self):
        """Test eqaulity"""
        node1 = BlockNode([TextNode(PARA_TEXT, TextType.TEXT)], BlockType.PARAGRAPH)
        node2 = BlockNode([TextNode(PARA_TEXT, TextType.TEXT)], BlockType.PARAGRAPH)
        self.assertEqual(node1, node2)

    def test_neq(self):
        """Confirm ineqaulity"""
        node1 = BlockNode([TextNode(PARA_TEXT, TextType.TEXT)], BlockType.PARAGRAPH)
        node2 = BlockNode([TextNode(PARA_TEXT, TextType.TEXT)], BlockType.CODE)
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        """Confirm string output"""
        node = BlockNode([TextNode(HEADING_TEXT, TextType.TEXT)], BlockType.HEADING)
        expectation = f"BlockType({[str(TextNode(HEADING_TEXT, TextType.TEXT))]}, {BlockType.HEADING})"
        self.assertEqual(str(node), expectation)

    def test_weight(self):
        """Confirm weightness"""
        node = BlockNode([TextNode(UPPER_MOST_HEADING_TEST, TextType.TEXT)], BlockType.HEADING, 6)
        self.assertEqual(node.get_weight(), 6)



if __name__ == "__main__":
    unittest.main()
