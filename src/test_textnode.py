import unittest

from textnode import TextNode, TextType
from helper_functions import split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_print(self):
        node = TextNode("This is a text node", TextType.BOLD)
        checkstr = 'TextNode(This is a text node, TextType.BOLD, None)'
        self.assertEqual(str(node), checkstr)

    def test_url(self):
        node = TextNode("This is checking for URL", TextType.LINK, "dummyurl.xyz")
        self.assertNotEqual(node.url, None)

    def test_no_url(self):
        node = TextNode("This is checking for no URL", TextType.ITALIC)
        self.assertEqual(node.url, None)

    def test_split_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        check = [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)]
        self.assertEqual(new_nodes, check)

    def test_split_delimiter_bold_front(self):
        node = TextNode("**This** is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        check = [TextNode("This", TextType.BOLD), TextNode(" is text with a ", TextType.TEXT), TextNode("bold block", TextType.BOLD), TextNode(" word", TextType.TEXT)]
        self.assertEqual(new_nodes, check)


    def test_split_delimiter_italics_end(self):
        node = TextNode("This is text with a word ending with *italics*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        check = [TextNode("This is text with a word ending with ", TextType.TEXT), TextNode("italics", TextType.ITALIC)]
        self.assertEqual(new_nodes, check)

if __name__ == "__main__":
    unittest.main()