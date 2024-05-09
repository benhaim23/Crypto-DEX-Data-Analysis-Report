#!/usr/bin/env python
# coding: utf-8

# # DEX Data Analysis Report by Chain
# 
# ## Introduction
# This report provides a comprehensive analysis of the Decentralized Exchange (DEX) data of several blockchains including Ethereum, Binance Smart Chain (BNB), Solana, Polygon, Arbitrum and Optimism. We aim to uncover insights into trading volumes, liquidity, and market trends. Additionally, we integrate key events and provide a prototype dashboard for real-time monitoring.
# 
# ## Data Loading
# First, we import the necessary libraries and load the data from the CSV file.
# 

# ## Step 1: Load and Examine Datasets
# First, I'll load each CSV file and provide a brief overview of their structure.

# In[1]:


import pandas as pd

# Paths to the dataset files
file_paths = {
    'Ethereum': 'Downloads/dex_data/dex_pairs_ethereum.csv',
    'BNB': 'Downloads/dex_data/dex_pairs_bnb.csv',
    'Solana': 'Downloads/dex_data/dex_pairs_solana.csv',
    'Polygon': 'Downloads/dex_data/dex_pairs_polygon.csv',
    'Arbitrum': 'Downloads/dex_data/dex_pairs_arbitrum.csv',
    'Optimism': 'Downloads/dex_data/dex_pairs_optimism.csv'
}

# Load each dataset into a dictionary of DataFrames
dex_datasets = {chain: pd.read_csv(path) for chain, path in file_paths.items()}

# Display the first few rows and info of each dataset
for chain, data in dex_datasets.items():
    print(f"Data for {chain}:")
    print(data.head())
    print(data.info())
    print("\n")


# After confirming the structure and content of each dataset, I'll merge them and perform necessary cleaning and integration steps. Let's start by loading and examining the data.
# 
# The datasets for each chain have been successfully loaded, and they all appear to share a similar structure, which is beneficial for the integration process. 
# 
# Each dataset includes details such as trading volumes, token addresses, liquidity metrics, and associated projects.

# ### Next Steps for Data Consolidation and Cleaning
# Before proceeding to analysis, I'll unify these datasets into a single DataFrame. This will involve:
# 
# Adding a 'chain' column to each dataset if not already present, to identify the source of each record.
# Standardizing column names across all datasets if there are discrepancies.
# Concatenating all datasets into a single DataFrame.
# Cleaning the unified dataset by converting volumes to a consistent unit, simplifying columns like 'projects' to numeric counts, and removing unnecessary columns such as token addresses.

# ## Data Cleaning and Integration Code:

# In[2]:


# Concatenate all datasets into a single DataFrame
all_dex_data = pd.concat(dex_datasets.values(), ignore_index=True)

# Data cleaning steps
# Convert volumes to billions and round to two decimals
columns_to_convert = ['all_time_volume', 'one_day_volume', 'seven_day_volume', 'thirty_day_volume', 'usd_liquidity']
for col in columns_to_convert:
    all_dex_data[col] = all_dex_data[col] / 1e9
    all_dex_data[col] = all_dex_data[col].round(2)

# Simplify the 'projects' column to count of projects
all_dex_data['project_count'] = all_dex_data['projects'].apply(lambda x: len(eval(x)))

# Remove unnecessary columns
all_dex_data.drop(['token_a_address', 'token_b_address', 'pool_ids', 'projects'], axis=1, inplace=True)

# Display the cleaned, integrated data
print(all_dex_data.head())
print(all_dex_data.info())


# After running the above code, we will have a clean, unified dataset ready for exploratory data analysis (EDA) and comparison across different chains. I'll proceed with this integration and cleaning step now.
# 
# The data from all chains has been successfully cleaned and consolidated into a unified DataFrame, ready for detailed analysis. Below, I'll outline the exploratory data analysis (EDA), visualization, and the derivation of insights from this integrated dataset.

# # Feature Engineering of Dex Dataset by Chain

# We can create a simplified dataset that aggregates DEX data by chain. This dataset will focus on key metrics such as average volumes, liquidity, and project counts across different blockchain chains. I'll also perform some feature engineering to derive additional useful metrics.

# ### Steps to Create the Simplified Dataset:
# #### Aggregate Data: 
# Calculate average trading volumes and liquidity per chain.
# #### Feature Engineering:
#  - Volatility Index: 
# Create a feature representing the volatility of trading volumes to gauge market stability.
#  - Liquidity Ratio: 
# Calculate the average liquidity to volume ratio to assess market efficiency.

