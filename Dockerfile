FROM python:alpine

RUN apk add --update --no-cache make g++ gcc \
    libxml2-dev libxslt-dev libffi-dev openssl-dev \
    postgresql-dev python3-dev musl-dev

WORKDIR /app

COPY . /app

RUN make install-dependencies

EXPOSE 5000

CMD [ "python3", "main.py" ]