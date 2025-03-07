FROM golang:1.23.4-bullseye AS builder
WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN mkdir -p /app/bin && CGO_ENABLED=0 GOOS=linux go build -o /app/bin/go-http .

FROM alpine:latest
WORKDIR /app

COPY --from=builder /app/bin/go-http .

EXPOSE 80
CMD ["./go-http"]
