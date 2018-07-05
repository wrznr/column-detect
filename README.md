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
should create a file `test.json` which contains a list of corrdinates representing the detected column areas.
```json
{
    "test.bin.png": [
        {
            "l": 0,
            "t": 0,
            "r": 1255,
            "b": 4274
        },
        {
            "l": 1225,
            "t": 0,
            "r": 2280,
            "b": 4274
        },
        {
            "l": 2251,
            "t": 0,
            "r": 3365,
            "b": 4274
        }
    ]
}
```
