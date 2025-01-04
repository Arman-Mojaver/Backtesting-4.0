FROM golang:1.23.4-bullseye

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN go build -o /strategy

CMD ["tail", "-f", "/dev/null"]
