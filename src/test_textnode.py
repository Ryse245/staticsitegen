import unittest

from textnode import TextNode, TextType
from helper_functions import split_nodes_delimiter
from helper_functions import extract_markdown_images
from helper_functions import extract_markdown_links
from helper_functions import split_nodes_image
from helper_functions import split_nodes_link
from helper_functions import text_to_textnodes

from markdown import BlockType
from markdown import markdown_to_blocks
from markdown import block_to_blocktype


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
        self.assertListEqual(new_nodes, check)

    def test_split_delimiter_bold_front(self):
        node = TextNode("**This** is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        check = [TextNode("This", TextType.BOLD), TextNode(" is text with a ", TextType.TEXT), TextNode("bold block", TextType.BOLD), TextNode(" word", TextType.TEXT)]
        self.assertListEqual(new_nodes, check)

    def test_split_delimiter_italics_end(self):
        node = TextNode("This is text with a word ending with _italics_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        check = [TextNode("This is text with a word ending with ", TextType.TEXT), TextNode("italics", TextType.ITALIC)]
        self.assertListEqual(new_nodes, check)

    def test_split_delimiter_none(self):
        node = TextNode("This is text with a word ending with nothing", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        check = [TextNode("This is text with a word ending with nothing", TextType.TEXT)]
        self.assertListEqual(new_nodes, check)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"),("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links("This is text with a [link](https://www.boot.dev)")
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    def test_extract_multiple_markdown_link(self):
        matches = extract_markdown_links("This is text with a [boot dev](https://www.boot.dev) and [youtube](https://www.youtube.com/) link!")
        self.assertListEqual([("boot dev", "https://www.boot.dev"), ("youtube", "https://www.youtube.com/")], matches)
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_links(self):
        node = TextNode(
            "This is text with a [first link](https://i.imgur.com/zjjcJKZ.png) and a [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("first link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nothing(self):
        node = TextNode("This is a text with nothing to split", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [TextNode("This is a text with nothing to split", TextType.TEXT)])

    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        check = [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                ]
        self.assertListEqual(nodes, check)

    def test_text_to_textnode_alt(self):
        text = "This is _text_ with a **bold** word and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a `code block` and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        check = [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.ITALIC),
                    TextNode(" with a ", TextType.TEXT),
                    TextNode("bold", TextType.BOLD),
                    TextNode(" word and an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                ]
        self.assertListEqual(nodes, check)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_more_spaces(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line






- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_blocktype_header(self):
        md = "#### Header"
        type = block_to_blocktype(md)
        self.assertEqual(type, BlockType.HEADING)

    def test_block_to_blocktype_none_header(self):
        md = "########## Header too long"
        type = block_to_blocktype(md)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_block_to_blocktype_code(self):
        md = "```This is a code block```"
        type = block_to_blocktype(md)
        self.assertEqual(type, BlockType.CODE)

    def test_block_to_blocktype_not_code(self):
        md = "```This is not a code block"
        type = block_to_blocktype(md)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_block_to_blocktype_quote(self):
        md = """>This is a quote
        >Multiple
        >lines"""
        type = block_to_blocktype(md)
        self.assertEqual(type, BlockType.QUOTE)

    def test_block_to_blocktype_not_quote(self):
        md = """>This is not
        a quote
        >Multiple
        >lines"""
        type = block_to_blocktype(md)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_block_to_blocktype_un_list(self):
        md = """- This is a list
        - Multiple
        - lines"""
        type = block_to_blocktype(md)
        self.assertEqual(type, BlockType.UNORDERED_LIST)

    def test_block_to_blocktype_not_un_list(self):
        md = """- This is not
        a list
        - Multiple
        - lines"""
        type = block_to_blocktype(md)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_block_to_blocktype_ord_list(self):
        md = """1. This is a list
        2. Multiple
        3. lines"""
        type = block_to_blocktype(md)
        self.assertEqual(type, BlockType.ORDERED_LIST)

    def test_block_to_blocktype_not_ord_list(self):
        md = """1. This is not a list
        4. Multiple
        3. lines"""
        type = block_to_blocktype(md)
        self.assertEqual(type, BlockType.PARAGRAPH)




if __name__ == "__main__":
    unittest.main()