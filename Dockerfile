FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY ./app /app

CMD ["uvicorn", "main:app", "--localhost", "0.0.0.0", "--port", "8000"]