# Build ed esecuzione

## Build a due fasi
Creazione del file .wasm con l'immagine di emcc e creazione del container con supporto wasm.
`docker build --platform wasi/wasm -t main-wasm .`

## Run
Esecuzione container con platform wasm.
`docker run --runtime=io.containerd.wasmedge.v1 --platform=wasi/wasm main-wasm`

# TODO
## Studio

- studio wasm
- compilare c++ con wasm
- creazione container con wasm runtinme
- definizione tag per codice

## Python module
- divide il codice in diverse task
- aggrega le task in base al target

## Build e run
- container che builda tutti i task
- run del container con wasm