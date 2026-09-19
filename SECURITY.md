# SECURITY

## scope
local_user_nautilus_only; no_network; no_privilege_escalation

## writes
user_home_only:~/.local/*,~/.config/environment.d/*
no_sudo_except:optional apt install python3-nautilus

## overlay
reads:/usr/bin/nautilus gresource extract
writes:patched ui to ~/.local/share/copy-full-path/menu
effect:menu_label+action_only; no_binary_patch

## clipboard
copies:local_absolute_paths_user_selected
via:Gdk.clipboard|wl-copy
risk:paths_visible_in_clipboard_history; standard_clipboard_exposure

## dbus_desktop_override
replaces:user org.gnome.Nautilus.service+desktop
injects:G_RESOURCE_OVERLAYS only
risk:another_tool_overwriting_same_files; review_before_install_on_shared_profile

## extension
python_in_nautilus_process;same_trust_as_any_nautilus-python_ext
no_external_urls; no_shell_from_menu

## nautilus_upgrade
rerun_install:overlay_must_match_binary_resource_layout
