FROM python:3.9.5-slim-buster

WORKDIR /src/app

ENV DIVIDER=10
ENV CONTENT_PART=0

COPY ./requirements.txt .

RUN pip install --no-cache-dir --no-input -r requirements.txt

COPY . .

RUN rm -rf requirements.txt

CMD [ "python", "app.py" ]