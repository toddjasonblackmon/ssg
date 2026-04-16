import os, shutil

def log_print(s):
    pass
    # print(s)

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


