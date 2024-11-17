import unittest
from textnode import TextNode, TextType
from htmlnode import LeafNode

from common import text_node_to_html_node, split_nodes_delimiter, split_text_nodes_nested



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

class Test_split_nodes_delimiter(unittest.TestCase):
    def test_bold_extraction(self):
        """Extract a single MID point bold word"""
        sample = [TextNode("Hello **World**!", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(sample, TextType.BOLD), [TextNode("Hello ", TextType.TEXT),TextNode("World", TextType.BOLD),
                                                                         TextNode("!", TextType.TEXT)])
        
    def test_multi_bold_extraction(self):
        """Extract multiple Mid point bold markup"""
        sample = [TextNode("**Hello** **World**!", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(sample, TextType.BOLD), [TextNode("Hello", TextType.BOLD),
                                                                        TextNode(" ", TextType.TEXT),
                                                                        TextNode("World", TextType.BOLD),
                                                                         TextNode("!", TextType.TEXT)])
        
    def test_italic_extraction(self):
        """Extract a single MID point italic word"""
        sample = [TextNode("Hello *World*!", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(sample, TextType.ITALIC), [TextNode("Hello ", TextType.TEXT),
                                                                        TextNode("World", TextType.ITALIC),
                                                                         TextNode("!", TextType.TEXT)])
    
    def test_multi_italic_extraction(self):
        """Extract multiple Mid point italic markup"""
        sample = [TextNode("*Hello* *World*!", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(sample, TextType.ITALIC), [TextNode("Hello", TextType.ITALIC),
                                                                        TextNode(" ", TextType.TEXT),
                                                                        TextNode("World", TextType.ITALIC),
                                                                         TextNode("!", TextType.TEXT)])
        
    def test_code_extraction(self):
        """Extract a single MID point code word"""
        sample = [TextNode("Hello `World`!", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(sample, TextType.CODE), [TextNode("Hello ", TextType.TEXT),
                                                                        TextNode("World", TextType.CODE),
                                                                         TextNode("!", TextType.TEXT)])
    
    def test_multi_italic_extraction(self):
        """Extract multiple Mid point code markup"""
        sample = [TextNode("`Hello` `World`!", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(sample, TextType.CODE), [TextNode("Hello", TextType.CODE),
                                                                        TextNode(" ", TextType.TEXT),
                                                                        TextNode("World", TextType.CODE),
                                                                         TextNode("!", TextType.TEXT)])
        
    def test_combined_extraction(self):
        """Test combining extractions, ORDER matters BOLD->ITALIC->CODE"""
        sample = [TextNode("This **MUST** be done in the *correct* order `to be seen`!", TextType.TEXT)]
        expectation = [
            TextNode("This ", TextType.TEXT),
            TextNode("MUST", TextType.BOLD),
            TextNode(" be done in the ", TextType.TEXT),
            TextNode("correct", TextType.ITALIC),
            TextNode(" order ", TextType.TEXT),
            TextNode("to be seen", TextType.CODE),
            TextNode("!", TextType.TEXT)
        ]
        self.assertEqual(split_text_nodes_nested(sample), expectation)

    def test_combined_nested(self):
        """Test Nested markup"""
        sample = [TextNode("Hello **all you *humans* out there**", TextType.TEXT)]
        expectation = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("all you ", TextType.BOLD),
            TextNode("humans", TextType.ITALIC),
            TextNode(" out there", TextType.BOLD),
        ]
        self.assertEqual(split_text_nodes_nested(sample), expectation)

    def test_end_to_end_extraction(self):
        """Test IMAGE -> LINK -> BOLD -> ITALIC -> CODE extraction"""
        sample = [TextNode("This `string` contains ![rick roll](https://i.imgur.com/aKaOqIh.gif) [to boot dev](https://www.boot.dev) **Wee whoo*** summer*`child`", TextType.TEXT)]
        expectation = [
            TextNode("This ", TextType.TEXT),
            TextNode("string", TextType.CODE),
            TextNode(" contains ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" ", TextType.TEXT),
            TextNode("Wee whoo", TextType.BOLD),
            TextNode(" summer", TextType.ITALIC),
            TextNode("child", TextType.CODE)
        ]
        self.assertEqual(split_text_nodes_nested(sample), expectation)

    def test_nesting_image_link(self):
        """Should not support nesting"""
        sample = [TextNode("![*rick roll*](https://i.imgur.com/aKaOqIh.gif) [`to boot dev`](https://www.boot.dev)", TextType.TEXT)]
        expectation = [
            TextNode("*rick roll*", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" ", TextType.TEXT),
            TextNode("`to boot dev`", TextType.LINK, "https://www.boot.dev")
        ]
        self.assertEqual(split_text_nodes_nested(sample), expectation)

    def test_bad_input(self):
        with self.assertRaises(TypeError) as cm:
            split_nodes_delimiter(TextNode("Non list sent in!", TextType.TEXT), TextType.BOLD)
            self.assertEqual(cm.exception, "Old_nodes must be a list of TextNode!")

if __name__ == "__main__":
    unittest.main()