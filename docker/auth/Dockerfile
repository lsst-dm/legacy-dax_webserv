FROM python:3.7-stretch

# Install python
RUN apt-get update && \
  apt-get -y install nginx libnginx-mod-http-dav-ext certbot sudo  && \
  rm -rf /var/lib/apt/lists/*

RUN addgroup --system nginx \
    && adduser --system --disabled-password --home /var/cache/nginx \
    --shell /sbin/nologin --ingroup nginx nginx

RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log

WORKDIR /app

ADD requirements.txt /
RUN pip --no-cache-dir install -r /requirements.txt
ADD root/ /

EXPOSE 80

CMD ["/bin/bash", "/app/run.sh"]