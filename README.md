# Genoss GPT
## One line replacement for openAI ChatGPT & Embeddings powered by OSS models


<div align="center">
    <img src="./logo.png" alt="Genoss" width="40%"  style="border-radius: 50%; padding-bottom: 20px"/>
</div>

# Genoss

Genoss is a pioneering open-source initiative that aims to offer a seamless alternative to OpenAI models such as GPT 3.5 & 4, using open-source models like GPT4ALL.

Built on FastAPI, this API service is expertly designed to yield chat completions based on specified models and questions.

## Starting Up

Before you embark, ensure Python 3.8 or higher is installed on your machine.

## Installation

The first step is to install GPT4ALL, which is the only supported model at the moment. You can do this by following these steps:

1. Clone the repository:

```bash
git clone --recurse-submodules git@github.com:nomic-ai/gpt4all.git
```

2. Navigate to the backend directory:

```bash
cd gpt4all/gpt4all-backend/
```

3. Create a new build directory and navigate into it:

```bash
mkdir build && cd build
```

4. Configure and build the project using cmake:

```bash
cmake ..
cmake --build . --parallel
```

5. Verify that libllmodel.* exists in `gpt4all-backend/build`.

6. Navigate back to the root and install the Python package:

```bash
cd ../../gpt4all-bindings/python
pip3 install -e .
```

## Running the Application

After the Python package has been installed, you can run the application. The Uvicorn ASGI server can be used to run your application:

```bash
uvicorn main:app --host 0.0.0.0 --port 4321
```

This command launches the Genoss application on port 4321 of your machine.

## Genoss API Usage

The Genoss API provides the `/chat/completions` endpoint for generating language completions. Two query parameters are available, `model` (for specifying the model to use for generating completions) and `question` (for the input question).

```bash
curl -X 'POST' \
  'http://localhost:4321/chat/completions?model=gpt4all&question=What%20is%20the%20color%20of%20the%20sky%20%3F' \
  -H 'accept: application/json' \
  -d ''
```

### Responses

- 200: Successful Response. Returns the completion as a JSON string.
- 422: Validation Error. An error indicates that the provided input parameters are incorrect.

For more detailed API documentation, please consult the OpenAPI specification at `/openapi.json`.

## Upcoming Developments

While GPT4ALL is the only model currently supported, we are planning to add more models in the future. So, stay tuned for more exciting updates.

## Contributions

Your contributions to Genoss are immensely appreciated! Feel free to submit any issues or pull requests.

## License

Genoss is licensed under the MIT License. For more details, refer to the [LICENSE](LICENSE) file.