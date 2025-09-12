import os
from htmlnode import markdown_to_html_node
from helper_functions import extract_title


def generate_page(from_path, template_path, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    dest_info = dest_path.rsplit("/", 1)
    abs_from = os.path.abspath(from_path)
    abs_temp = os.path.abspath(template_path)
    abs_dest = os.path.abspath(dest_info[0])
    from_file_content = open(abs_from).read()
    template_file_content = open(abs_temp).read()
    html_string = markdown_to_html_node(from_file_content).to_html()
    title = extract_title(from_file_content)
    added_content = template_file_content.replace("{{ Title }}", title)
    added_content = added_content.replace("{{ Content }}", html_string)

    os.makedirs(abs_dest, 511, True)
    new_file = open(os.path.join(abs_dest,dest_info[1]),"x")
    new_file.write(added_content)
    new_file.close()