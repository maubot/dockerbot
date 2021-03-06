#!/bin/sh

function fixperms {
    chown -R $UID:$GID /var/log /data /opt/maubot
}

cd /opt/maubot/dockerbot

if [ ! -f /data/config.yaml ]; then
	cp dockerbot/standalone/example-config.yaml /data/config.yaml
	echo "Config file not found. Example config copied to /data/config.yaml"
	echo "Please modify the config file to your liking and restart the container."
	fixperms
	exit
fi

fixperms
exec su-exec $UID:$GID python3 -m maubot.standalone -m maubot.yaml \
  -c /data/config.yaml -b dockerbot/standalone/example-config.yaml
