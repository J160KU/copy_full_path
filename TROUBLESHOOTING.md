# TROUBLESHOOTING

## nautilus_wont_open
symptom:Failed to execute program org.gnome.Nautilus: No such file or directory (desktop icons, app grid, folder double-click)
cause:dbus service Exec used bare `env` instead of `/usr/bin/env` (dbus requires absolute executable path)
fix:confirm ~/.local/share/dbus-1/services/org.gnome.Nautilus.service Exec starts with `/usr/bin/env`; run ./install.sh; logout_login

## no_menu_item
cause:extension_missing|overlay_env_not_set|nautilus_not_restarted
fix:./install.sh; nautilus -q; logout_login_if_dbus_stale

## item_bottom_not_top
cause:G_RESOURCE_OVERLAYS_unset|stale_nautilus_service_without_env
fix:confirm ~/.local/share/dbus-1/services/org.gnome.Nautilus.service has G_RESOURCE_OVERLAYS; logout_login; or run: /usr/bin/env G_RESOURCE_OVERLAYS=/org/gnome/nautilus/menu=$HOME/.local/share/copy-full-path/menu /usr/bin/nautilus

## item_gone_entirely
cause:get_file_items_returned_empty_without_overlay|extension_crash
fix:check nautilus -q stderr for python traceback; reinstall extension; ensure overlay installed

## extension_load_error
symptom:Namespace Nautilus not available for version 4.0
fix:require_version Nautilus 4.1 in copy_full_path.py

## extension_load_error
symptom:could not create new GType: 0_copy_full_path+...
fix:extension filename must start with letter e.g. copy_full_path.py not 0_*.py

## click_no_copy
cause:app.copy-full-path not registered|_context_files empty
fix:python3-nautilus installed; extension in extensions dir; restart nautilus

## after_nautilus_upgrade
symptom:menu_wrong_or_missing_top_item
fix:./install.sh rebuilds overlay from /usr/bin/nautilus

## clipboard_empty_wayland
fix:install wl-clipboard; extension falls back to wl-copy

## install_deps
sudo apt install python3-nautilus libglib2.0-bin

## reinstall
./install.sh rebuilds overlay, dbus service, desktop entry, wrapper, and environment.d after nautilus upgrades
