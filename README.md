# Data-Driven-Stock-Analysis---Project---02

Stock Market Analysis Dashboard (Nifty 50)

This project is a data analysis and visualization dashboard developed using Power BI and Streamlit. It analyzes the performance of Nifty 50 stocks over the past year, offering powerful insights into stock trends, sector movements, and price behaviors. The data is sourced from historical monthly stock data (in YAML/CSV format), cleaned and transformed into structured tables using Python, and visualized interactively for users ranging from casual investors to financial analysts.

Features:

Visual Analysis (Both Power BI and Streamlit):

Top 10 Gainers and Losers (overall and monthly)
Cumulative Return of each stock over the year
Volatility Analysis using standard deviation of daily returns
Sector-wise Average Returns (using sector mapping CSV)
Stock Correlation Heatmap to show inter-stock relationships

Monthly Breakdown:

Top 5 gainers and losers for each month with dynamic bar charts
Filterable by sector, ticker, and date in Streamlit
Interactive Power BI visuals with slicers and filters

Tech Stack:

Frontend: Power BI, Streamlit
Backend/Data Processing: Python (Pandas, NumPy)
Visualization Libraries: Seaborn, Matplotlib, Plotly

Database (Optional): MySQL / PostgreSQL
Data Source: Nifty 50 monthly stock data (.csv/.yaml format)
