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
    
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'${x:.0f}'))
    sns.despine(offset=15, left=True)
    st.pyplot(plt.gcf())

def barchart_maker(agency):
    plt.figure(figsize=(12, 5.3))
    sns.set_style('white')
    barchart_df = cs_increase_programs[cs_increase_programs['Agency'] == agency]
    barchart_df = pd.melt(barchart_df, id_vars='Title', value_vars=['22-31', '25-34'], var_name='10-year Projections', value_name='Value').sort_values(by=["10-year Projections"], ascending=True)
    barchart_df['Value'] = barchart_df['Value'] / 1000
    barchart = sns.barplot(data=barchart_df, x='Title', y='Value', hue='10-year Projections', palette={'22-31': '#84AE95', '25-34': '#004647'})
    plt.title(f'{agency} \n 10-Year Outlay Increases by Program', weight='bold', fontsize=16)
    plt.ylabel('Outlay Increase \n (in billions)')
    plt.xlabel('')
    sns.despine()
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'${x:,.0f}'))
    
    legend = barchart.get_legend() # Get the current legend
    legend.set_title('')
    for t, l in zip(legend.texts, ('2021 Projection', '2024 Projection')): # Rename the legend labels
        t.set_text(l)
    st.pyplot(plt.gcf())

### STEP THREE: Streamlit app ###

#sidebar
page = st.sidebar.radio("Go to page", ["Home", "Case Studies" "About"])
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
    st.write("Take a deeper dive into the data behind the increased spending projections for six key agencies.")
    case_studies = ['Department of Agriculture', 'Department of Commerce', 'Department of Labor', "Department of the Treasury",
                     "Department of Transportation", "Environmental Protection Agency"]
    agency = st.selectbox('Select an agency:', case_studies)

    cs_increase = pd.read_excel('output/cbo_projection_changes.xlsx', sheet_name="case studies increases by agency")
    cs_increase = cs_increase[cs_increase['Agency'] == agency]
    st.subheader(f"{agency}")
    st.markdown("##### Changes in projected outlays (in billions)")
    cs_21 = f"${int(round(cs_increase['22-31'].values[0] / 1000, 0)):,}"
    cs_24 = f"${int(round(cs_increase['25-34'].values[0] / 1000,0)):,}"
    cs_pct = f"{round(cs_increase['percent_change'].values[0])}%"

    col1, col2, col3 = st.columns(3)
    col1.metric(label="10 Year Projection in 2021", value=cs_21)
    col2.metric(label="10 Year Projection in 2024", value=cs_24)
    col3.metric(label="Increase in 10 Year Projection", value=cs_pct)

    st.write('\n')
    st.markdown("##### Program increases behind the change:")
    cs_increase_programs = pd.read_excel('output\program_increases.xlsx', sheet_name="case studies")
    barchart_maker(agency)
