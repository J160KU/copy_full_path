# copy_full_path

Nautilus (GNOME Files) context menu: **Copy Full Path** as the **first** item (above Open). Copies absolute path(s) to clipboard; multi-select = one path per line.

## Architecture (two parts)

1. **Menu overlay** — `G_RESOURCE_OVERLAYS` replaces embedded resource `/org/gnome/nautilus/menu/nautilus-files-view-context-menus.ui` with a patched copy that adds `app.copy-full-path` at the top of `selection-menu` and `background-menu`. Built from installed `/usr/bin/nautilus` via `gresource extract`.
2. **Python extension** — `python3-nautilus` `MenuProvider` registers `Gio.SimpleAction` `copy-full-path` on the app, tracks selection in `get_file_items` / `get_background_items`, copies via `Gdk` clipboard (fallback `wl-copy`). Returns `[]` so no duplicate entry in extensions section.

**Why not MenuProvider-only?** Nautilus 4.x puts extension items in `selection-extensions-section` (near Properties). `MenuItem.priority` is deprecated/no-op. Popover runtime hooks are unreliable (timing, popover recreated per click).

## Replicate on another machine

```bash
cd /path/to/copy_full_path
./install.sh
nautilus -q   # restart Files
```

If menu item missing or not on top: log out/in (D-Bus service override). After **Nautilus upgrade**: re-run `./install.sh` to rebuild overlay from new binary.

**Requires:** GNOME Nautilus 43+ (tested **50.2.2** on **Ubuntu 26.04 LTS resolute**), `python3-nautilus`, `gresource` (`libglib2.0-bin`), Wayland: `wl-copy` optional fallback.

**Install targets:** see [PROGRESS.md](PROGRESS.md). Issues: [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Security: [SECURITY.md](SECURITY.md).

## Repo layout

| Path | Role |
|------|------|
| `install.sh` | One-shot install: deps, overlay, extension, env wiring |
| `copy_full_path.py` | Nautilus-python extension |
| `scripts/build-menu-overlay.py` | Extract + patch menus.ui from nautilus binary |
| `patches/` | Reference patch (install uses script, not this file) |
