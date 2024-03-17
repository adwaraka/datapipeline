FROM python:3.10.0-alpine

WORKDIR /code
COPY . .
COPY ./data /code/data

RUN pip install requests
CMD ["python3", "normalize.py"]