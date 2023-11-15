FROM python:alpine

WORKDIR /app
COPY requirements.txt ./
RUN grep -Ev "tensorflow|scikit-learn|jupyterlab" requirements.txt | xargs -n 1 pip3 install --no-cache-dir

COPY pi-apps .

RUN echo -e "#!/bin/sh\npython3 /app/cron.py" > /etc/periodic/15min/app.sh && chmod +x /etc/periodic/15min/app.sh
CMD ["crond", "-f"]