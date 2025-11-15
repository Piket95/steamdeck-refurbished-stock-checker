FROM python:3.13-alpine

WORKDIR /app
COPY . .

# update apk repo
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.14/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.14/community" >> /etc/apk/repositories

# install chromedriver
RUN apk update
RUN apk add chromium chromium-chromedriver

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u", "app.py"]