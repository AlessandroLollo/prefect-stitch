from prefect import flow

from prefect_stitch.tasks import (
    goodbye_prefect_stitch,
    hello_prefect_stitch,
)


def test_hello_prefect_stitch():
    @flow
    def test_flow():
        return hello_prefect_stitch()

    flow_state = test_flow()
    task_state = flow_state.result()
    assert task_state.result() == "Hello, prefect-stitch!"


def goodbye_hello_prefect_stitch():
    @flow
    def test_flow():
        return goodbye_prefect_stitch()

    flow_state = test_flow()
    task_state = flow_state.result()
    assert task_state.result() == "Goodbye, prefect-stitch!"
