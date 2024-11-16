import unittest

from textnode import TextNode, TextType

TEXT_STRING = "This is a test node."
EXPECTED_REPR = f"TextNode({TEXT_STRING}, text, None)"

class TestTextNode(unittest.TestCase):
    def test_text(self):
        node = TextNode(TEXT_STRING, TextType.TEXT)
        self.assertEqual(TEXT_STRING, node.text)
    
    def test_eq(self):
        node = TextNode(TEXT_STRING, TextType.TEXT)
        node2 = TextNode(TEXT_STRING, TextType.TEXT)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode(TEXT_STRING, TextType.TEXT)
        node2 = TextNode(TEXT_STRING, TextType.TEXT, "http://localhost")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode(TEXT_STRING, TextType.TEXT)
        self.assertEqual(EXPECTED_REPR, str(node))

    


if __name__ == "__main__":
    unittest.main()
