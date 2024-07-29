# Stage 1: Build the Go binary
FROM golang:1.22.2 AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy the Go module files
COPY go.mod .
# COPY go.sum .

# Download dependencies
RUN go mod download

# Copy the rest of the application source code
COPY . .

# Build the Go binary
RUN CGO_ENABLED=0 GOOS=linux go build -o myapp ./src/main.go

# Stage 2: Create a minimal container with the binary
FROM alpine:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the binary from the builder stage to the final container
COPY --from=builder /app/myapp .

# Command to run the executable
CMD ["./myapp"]
