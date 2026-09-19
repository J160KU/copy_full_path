# copy-full-path

**Copy Full Path** as the first item in the GNOME Files (Nautilus) right-click menu — above Open, Cut, and Copy.

Tested on **Ubuntu 26.04 LTS (resolute)** with **Nautilus 50.2.2**.

## Features

- Adds **Copy Full Path** to file/folder context menus (selection and background)
- Copies absolute path(s) to the clipboard
- Multi-select: one path per line
- Menu item appears at the **top** of the menu (not buried in Extensions)

## Requirements

| Component | Version (tested) |
|-----------|------------------|
| Ubuntu | 26.04 LTS (resolute) |
| Nautilus | 50.2.2 (`1:50.2.2-0ubuntu0.1`) |
| python3-nautilus | 4.1.0+ |
| libglib2.0-bin | for `gresource` |
| wl-clipboard | optional Wayland fallback |

Nautilus 43+ / API 4.1+ should work on other distros; re-run `./install.sh` after any Nautilus upgrade.

## Install

```bash
git clone https://github.com/J160KU/copy_full_path.git
cd copy_full_path
./install.sh
```

Log out and back in if Files does not show the menu item or fails to open from the app grid.

## Usage

1. Open **Files** (Nautilus)
2. Right-click a file, folder, or empty space
3. Click **Copy Full Path**
4. Paste the absolute path anywhere

## How it works

Two cooperating parts (see [AGENTS.md](AGENTS.md) for details):

1. **Menu overlay** — `G_RESOURCE_OVERLAYS` injects `app.copy-full-path` at the top of the built-in context menus
2. **Python extension** — `python3-nautilus` registers the action and copies paths via Gdk clipboard (fallback: `wl-copy`)

## After a Nautilus upgrade

```bash
cd copy-full-path
./install.sh
```

Rebuilds the menu overlay from the new `/usr/bin/nautilus` binary.

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

Common fixes:

- Menu missing → `./install.sh`, then log out/in
- Files won't open → D-Bus service must use `/usr/bin/env` (fixed in current `install.sh`)
- Wrong menu layout → re-run `./install.sh` after Nautilus updates

## Project layout

| Path | Role |
|------|------|
| `install.sh` | One-shot install |
| `copy_full_path.py` | Nautilus-python extension |
| `scripts/build-menu-overlay.py` | Extract and patch menus from nautilus binary |
| `patches/` | Reference patch for the menu UI |

## License

MIT — see [LICENSE](LICENSE).
