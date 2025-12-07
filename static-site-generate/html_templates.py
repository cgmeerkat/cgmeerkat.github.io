from jinja2 import Environment, FileSystemLoader
import os
from pathlib import Path

def get_site_data(rel_path: str) -> dict:
    # Define dynamic data
    site_data_overrides_tree = {
        '/blender' : {
            'use_extended_footer': True,
        },
        '/blog' : {
            '/13-features-removed-from-blender': {},
        },
        '/fabric-textures-giveaway' : {},
        '/impulse-response-player' : {},
        'use_extended_footer': False,
    }

    p = Path(rel_path).parent
    site_data = {}
    local_tree = site_data_overrides_tree
    for part in p.parts:
        for key in local_tree:
            if key.startswith('/'):
                continue
            site_data[key] = local_tree[key]

        if not ('/' + part in local_tree):
            return site_data
        local_tree = local_tree['/' + part]
    return site_data

def build(TEMPLATES_DIR: str, sub:str='.'):
    # Configure Jinja2 environment to load templates
    # This loader will look in the 'templates' directory
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

    pages_subdir: str = str((Path(TEMPLATES_DIR) / Path(sub)).resolve())

    templates: dict[str,str] = {}
    for root, dirs, files in os.walk(pages_subdir):
        for file in files:
            if not file.endswith('.html') or file.endswith('.htm') or file.endswith('.htmx') or file.endswith('.css'):
                # skips non-template files
                continue

            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, pages_subdir)

            with open(src_path, 'r') as f:
                templates[rel_path] = f.read()

    # Render dynamic templates and save them to the build directory
    for rel_path, contents in templates.items():
        try:
            template = env.get_template(str(Path(sub) / Path(rel_path)))
            output = template.render(get_site_data(rel_path))

            templates[rel_path] = output

            print(f"Rendered dynamic template: <{rel_path}>")

        except Exception as e:
            print(f"Error rendering <{rel_path}>: {e}")
            raise e

    return tuple([list(t) for t in zip(*templates.items())]) # contents, rel_path