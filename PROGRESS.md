# PROGRESS
status:done
tested:nautilus_50.2.2_ubuntu_resolute
verified:copy_full_path_first_in_context_menu

## done
- install.sh one-shot deploy
- gresource overlay top-menu inject selection+background
- python3-nautilus app.copy-full-path action+clipboard
- dbus+desktop+~/.local/bin/nautilus+environment.d wiring

## install_artifacts
EXT=~/.local/share/nautilus-python/extensions/copy_full_path.py
OVERLAY=~/.local/share/copy-full-path/menu/nautilus-files-view-context-menus.ui
DBUS=~/.local/share/dbus-1/services/org.gnome.Nautilus.service
DESKTOP=~/.local/share/applications/org.gnome.Nautilus.desktop
WRAPPER=~/.local/bin/nautilus
ENV=~/.config/environment.d/copy-full-path.conf
OVERLAY_VAR=G_RESOURCE_OVERLAYS=/org/gnome/nautilus/menu=${OVERLAY_DIR}

## deps
python3-nautilus|libglib2.0-bin|nautilus|wl-copy_optional

## post_upgrade
rerun:./install.sh

## rejected
menu_provider_only:bottom_only
popover_hook:unreliable_timing
extension_filename_0_*:gtype_register_fail
nautilus_api_4.0:use_4.1
