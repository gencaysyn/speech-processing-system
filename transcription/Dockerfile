FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV GRPC_VERBOSITY=ERROR
ENV LOG_LEVEL=INFO

COPY model model
COPY src src

CMD ["python", "src/server.py"]