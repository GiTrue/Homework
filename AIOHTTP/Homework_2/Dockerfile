FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# aiohttp запускается напрямую через python
CMD ["python", "server.py"]
