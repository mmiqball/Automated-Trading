# Cryptocurrency Arbitrage Detection Bot

This bot analyzes cryptocurrency markets on the dYdX exchange to detect potential arbitrage opportunities using cointegration. It informs users about these opportunities via Telegram, allowing them to make informed trading decisions.

## Features

- Connects to the dYdX exchange API
- Analyzes market data to find cointegrated pairs
- Calculates z-scores to identify potential arbitrage opportunities
- Sends notifications to users via Telegram
- Runs continuously on an AWS EC2 instance

## How it works

1. The bot fetches recent price data for various cryptocurrency pairs on dYdX.
2. It performs cointegration analysis to identify pairs that tend to move together.
3. For cointegrated pairs, it calculates z-scores to determine when the pairs have diverged significantly.
4. When a potential arbitrage opportunity is detected, the bot sends a notification to users via Telegram.

## Key Components

- `main.py`: The main entry point of the bot
- `cointegration.py`: Contains functions for cointegration analysis
- `public.py`: Handles public API calls to fetch market data
- `send_updates.py`: Manages Telegram notifications

## Setup

1. Clone this repository
2. Install the required packages: `pip install -r requirements.txt`
3. Set up your environment variables in a `.env` file (see `.env.example` for required variables)
4. Run the bot: `python program/main.py`

## Configuration

You can adjust various parameters in the `constants.py` file, such as:

- `ZSCORE_THRESHOLD`: The z-score at which to notify users of potential arbitrage opportunities
- `RESOLUTION`: The timeframe for analyzing price data
- `WINDOW`: The window size for calculating moving averages and standard deviations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
