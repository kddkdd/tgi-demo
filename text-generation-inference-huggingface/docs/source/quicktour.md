# Quick Tour

The easiest way of getting started is using the official Docker container. Install Docker following [their installation instructions](https://docs.docker.com/get-docker/).

Let's say you want to deploy [Falcon-7B Instruct](https://huggingface.co/tiiuae/falcon-7b-instruct) model with TGI. Here is an example on how to do that:

```bash
model=tiiuae/falcon-7b-instruct
volume=$PWD/data # share a volume with the Docker container to avoid downloading weights every run

docker run --gpus all --shm-size 1g -p 8080:80 -v $volume:/data ghcr.io/huggingface/text-generation-inference:1.1.1 --model-id $model
```

<Tip warning={true}>

To use GPUs, you need to install the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)  . We also recommend using NVIDIA drivers with CUDA version 11.8 or higher.

</Tip>

Once TGI is running, you can use the `generate` endpoint by doing requests. To learn more about how to query the endpoints, check the [Consuming TGI](./basic_tutorials/consuming_tgi) section, where we show examples with utility libraries and UIs. Below you can see a simple snippet to query the endpoint.


<inferencesnippet>
<python>

```python
import requests

headers = {
    "Content-Type": "application/json",
}

data = {
    'inputs': 'What is Deep Learning?',
    'parameters': {
        'max_new_tokens': 20,
    },
}

response = requests.post('http://127.0.0.1:8080/generate', headers=headers, json=data)
print(response.json())
# {'generated_text': '\n\nDeep Learning is a subset of Machine Learning that is concerned with the development of algorithms that can'}
```
</python>
<js>

```js
async function query() {
    const response = await fetch(
        'http://127.0.0.1:8080/generate', 
        {
            method: 'POST',
            headers: { 'Content-Type': 'application/json'},
            body: JSON.stringify({
                'inputs': 'What is Deep Learning?',
                'parameters': {
                    'max_new_tokens': 20
                }
            })
        }
    );
}

query().then((response) => {
    console.log(JSON.stringify(response));
});
/// {"generated_text":"\n\nDeep Learning is a subset of Machine Learning that is concerned with the development of algorithms that can"}
```

</js>
<curl>

```curl
curl 127.0.0.1:8080/generate \
    -X POST \
    -d '{"inputs":"What is Deep Learning?","parameters":{"max_new_tokens":20}}' \
    -H 'Content-Type: application/json'
```

</curl>
</inferencesnippet>

<Tip>

To see all possible deploy flags and options, you can use the `--help` flag. It's possible to configure the number of shards, quantization, generation parameters, and more.

```bash
docker run ghcr.io/huggingface/text-generation-inference:1.1.1 --help
```

</Tip>
