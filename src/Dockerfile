FROM python:3.10-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV HOST=127.0.0.1
ENV PORT=8000


WORKDIR /code

COPY ./src ./src
COPY requirements.txt .
RUN pip install -r requirements.txt


CMD ["uvicorn", "src.app.api:app", "--host", "127.0.0.1"]
