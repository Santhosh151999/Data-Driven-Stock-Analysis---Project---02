import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# ----------------------- Database Connection ----------------------- #
engine = create_engine("mysql+mysqlconnector://root:Dark2020%40@localhost/StockMarketDB")
df = pd.read_sql("SELECT * FROM stock_data", con=engine)

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# ----------------------- Page Setup ----------------------- #
st.set_page_config(page_title="Stock Market Dashboard", layout="wide")

# ----------------------- Page Navigation ----------------------- #
page = st.sidebar.selectbox("Choose Page", ["Dashboard", "Interactive Stock Filter"])

# ----------------------- PAGE 1: Dashboard ----------------------- #
if page == "Dashboard":
    st.title("Stock Market Analysis Dashboard")
    st.markdown("""
    This dashboard provides insights based on:
    - Stock Volatility
    - Cumulative Returns
    - Sector Performance
    - Stock Price Correlation
    - Monthly Top Gainers and Losers
    """)

    # 1. Volatility
    df['prev_close'] = df.groupby('ticker')['close'].shift(1)
    df['daily_return'] = (df['close'] - df['prev_close']) / df['prev_close']
    df = df.dropna(subset=['daily_return'])
    vol_df = df.groupby('ticker')['daily_return'].std().reset_index()
    vol_df.columns = ['ticker', 'volatility']
    vol_df = vol_df.sort_values(by='volatility', ascending=False).head(10)
    sector_info = df[['ticker', 'sector']].drop_duplicates()
    vol_df = vol_df.merge(sector_info, on='ticker', how='left')
    st.subheader("Top 10 Most Volatile Stocks")
    st.dataframe(vol_df, use_container_width=True)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(vol_df['ticker'], vol_df['volatility'], color='orange')
    ax.set_title("Top 10 Most Volatile Stocks")
    st.pyplot(fig)

    # 2. Cumulative Return
    df['daily_return'] = df.groupby('ticker')['close'].pct_change()
    df['cumulative_return'] = df.groupby('ticker')['daily_return'].transform(lambda x: (1 + x).cumprod())
    final_returns = df.groupby('ticker')['cumulative_return'].last().sort_values(ascending=False)
    top_5 = final_returns.head(5).index.tolist()
    top_data = df[df['ticker'].isin(top_5)]
    st.subheader("Cumulative Return Over Time – Top 5 Performers")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    for t in top_5:
        sub = top_data[top_data['ticker'] == t]
        ax2.plot(sub['date'], sub['cumulative_return'], label=t)
    ax2.set_title("Cumulative Return Over Time")
    ax2.legend()
    st.pyplot(fig2)

    # 3. Sector-wise Performance
    st.subheader("Sector-wise Performance")
    final = df.groupby(['ticker', 'sector'])['cumulative_return'].last().reset_index()
    sector_perf = final.groupby('sector')['cumulative_return'].mean().sort_values(ascending=False)
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    ax3.bar(sector_perf.index, sector_perf.values, color='skyblue')
    ax3.set_title("Average Yearly Return by Sector")
    ax3.tick_params(axis='x', rotation=45)
    st.pyplot(fig3)

    # 4. Correlation Heatmap
    st.subheader("Stock Price Correlation")
    pivot_df = df.pivot(index='date', columns='ticker', values='close')
    corr = pivot_df.pct_change().corr()
    fig4, ax4 = plt.subplots(figsize=(14, 10))
    cax = ax4.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
    ax4.set_xticks(range(len(corr.columns)))
    ax4.set_xticklabels(corr.columns, rotation=90)
    ax4.set_yticks(range(len(corr.columns)))
    ax4.set_yticklabels(corr.columns)
    fig4.colorbar(cax)
    st.pyplot(fig4)

    # 5. Monthly Gainers and Losers
    st.subheader("Monthly Top Gainers and Losers")
    df['month'] = df['date'].dt.to_period('M')
    monthly = df.groupby(['month', 'ticker'])['close'].agg(['first', 'last'])
    monthly['monthly_return'] = (monthly['last'] - monthly['first']) / monthly['first']
    monthly.reset_index(inplace=True)
    monthly['month'] = monthly['month'].astype(str)
    tabs = st.tabs(sorted(monthly['month'].unique()))
    for i, m in enumerate(sorted(monthly['month'].unique())):
        with tabs[i]:
            sub = monthly[monthly['month'] == m]
            gainers = sub.sort_values(by='monthly_return', ascending=False).head(5)
            losers = sub.sort_values(by='monthly_return', ascending=True).head(5)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"#### Top 5 Gainers – {m}")
                fig_g, ax_g = plt.subplots()
                ax_g.bar(gainers['ticker'], gainers['monthly_return'] * 100, color='green')
                st.pyplot(fig_g)
            with col2:
                st.markdown(f"#### Top 5 Losers – {m}")
                fig_l, ax_l = plt.subplots()
                ax_l.bar(losers['ticker'], losers['monthly_return'] * 100, color='red')
                st.pyplot(fig_l)

# ----------------------- PAGE 2: Interactive Stock Filter ----------------------- #
elif page == "Interactive Stock Filter":
    st.title("Interactive Stock Filter")

    min_date = df['date'].min()
    max_date = df['date'].max()

    st.sidebar.subheader("Filter Options")
    selected_ticker = st.sidebar.selectbox("Select a Stock Ticker", sorted(df['ticker'].unique()))
    date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

    if len(date_range) == 2:
        start_date, end_date = date_range
        filt = df[(df['ticker'] == selected_ticker) &
                  (df['date'] >= pd.to_datetime(start_date)) &
                  (df['date'] <= pd.to_datetime(end_date))]

        st.subheader(f"Stock Data: {selected_ticker} from {start_date} to {end_date}")
        st.dataframe(filt[['date', 'open', 'high', 'low', 'close', 'volume']], use_container_width=True)

        fig_filt, ax_filt = plt.subplots(figsize=(10, 5))
        ax_filt.plot(filt['date'], filt['high'], label='High', color='green')
        ax_filt.plot(filt['date'], filt['low'], label='Low', color='red')
        ax_filt.plot(filt['date'], filt['close'], label='Close', color='blue')
        ax_filt.set_title(f"{selected_ticker} – High/Low/Close Over Time")
        ax_filt.legend()
        ax_filt.grid(True)
        st.pyplot(fig_filt)
    else:
        st.warning("Please select a valid date range.")
