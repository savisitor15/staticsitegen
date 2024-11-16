import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


HTML_MEMBERS = ["tag", "value", "props", "children"]
LEAF_DATA_A = {"tag": "p", "value": "This is a paragraph of text.", "props": None}
LEAF_DATA_B = {"tag": "a", "value": "Click me!", "props": {"href":"https://www.google.com"}}
PARENT_DATA_A = {"tag": "p", "children": [LeafNode(LEAF_DATA_A.get("tag"), LEAF_DATA_A.get("value"))], "props": None}
PARENT_DATA_B = {"tag": "p", "children": [LeafNode(LEAF_DATA_A.get("tag"), LEAF_DATA_A.get("value")),
                                           LeafNode(LEAF_DATA_B.get("tag"), LEAF_DATA_B.get("value"), LEAF_DATA_B.get("props"))],
                                             "props": {"class": "content"}}
HELLO = "Hello World!"

class TestHTMLNode(unittest.TestCase):
    def test_HTMLNode(self):
        """Testing HTMLNode data members"""
        node = HTMLNode()
        for mem in HTML_MEMBERS:
            self.assertTrue(hasattr(node, mem), f"Missing ->{mem}<- data member in HTMLNode definition!")

    def test_HTMLNode_eq(self):
        """Ensure eqaulity works"""
        node1 = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node1, node2)
        node3 = HTMLNode("b", HELLO)
        self.assertNotEqual(node1, node3)

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
        node4 = LeafNode("p", None)
        self.assertEqual(node1.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')
        self.assertEqual(node3.to_html(), HELLO)
        self.assertRaises(ValueError, node4.to_html)


class TestParentNode(unittest.TestCase):
    def test_ParentNode_values(self):
        """Confirm ParentNode data members"""
        node1 = ParentNode(PARENT_DATA_A.get("tag"), PARENT_DATA_A.get("children"))
        node2 = ParentNode(PARENT_DATA_B["tag"], PARENT_DATA_B["children"], PARENT_DATA_B["props"])
        for attr, value in PARENT_DATA_A.items():
            self.assertEqual(getattr(node1, attr), value)
        for attr, value in PARENT_DATA_B.items():
            self.assertEqual(getattr(node2, attr), value)

    def test_ParentNode_to_html_fail(self):
        """Confirm that the html output errors correctly"""
        node1 = ParentNode("", [LeafNode("","test")])
        node2 = ParentNode("p", [])
        self.assertRaises(ValueError, node1.to_html)
        # Confirm the error messages!
        with self.assertRaises(ValueError) as cm:
            node1.to_html()
            self.assertEqual(cm.exception, "Parent - tag invalid")
        with self.assertRaises(ValueError) as cm:
            node2.to_html()
            self.assertEqual(cm.exception, "Parent - no children")
    
    def test_ParentNode_to_html_output(self):
        """Confirm we get html from the parent node"""
        node1 = ParentNode(PARENT_DATA_A.get("tag"), PARENT_DATA_A.get("children"))
        node2 = ParentNode(PARENT_DATA_B["tag"], PARENT_DATA_B["children"], PARENT_DATA_B["props"])
        self.assertEqual(node1.to_html(), "<p><p>This is a paragraph of text.</p></p>")
        self.assertEqual(node2.to_html(), '<p><p>This is a paragraph of text.</p><a href="https://www.google.com">Click me!</a></p>')

    def test_ParentNode_to_html_child_failure(self):
        """Test case for if child is invalid"""
        node = ParentNode("p", [LeafNode("p", None)])
        with self.assertRaises(ValueError) as cm:
            node.to_html()
            self.assertEqual(cm.exception, "LeafNodes must have a value!")

if __name__ == "__main__":
    unittest.main()
