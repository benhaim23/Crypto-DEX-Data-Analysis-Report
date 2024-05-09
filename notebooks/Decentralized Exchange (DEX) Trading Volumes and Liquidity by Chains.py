#!/usr/bin/env python
# coding: utf-8

# # Decentralized Exchange (DEX) Trading Volumes and Liquidity Across Chains
# 
# ## Introduction
# This report provides a comprehensive analysis of DEX trading across multiple blockchains, including Ethereum, Binance Smart Chain, Solana, Polygon, Arbitrum, and Optimism. The goal is to uncover insights into trading volumes, liquidity, and market trends across these platforms. We aim to identify unique characteristics and trends that differentiate these blockchains and contribute to their market dynamics.
# 

# In[2]:


# Import necessary libraries
import pandas as pd
import numpy as np

# Data Loading
def load_data(file_path):
    return pd.read_csv(file_path)

# Load datasets
eth_data = load_data('Downloads/dex_data/dex_pairs_ethereum.csv')
bnb_data = load_data('Downloads/dex_data/dex_pairs_bnb.csv')
sol_data = load_data('Downloads/dex_data/dex_pairs_solana.csv')
polygon_data = load_data('Downloads/dex_data/dex_pairs_polygon.csv')
arbitrum_data = load_data('Downloads/dex_data/dex_pairs_arbitrum.csv')
optimism_data = load_data('Downloads/dex_data/dex_pairs_optimism.csv')

# Data Preprocessing
def preprocess_data(data):
    # Replace any inf or -inf with NaN
    data.replace([np.inf, -np.inf], np.nan, inplace=True)
    # Fill missing values
    data.fillna(method='ffill', inplace=True)
    return data

# Preprocess each dataset
eth_data = preprocess_data(eth_data)
bnb_data = preprocess_data(bnb_data)
sol_data = preprocess_data(sol_data)
polygon_data = preprocess_data(polygon_data)
arbitrum_data = preprocess_data(arbitrum_data)
optimism_data = preprocess_data(optimism_data)


# ## Exploratory Data Analysis (EDA)
# 
# In this section, we analyze trading volumes, liquidity, and other relevant metrics to understand the dynamics and performance of DEXs on different blockchains. We'll explore daily, weekly, and monthly volumes, as well as liquidity patterns.
# 

# In[4]:


# Import visualization libraries
import matplotlib.pyplot as plt
import seaborn as sns

# Set the aesthetic style of the plots
sns.set_style("whitegrid")

# Function to plot trading volumes
def plot_trading_volumes(data, chain_name):
    plt.figure(figsize=(14, 7))
    plt.plot(data['one_day_volume'], label='Daily Volume')
    plt.plot(data['seven_day_volume'], label='Weekly Volume')
    plt.plot(data['thirty_day_volume'], label='Monthly Volume')
    plt.title(f'Trading Volumes on {chain_name}')
    plt.xlabel('Date')
    plt.ylabel('Volume (in USD)')
    plt.legend()
    plt.show()

# Function to plot liquidity
def plot_liquidity(data, chain_name):
    plt.figure(figsize=(14, 7))
    plt.plot(data['usd_liquidity'], color='purple')
    plt.title(f'Liquidity Over Time on {chain_name}')
    plt.xlabel('Date')
    plt.ylabel('USD Liquidity')
    plt.show()

# Plotting the data for Ethereum
plot_trading_volumes(eth_data, 'Ethereum')
plot_liquidity(eth_data, 'Ethereum')

# Plotting the data for Ethereum
plot_trading_volumes(bnb_data, 'Binance Smart Chain')
plot_liquidity(bnb_data, 'Binance Smart Chain')

# Plotting the data for Ethereum
plot_trading_volumes(sol_data, 'Solana')
plot_liquidity(sol_data, 'Solana')

# Plotting the data for Ethereum
plot_trading_volumes(polygon_data, 'Polygon')
plot_liquidity(polygon_data, 'Polygon')

# Plotting the data for Ethereum
plot_trading_volumes(arbitrum_data, 'Arbitrum')
plot_liquidity(arbitrum_data, 'Arbitrum')

# Plotting the data for Ethereum
plot_trading_volumes(optimism_data, 'Optimism')
plot_liquidity(optimism_data, 'Optimism')


# ## Comparative Analysis
# 
# In this section, we compare the performance metrics such as trading volumes, liquidity, and market trends across different blockchains. The aim is to identify distinctive patterns or behaviors that set each blockchain apart in the DEX landscape.
# 

# In[5]:


