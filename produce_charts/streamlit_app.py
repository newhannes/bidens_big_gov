import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import ticker
import streamlit as st

#notes: Playfair Display font is not available in the streamlit app
#            what if we changed the legend labels to be something like "Projection Before Biden" and "Projection After Biden"?


### STEP ONE: load data ###
@st.cache_data
df_long = pd.read_excel('data/agency_outlays.xlsx')

### STEP TWO: charts ###

def linechart_maker(agency):
    df_agency = df_long[df_long['agency'] == agency]
    df_agency = df_agency.sort_values(by=['source','year'])
    df_agency['outlays'] = df_agency['outlays'] / 1000 #convert to billions
    sns.set_style('whitegrid')
    #plt.rcParams['font.family'] = 'Playfair Display'  
    plt.figure(figsize=(12, 5.3))
    palette = {'CBO21': '#967D4A', 'CBO24': '#84AE95', 'OMB': '#000000'}
    lineplot = sns.lineplot(data=df_agency, x='year', y='outlays', hue='source', palette=palette, linewidth=3.4)
    plt.title(f'{agency} \n Outlay Projections Before Biden vs. Now', weight='bold', fontsize=16)
    plt.ylabel('Outlays \n (billions of $)')
    plt.xlabel('Fiscal Year')
    plt.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=3)
    lineplot.grid(False, 'both', 'x')
    legend = lineplot.get_legend() # Get the current legend
    legend.set_title('') # Remove the legend title
    for t, l in zip(legend.texts, ('CBO 2021 Projection', 'CBO 2024 Projection', 'Actual Outlays')): # Rename the legend labels
        t.set_text(l)
    
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'${x:.0f}'))
    sns.despine(offset=15, left=True)
    st.pyplot(plt.gcf())

### STEP THREE: Streamlit app ###
st.title("Biden's Big Government")
st.write("Projected Outlays Before Biden vs. Now")
agency = st.selectbox('Select an agency:', df_long['agency'].unique())
linechart_maker(agency)