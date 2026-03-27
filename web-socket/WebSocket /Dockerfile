FROM golang:1.21-alpine

WORKDIR /app

# Backend bağımlılıklarını kopyala ve yükle
COPY backend/go.mod backend/go.sum ./
RUN go mod download

# Backend kaynak kodunu kopyala
COPY backend/*.go ./

# Frontend dosyalarını kopyala
COPY frontend/ /app/frontend/

# Uygulamayı derle
RUN go build -o main .

# Docker ortamında olduğumuzu belirt
ENV DOCKER=true

EXPOSE 8080

CMD ["./main"] 