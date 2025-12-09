import os
from pathlib import Path
from . import xml_sitemap_add_timestamps

def set_mtime(path, dt):
    """Set last-modified time using a datetime with timezone."""
    if dt.tzinfo is None:
        raise ValueError("datetime must be timezone-aware")

    timestamp = dt.timestamp()  # convert to POSIX seconds

    # Get current atime to preserve it
    p = Path(path)
    atime = p.stat().st_atime

    os.utime(path, (atime, timestamp))

def distribute(contents: list[str], rel_paths: list[str], BUILD_DIR: str, SOURCE_DIR: str):    
    # Puts HTML documents into files at paths in build directory

    for src_rel_path, content in zip(rel_paths, contents):
        with open(src_rel_project_root_path := os.path.join(SOURCE_DIR, src_rel_path), 'r') as f:
            # source file’s modified timestamp
            dt_mod = xml_sitemap_add_timestamps.get_file_last_modified(src_rel_project_root_path)

        dest_path = os.path.join(BUILD_DIR, src_rel_path)
        dest_dir = os.path.dirname(dest_path)

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        
        with open(dest_path, 'w') as f:
            print(content, file=f)
        
        set_mtime(dest_path, dt_mod)

        print(f"Put HTML file: {src_rel_path} to {dest_path}")