from textnode import *

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter, text_type):
    result_nodes = []
    for old_node in old_nodes:
        split = old_node.text.split(delimiter)
        #if delimiter starts old_node.text, even indecies are the affected strings, else odd indecies are affected
        affecting_odd_indecies = True
        if old_node.text[:len(delimiter)] == delimiter:
            #text starts with delimiter
            affecting_odd_indecies = False
        for iter in range(len(split)):
            if len(split[iter]) > 0:
                current_type = text_type if iter % 2 != 0 else TextType.TEXT
                current = TextNode(split[iter], current_type)
                result_nodes.append(current)
    return result_nodes