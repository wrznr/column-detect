# column-detect
Simple approach to column detection in (book) pages

## Setup

0. Clone the repository.
1. Install `python3`.
2. Install dependencies. (Using `virtualenv` is recommended.)
```shell
$ virtualenv -p python3 env
$ . env/bin/activate
(env) $ pip install -r requirements.txt
```

## Invocation

Running
```shell
(env) $ python column_detect.py --help
```
gives an overview on mandatory and optional parameters.

Running
```shell
(env) $ python column_detect.py -o test.json -O json test/test.bin.png
```
should create a file `test.json`:
```json
...
```
