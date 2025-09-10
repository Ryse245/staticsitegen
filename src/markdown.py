import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = 0
    HEADING = 1
    CODE = 2
    QUOTE = 3
    UNORDERED_LIST = 4
    ORDERED_LIST = 5

def markdown_to_blocks(markdown: str):
    result = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        block = block.strip()
        block = block.strip("\n")
        if len(block) > 0:
            result.append(block)
    return result

def block_to_blocktype(markdown_block: str):
    markdown_block = markdown_block.strip()
    if re.search(r"^(#{1,6} )", markdown_block) is not None:
        return BlockType.HEADING
    if re.search(r"^\`\`\`(.|\s)*\`\`\`$", markdown_block) is not None:
        return BlockType.CODE
    is_quote, is_un_list, is_ord_list = (True, True, True)
    lines = markdown_block.split("\n")
    for i in range(0, len(lines)):
        current = lines[i].strip()
        if current[0] != ">":
            is_quote = False
        if current[:2] != "- ":
            is_un_list = False
        if current[:3] != str(i+1)+". ":
            is_ord_list = False
        if not is_quote and not is_un_list and not is_ord_list:
            break
    if is_quote:
        return BlockType.QUOTE
    elif is_un_list:
        return BlockType.UNORDERED_LIST
    elif is_ord_list:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def get_heading_count(markdown_block: str):
    match_obj = re.search(r"^(#{1,6} )", markdown_block)
    if match_obj is not None:
        return match_obj.string.count("#")
    raise Exception("Not a heading block")

def trim_markdown_block_specifiers(markdown_block: str, type: BlockType,):
    match type:
        case BlockType.HEADING:
            count = get_heading_count(markdown_block)
            return markdown_block[count+1:]
        case BlockType.CODE:
            return markdown_block[3:-3].strip()+"\n"
        case BlockType.PARAGRAPH:
            return markdown_block
        case BlockType.QUOTE:
            trimmed = ""
            for line in markdown_block.split("\n"):
                trimmed += line[2:] + "\n"
            return trimmed.strip()
        case BlockType.UNORDERED_LIST:
            trimmed = ""
            for line in markdown_block.split("\n"):
                trimmed += line[2:] + "\n"
            return trimmed.strip()
        case BlockType.ORDERED_LIST:
            trimmed = ""
            for line in markdown_block.split("\n"):
                trimmed += line[3:] + "\n"
            return trimmed.strip()
        case _:
            raise Exception("Trim block type not found")
