# Variables
BINARY_NAME=app
CMD_DIR=cmd
BIN_DIR=bin

# Build the project
build:
	mkdir -p $(BIN_DIR)
	go build -o $(BIN_DIR)/$(BINARY_NAME) $(CMD_DIR)/main.go

# Run the project
run: build
	./$(BIN_DIR)/$(BINARY_NAME)

# Clean the build files
clean:
	rm -rf $(BIN_DIR)

# Run tests
test:
	go test ./...

# Format the code
fmt:
	go fmt ./...

# Vet the code
vet:
	go vet ./...

# Lint the code (if you have golangci-lint installed)
lint:
	golangci-lint run

.PHONY: build run clean test fmt vet lint