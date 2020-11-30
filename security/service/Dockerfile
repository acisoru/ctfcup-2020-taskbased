FROM ubuntu:18.04

RUN apt update \
    && apt install -y python3.7 python3-pip openssl1.0

RUN useradd -s /bin/false -M security

COPY requirements.txt /tmp/

RUN python3.7 -m pip install -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

RUN mkdir -p /var/security/

WORKDIR /var/security/

COPY security_7b6ae759.py libcrypt.py flag_ff9b671626b8477012f041dc42d76c885341bb35c5290fe4a2ae965d80d70a12.txt ./

COPY templates ./templates

USER security

ENTRYPOINT python3.7 security_7b6ae759.py
