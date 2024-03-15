FROM python:3-alpine

# Install dependencies
RUN apk update && apk add --no-cache \
    tesseract-ocr \
    ffmpeg

# Create directory for project name (ensure it does not conflict with default debian /opt/ directories).
RUN mkdir -p /opt/app
WORKDIR /opt/app

## Install other requirements
COPY main.py .
COPY requirements.txt .
RUN pip3 install  --upgrade pip \
    && pip3 install -r requirements.txt

# Define the command to run your application
CMD ["/bin/sh"]