# In[3]:


# Group data by 'chain' and aggregate with mean for basic metrics
chain_aggregates = all_dex_data.groupby('chain').agg({
    'one_day_volume': 'mean',
    'seven_day_volume': 'mean',
    'thirty_day_volume': 'mean',
    'usd_liquidity': 'mean',
    'project_count': 'mean'
}).reset_index()

# Feature Engineering
# Volatility Index: Standard deviation of the different volume metrics normalized by the mean volume
volume_columns = ['one_day_volume', 'seven_day_volume', 'thirty_day_volume']
chain_aggregates['volume_std'] = all_dex_data[volume_columns].std(axis=1) / all_dex_data[volume_columns].mean(axis=1)

# Liquidity Ratio: Liquidity to average volume ratio
chain_aggregates['liquidity_ratio'] = chain_aggregates['usd_liquidity'] / chain_aggregates[volume_columns].mean(axis=1)

# Display the simplified dataset
print(chain_aggregates.head())


# ## Exploratory Data Analysis (EDA) and Visualization
# We'll analyze this combined dataset to uncover trends and differences across chains in trading volumes, liquidity, and project counts. Here's the plan for the EDA:
# 
# Volume and Liquidity Trends: Analyze trends across different chains regarding trading volumes and liquidity.
# Comparative Analysis: Compare the performance and characteristics of DEX pairs across different chains.
# Impact of Project Counts: Investigate whether a higher number of projects correlates with higher trading volumes or liquidity.

# In[4]:


import seaborn as sns
import matplotlib.pyplot as plt

# Set the aesthetic style of the plots
sns.set_style("whitegrid")

# Volume and Liquidity Comparison Across Chains
plt.figure(figsize=(16, 6))
plt.subplot(1, 2, 1)
sns.boxplot(x='chain', y='seven_day_volume', data=all_dex_data)
plt.title('Comparison of 7-Day Trading Volume Across Chains')
plt.ylabel('Volume (in billions)')
plt.xlabel('Blockchain Chain')

plt.subplot(1, 2, 2)
sns.boxplot(x='chain', y='usd_liquidity', data=all_dex_data)
plt.title('Comparison of USD Liquidity Across Chains')
plt.ylabel('Liquidity (in billions)')
plt.xlabel('Blockchain Chain')

plt.tight_layout()
plt.show()

# Analyzing Project Count Impact
plt.figure(figsize=(10, 6))
sns.scatterplot(x='project_count', y='seven_day_volume', hue='chain', data=all_dex_data, palette='Set2', size='usd_liquidity', sizes=(20, 200))
plt.title('Project Count Impact on 7-Day Volume and Liquidity')
plt.xlabel('Number of Projects')
plt.ylabel('7-Day Volume (in billions)')
plt.grid(True)
plt.legend(title='Chain')
plt.show()


# ## Visual Analysis Results
# The plots reveal several insights about trading volumes, liquidity, and the impact of project counts across different blockchain chains:
# 
# #### Volume and Liquidity Comparison Across Chains:
# The boxplots show significant variation in trading volume and liquidity across chains. Some chains exhibit higher median volumes and a broader range of liquidity, indicating more active trading environments.
# Certain chains might display outliers in trading volume or liquidity, which could indicate either high-performing DEX pairs or potential data anomalies.
# #### Project Count Impact on Volume and Liquidity:
# The scatter plot indicates varying relationships between the number of projects and trading volumes across different chains. While some chains show a positive correlation between project count and volume, others do not show a strong link.
# The size of the markers (representing liquidity) in the scatter plot also varies significantly, suggesting that higher project counts do not consistently translate to higher liquidity.
# ### Insights and Key Takeaways
# #### Strategic Opportunities: 
# Chains with consistently high volumes and liquidity might be more attractive for traders and investors looking for stable and active markets. These chains could also be targeted for further development and investment.
# #### Need for Detailed Analysis: 
# The outliers and variations across chains warrant a deeper dive to understand the causes—whether they are due to market conditions, specific projects, or other external factors.
# #### Project Impact: 
# The varied impact of project count on volume and liquidity suggests that the mere number of projects is not a direct indicator of market health. The nature and quality of these projects, along with their integration and utility within the DEX ecosystem, are likely more influential.
# This structured analysis not only highlights the current state of various DEX markets across different blockchain technologies but also points towards strategic decisions for stakeholders in these ecosystems. Further steps might involve a more granular analysis of individual token pairs or projects to identify specific drivers of success or issues needing attention.

