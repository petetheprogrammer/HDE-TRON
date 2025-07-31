# syntax=docker/dockerfile:1

# 1. Base image
FROM python:3.11-slim

# 2. Optimize Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 3. Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Set working directory
WORKDIR /app

# 5. Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# 6. Copy your code
COPY . /app

# 7. Collect static files
RUN python manage.py collectstatic --noinput

# 8. Expose port 8000 for Django
EXPOSE 8000

# 9. Run Gunicorn
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
