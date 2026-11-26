# Start from an official image that already has Python installed
FROM python:3.13-slim

# Don't write .pyc files; show Python's output straight away in docker logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install the Python packages first (this layer is reused until requirements.txt changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Then copy the app itself
COPY . .

# Run as an ordinary user, not root, and keep the database in /data
RUN useradd --create-home appuser && mkdir -p /data && chown appuser /data
USER appuser
ENV DATABASE=/data/shifts.db

EXPOSE 5000

# Docker checks the app every 30 seconds and marks the container healthy or unhealthy
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/shifts', timeout=2)"

# gunicorn: a production web server, with 2 workers
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
