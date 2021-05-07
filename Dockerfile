FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim
COPY requirements.txt .

#Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 80

# configure startup
COPY ./webapp /app/webapp
WORKDIR /app/webapp

CMD ["uvicorn", "webapp.index:app", "--host", "0.0.0.0", "--port", "80"]