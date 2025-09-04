import re
from textnode import TextNode
from textnode import TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter, text_type):
    result_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            result_nodes.append(old_node)
            continue
        split = old_node.text.split(delimiter)
        for iter in range(len(split)):
            if len(split[iter]) > 0:
                current_type = text_type if iter % 2 != 0 else TextType.TEXT
                current = TextNode(split[iter], current_type)
                result_nodes.append(current)
    return result_nodes

def extract_markdown_images(text):
    image_info = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return image_info

def extract_markdown_links(text):
    link_info = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return link_info

def split_nodes_image(old_nodes: list[TextNode]):
    result_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            result_nodes.append(old_node)
            continue
        new_nodes = []
        current_text = old_node.text
        extract = extract_markdown_images(old_node.text)
        for image in extract:
            sections = current_text.split(f"![{image[0]}]({image[1]})", 1)
            new_nodes.append(TextNode(sections[0],TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            current_text = sections[1]
        if len(current_text) > 0:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
        result_nodes += new_nodes
    return result_nodes


def split_nodes_link(old_nodes: list[TextNode]):
    result_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            result_nodes.append(old_node)
            continue
        new_nodes = []
        current_text = old_node.text
        extract = extract_markdown_links(old_node.text)
        for link in extract:
            sections = current_text.split(f"[{link[0]}]({link[1]})", 1)
            new_nodes.append(TextNode(sections[0],TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            current_text = sections[1]
        if len(current_text) > 0:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
        result_nodes += new_nodes
    return result_nodes


    
def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes