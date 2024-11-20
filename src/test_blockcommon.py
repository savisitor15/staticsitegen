import unittest
from blocknode import BlockNode, BlockType
from textcommon import text_to_textnodes
from blockcommon import markdown_to_blocks, block_to_block_type, text_to_blocknodes

class Test_markdown_to_blocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        """Basic self test"""
        sample = """
        # This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item
        """
        expectation =[
            "# This is a heading\n",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item\n"
        ]
        self.assertEqual(markdown_to_blocks(sample), expectation)

class Test_block_to_block_type(unittest.TestCase):
    def test_block_to_block_type_H(self):
        """Basic self test Heading"""
        sample = "# This is a heading\n"
        self.assertEqual(block_to_block_type(sample), BlockType.HEADING)

    def test_block_to_block_type_P(self):
        sample = "This is a complex\nParagraph structure\nwith multiple lines\n"
        self.assertEqual(block_to_block_type(sample), BlockType.PARAGRAPH)

    def test_block_to_block_type_Q(self):
        sample = ">This is a valid qoute string\n"
        self.assertEqual(block_to_block_type(sample), BlockType.QUOTE)

    def test_block_to_block_type_C(self):
        sample1 = "```\ncode block section\n```"
        sample2 = "```code\nblock\nsection\n```"
        self.assertEqual(block_to_block_type(sample1), BlockType.CODE)
        self.assertEqual(block_to_block_type(sample2), BlockType.CODE)

    def test_block_to_block_type_UL(self):
        sample1 = "* Unordered list Item 1\n* Unordered List item 2\n* unordered list item 3\n"
        sample2 = "- Unordered list item 1\n- Unordered list item 2\n- Unordered list item 3\n"
        self.assertEqual(block_to_block_type(sample1), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(sample2), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_OL(self):
        sample = "1. Ordered list Item 1\n2. Ordered list Item 2\n3. Ordered list Item 3\n"
        self.assertEqual(block_to_block_type(sample), BlockType.ORDERED_LIST)

class Test_text_to_blocknodes(unittest.TestCase):
    def test_basic(self):
        Sample_Text = """
        # This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first item
        * This is a list item
        * This is another list item
        """
        Expectation = [BlockNode(text_to_textnodes("This is a heading"),BlockType.HEADING,1),
                    BlockNode(text_to_textnodes("This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n"), BlockType.PARAGRAPH),
                    BlockNode(text_to_textnodes("This is the first item") + text_to_textnodes("This is a list item") + text_to_textnodes("This is another list item"), BlockType.UNORDERED_LIST)]
        self.assertEqual(text_to_blocknodes(Sample_Text), Expectation )

if __name__ == "__main__":
    unittest.main()