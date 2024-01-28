# asynctradier

[![codecov](https://codecov.io/gh/jiak94/asynctradier/graph/badge.svg?token=T66WaJLNDd)](https://codecov.io/gh/jiak94/asynctradier)
[![PyPI version](https://badge.fury.io/py/asynctradier.svg)](https://badge.fury.io/py/asynctradier)
![Test](https://github.com/jiak94/asynctradier/actions/workflows/run_test.yaml/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/asynctradier/badge/?version=latest)](https://asynctradier.readthedocs.io/en/latest/?badge=latest)

Async api wrapper for [Tradier](https://documentation.tradier.com/).

This is _NOT_ an official package of Tradier.

## Install

`pip install asynctradier`

if your are using poetry

`poetry add asynctradier`

## Documentation

[Read The Doc](https://asynctradier.readthedocs.io/en/latest/)

## Supported API

### Account

:white_check_mark: Get User Profile

:white_check_mark: Get Balances

:white_check_mark: Get Positions

:white_check_mark: Get History

:white_check_mark: Get Gain/Loss

:white_check_mark: Get Orders

:white_check_mark: Get an Order

### Trading

:white_check_mark: Modify Order

:white_check_mark: Cancel Order

:white_square_button: Place Equity Order

:white_check_mark: Place Option Order

:white_check_mark: Place Multileg Order

:white_square_button: Place Combo Order

:white_square_button: Place OTO Order

:white_square_button: Place OCO Order

:white_square_button: Place OTOCO Order

### Market Data

:white_check_mark: Get Quotes

:white_check_mark: Get Option Chains

:white_check_mark: Get Option Strikes

:white_check_mark: Get Option Expirations

:white_check_mark: Lookup Option Symbols

:white_square_button: Get Historical Quotes

:white_square_button: Get Time and Sales

:white_square_button: Get ETB Securities

:white_square_button: Get Clock

:white_check_mark: Get Calendar

:white_square_button: Search Companies

:white_square_button: Lookup Symbol

### Streaming

:white_square_button: Market WebSocket

:white_check_mark: Account WebSocket
