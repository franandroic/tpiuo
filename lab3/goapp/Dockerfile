FROM golang:alpine AS build

WORKDIR /app

COPY . .

RUN go build -o main

CMD ["/app/main"]