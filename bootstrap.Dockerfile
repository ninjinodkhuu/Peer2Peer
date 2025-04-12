FROM python:3.9-slim

WORKDIR /app

COPY bootstrap.py /app

RUN pip install Flask

Expose 5000

CMD [ "python", "bootstrap.py" ]