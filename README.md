# Biden's Big Government Project
This project takes data from the CBO projections before Biden's presidency and compares them to CBO projections now, during the President's fourth year. Actual 
outlays taken from OMB data are also displayed. 
The main purpose of having this repo is to use Streamlit Community Cloud to host the app that produces charts for each agency comparing the two projections.

## App Version History
0.1 - launch app with the dropdown consisting of all unique values in the CBO24 "agency" column
0.2 - separate the cleaning and merging of the three datasets from the app
0.3 - for the drop down menu, only include "agencies" that have outlays recorded for all three sources

## Random Notes
(0.3) There are some agencies that don't really have significant differences (or are less than before):
    Department of Justice
    Department of Health and Human Services
    Deparment of Justice
    Department of Labor (has some funky stuff tho)
    Department of State (less now)
    Judicial Branch
    NASA
    SBA (shows covid spike tho)
    
(0.3) What is going on with 'Other Defense--Civil Programs'?

Agencies in the CBO24 that aren't in the CBO21:
    400 Years of African-American History Commission
    Southeast Crescent Regional Commission
    Southwest Border Regional Commission

"Agencies" in the OMB that aren't in CBO24:
    United States Enrichment Corporation Fund
    Social Security Administration (On-Budget)
    Social Security Administration (Off-Budget)
    Other Independent Agencies (On-Budget)
    Other Independent Agencies (Off-Budget)
    Undistributed Offsetting Receipts
    (On-budget)
    (Off-budget)
    Total outlays

Important to note that in the long format df, only the OMB data is actual outlays. The CBO21 and CBO24 are projections. NaN values fill the gaps. 
    on that note, to match Jame's charts, I added values to the outlays in the year previous to the CBO projections from OMB (so the actual outlays):
    so CBO24 has outlays recorded for 2023 but these are taken from OMB's data
    CBO21 has outlays recorded for 2020 but these are taken from OMB's data