import re
import os
import shutil
from textnode import TextNode
from textnode import TextType
from markdown import trim_markdown_block_specifiers
from markdown import BlockType

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


    
def text_to_textnodes(text: str):
    final_text = text.strip()

    new_nodes = [TextNode(final_text, TextType.TEXT)]
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def copy_directory(source, destination):
    abs_source = os.path.abspath(source)
    abs_dest = os.path.abspath(destination)
    if not os.path.exists(abs_source):
        raise Exception("Directory not found")
    shutil.rmtree(abs_dest)
    os.mkdir(abs_dest)
    copy_directory_rec(abs_source, abs_source, abs_dest)


def copy_directory_rec(current_path, source, destination):
    for item in os.listdir(current_path):
        current_item = os.path.join(current_path, item)
        if os.path.isdir(current_item):
            copy_directory_rec(current_item, source, destination)
        elif os.path.isfile(current_item):
            rel_path = os.path.relpath(current_path, source)
            dest_path = os.path.join(destination, rel_path)
            os.makedirs(dest_path, 511, True)
            shutil.copy(current_item, dest_path)

def extract_title(markdown: str):
    lines = markdown.split("\n")
    start = lines[0]
    start = start.strip()
    if start[0] != "#":
        raise Exception("No header found in markdown")
    return trim_markdown_block_specifiers(start, BlockType.HEADING)
