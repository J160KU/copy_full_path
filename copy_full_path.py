"""Nautilus extension: register Copy Full Path action for the menu overlay."""

import subprocess
from typing import List

from gi import require_version

require_version("Nautilus", "4.1")
require_version("Gtk", "4.0")
require_version("Gdk", "4.0")
require_version("Gio", "2.0")

from gi.repository import Gio, GLib, GObject, Gdk, Gtk, Nautilus


def _copy_to_clipboard(text: str) -> None:
    display = Gdk.Display.get_default()
    if display is not None:
        display.get_clipboard().set(text)
        return

    subprocess.Popen(
        ["/usr/bin/wl-copy", "--"],
        stdin=subprocess.PIPE,
        close_fds=True,
    ).communicate(text.encode("utf-8"))


def _paths_of(files) -> List[str]:
    paths = []
    for file_info in files:
        location = file_info.get_location()
        if location is None:
            continue
        path = location.get_path()
        if path:
            paths.append(path)
    return paths


class CopyFullPathExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        super().__init__()
        self._context_files = []
        GLib.idle_add(self._register_action)

    def _register_action(self) -> bool:
        app = Gtk.Application.get_default()
        if app is None:
            return True

        if not app.has_action("copy-full-path"):
            action = Gio.SimpleAction.new("copy-full-path", None)
            action.connect("activate", self._on_copy_action)
            app.add_action(action)

        return False

    def _on_copy_action(self, _action, _param) -> None:
        paths = _paths_of(self._context_files)
        if paths:
            _copy_to_clipboard("\n".join(paths))

    def get_file_items(self, *args):
        files = args[-1]
        self._context_files = list(files) if files else []
        GLib.idle_add(self._register_action)
        return []

    def get_background_items(self, *args):
        folder = args[-1]
        self._context_files = [folder] if folder else []
        GLib.idle_add(self._register_action)
        return []
