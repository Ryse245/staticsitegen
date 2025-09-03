import unittest

from htmlnode import *
from textnode import *


class TestHTMLNode(unittest.TestCase):

    def test_print(self):
        node = HTMLNode("p", "Test value")
        checkstr = "HTMLNode(p, Test value, None, None)"
        self.assertEqual(str(node), checkstr)

    def test_empty(self):
        node = HTMLNode()
        is_empty = node.tag is None and node.value is None and node.children is None and node.props is None
        self.assertEqual(is_empty, True)

    def test_has_content(self):
        node = HTMLNode("p", "Test value")
        is_empty = node.tag is None and node.value is None and node.children is None and node.props is None
        self.assertEqual(is_empty, False)
    
    def test_props_to_html(self):
        node = HTMLNode("p", "Test value", None, {"href": "https://www.google.com"})
        to_html = node.props_to_html()
        self.assertEqual(to_html, ' href="https://www.google.com"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')        

    def test_parent_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_to_html_with_children_and_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"href": "https://www.google.com"})
        self.assertEqual(parent_node.to_html(), '<div href="https://www.google.com"><span>child</span></div>')
        
    def test_parent_to_html_with_children_with_props(self):
        child_node = LeafNode("span", "child", {"href": "https://www.google.com"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><span href="https://www.google.com">child</span></div>')

    def test_parent_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})
        
    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.google.com", "alt": "This is an image node"})

if __name__ == "__main__":
    unittest.main()