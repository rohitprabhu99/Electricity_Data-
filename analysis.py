import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('owid-energy-data.txt')

#%% Computing global electricity mix in 2019


#Computing total electricity generation

electricity_total = np.nansum(df.loc[df['year'] == 2019, ['electricity_generation']].to_numpy())

#Computing total electricity generation by source


sources= ['coal', 
          'gas', 
          'oil',
          'nuclear', 
          'hydro', 
          'biofuel',
          'solar', 
          'wind', 
          'other_renewable_exc_biofuel' ] #List of sources

electricity_by_source = {} #Dictionary that will contain total electricity production from each source


for source in sources:
    electricity_by_source["{0}".format(source)] = np.nansum(df.loc[df['year'] == 2019, ['{0}_electricity'.format(source)]].to_numpy())    




#Checking that the sums of electricity production by source equals the total electricity production
print("The following values should be roughly equal")
print(sum(electricity_by_source.values()))
print(electricity_total)


#Computing share of electricity bt source
electricity_share_by_source = {} #Dictionary that will contain electricity share from each source


for source in sources:
    electricity_share_by_source["{0}".format(source)] = electricity_by_source["{0}".format(source)]/electricity_total


#%%
#Plotting as pie chart

labels = ['Coal',
          'Gas',
          'Oil',
          'Nuclear',
          'Hydropower',
          'Biofuel',
          'Solar',
          'Wind',
          'Other renewables']

sizes = electricity_share_by_source.values()

fig1, ax1 = plt.subplots()

ax1.pie(sizes, labels = labels)

ax1.set(title = "Global electricity by generation method")

plt.savefig('Generation_method.png')


#%% Relationship between low-carbon share and nuclear + hydro share


#Extracting low-carbon share (= 1 - fossil share) for each country in 2019

low_carbon_share = df.loc[df['year'] == 2019, ['country', 'fossil_share_elec']]

low_carbon_share['fossil_share_elec'] = low_carbon_share.fossil_share_elec.map(lambda p: 100 - p)

low_carbon_share = low_carbon_share.rename(columns={'fossil_share_elec': 'low_carbon_share_elec'})


#Computing sum of nuclear and hydro share for each country in 2019

nuclear_hydro_share = df.loc[df['year'] == 2019, ['country']]

nuclear_hydro_share['nuclear_hydro_share_elec'] = df.loc[df['year'] == 2019, ['hydro_share_elec', 'nuclear_share_elec']].sum(axis = 1)


#Combing the two DataFrames

low_carbon = pd.merge(low_carbon_share, nuclear_hydro_share, how='inner', on = 'country')

#Removing negative values
low_carbon = low_carbon.loc[low_carbon['low_carbon_share_elec']>=0]

#%%

#Plotting

fig2, ax2 = plt.subplots()

ax2.scatter(low_carbon.iloc[:, 1].to_numpy(), low_carbon.iloc[:, 2].to_numpy(), color = 'green')

ax2.set(xlabel = "Share of electricity from low-carbon sources",
        ylabel = "Share of electricity from nuclear or hydropower")

plt.savefig("Nuclear+hyrdo.png")






