FROM python:3.12-alpine3.20

RUN mkdir /backend_app
WORKDIR /backend_app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ../src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ../src .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]