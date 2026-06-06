import yfinance as yf
import pandas as pd


# ---------------------------------
# Variables to mess around with
# ---------------------------------

PERIOD = "10y" 
TICKER = "SPMO"
EDCA_THRESHOLD = -0.1
EDCA_MULTIPLIER = 2.0

# ================================================

# download market data
print("Downloading market data...")
stock_data = yf.download(TICKER, period=PERIOD)["Close"].squeeze()

# load spmo into dataframe
df = pd.DataFrame({
    'Price': stock_data
}).dropna()
print(f"Data downloaded! We have {len(df)} trading days.")

# calculate 200 dma
df["SMA_200"] = df["Price"].rolling(200).mean()

# calculate moving average deviation
df['MA_Deviation'] = (df['Price'] - df['SMA_200']) / df['SMA_200']
df = df.dropna()

df.index = pd.to_datetime(df.index)
# mark DCA days as such
df['Is_DCA_Day'] = df.index.to_series().dt.to_period('M') != df.index.to_series().shift(1).dt.to_period('M')
print(f"Total scheduled monthly buying days: {df['Is_DCA_Day'].sum()}")


# ------------------------------------------------------------------
# STRATEGY 1: REGULAR DCA WALLET
# ------------------------------------------------------------------
reg_cash = 0.0
reg_shares = 0.0
reg_income = 500.0

# ------------------------------------------------------------------
# STRATEGY 2: ENHANCED SMA DCA WALLET
# ------------------------------------------------------------------
edca_cash = 0.0
edca_shares = 0.0
edca_income = 500.0
edca_spend = 400.0

# Performance history logs
reg_history = []
edca_history = []


for row in df.itertuples():
    current_price = row.Price
    buying_day = row.Is_DCA_Day
    deviation = row.MA_Deviation
    

    if buying_day:
        # 1. Income arrives
        reg_cash += reg_income
        edca_cash += edca_income

        # 2. Regular DCA execution
        reg_shares += reg_income / current_price
        reg_cash -= reg_income 

        # 3. Enhanced DCA execution 
        if deviation < EDCA_THRESHOLD:
            target_spend = edca_spend * EDCA_MULTIPLIER
        else:
            target_spend = edca_spend

        # safety check
        if edca_cash >= target_spend:
            actual_spend = target_spend
        else:
            actual_spend = edca_cash
            
        # buy shares
        edca_shares += actual_spend / current_price
        edca_cash -= actual_spend

    # 4. Daily Net Worth trackings
    current_reg_value = reg_cash + (reg_shares * current_price)
    current_edca_value = edca_cash + (edca_shares * current_price)
    
    reg_history.append(current_reg_value)
    edca_history.append(current_edca_value)

print("Simulation finished!")



# ------------------------------------------------------------------
# PERFORMANCE EVALUATION
# ------------------------------------------------------------------
# Attach histories back to our dataframe so we can inspect them
df['Reg_Portfolio_Value'] = reg_history
df['Edca_Portfolio_Value'] = edca_history

# Calculate Total Invested Capital
# Count how many times an income stream actually happened
total_investment_days = df['Is_DCA_Day'].sum()
total_capital_injected = total_investment_days * reg_income 

final_reg_value = df['Reg_Portfolio_Value'].iloc[-1]
final_edca_value = df['Edca_Portfolio_Value'].iloc[-1]

reg_roi = ((final_reg_value / total_capital_injected) - 1) * 100
edca_roi = ((final_edca_value / total_capital_injected) - 1) * 100

print("\n" + "="*50)
print("             FINAL BACKTEST RESULTS")
print("="*50)
print(f"Total Capital Invested:   ${total_capital_injected:,.2f}")
print("-" * 50)
print(f"Regular DCA Net Worth:    ${final_reg_value:,.2f}")
print(f"Regular DCA Total Return: {reg_roi:.2f}%")
print("-" * 50)
print(f"EDCA Net Worth:       ${final_edca_value:,.2f}")
print(f"EDCA Total Return:   {edca_roi:.2f}%")
print("="*50)

# Quick look at cash reserves left over for EDCA
print(f"Remaining Uninvested Cash in EDCA Wallet: ${edca_cash:,.2f}")

