FROM python:3.12

WORKDIR /app

COPY ../ssl /ssl

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src .
CMD ["python", "server.py"]