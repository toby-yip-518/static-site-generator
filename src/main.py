import os
import shutil
import sys

from copystatic import copy_files_recursive
from generatepage import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
dir_path_docs = "./docs"
template_path = "./template.html"


def main():

    basepath = sys.argv
    if basepath == None:
        basepath = "/"

    print("Deleting public directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_docs)

    print("Generating page...")
    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_docs,
        "/"
    )

main()
