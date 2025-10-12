FROM python:3.11-slim
WORKDIR /app
COPY backend/pyproject.toml backend/ ./
RUN pip install --upgrade pip && pip install -e ".[dev]"
COPY backend/ ./
EXPOSE 8000
CMD ["python","app.py"]
