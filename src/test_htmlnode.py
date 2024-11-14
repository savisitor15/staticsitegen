import unittest

from htmlnode import HTMLNode

MEMBERS = ["tag", "value", "children", "props"]

class TestHTMLNode(unittest.TestCase):
    def test_HTMLNode(self):
        """Testing HTMLNode data members"""
        node = HTMLNode()
        for mem in MEMBERS:
            self.assertTrue(hasattr(node, mem), f"Missing ->{mem}<- data member in HTMLNode definition!")

    def test_HTMLNode_to_html(self):
        """Testing HTMLNode should not implement to_html method, just declare"""
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)

    def test_HTMLNode_props_to_html(self):
        """Test HTMLNode if the props_to_html output is correctly formatted"""
        node = HTMLNode(props={
    "href": "https://www.google.com", 
    "target": "_blank",})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"', "HTMLNode props_to_html failed to output correctly!")

    def test_HTMLNode_repr(self):
        """Test HTMLNode string representation"""
        node = HTMLNode()
        self.assertEqual(str(node), "HTMLNode(tag=None, value=None, props=None, children=None)")



if __name__ == "__main__":
    unittest.main()
