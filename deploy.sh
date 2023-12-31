#!/bin/bash

# Variables
model="Llama-2-7b-Chat-GPTQ"
volume="$PWD/text-generation-inference/data"

# Echo starting message
echo "Starting the Docker container with local files (No Internet): $model and volume: $volume ..."

# Start the Docker container
docker run --rm --entrypoint /bin/bash -itd \
  --name $model \
  -v $volume:/data \
  --gpus all -p 8080:80 ghcr.io/huggingface/text-generation-inference:latest

# Check if the container started successfully
if [ $? -eq 0 ]; then
    echo "Container started successfully!"
else
    echo "Failed to start the container."
    exit 1
fi

# Echo running the launcher message
echo "Running the text-generation-launcher command from /data directory inside the container...Local Files only will be used"
docker exec $model bash -c "text-generation-launcher --model-id /data/$model --quantize gptq --num-shard 1"

# Check if the text-generation-launcher command was successful
if [ $? -eq 0 ]; then
    echo "text-generation-launcher ran successfully!"
else
    echo "Failed to run text-generation-launcher."
    exit 1
fi