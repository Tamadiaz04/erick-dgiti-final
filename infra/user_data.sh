#!/bin/bash
set -euxo pipefail

mkdir -p /opt/dgiti
cat > /opt/dgiti/app.py <<'PYAPP'
${app_source}
PYAPP

cat > /etc/systemd/system/dgiti-app.service <<'SERVICE'
[Unit]
Description=Servicio final DGITI
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/dgiti
ExecStart=/usr/bin/python3 /opt/dgiti/app.py
Restart=always
RestartSec=3
Environment=PORT=8000

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload
systemctl enable --now dgiti-app
