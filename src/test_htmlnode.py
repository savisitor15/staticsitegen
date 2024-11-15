import unittest

from htmlnode import HTMLNode, LeafNode

HTML_MEMBERS = ["tag", "value", "props", "children"]
LEAF_DATA_A = {"tag": "p", "value": "This is a paragraph of text.", "props": None}
LEAF_DATA_B = {"tag": "a", "value": "Click me!", "props": {"href":"https://www.google.com"}}
HELLO = "Hello World!"

class TestHTMLNode(unittest.TestCase):
    def test_HTMLNode(self):
        """Testing HTMLNode data members"""
        node = HTMLNode()
        for mem in HTML_MEMBERS:
            self.assertTrue(hasattr(node, mem), f"Missing ->{mem}<- data member in HTMLNode definition!")

    def test_HTMLNode_to_html(self):
        """Testing HTMLNode should not implement to_html method, just declare"""
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)

    def test_HTMLNode_props_to_html(self):
        """Test HTMLNode if the props_to_html output is correctly formatted"""
        node1 = HTMLNode(props={
    "href": "https://www.google.com", 
    "target": "_blank",})
        node2 = HTMLNode()
        self.assertEqual(node1.props_to_html(), ' href="https://www.google.com" target="_blank"', "HTMLNode props_to_html failed to output correctly!")
        self.assertEqual(node2.props_to_html(), "")

    def test_HTMLNode_repr(self):
        """Test HTMLNode string representation"""
        node = HTMLNode()
        self.assertEqual(str(node), "HTMLNode(tag=None, value=None, props=None, children=None)")

class TestLeafNode(unittest.TestCase):
    def test_LeafNode(self):
        """Testing LeafNode data members"""
        node = LeafNode(LEAF_DATA_A.get("tag"), LEAF_DATA_A.get("value"))
        for attr in LEAF_DATA_A.keys():
            self.assertTrue(hasattr(node, attr))

    def test_LeafNode_Values(self):
        """Test LeafNode values corrospond in the correct members"""
        node1 = LeafNode(LEAF_DATA_A.get("tag"), LEAF_DATA_A.get("value"),)
        node2 = LeafNode(LEAF_DATA_B.get("tag"), LEAF_DATA_B.get("value"), LEAF_DATA_B.get("props"))
        for attr, value in LEAF_DATA_A.items():
            self.assertEqual(getattr(node1, attr, -1), value)
        for attr, value in LEAF_DATA_B.items():
            self.assertEqual(getattr(node2, attr, -1), value)

    def test_LeafNode_to_html(self):
        """Test LeafNode produces valid HTML"""
        node1 = LeafNode(LEAF_DATA_A.get("tag"), LEAF_DATA_A.get("value"),)
        node2 = LeafNode(LEAF_DATA_B.get("tag"), LEAF_DATA_B.get("value"), LEAF_DATA_B.get("props"))
        node3 = LeafNode(None, HELLO)
        node4 = LeafNode("p", "")
        self.assertEqual(node1.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')
        self.assertEqual(node3.to_html(), HELLO)
        self.assertRaises(ValueError, node4.to_html)



if __name__ == "__main__":
    unittest.main()
