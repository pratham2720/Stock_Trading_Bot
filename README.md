# Stock_Trading_Bot
# Binance Futures Trading Bot

A simplified Python trading bot for Binance Futures Testnet (USDT-M).  
This bot allows you to place **market orders**, **limit orders**, and **stop-limit orders** via a command-line interface (CLI). It logs all API requests, responses, and errors for easy tracking.

---

## Features

- Connects to **Binance Futures Testnet** using your API credentials.
- Supports **buy** and **sell** orders.
- Place **market orders**, **limit orders**, and **stop-limit orders**.
- Syncs local time with Binance server to prevent timestamp errors.
- Logs API activity and errors in `trading_bot.log`.
- Input validated via CLI.

---

## Prerequisites

- Python 3.9+
- [python-binance](https://pypi.org/project/python-binance/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

Install dependencies:

```bash
pip install python-binance python-dotenv
