import pandas as pd
import numpy as np
import networkx as nx
import random

international_flights = pd.read_csv('international_graph.csv')
international_flights = international_flights[['pais_origem', 'pais_destino', 'qtde_voos']]
column_list = international_flights.columns.values.tolist() 

source = international_flights['pais_origem'].unique()
target = international_flights['pais_destino'].unique()

for country in source:
    if country not in target:  
        #print('pais_origem: '+str(country))
        df = pd.DataFrame([[country, country, 0]], columns=column_list)
        international_flights = international_flights.append(df, ignore_index = True)

for country in target: 
    if country not in source:
        #print('pais_destino: '+str(country))
        df = pd.DataFrame([[country, country, 0]], columns=column_list) 
        international_flights = international_flights.append(df, ignore_index = True) 


#print(international_flights)
country_international_flights = international_flights.groupby(['pais_origem']).sum() 
transition_matrix = international_flights.copy()
transition_matrix = transition_matrix.drop(columns= ['qtde_voos'])
transition_matrix['prob'] = 0.
#print(country_international_flights)
#print(transition_matrix)

for index, row in international_flights.iterrows():
    weight = country_international_flights.loc[row['pais_origem']]
    weight = float(weight)
    if weight == 0:
        weight = 1
    transition_matrix.loc[index,'prob'] = row['qtde_voos']/weight

transition_matrix = transition_matrix.set_index('pais_origem')  
transition_matrix.to_csv("transition_matrix_edge_list.csv")

transition_matrix = transition_matrix.pivot(columns='pais_destino', values='prob') 
transition_matrix = transition_matrix.fillna(0)
#print(transition_matrix)                  

#print(transition_matrix.iloc[[25]])
state_vector = [0]*142
state_vector[25] = 1000
#print(state_vector) 

country_list = transition_matrix.index.values.tolist()

for i in range(30):
    state_vector = np.dot(state_vector, transition_matrix)
    #print(state_vector)

i = 0
df = pd.DataFrame()
df['country'] = ' '
df['state'] = 0

for country in country_list:
    df = df.append({'country': country, 'state': state_vector[i]}, ignore_index = True)
    i = i+1

df = df.set_index(['country'])
df.sort_values(by='state', ascending=False, inplace=True)

df.to_csv('state_vector.csv')
transition_matrix.to_csv('transition_matrix.csv')
#print(df)

