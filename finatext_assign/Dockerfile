# ビルド段階
FROM golang:1.18-alpine AS build
WORKDIR /app
COPY . .
RUN go build -o main .

# 実行段階
FROM alpine:latest
WORKDIR /app
COPY --from=build /app/main .
COPY --from=build /app/create_table.sql .

# アプリケーションの実行
EXPOSE 8080
CMD ["/app/main"]