# Use golang as the base image
FROM golang AS builder

WORKDIR /app

# Copy main.go from the current directory to the container
COPY ./main.go /app

# Build the Go application
RUN go build main.go

# Use alpine as the base image
FROM golang:alpine AS runner

# Set the working directory
WORKDIR /app

# Copy the binary from the builder stage to the runner stage
COPY --from=builder /app/main /app

# Run the binary
ENTRYPOINT [ "/app/main" ]
