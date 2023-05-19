FROM python:3.10-slim-buster

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY src /

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]