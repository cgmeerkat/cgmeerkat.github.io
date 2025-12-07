import os
import shutil

from . import copy_static, html_templates, distribute_rendered_html

# Define source and destination directories
TEMPLATES_DIR = 'templates'
TEMPLATES_PAGES_SUBDIR = 'public'
STATIC_DIR = 'static'
BUILD_DIR = 'serve'

def build_site():
    # Clean up the build directory if it exists
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    os.makedirs(BUILD_DIR)
    print(f"✔ (Re)created <{BUILD_DIR}> Folder")

    copy_static.copy_static(STATIC_DIR, BUILD_DIR)
    print("✔ Built All Statics")

    rel_paths, contents = html_templates.build(TEMPLATES_DIR, sub=TEMPLATES_PAGES_SUBDIR)
    print("✔ Filled All Templates")

    distribute_rendered_html.distribute(contents, rel_paths, BUILD_DIR)
    print("✔ Exported All HTML")

if __name__ == '__main__':
    build_site()
