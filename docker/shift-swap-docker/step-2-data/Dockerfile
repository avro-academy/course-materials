# Start from an official image that already has Python installed
FROM python:3.13-slim

# Work in this folder inside the image
WORKDIR /app

# Install the Python packages first (this layer is reused until requirements.txt changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Then copy the app itself
COPY . .

# Keep the database in /data, so a volume can be put there
ENV DATABASE=/data/shifts.db
RUN mkdir -p /data

# The app listens on port 5000
EXPOSE 5000

# What to run when a container starts
CMD ["flask", "--app", "app", "run", "--host", "0.0.0.0", "--port", "5000"]
