import unittest
from textnode import TextNode, TextType
from htmlnode import LeafNode

from common import text_node_to_html_node



HELLO = "Hello World!"

class Test_text_node_to_html_node(unittest.TestCase):
    def test_Bold_Conversion(self):
        """Convert a TextNode with BOLD text to HTML"""
        node = TextNode(HELLO, TextType.BOLD)
        h_node = text_node_to_html_node(node)
        self.assertEqual(h_node, LeafNode("b", HELLO))

    def test_Text_Conversion(self):
        """Normal text node to HTML"""
        node = TextNode(HELLO, TextType.TEXT)
        h_node = text_node_to_html_node(node)
        self.assertEqual(h_node, LeafNode("", HELLO))

    def test_Italic_Conversion(self):
        """Italic node to HTML node"""
        node = TextNode(HELLO, TextType.ITALIC)
        h_node = text_node_to_html_node(node)
        self.assertEqual(h_node, LeafNode("i", HELLO))

    def test_Code_Conversion(self):
        """Code block text node to html node"""
        node = TextNode(HELLO, TextType.CODE)
        h_node = text_node_to_html_node(node)
        self.assertEqual(h_node, LeafNode("code", HELLO))

    def test_Image_conversion(self):
        """Image text node to html node"""
        node = TextNode(HELLO, TextType.IMAGE, "flower.jpg")
        h_node = text_node_to_html_node(node)
        self.assertEqual(h_node, LeafNode("img", "", {"src": "flower.jpg", "alt": HELLO}))

    def test_Link_Conversion(self):
        """Converting links to HTML nodes"""
        node = TextNode(HELLO, TextType.LINK, "https://google.com")
        h_node = text_node_to_html_node(node)
        self.assertEqual(h_node, LeafNode("a", HELLO, {"href": "https://google.com"}))


if __name__ == "__main__":
    unittest.main()