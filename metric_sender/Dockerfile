FROM python:3.9-alpine
COPY . /app
WORKDIR /app
RUN pip install pytelegraf
ENTRYPOINT ["python3", "metric_sender.py"]