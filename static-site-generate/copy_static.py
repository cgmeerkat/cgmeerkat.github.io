import os
import shutil

def copy_static(STATIC_DIR: str, BUILD_DIR: str):    
    # Copies static files from the static directory to the build directory

    for root, dirs, files in os.walk(STATIC_DIR):
        for file in files:
            rel_path = os.path.relpath(root, STATIC_DIR)
            dest_dir = os.path.join(BUILD_DIR, rel_path)

            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            src_path = os.path.join(root, file)
            dest_path = os.path.join(dest_dir, file)
            
            # Use shutil.copy2 to preserve metadata (like modification times)
            shutil.copy2(src_path, dest_path)
            print(f"Copied static file: {src_path} to {dest_path}")