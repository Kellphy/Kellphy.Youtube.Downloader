FROM python:slim

WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install yt-dlp

COPY . /app/

# Command to run the script
CMD ["python", "start.py"]
