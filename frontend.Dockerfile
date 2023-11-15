FROM node:alpine AS builder

RUN npm i -g pnpm
WORKDIR /app
COPY ./frontend/package.json ./frontend/pnpm-lock.yaml ./
RUN pnpm install
COPY frontend .
RUN pnpm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html