FROM python:3.10-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install yt-dlp

# Command to run the script
CMD ["python", "start.py"]
