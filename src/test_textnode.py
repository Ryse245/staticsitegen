import unittest

from textnode import TextNode, TextType


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



if __name__ == "__main__":
    unittest.main()