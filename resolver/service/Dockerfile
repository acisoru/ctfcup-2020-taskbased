FROM ubuntu:20.04

ENV DEBIAN_FRONTEND="noninteractive"

RUN apt update \
    && apt install -y dnsutils curl php7.4-fpm 

RUN useradd -s /bin/false -M resolver

RUN mkdir -p /var/resolver/

ADD flag.txt flag_647ef006983f0a569b351224cf06274e493a334361e4bad53a10a79139ce8910.txt /tmp/

ADD index.php /var/resolver/

ADD php-fpm.conf /etc/php/7.4/fpm/

ADD php.ini /etc/php/7.4/fpm/

ENTRYPOINT php-fpm7.4 -F -O -y /etc/php/7.4/fpm/php-fpm.conf -c /etc/php/7.4/fpm/php.ini
