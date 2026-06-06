# Enhanced DCA vs. Regular DCA Backtester from Scratch

A lightweight, high-performance financial backtesting engine built from scratch in Python using pandas and yfinance. This project evaluates the mathematical effectiveness of a baseline Regular Dollar-Cost Averaging (DCA) strategy against an Enhanced Moving Average DCA (EDCA) strategy using SPMO historical data over a 10-year horizon.

---

## Overview and Core Concept

While standard DCA blindly invests a fixed amount at regular intervals, Enhanced DCA attempts to optimize capital deployment by tracking an asset's deviation from its 200-day Simple Moving Average (SMA). 

### Strategy Rules Applied:
* **Regular DCA (Control):** Deposits and immediately invests a fixed amount ($500) on the first trading day of every month, regardless of market conditions.
* **Enhanced DCA (SMA-Based):** Receives the same monthly income stream ($500), but alters deployment based on the asset position:
  * **Normal/Bull Markets (Deviation >= 0):** Invests a conservative baseline amount ($400), hoarding the leftover ($100) into a cash reserve pool.
  * **Market Corrections (Deviation < 0):** Triggers a dip-buying mechanism, doubling the target baseline investment allocation ($800) by drawing down accumulated cash reserves.

---

## Key Financial Insight: The Cash Drag Trap

Through running this backtest over various market horizons, this project highlights a critical quantitative paradox: **Regular DCA frequently outperforms Enhanced DCA during long-term bull markets.**

This occurs due to **Cash Drag**. Because the Enhanced strategy holds cash on the sidelines waiting for a correction, it misses out on the continuous compounding growth of the asset. By the time a dip finally occurs, the asset price may have already risen significantly from the initial backtest start date, meaning the "discounted" price paid by EDCA is still higher than the price Regular DCA paid years prior.

---

## Code Features

* **Built from Scratch:** Pure state-variable accounting loop logic prevents look-ahead bias without heavy algorithmic framework dependencies.
* **Lightweight Time Loop:** Utilizes Pandas .itertuples() instead of .iterrows() to execute forward-looking calendar tracking over 10x faster.
* **Strict Cash Accounting:** Enforces realistic wallet bounds. The enhanced strategy cannot spend "ghost money" during market crashes—it can only deploy cash it has explicitly saved or maintained in reserve.

---

## Getting Started

### Prerequisites
Make sure you have the required packages installed:
```bash
pip install yfinance pandas