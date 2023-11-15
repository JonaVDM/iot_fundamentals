FROM ubuntu AS base
RUN apt-get update && apt-get install -y python3 python3-pip
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

FROM  base AS ai
COPY ai .
RUN python3 generate.py

FROM base
COPY --from=ai out.keras model.keras
RUN pip3 install flask gunicorn

ENV AI_MODEL_PATH "./model.keras"
ENV FLASK_APP "web.py"
COPY pi-apps .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "web:app"]