# Function to compare average trading volumes
def compare_average_volumes(*datasets, labels):
    averages = [data[['one_day_volume', 'seven_day_volume', 'thirty_day_volume']].mean() for data in datasets]
    df_averages = pd.DataFrame(averages, index=labels)
    df_averages.plot(kind='bar', figsize=(14, 7))
    plt.title('Comparison of Average Trading Volumes Across Blockchains')
    plt.xlabel('Blockchain')
    plt.ylabel('Average Volume (in USD)')
    plt.legend(['Daily Volume', 'Weekly Volume', 'Monthly Volume'])
    plt.show()

# Compare trading volumes across all blockchains
compare_average_volumes(eth_data, bnb_data, sol_data, polygon_data, arbitrum_data, optimism_data,
                        labels=['Ethereum', 'Binance Smart Chain', 'Solana', 'Polygon', 'Arbitrum', 'Optimism'])

# Function to compare liquidity
def compare_liquidity(*datasets, labels):
    liquidity = [data['usd_liquidity'].mean() for data in datasets]
    df_liquidity = pd.DataFrame(liquidity, index=labels, columns=['Average USD Liquidity'])
    df_liquidity.plot(kind='bar', color='purple', figsize=(14, 7))
    plt.title('Comparison of Average USD Liquidity Across Blockchains')
    plt.xlabel('Blockchain')
    plt.ylabel('USD Liquidity')
    plt.show()

# Compare liquidity across all blockchains
compare_liquidity(eth_data, bnb_data, sol_data, polygon_data, arbitrum_data, optimism_data,
                  labels=['Ethereum', 'Binance Smart Chain', 'Solana', 'Polygon', 'Arbitrum', 'Optimism'])


# ## Conclusion and Recommendations
# 
# This report has explored various performance metrics across multiple DEXs operating on different blockchains. We have identified key trends and differences that could influence investment and operational decisions. Based on our findings:
# 
# - *Ethereum* continues to show robust trading volumes, suggesting high market activity.
# - *Solana* and *Polygon* show promising growth in liquidity, potentially offering new opportunities for traders.
# - Smaller blockchains like *Arbitrum* and *Optimism* might benefit from targeted strategies to boost their liquidity and trading volume.
# 
# ### Recommendations:
# - Investors should consider diversifying their portfolios across these blockchains to mitigate risks and capitalize on growth opportunities.
# - Developers should focus on enhancing user experience and integration features to attract more users to newer or less popular platforms.
# 
# Further research could delve into the impact of specific events on trading behaviors and explore the correlation between market trends and external economic factors.
# 

# ## Interactive Dashboard
# 
# This section introduces an interactive dashboard for real-time monitoring of trading volumes and liquidity across different blockchains. The dashboard is designed to provide a quick and effective way to visually compare the DEX performance metrics, facilitating easier decision-making and trend analysis.
# 

# In[7]:


# Import necessary libraries for the dashboard
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Create a Dash application
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1('DEX Trading Volumes and Liquidity Dashboard'),
    dcc.Dropdown(
        id='chain-dropdown',
        options=[
            {'label': 'Ethereum', 'value': 'eth'},
            {'label': 'Binance Smart Chain', 'value': 'bnb'},
            {'label': 'Solana', 'value': 'sol'},
            {'label': 'Polygon', 'value': 'polygon'},
            {'label': 'Arbitrum', 'value': 'arbitrum'},
            {'label': 'Optimism', 'value': 'optimism'}
        ],
        value='eth',
        style={'width': '50%'}
    ),
    dcc.Graph(id='volume-graph'),
    dcc.Graph(id='liquidity-graph')
])

# Define the callback to update the graph
@app.callback(
    [Output('volume-graph', 'figure'),
     Output('liquidity-graph', 'figure')],
    [Input('chain-dropdown', 'value')]
)
def update_graphs(selected_chain):
    data_map = {
        'eth': eth_data,
        'bnb': bnb_data,
        'sol': sol_data,
        'polygon': polygon_data,
        'arbitrum': arbitrum_data,
        'optimism': optimism_data
    }
    data = data_map[selected_chain]
    
    # Create volume graph
    volume_fig = {
        'data': [
            {'x': data.index, 'y': data['one_day_volume'], 'type': 'line', 'name': 'Daily Volume'},
            {'x': data.index, 'y': data['seven_day_volume'], 'type': 'line', 'name': 'Weekly Volume'},
            {'x': data.index, 'y': data['thirty_day_volume'], 'type': 'line', 'name': 'Monthly Volume'}
        ],
        'layout': {'title': 'Trading Volumes'}
    }
    
    # Create liquidity graph
    liquidity_fig = {
        'data': [{'x': data.index, 'y': data['usd_liquidity'], 'type': 'line', 'name': 'USD Liquidity'}],
        'layout': {'title': 'USD Liquidity'}
    }
    
    return volume_fig, liquidity_fig

# Run the server on a specified port
if __name__ == '__main__':
    app.run_server(debug=True, port=8053)  # Use a different port if 8050 is in use

