import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import ticker
import streamlit as st

#notes: Playfair Display font is not available in the streamlit app
# hat if we changed the legend labels to be something like "Projection Before Biden" and "Projection After Biden"?


### STEP ONE: load data ###
df = pd.read_excel('output/agency_outlays.xlsx')
#only include agencies that have an outlay for each year and each source
agency_counts = df['agency'].value_counts()
agencies_to_drop = agency_counts[agency_counts != 51].index 
df = df[~df['agency'].isin(agencies_to_drop)].query('agency != "Allowances"') #also get rid of allowances cause its weird

### STEP TWO: charts ###

def linechart_maker(agency):
    df_agency = df[df['agency'] == agency]
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
    
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'${x:,.0f}'))
    sns.despine(offset=15, left=True)
    st.pyplot(plt.gcf())

def barchart_maker(agency):
    plt.figure(figsize=(12, 5.3))
    sns.set_style('white')
    barchart_df = increase_by_program[increase_by_program['Agency'] == agency]
    
    if barchart_df.shape[0] < 3:
        barchart_df = barchart_df.sort_values(by="dollar_change", ascending=False)
    else:  
        barchart_df = barchart_df.sort_values(by="dollar_change", ascending=False).head(3)
    
    if agency == "Department of Commerce":
        barchart_df.loc[barchart_df['Bureau'] == "National Oceanic and Atmospheric Administration", "Bureau"] = "NOAA"
        barchart_df.loc[barchart_df['Bureau'] == "National Institute of Standards and Technology", "Bureau"] = "NIST"
        barchart_df.loc[barchart_df["Bureau"] == "National Telecommunications and Information Administration", "Bureau"] = "NTIA"
    if agency == "Department of the Treasury":
        barchart_df = barchart_df[barchart_df['Bureau'] != 'Fiscal Service'] #this just doesnt show up well compared to the massive inc in interest

    barchart_df = pd.melt(barchart_df, id_vars='Bureau', value_vars=['22-31', '25-34'], var_name='10-year Projections', value_name='Value').sort_values(by=["10-year Projections"], ascending=True)
    barchart_df['Value'] = barchart_df['Value'] / 1000
    ax = barchart = sns.barplot(data=barchart_df, x='Bureau', y='Value', hue='10-year Projections', palette={'22-31': '#84AE95', '25-34': '#004647'})

    for i in ax.containers:
        ax.bar_label(i, labels = [f"${x:,.0f}" for x in i.datavalues], weight="bold", fontsize = 12)
   
    plt.title(f'{agency} \n 10-Year Outlay Increases by Program (billions of dollars) \n', weight='bold', fontsize=16)
    #plt.ylabel('Outlays \n (in billions)')
    ax.set_yticks([])
    plt.ylabel('')
    plt.xlabel('')
    sns.despine(left=True)
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'${x:,.0f}'))
    
    legend = barchart.get_legend() # Get the current legend
    try:
        legend.set_title('')
        for t, l in zip(legend.texts, ('2021 Projection', '2024 Projection')): # Rename the legend labels
            t.set_text(l)
    except:
        st.write(barchart_df)
        raise ValueError("This agency currently has no data to show.")
    st.pyplot(plt.gcf())

### STEP THREE: Streamlit app ###

#sidebar
page = st.sidebar.radio("Go to page", ["Home", "Case Studies", "About"])
rd_file_path = "README.md"

if page == "Home":
    st.title("Biden's Big Government")
    st.write(f"""President Biden has presided over a flood of government spending. His executive agencies have been the beneficiaries of this involuntary gift from taxpayers. 
             Explore the data below to see how the projected outlays of {len(df['agency'].unique())} agencies have changed since Biden took office.""")
    #Chart maker
    agency = st.selectbox('Select an agency or start typing:', df['agency'].unique())
    linechart_maker(agency)

if page == "About":
     with open(rd_file_path, "r") as f:
        readme_text = f.read()
        st.markdown(readme_text)

if page == "Case Studies":
    st.header("Case Studies")
    #st.write("Take a deeper dive into the data behind the increased spending projections for six key agencies.")
    agency_df = pd.read_excel('output/cbo_projection_changes.xlsx', sheet_name="agency increases").query("percent_change > 0") #all agencies with an increase
    agency_df = agency_df[~agency_df["Agency"].isin(agencies_to_drop)]
    st.write(f"Take a deeper dive into the data behind the increased spending projections for {agency_df['Agency'].nunique()} agencies.")
    
    #case_studies = ['Department of Agriculture', 'Department of Commerce', 'Department of Labor', "Department of the Treasury",
    #                 "Department of Transportation", "Environmental Protection Agency"]
    agency = st.selectbox('Select an agency:', agency_df['Agency'].unique())
    agency_df = agency_df[agency_df['Agency'] == agency]
    #cs_increase = pd.read_excel('output/cbo_projection_changes.xlsx', sheet_name="cs inc by agency")
    #cs_increase = cs_increase[cs_increase['Agency'] == agency]
    st.subheader(f"{agency}")
    st.markdown("##### Changes in projected outlays (in billions)")
    cs_21 = f"${int(round(agency_df['22-31'].values[0] / 1000, 0)):,}"
    cs_24 = f"${int(round(agency_df['25-34'].values[0] / 1000,0)):,}"
    cs_pct = f"{round(agency_df['percent_change'].values[0])}%"

    col1, col2, col3 = st.columns(3)
    col1.metric(label="10 Year Projection in 2021", value=cs_21)
    col2.metric(label="10 Year Projection in 2024", value=cs_24)
    col3.metric(label="Increase in 10 Year Projection", value=cs_pct)

    st.write('\n')
    st.markdown("##### Program increases behind the change:")
    increase_by_program = pd.read_excel("output/cbo_projection_changes.xlsx", sheet_name="agency-bureau inc").query('percent_change > 0') #filter out decreases in spending
    
    barchart_maker(agency)
