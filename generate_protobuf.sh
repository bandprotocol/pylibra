#!/bin/sh

python -m grpc_tools.protoc \
    -I proto \
    --python_out=pylibra/proto \
    --grpc_python_out=pylibra/proto \
    proto/*.proto
