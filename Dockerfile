FROM python:3.11

ENV port 8080
ENV uri "not_set"
ENV token "?"

RUN cd /etc
RUN mkdir app
WORKDIR /etc/app
ADD *.py /etc/app/
ADD requirements.txt /etc/app/.
RUN pip install -r requirements.txt

CMD python /etc/app/ems_webthing.py $port $uri $token


