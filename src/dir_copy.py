import os, shutil
from blocks import markdown_to_html_node
from split_nodes import extract_title

def log_print(s):
    pass
#    print(s)

def copy_directory(source, dest):

    if os.path.exists(dest):
        log_print(f"Removing previous {dest}")
        shutil.rmtree(dest)

    os.mkdir(dest)
    log_print(f"Adding new {dest}")

    if not os.path.exists(source):
        log_print(f"Nothing to copy from {source}")
        return

    for file_path in os.listdir(source):
        src_path = os.path.join(source, file_path)
        dest_path = os.path.join(dest, file_path)
        if os.path.isfile(src_path):
            log_print(f"Copying {src_path} -> {dest_path}")
            shutil.copy(src_path, dest_path)
        elif os.path.isdir(src_path):
            log_print(f"{src_path} is a directory")
            copy_directory(src_path, dest_path)
        else:
            log_print(f"Ignoring {full_path}: unknown type.")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    with open(from_path) as f:
        markdown = f.read()

    with open(template_path) as f:
        template = f.read()

    content = markdown_to_html_node(markdown).to_html()

    title = extract_title(markdown)

    html_page = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    dest_dirname = os.path.dirname(dest_path)
    if dest_dirname:
        os.makedirs(dest_dirname, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(html_page)

    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    log_print(f"generate_pages_recursive({dir_path_content}, {template_path}, {dest_dir_path})")
    if not os.path.exists(dest_dir_path):
        log_print(f"Error: {dest_dir_path} does not exist")
        return

    if not os.path.exists(dir_path_content):
        log_print(f"Nothing to generate from {dir_path_content}")
        return

    for file_path in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, file_path)
        dest_path = os.path.join(dest_dir_path, file_path)
        if os.path.isfile(src_path):
            if file_path.endswith(".md"):
                dest_path = dest_path[:-2] + "html"
                generate_page(src_path, template_path, dest_path)
                log_print(f"Generating {src_path} -> {dest_path}")
            else:
                log_print(f"Ignoring non-markdown file {src_path}")
        elif os.path.isdir(src_path):
            log_print(f"{src_path} is a directory")
            os.makedirs(dest_path, exist_ok=True)
            generate_pages_recursive(src_path, template_path, dest_path)
        else:
            log_print(f"Ignoring {full_path}: unknown type.")



