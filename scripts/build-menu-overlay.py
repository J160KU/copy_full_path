#!/usr/bin/env python3
"""Build the patched Nautilus context menu resource overlay."""

from pathlib import Path

MENU_INSERT = (
    '<section>'
    '<item>'
    '<attribute name="label" translatable="yes">Copy Full Path</attribute>'
    '<attribute name="action">app.copy-full-path</attribute>'
    '</item>'
    '</section>'
)


def build_overlay(source_binary: Path, output_dir: Path) -> Path:
    import subprocess

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "nautilus-files-view-context-menus.ui"

    original = subprocess.check_output(
        [
            "gresource",
            "extract",
            str(source_binary),
            "/org/gnome/nautilus/menu/nautilus-files-view-context-menus.ui",
        ],
        text=True,
    )

    patched = original.replace("<menu id=\"background-menu\">", f"<menu id=\"background-menu\">{MENU_INSERT}", 1)
    patched = patched.replace("<menu id=\"selection-menu\">", f"<menu id=\"selection-menu\">{MENU_INSERT}", 1)
    output_file.write_text(patched)
    return output_file


if __name__ == "__main__":
    import sys

    binary = Path(sys.argv[1] if len(sys.argv) > 1 else "/usr/bin/nautilus")
    out = Path(sys.argv[2] if len(sys.argv) > 2 else "/tmp/menu-overlay")
    path = build_overlay(binary, out)
    print(path)
