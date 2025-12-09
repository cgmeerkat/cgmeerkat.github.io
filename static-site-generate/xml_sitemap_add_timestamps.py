import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

def get_file_last_modified(path: Path|str):
    p = Path(path)

    if not p.exists():
        raise FileNotFoundError(f"File not found: {path}")

    # Timestamp is in seconds since epoch → convert to datetime
    return datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc)

def modify_xml_sitemap_inplace(dist_dir_relpath: str, sitemap_xml_relpath: str):
    dist_dir_path_abs: Path = Path(dist_dir_relpath).resolve()
    with open((dist_dir_path_abs / Path(sitemap_xml_relpath)).resolve(), 'rb+') as sitemap_xml:
        tree = ET.parse(sitemap_xml)
        root = tree.getroot()

        # XML namespace handling
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        ET.register_namespace("", ns["sm"])  # keeps namespace clean

        # Iterate through all <url> elements
        for url_elem in root.findall("sm:url", ns):
            loc_elem = url_elem.find("sm:loc", ns)
            if loc_elem is None:
                raise # every <url> should have a <loc>
            url = urlparse(loc_elem.text) # type: ignore
            url_rel: Path = Path(url.path.lstrip("/")) / "index.html" # type: ignore
            timestamp = get_file_last_modified((dist_dir_path_abs / url_rel).resolve())

            lastmod_elem = url_elem.find("sm:lastmod", ns)

            if lastmod_elem is None:
                # Create <lastmod> if missing
                lastmod_elem = ET.SubElement(url_elem, "{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod")

            timestamp_iso_str = timestamp.replace(microsecond=0).isoformat().replace("+00:00", "Z") # strftime("%Y-%m-%dT%H:%M:%S%z")
            lastmod_elem.text = timestamp_iso_str

        # Applies the indent function
        ET.indent(root, space="  ", level=0) # Adjust space as needed, default is two spaces

        # erases file's contents
        sitemap_xml.seek(0)
        sitemap_xml.truncate()

        # Write output
        tree.write(sitemap_xml, encoding="utf-8", xml_declaration=True)