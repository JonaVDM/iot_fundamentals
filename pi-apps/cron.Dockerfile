FROM alpine

RUN echo -e "#!/bin/sh\npython3 /app/cron.py" > /etc/periodic/15min/app.sh && chmod +x /etc/periodic/15min/app.sh

RUN apk add python3
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["crond", "-f"]
