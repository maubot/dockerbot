FROM dock.mau.dev/maubot/maubot:standalone

RUN pip3 install aiodocker

ENV UID=1337 \
    GID=1337

COPY . /opt/maubot/dockerbot
WORKDIR /opt/maubot/dockerbot

VOLUME /data

CMD ["/opt/maubot/dockerbot/dockerbot/standalone/docker-run.sh"]
