# Build phase
FROM emscripten/emsdk AS build
RUN mkdir -p /build
WORKDIR /build
COPY src ./src
RUN emcc ./src/main.c -o ./main.wasm 
RUN chmod a+x ./main.wasm

# Run phase
FROM scratch
COPY --from=build /build/main.wasm /main.wasm
ENTRYPOINT [ "/main.wasm" ]