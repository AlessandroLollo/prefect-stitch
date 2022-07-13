# prefect-stitch

## Welcome!

Prefect collection to interact with Stitch

## Getting Started

### Python setup

Requires an installation of Python 3.7+.

We recommend using a Python virtual environment manager such as pipenv, conda or virtualenv.

These tasks are designed to work with Prefect 2.0. For more information about how to use Prefect, please refer to the [Prefect documentation](https://orion-docs.prefect.io/).

### Installation

Install `prefect-stitch` with `pip`:

```bash
pip install prefect-stitch
```

### Write and run a flow

```python
from prefect import flow
from prefect_stitch.tasks import (
    start_replication_job
)


@flow
def example_flow():
    start_replication_job(
        access_token="my_secret_token",
        source_id=1234
    )

example_flow()
```

## Resources

If you encounter any bugs while using `prefect-stitch`, feel free to open an issue in the [prefect-stitch](https://github.com/AlessandroLollo/prefect-stitch) repository.

If you have any questions or issues while using `prefect-stitch`, you can find help in either the [Prefect Discourse forum](https://discourse.prefect.io/) or the [Prefect Slack community](https://prefect.io/slack).

## Development

If you'd like to install a version of `prefect-stitch` for development, clone the repository and perform an editable install with `pip`:

```bash
git clone https://github.com/AlessandroLollo/prefect-stitch.git

cd prefect-stitch/

pip install -e ".[dev]"

# Install linting pre-commit hooks
pre-commit install
```
