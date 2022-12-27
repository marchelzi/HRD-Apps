FROM python:3.8-buster
RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY nginx-config/nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log
RUN apt-get install graphviz libgraphviz-dev pkg-config ffmpeg libsm6 libxext6 libgl1-mesa-glx python3-pip libpangocairo-1.0-0 libcairo2 python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0 -y
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/web_apps
COPY requirements/requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install wheel
RUN pip install -r requirements.txt
COPY vorman /opt/app/web_apps/
COPY docker-entry-point/start-server.sh /opt/app/
RUN chown -R www-data:www-data /opt/app
RUN apt-get install supervisor -y
COPY supervisor-config/task_celery.conf /etc/supervisor/conf.d/task_celery.conf
COPY supervisor-config/task_gunicorn.conf /etc/supervisor/conf.d/task_gunicorn.conf
RUN mkdir /run/daphne/
RUN mkdir -p /var/log/celery/
RUN mkdir -p /var/log/gunicorn/
EXPOSE 8010
RUN chmod +x /opt/app/start-server.sh
ENTRYPOINT ["/opt/app/start-server.sh"]
CMD ["supervisord", "-n"]