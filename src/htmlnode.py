from textnode import *
from markdown import markdown_to_blocks
from markdown import block_to_blocktype
from markdown import get_heading_count
from markdown import BlockType
from markdown import trim_markdown_block_specifiers

from helper_functions import text_to_textnodes

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def to_html(self):
        raise NotImplementedError("Function not yet implemented")
    
    def props_to_html(self):
        result = ""
        if self.props is not None:
            for prop in self.props:
                val = self.props[prop]
                result += f' {prop}="{val}"'
        return result
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node has no set value.")
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node has no set tag.")
        if self.children is None:
            raise ValueError("Parent node has 'None' in children array.")
        result = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            result += child.to_html()
        result += f"</{self.tag}>"
        return result


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Node type not found")
        
def block_type_to_html_node(block_type: BlockType, markdown_block: str, header_count = None):
    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode("p", [])
        case BlockType.HEADING:
            header_tag = "h" + str(get_heading_count(markdown_block))
            return ParentNode(header_tag, [])
        case BlockType.CODE:
            return ParentNode("pre", [])
        case BlockType.QUOTE:
            return ParentNode("blockquote", [])
        case BlockType.UNORDERED_LIST:
            return ParentNode("ul", [])
        case BlockType.ORDERED_LIST:
            return ParentNode("ol", [])
        case _:
            raise Exception("Block type not found")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        type = block_to_blocktype(block)
        node = None
        if type == BlockType.HEADING:
            node = block_type_to_html_node(type, block, get_heading_count(block))
        else:
            node = block_type_to_html_node(type, block)
        if type != BlockType.CODE:
            trimmed_block = trim_markdown_block_specifiers(block, type)
            html_children = []
            for line in trimmed_block.split("\n"):
                children = text_to_textnodes(line)
                for child in children:
                    if len(child.text.strip()) != 0:
                        if type == BlockType.UNORDERED_LIST or type == BlockType.ORDERED_LIST:
                            html_children.append(ParentNode("li",[text_node_to_html_node(child)]))
                        else:
                            html_children.append(text_node_to_html_node(child))
            node.children = html_children
        else:
            child = TextNode(block, TextType.CODE)
            node.children = [text_node_to_html_node(child)]
        block_nodes.append(node)
    return ParentNode("div", block_nodes)


