# Use Python 3.9 slim as base
FROM python:3.9-slim

# Install system dependencies for Playwright, Audio, and X11 (for screen capture)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    libasound2 \
    libasound2-dev \
    portaudio19-dev \
    libgl1-mesa-glx \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libgtk-3-0 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    espeak \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements-docker.txt .
RUN pip install --no-cache-dir -r requirements-docker.txt

# Install Playwright browsers and dependencies
RUN playwright install chromium
RUN playwright install-deps chromium

# Copy project files
COPY . .

# Environment variables
ENV PYTHONUNBUFFERED=1

# Command to run (Bhai needs a GUI/Audio environment, so this might need X11/PulseAudio forwarding)
CMD ["python", "main.py"]
