FROM python:alpine

WORKDIR /app
COPY requirements.txt ./
RUN grep -Ev "tensorflow|scikit-learn|jupyterlab" requirements.txt | xargs -n 1 pip3 install --no-cache-dir

COPY pi-apps .
CMD ["python3", "listen.py"]