# ### Visualization of Dex Dataset by Chain:

# In[5]:


# Visualizing liquidity ratio across chains
plt.figure(figsize=(10, 6))
sns.barplot(x='chain', y='liquidity_ratio', data=chain_aggregates)
plt.title('Liquidity to Volume Ratio by Chain')
plt.xlabel('Blockchain Chain')
plt.ylabel('Liquidity to Volume Ratio')
plt.show()

# Visualizing average project count across chains
plt.figure(figsize=(10, 6))
sns.barplot(x='chain', y='project_count', data=chain_aggregates)
plt.title('Average Number of Projects by Chain')
plt.xlabel('Blockchain Chain')
plt.ylabel('Average Project Count')
plt.show()


# #### Market Efficiency: 
# - The liquidity ratio highlights chains where liquidity is efficiently managed relative to trading volume. Higher ratios suggest more liquid markets, potentially offering smoother trading experiences.
# 
# #### Ecosystem Activity: 
# - The average number of projects serves as a proxy for ecosystem activity and developer engagement. Chains with higher project counts may offer more diversity and innovation within their markets
# 
# The Dex Dataset by Chain aggregates key metrics across different blockchain chains, providing a clear comparison of average volumes, liquidity, and project counts.

# ## Insights from the Dex Dataset by Chain:
# #### Liquidity to Volume Ratio by Chain:
# The bar graph illustrates the liquidity ratios across different chains. This ratio is an indicator of how well liquidity is maintained relative to the trading volume. Chains with higher ratios, such as BNB and Ethereum, indicate more efficient liquidity management, which could be appealing for traders seeking stable trading environments.
# #### Average Number of Projects by Chain:
# This graph shows the average number of projects associated with each chain. Optimism leads with the highest average number of projects, suggesting a vibrant and active ecosystem. Higher project counts can be indicative of greater innovation and community engagement within the chain.

# ## Concluding Insights:
# #### Strategic Decisions: 
# Chains with higher liquidity ratios may be more attractive for launching new projects or for traders prioritizing stable market conditions. Conversely, chains with lower liquidity ratios might need strategies to enhance their market efficiency.
# #### Ecosystem Development: 
# A higher average number of projects typically suggests a robust developer ecosystem. Chains like Optimism could be targeted for partnerships or further development due to their active community engagement.
# #### Resource Allocation: 
# Understanding the dynamics illustrated in these visualizations can help stakeholders allocate resources more effectively, whether it's capital investment, marketing efforts, or development priorities.

# # Create Dashboard for Dex Data

# In[9]:


import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd

# Initialize the Dash application
app = dash.Dash(__name__)

# Define custom color sequences for visualizations
custom_colors = ['#0074D9', '#FF4136', '#2ECC40', '#FF851B', '#7FDBFF', '#B10DC9']

# Create Plotly Express graphs for the dashboard
fig_liquidity_ratio = px.bar(chain_aggregates, x='chain', y='liquidity_ratio', title='Liquidity to Volume Ratio by Chain',
                             color='chain', color_discrete_sequence=custom_colors)
fig_project_count = px.bar(chain_aggregates, x='chain', y='project_count', title='Average Number of Projects by Chain',
                           color='chain', color_discrete_sequence=custom_colors)

# Adding detailed visualizations for each chain
fig_one_day_volume = px.bar(chain_aggregates, x='chain', y='one_day_volume', title='Average One-Day Volume by Chain',
                            color='chain', color_discrete_sequence=custom_colors)
fig_seven_day_volume = px.bar(chain_aggregates, x='chain', y='seven_day_volume', title='Average Seven-Day Volume by Chain',
                              color='chain', color_discrete_sequence=custom_colors)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='DEX Data Dashboard'),

    html.Div(children='''
        A web dashboard for displaying DEX data metrics.
    '''),

    dcc.Graph(
        id='liquidity-ratio-graph',
        figure=fig_liquidity_ratio
    ),

    dcc.Graph(
        id='project-count-graph',
        figure=fig_project_count
    ),

    dcc.Graph(
        id='one-day-volume-graph',
        figure=fig_one_day_volume
    ),

    dcc.Graph(
        id='seven-day-volume-graph',
        figure=fig_seven_day_volume
    )
])

# Run the server on a specified port
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)  # Use a different port if 8050 is in use

