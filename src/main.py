from textnode import TextNode, TextType
from markdown import markdown_to_html_node, extract_title
import os, sys
from shutil import copy, rmtree

def copy_contents_to_dir(source_dir, target_dir):
    if os.path.exists(target_dir):
        rmtree(target_dir)
    os.mkdir(target_dir)

    for item in os.listdir(source_dir):
        itempath = os.path.join(source_dir, item)
        if os.path.isfile(itempath):
            copy(itempath, target_dir)
        else:
            mirror_target_path = os.path.join(target_dir, item)
            os.mkdir(mirror_target_path)
            copy_contents_to_dir(itempath, mirror_target_path)

def generate_page(basepath, from_path, template_path, dest_path):
    if not os.path.exists(from_path):
        raise FileExistsError(f"from_path {from_path} is not a valid folder")
    elif not os.path.exists(template_path):
        raise FileExistsError(f"template_path {template_path} is not a valid folder")
    elif not os.path.exists(dest_path):
        raise FileExistsError(f"dest_path {dest_path} is not a valid folder")
    else:   
        print(f"Generating page from {from_path} to {dest_path} using {template_path} as template")
        with open(from_path) as md_file:
            md_content = md_file.read()

            with open(template_path) as template_file:
                template_content = template_file.read()

                md_to_html = markdown_to_html_node(md_content).to_html()
                md_title = extract_title(md_content)

                template_content = template_content.replace("{{ Title }}", md_title)
                template_content = template_content.replace("{{ Content }}", md_to_html)
                template_content = template_content.replace("href=\"/", "href=\"" + basepath)
                template_content = template_content.replace("src=\"/", "src=\"" + basepath)

                with open(os.path.join(dest_path, "".join(from_path.split("/")[-1].split(".")[0]) + ".html"), "w") as out_file:
                    out_file.write(template_content)
                out_file.close()
            template_file.close()
        md_file.close()

def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    ls = os.listdir(dir_path_content)
    for item in ls:
        current_path = os.path.join(dir_path_content, item)
        if os.path.isfile(current_path):
            if item.split(".")[-1] == "md":
                generate_page(basepath, os.path.join(dir_path_content,item), template_path, dest_dir_path)
        else:
            new_dest_dir_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(basepath, current_path, template_path, new_dest_dir_path)
        

def main(basepath = "/"):
    if len(basepath) < 2:
        basepath = [None, "/"]

    copy_contents_to_dir("static", "public")
    generate_pages_recursive(basepath[1], "content", "./template.html", "docs")

main(sys.argv)