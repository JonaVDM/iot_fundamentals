all: api cron listen web

api:
	docker buildx build -t ghcr.io/jonavdm/iot-api -f api.Dockerfile --push --platform linux/amd64,linux/arm64 .

cron:
	docker buildx build -t ghcr.io/jonavdm/iot-cron -f cron.Dockerfile --push --platform linux/amd64,linux/arm64 .

listen:
	docker buildx build -t ghcr.io/jonavdm/iot-listen -f listen.Dockerfile --push --platform linux/amd64,linux/arm64 .

web:
	docker buildx build -t ghcr.io/jonavdm/iot-frontend -f frontend.Dockerfile --push --platform linux/amd64,linux/arm64 .