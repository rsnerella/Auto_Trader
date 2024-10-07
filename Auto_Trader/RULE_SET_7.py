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

    # Buy signal conditions
    if (
        (df["EMA9"].iloc[-1] > df["EMA21"].iloc[-1] * 1.01 > df["EMA50"].iloc[-1] * 1.01)  # Added buffer to avoid false signals
        and (df["RSI"].iloc[-1] > 55)  # Lowered RSI threshold to capture more momentum
        and (df["MACD_Hist"].iloc[-1] > 0)
        and (df["MACD_Hist"].iloc[-1] > df["MACD_Hist"].shift(1).iloc[-1])  # Ensure MACD Histogram is increasing
        and (df['Volume'] > (1.5 * df['AvgVolume'])).iloc[-1]  # Stronger volume confirmation
    ):
        return "BUY"  # Buy Signal

    # Sell signal conditions
    elif (
        (df["EMA9"].iloc[-1] < df["EMA21"].iloc[-1] * 0.99 < df["EMA50"].iloc[-1] * 0.99)  # Added buffer to avoid false signals
        and (df["RSI"].iloc[-1] < 45)  # Raised RSI threshold to exit earlier when momentum weakens
        and (df["MACD_Hist"].iloc[-1] < 0)
        and (df['Volume'] > (1.5 * df['AvgVolume'])).iloc[-1]  # Stronger volume confirmation
    ):
        return "SELL"  # Sell Signal

    else:
        return "HOLD"  # No action