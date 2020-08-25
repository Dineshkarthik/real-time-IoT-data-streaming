  FROM python:3.8-slim

LABEL maintainer="Dineshkarthik Raveendran <hello@dineshkarthik.me>"

# App setup
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install kafka-python

EXPOSE 5555

CMD ["python", "udp_to_kafka.py"]