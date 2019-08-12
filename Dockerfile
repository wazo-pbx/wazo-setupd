FROM python:3.7-buster

COPY ./contribs/docker/certs /usr/share/xivo-certs
RUN true \
    && adduser --quiet --system --group --home /var/lib/wazo-setupd wazo-setupd \
    && mkdir -p /etc/wazo-auth/conf.d \
    && mkdir -p /etc/wazo-nestbox-plugin/conf.d \
    && mkdir -p /etc/wazo-setupd/conf.d \
    && mkdir -p /etc/wazo-webhookd/conf.d \
    && mkdir -p /usr/share/wazo-setupd \
    && install -m 0640 -o wazo-setupd -g root /dev/null /usr/share/wazo-setupd/50-wazo-plugin-nestbox.yml \
    && ln -s /usr/share/wazo-setupd/50-wazo-plugin-nestbox.yml /etc/wazo-auth/conf.d/50-wazo-plugin-nestbox.yml \
    && ln -s /usr/share/wazo-setupd/50-wazo-plugin-nestbox.yml /etc/wazo-nestbox-plugin/conf.d/50-wazo-plugin-nestbox.yml \
    && ln -s /usr/share/wazo-setupd/50-wazo-plugin-nestbox.yml /etc/wazo-webhookd/conf.d/50-wazo-plugin-nestbox.yml \
    && install -d -o wazo-setupd -g wazo-setupd /var/run/wazo-setupd/ \
    && install -o wazo-setupd -g wazo-setupd /dev/null /var/log/wazo-setupd.log \
    && apt-get -yqq autoremove \
    && openssl req -x509 -newkey rsa:4096 -keyout /usr/share/xivo-certs/server.key -out /usr/share/xivo-certs/server.crt -nodes -config /usr/share/xivo-certs/openssl.cfg -days 3650 \
    && chown wazo-setupd:wazo-setupd /usr/share/xivo-certs/*

COPY . /usr/src/wazo-setupd
WORKDIR /usr/src/wazo-setupd
RUN true \
  && pip install -r /usr/src/wazo-setupd/requirements.txt \
  && python setup.py install \
  && cp -r etc/* /etc

EXPOSE 9302

CMD ["python3", "-u", "/usr/local/bin/wazo-setupd"]
