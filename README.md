# Biden's Big Government Project
This project takes data from the CBO projections before Biden's presidency and compares them to CBO projections now, during the President's fourth year. Actual 
outlays taken from OMB data are also displayed. 
The main purpose of having this repo is to use Streamlit Community Cloud to host the app that produces charts for each agency comparing the two projections.

## App Version History
- 0.1 - launch app with the dropdown consisting of all unique values in the CBO24 "agency" column
- 0.2 - separate the cleaning and merging of the three datasets from the app
- 0.3 - for the drop down menu, only include "agencies" that have outlays recorded for all three sources
- 0.4 - add case studies page, switch largest increases to largest dollar increases rather than largest percent increases 
- 0.5 - instead of looking at "Title" for programmatic increases, look at "Bureau", drop "Fiscal Services" bureau from the Treasury's increases as it just fades to oblivion with the debt increases, add values on bars 
- 0.6 - expand case studies to the 25 of the 27 agencies in home page with increased spending

## Random Notes
(0.6) Expanding "Case Studies" to include the agencies in the "Home" page. Agencies with decreased spending are dropped (State and SBA). One problem is that some agencies did not have more than three bureaus and therefore are not in the data that the barchart_maker function pulls from. To fix this, I will have to have the funtion pull from the unsorted agency-bureau increases then select the three (or less than three if the agency has less than three bureaus) bureaus that have the highest (absolute) increases, then graph from there. Another "issue" is that a few agencies don't really have programs (Corps of Engs, National Science Foundation, OPM). Maybe need to give these the EPA treatment from 0.5? Potentially could create a rougher data explorer of the CBO changes intended for just HBC? Could go to the granular level of "Title" for people to explore any interesting irregularities. 

(0.5) There are 13 Agency-Bureau combinations in the 2024 CBO that are not in 2021 CBO. There are 8 Agency-Bureau combinations in the 2021 CBO that are not in the 2024 CBO. See "Differences" section below for the mismatches. A few are just renamed bureaus. Only two mismatchs are in agencies in our case studies so I am content to let this sit. Also, EPA has no bureaus so for both CBO21 and CBO24 data I replaced the "Bureau" entries with the "Title" entries. 

(0.4) The program increases were switched to include the three largest absolute (rather than percent) increases in projections. This seems to be how last year's edition caclulated the increases but I can switch to percent increases. Also, it looks like the programmatic increases within the agencies, with the exception of the EPA, were at the "Bureau" rather than "Title" level. That kinda makes more sense and I will fix that. 

(0.3) Playfair Display font is not available natively for the app. Would have to add it to the directory, which shouldn't be too much trouble?

(0.3) There are some agencies that don't really have significant differences between projections (or are less than before):
Department of Justice  
Department of Health and Human Services  
Deparment of Justice  
Department of Labor (has some funky stuff tho)  
Department of State (less now)  
Judicial Branch  
NASA  
SBA (shows covid spike tho)  
    
(0.3) What is going on with 'Other Defense--Civil Programs'?

Important to note that in the long format df, only the OMB data is actual outlays. The CBO21 and CBO24 are projections. NaN values fill the gaps. 
on that note, to match Jame's charts, I added values to the outlays in the year previous to the CBO projections from OMB (so the actual outlays):
so CBO24 has outlays recorded for 2023 but these are taken from OMB's data
CBO21 has outlays recorded for 2020 but these are taken from OMB's data

## Differences Between Datasets
Agency-Bureaus in CBO24 but not CBO21:
400 Years of African-American History CommissionBUREAU: 400 Years of African-American History Commission  
Department of Health and Human ServicesBUREAU: Substance Use And Mental Health Services Administration  
Department of JusticeBUREAU: Immigration and Naturalization Service  
Department of JusticeBUREAU: Justice Operations, Management, and Accountability  
Department of JusticeBUREAU: State, Local, and Tribal Justice Assistance  
Department of LaborBUREAU: Veterans' Employment and Training Service  
Department of TransportationBUREAU: Great Lakes St. Lawrence Seaway Development Corporation  
Department of the TreasuryBUREAU: Bureau of Engraving and Printing  
Environmental Protection AgencyBUREAU: Intrabudgetary Transactions
Executive Office of the PresidentBUREAU: Office of the National Cyber Director  
Multi-AgencyBUREAU: Budget Committee Unspecified Changes  
Southeast Crescent Regional CommissionBUREAU: Southeast Crescent Regional Commission  
Southwest Border Regional CommissionBUREAU: Southwest Border Regional Commission  

Agency-Bureaus in CBO21 but not CBO24:
Department of Health and Human ServicesBUREAU: Substance Abuse and Mental Health Services Administration  
Department of JusticeBUREAU: General Administration  
Department of JusticeBUREAU: Office of Justice Programs  
Department of TransportationBUREAU: Saint Lawrence Seaway Development Corporation  
Department of the InteriorBUREAU: Office of the Special Trustee for American Indians  
Multi-AgencyBUREAU: Multi-Agency  
Other Independent AgenciesBUREAU: Intelligence Community Staff  
United States Enrichment Corporation FundBUREAU: United States Enrichment Corporation Fund  

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

## Big Picture Process
Step 1: clean and merge the datasets, analyze by the three different levels (agency, bureau, title)
Step 2: create chart making functions
Step 3: develop streamlit app

## Ways I could improve my code (more robust)
In Step 1, I could have a conditional that checks if, for a unique "Agency" entry, there is only one unique "Bureau" entry. This would mean we have the "EPA problem" and should replace this agency's "Bureau" entries with its "Title" agencies.

In Step 2, I could develop some conditionals to decide the best way to visualize the data for that agency (like deciding whether to include three programs or less if it doesn't look good) aka the "Treasury problem" or view as millions of dollars if the agency is a small fish, what we will call the "Executive OOP Problem"