FROM lmmdock/flask-webserver

COPY ./ /app

RUN pip3 install -r requirements.txt

RUN chown uwsgi:uwsgi /app
