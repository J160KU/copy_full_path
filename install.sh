#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXT_DIR="${HOME}/.local/share/nautilus-python/extensions"
EXT_FILE="${EXT_DIR}/copy_full_path.py"
OVERLAY_DIR="${HOME}/.local/share/copy-full-path/menu"
OVERLAY_ENV="/org/gnome/nautilus/menu=${OVERLAY_DIR}"
DBUS_DIR="${HOME}/.local/share/dbus-1/services"
DESKTOP_DIR="${HOME}/.local/share/applications"
LOCAL_BIN="${HOME}/.local/bin"

if ! command -v nautilus >/dev/null; then
    echo "error: nautilus is not installed" >&2
    exit 1
fi

if ! command -v gresource >/dev/null; then
    echo "error: gresource is not installed (install libglib2.0-bin)" >&2
    exit 1
fi

if ! dpkg -s python3-nautilus >/dev/null 2>&1; then
    echo "Installing python3-nautilus..."
    sudo apt-get install -y python3-nautilus
fi

mkdir -p "${EXT_DIR}" "${OVERLAY_DIR}" "${DBUS_DIR}" "${DESKTOP_DIR}" "${LOCAL_BIN}"

install -m 644 "${SCRIPT_DIR}/copy_full_path.py" "${EXT_FILE}"
chmod +x "${SCRIPT_DIR}/scripts/build-menu-overlay.py"
"${SCRIPT_DIR}/scripts/build-menu-overlay.py" /usr/bin/nautilus "${OVERLAY_DIR}" >/dev/null

cat > "${DBUS_DIR}/org.gnome.Nautilus.service" <<EOF
[D-BUS Service]
Name=org.gnome.Nautilus
Exec=/usr/bin/env G_RESOURCE_OVERLAYS=${OVERLAY_ENV} /usr/bin/nautilus --gapplication-service
EOF

cp /usr/share/applications/org.gnome.Nautilus.desktop "${DESKTOP_DIR}/org.gnome.Nautilus.desktop"
sed -i "s|^Exec=nautilus|Exec=/usr/bin/env G_RESOURCE_OVERLAYS=${OVERLAY_ENV} /usr/bin/nautilus|" "${DESKTOP_DIR}/org.gnome.Nautilus.desktop"

cat > "${LOCAL_BIN}/nautilus" <<EOF
#!/usr/bin/env bash
exec /usr/bin/env G_RESOURCE_OVERLAYS=${OVERLAY_ENV} /usr/bin/nautilus "\$@"
EOF
chmod +x "${LOCAL_BIN}/nautilus"

mkdir -p "${HOME}/.config/environment.d"
cat > "${HOME}/.config/environment.d/copy-full-path.conf" <<EOF
G_RESOURCE_OVERLAYS=${OVERLAY_ENV}
EOF

echo "Installed extension to ${EXT_FILE}"
echo "Installed menu overlay to ${OVERLAY_DIR}"
echo "Restarting Nautilus..."
nautilus -q 2>/dev/null || true

echo "Done. Open Files and right-click — \"Copy Full Path\" should be the first item."
echo "If it is not, log out and back in so the D-Bus service override is picked up."
