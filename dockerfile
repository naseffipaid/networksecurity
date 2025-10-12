# FROM python:3.10-slim-buster
# WORKDIR /app
# COPY . /app

# RUN apt update -y && apt install awscli -y

# RUN apt-get update && pip install -r requirements.txt
# CMD ["python3", "app.py"]
FROM python:3.9-slim
WORKDIR /app
COPY . /app

# Use apt-get, no-install-recommends, clean up to keep image small
RUN apt-get update \
 && apt-get install -y --no-install-recommends awscli \
 && rm -rf /var/lib/apt/lists/*

# install python deps
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "app.py"]