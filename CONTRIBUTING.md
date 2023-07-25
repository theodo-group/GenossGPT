# GenossGPT
## Project requirements

### `Python 3.11`
#### Install with pyenv
- Install [pyenv](https://github.com/pyenv/pyenv) to manage your Python versions and virtual environments:
  ```bash
  curl -sSL https://pyenv.run | bash
  ```
  - If you are on MacOS and experiencing errors on python install with pyenv, follow this [comment](https://github.com/pyenv/pyenv/issues/1740#issuecomment-738749988)
  - Add these lines to your `~/.bashrc` or `~/.zshrc` to be able to activate `pyenv virtualenv`:
      ```bash
      eval "$(pyenv init -)"
      eval "$(pyenv virtualenv-init -)"
      eval "$(pyenv init --path)"
      ```
  - Restart your shell

- Install the right version of `Python` with `pyenv`:
  ```bash
  pyenv install 3.11.3
  ```

### Poetry

- Install [Poetry](https://python-poetry.org) to manage your dependencies and tooling configs:
  ```bash
  curl -sSL https://install.python-poetry.org | python - --version 1.5.1
  ```
  *If you have not previously installed any Python version, you may need to set your global Python version before installing Poetry:*
    ```bash
    pyenv global 3.11.3
    ```

### Docker Engine
Install [Docker Engine](https://docs.docker.com/engine/install/) to build and run the API's Docker image locally.

## Installation

### Create a virtual environment

Create your virtual environment and link it to your project folder:

```bash
pyenv virtualenv 3.11.3 genoss-gpt
pyenv local genoss-gpt
```
Now, every time you are in your project directory your virtualenv will be activated thanks to `pyenv`!

### Install Python dependencies through poetry

```bash
poetry install --no-root
```

### Install git hooks (running before commit and push commands)

```bash
poetry run pre-commit install
```

## Testing

To run unit tests, run `pytest` with:
```bash
pytest tests --cov genoss
```
or
```bash
make test
```

## Formatting and static analysis

### Code formatting with `black`

To check code formatting, run `black` with:
```bash
black . --check
```
or
```bash
make black
```

You can also [integrate it to your IDE](https://black.readthedocs.io/en/stable/integrations/editors.html) to reformat
your code each time you save a file.

### Static analysis with `ruff`

To run static analysis, run `ruff` with:
```bash
ruff check genoss tests
```
or
```bash
make ruff
```

To run static analysis and to apply auto-fixes, run `ruff` with:
```bash
make fix-ruff
```
### Type checking with `mypy`

To type check your code, run `mypy` with:
```bash
mypy genoss --explicit-package-bases --namespace-packages
```
or
```bash
make mypy
```

## API
The project includes an API built with [FastAPI](https://fastapi.tiangolo.com/). Its code can be found at `genoss`.

The API is containerized using a [Docker](https://docs.docker.com/get-started/) image, built from the `Dockerfile` and `docker-compose.yml` at the root.

To build and start the API, use the following Makefile command:
```bash
make start-api
```

For more details on the API routes, check the automatically generated [swagger](https://learning.postman.com/docs/getting-started/importing-and-exporting-data/#importing-postman-data) at the `/docs` url.
