FROM python:3

WORKDIR /app

ADD . /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

EXPOSE 80

ENV NAME World

CMD [ "python", "app.py" ]
