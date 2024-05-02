# Nornir Dispatch

Nornir Dispatch is a utility for Nornir to simplify how to run multi-vendor workflows.

Nornir Dispatch allows you to register some tasks per platform and execute them seamlessly based on each host's characteristics.

## Installation

You can install _Nornir Dispatch_ via [pip] from [PyPI]:

```console
$ pip install nornir-dispatch
```

## Usage

Nornir Dispatch can be used by registering tasks, or implementing and registering a NornirDispatchBaseDriver.

- [using tasks](./examples/example_tasks.py)
- [using NornirDispatchBaseDriver](./examples/example_driver.py)

## License

Distributed under the terms of the [Apache 2.0 license](./LICENSE), Nornir Dispatch is free and open source software.
