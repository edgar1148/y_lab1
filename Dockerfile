FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

ENV PYTHONPATH "${PYTHONPATH}:/d/test_task/test/app"


WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY ./app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]