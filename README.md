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

- [ ] Get User Profile
- [ ] Get Balances
- [x] Get Positions
- [ ] Get History
- [ ] Get Gain/Loss
- [x] Get Orders
- [x] Get an Order

### Trading

- [x] Modify Order
- [x] Cancel Order
- [ ] Place Equity Order
- [x] Place Option Order
- [x] Place Multileg Order
- [ ] Place Combo Order
- [ ] Place OTO Order
- [ ] Place OCO Order
- [ ] Place OTOCO Order

### Market Data

- [ ] Get Quotes
- [ ] Get QUotes
- [ ] Get Option Chains
- [ ] Get Option Strikes
- [ ] Get Option Expirations
- [ ] Lookup Option Symbols
- [ ] Get Historical Quotes
- [ ] Get Time and Sales
- [ ] Get ETB Securities
- [ ] Get Clock
- [ ] Get Calendar
- [ ] Search Companies
- [ ] Lookup Symbol

### Streaming

- [ ] Market WebSocket
- [x] Account WebSocket
