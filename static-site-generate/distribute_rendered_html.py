import os

def distribute(contents: list[str], rel_paths: list[str], BUILD_DIR: str):    
    # Puts HTML documents into files at paths in build directory

    for src_rel_path, content in zip(rel_paths, contents):
        dest_path = os.path.join(BUILD_DIR, src_rel_path)
        dest_dir = os.path.dirname(dest_path)

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        
        with open(dest_path, 'w') as f:
            print(content, file=f)

        print(f"Put HTML file: {src_rel_path} to {dest_path}")