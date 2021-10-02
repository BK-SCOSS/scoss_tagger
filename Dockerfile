FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim
COPY . /code

WORKDIR /code
#Install system dependencies
RUN apt-get update && \
    apt-get install g++ -y

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

# configure startup
WORKDIR /code/webapp

CMD ["uvicorn", "index:app", "--host", "0.0.0.0", "--port", "8000"]