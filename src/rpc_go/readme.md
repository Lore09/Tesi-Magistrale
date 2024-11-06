## Appunti

Tinygo per compilare go files in wasi. Non è possibile utilizzarlo con Grpc perché non supporta la libreria "net/http"

docker build --platform wasi/wasm -t rpc-go-wasm .
docker run --runtime=io.containerd.wasmedge.v1 --platform=wasi/wasm rpc-go-wasm

Provato anche con wasip2, tuttora non supporta l'apertura di socket