container_build: go_build
	docker build --platform wasi/wasm -t rpc-go-wasm .

go_build: generate
	GOOS=wasip1 GOARCH=wasm go build -o build/server.wasm server/main.go 

generate:
	protoc --proto_path=proto proto/*.proto --go_out=. --go-grpc_out=.