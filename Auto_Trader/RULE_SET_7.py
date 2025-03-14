def buy_or_sell(df, row, holdings):
    """
    Refined swing trading strategy for Indian stocks on daily timeframe.

    Parameters:
    -----------
    df : pd.DataFrame
        The DataFrame containing the historical data, including necessary technical indicators.
    row : int
        The latest row for evaluation.
    holdings : dict
        A dictionary representing the current stock holdings.

    Returns:
    --------
    str
        Returns 'BUY', 'SELL', or 'HOLD' signal based on technical indicator evaluation.
    """

    # Additional Close Conditions for Buy
    buy_close_condition = (
        (df['Close'].iloc[-1] > df['SMA_20_Close'].iloc[-1]) and
        (df['Close'].iloc[-1] >= df['SMA_10_Close'].iloc[-1] * 1.01) and
        (df['Close'].iloc[-1] <= df['SMA_10_Close'].iloc[-1] * 1.08)
    )
    
    buy_EMA_condition = ((df['Close'].iloc[-1] > df['EMA20'].iloc[-1]) and
        (df['Close'].iloc[-1] > df['EMA50'].iloc[-1]) and
        (df['Close'].iloc[-1] > df['EMA100'].iloc[-1]) and
        (df['Close'].iloc[-1] > df['EMA200'].iloc[-1]) and
        (df['EMA20'].iloc[-1] > df['EMA50'].iloc[-1]) and
        (df['EMA50'].iloc[-1] > df['EMA100'].iloc[-1]) and
        (df['EMA100'].iloc[-1] > df['EMA200'].iloc[-1]))
    
    # Define a MACD crossover in the last 5 days
    macd_crossover_last_3_days = (
        ((df['MACD'] > df['MACD_Signal']) & (df['MACD'].shift(1) <= df['MACD_Signal'].shift(1)))  # MACD crosses above MACD_Signal
        .tail(5)  # Look at the last 5 days
        .any()  # Check if crossover happened on any of the last 5 days
    )
    
    # Buy signal conditions
    if (
        (df["EMA9"].iloc[-1] > df["EMA21"].iloc[-1] * 1.02 > df["EMA50"].iloc[-1] * 1.02)  # Added buffer to avoid false signals
        and (df["RSI"].iloc[-1] > 60)  # Lowered RSI threshold to capture more momentum
        and (df["MACD_Hist"].iloc[-1] > 0)
        and (df["MACD_Hist"].iloc[-1] > df["MACD_Hist"].shift(1).iloc[-1])  # Ensure MACD Histogram is increasing
        and (df['Volume'] > (1.5 * df['SMA_20_Volume'])).iloc[-1]  # Stronger volume confirmation
    ) and buy_close_condition and macd_crossover_last_3_days and buy_EMA_condition:
        return "BUY"  # Buy Signal

    # Sell signal conditions
    elif (
        (df["EMA9"].iloc[-1] < df["EMA21"].iloc[-1] * 0.99 < df["EMA50"].iloc[-1] * 0.99)  # Added buffer to avoid false signals
        and (df["RSI"].iloc[-1] < 45)  # Raised RSI threshold to exit earlier when momentum weakens
        and (df["MACD_Hist"].iloc[-1] < 0)
        and (df['Volume'] > (1.5 * df['SMA_20_Volume'])).iloc[-1]  # Stronger volume confirmation
    ):
        return "SELL"  # Sell Signal

    else:
        return "HOLD"  # No action