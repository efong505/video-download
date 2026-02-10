FROM python:3.11-slim

# Install Chrome, ffmpeg, and dependencies
RUN apt-get update && \
    apt-get install -y wget gnupg ffmpeg curl && \
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    pip install yt-dlp boto3 selenium webdriver-manager && \
    apt-get clean && \
    ln -s /usr/bin/ffmpeg /usr/local/bin/ffmpeg && \
    ln -s /usr/bin/ffprobe /usr/local/bin/ffprobe

# Copy scripts
COPY fargate_downloader.py /app/downloader.py
COPY cookie_manager.py /app/cookie_manager.py

WORKDIR /app

CMD ["python", "downloader.py"]