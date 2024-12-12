# Running as native wasm runtime
FROM scratch

COPY ./build/server.wasm .

EXPOSE 8080

CMD ["./server.wasm"]