import os
from htmlnode import markdown_to_html_node
from helper_functions import extract_title


def generate_page(from_path:str, template_path, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    rel_path = from_path.split("/", 1)[1]
    rel_path = rel_path.rsplit("/", 1)[0]

    abs_from = os.path.abspath(from_path)
    abs_temp = os.path.abspath(template_path)
    abs_dest = os.path.abspath(dest_path)
    from_file_content = open(abs_from).read()
    template_file_content = open(abs_temp).read()
    html_string = markdown_to_html_node(from_file_content).to_html()
    title = extract_title(from_file_content)
    added_content = template_file_content.replace("{{ Title }}", title)
    added_content = added_content.replace("{{ Content }}", html_string)

    if rel_path[-3:] != ".md":
        os.makedirs(os.path.join(abs_dest, rel_path), 511, True)

    to_path = from_path.split("/",1)[1][:-3]+".html"
    new_file = open(os.path.join(abs_dest,to_path),"x")
    new_file.write(added_content)
    new_file.close()

def generate_pages_recursive(from_path, template_path, dest_path: str):
    abs_from = os.path.abspath(from_path)
    for item in os.listdir(abs_from):
        current_item = os.path.join(abs_from, item)
        if os.path.isdir(current_item):
            generate_pages_recursive(os.path.join(from_path, item), template_path, dest_path)
        elif os.path.isfile(current_item) and current_item[-3:] == ".md":
            generate_page(os.path.join(from_path, item), template_path, dest_path)
