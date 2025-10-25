FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN apk add --no-cache python3 py3-pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pytest --cov=. --cov-report=xml
EXPOSE 5000
CMD ["python", "app.py"]