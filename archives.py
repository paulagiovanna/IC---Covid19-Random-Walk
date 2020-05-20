import pandas as pd
import numpy as np

flights_2018 = pd.read_csv('filghts_2018_model.csv') 
flights_2018 = flights_2018[['pais_origem', 'pais_destino']]

flights_2019_1 = pd.read_csv('filghts_2019_1_model.csv')
flights_2019_1 = flights_2019_1[['pais_origem', 'pais_destino']]
flights_2019_2 = pd.read_csv('filghts_2019_2_model.csv')
flights_2019_2 = flights_2019_2[['pais_origem', 'pais_destino']]

flights = flights_2018.append(flights_2019_2)
flights = flights.append(flights_2019_1)

#print(flights)
flights = flights.dropna()
#print('Total de voos:' + str(flights.shape))
flights['qtde_voos'] = 1

national = np.where(flights['pais_origem']==flights['pais_destino'], True, False)
national_flights = flights[national]
international = np.where(flights['pais_origem']!=flights['pais_destino'], True, False)
international_flights = flights[international]
#print('Total de voos internacionais: ' + str(international_flights.shape))
#print('Total de voos nacionais: ' + str(national_flights.shape))

national_flights = national_flights.groupby(['pais_origem', 'pais_destino']).sum()
national_flights['qtde_voos'] = national_flights['qtde_voos']/720
international_flights = international_flights.groupby(['pais_origem', 'pais_destino']).sum()
international_flights['qtde_voos'] = international_flights['qtde_voos']/730

international_flights = international_flights.reset_index()
#print(international_flights)
international_flights.to_csv('international_graph.csv') 
