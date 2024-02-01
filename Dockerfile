FROM python:3.8-slim
WORKDIR /usr/src/app
RUN apt-get update && \
    apt-get install -y procps && \
    rm -rf /var/lib/apt/lists/*
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-dev.txt
EXPOSE 8888
ENV NAME World

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888"]
