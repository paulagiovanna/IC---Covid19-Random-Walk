import pandas as pd
import numpy as np
import networkx as nx
import random
from scipy.stats import pearsonr

'''Carrega o arquivo de voos'''
international_flights = pd.read_csv('international_graph.csv')
international_flights = international_flights[['pais_origem', 'pais_destino', 'qtde_voos']]
column_list = international_flights.columns.values.tolist() 

source = international_flights['pais_origem'].unique()
target = international_flights['pais_destino'].unique()

'''Coloca na base os registros de paises que nao tem voos de chegada ou de partida'''
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


'''Faz o grafo de voos entre paises'''
#print(international_flights)
country_international_flights = international_flights.groupby(['pais_origem']).sum() 
transition_matrix = international_flights.copy()
transition_matrix = transition_matrix.drop(columns= ['qtde_voos'])
transition_matrix['prob'] = 0.
#print(country_international_flights)
#print(transition_matrix)

'''Poe nas arestas a probabilidade de um voo ocorrer do pais a para o pais b'''
for index, row in international_flights.iterrows():
    weight = country_international_flights.loc[row['pais_origem']]
    weight = float(weight)
    if weight == 0:
        weight = 1
    transition_matrix.loc[index,'prob'] = row['qtde_voos']/weight

transition_matrix = transition_matrix.set_index('pais_origem')  
transition_matrix.to_csv("transition_matrix_edge_list.csv")

'''Transforma o dataframe em uma matriz de correlacao'''
transition_matrix = transition_matrix.pivot(columns='pais_destino', values='prob') 
transition_matrix = transition_matrix.fillna(0)
#print(transition_matrix)                  

#print(transition_matrix.iloc[[24]])

'''Carrega o arquivo com o total de casos diarios'''
total_cases = pd.read_csv('total_cases_countries_normalized.csv')
total_cases = total_cases[['Name', 'Day', 'DailyCases']].set_index(['Name', 'Day'])

countries = transition_matrix.columns.to_list()

indexes = []
for index in total_cases.index:
    indexes.append(index)

daily_cases = []
for country in countries:
    if (country, 77) not in indexes:
        daily_cases.append(0.) 
    else:
        daily_cases.append(total_cases.loc[country, 77][0])

#daily_cases = np.reshape(daily_cases,(-1, 1)) 

df_final = pd.DataFrame()
df_final['daily_cases'] = daily_cases

arquivo = open("resultados.csv", "w")
arquivo.write('v;r\n')

respostas = open("respostas.csv","w")

contamination_rate = [float(x)/10.0 for x in range(10,31,1)]
initial_number = [x for x in range(10,510,10)] 

def pearsonr_pval(x,y):
        return pearsonr(x,y)[1]

for v in initial_number:
    for r in contamination_rate:
        state_vector = [0]*129
        state_vector[24]=v  
        for i in range(78):
            if i == 0:
                state_vector = np.dot(state_vector, transition_matrix)
            else:
                state_vector = np.dot(state_vector, transition_matrix)
                state_vector_multiply = [state_country*r for state_country in state_vector]
                state_vector = state_vector_multiply
        df_final['state_vector'] = state_vector
        

        df_corr = df_final.corr(method='pearson', min_periods = 6)
        df_p = df_final.corr(method=pearsonr_pval, min_periods = 6)
        df_corr_display = df_corr.round(2).applymap(str) + ' p=' + df_p.round(2).applymap(str) + ''
        '''Pearson na mao
        cov = np.cov(state_vector,daily_cases)
        prod_var = np.var(state_vector) * np.var(daily_cases)
        sqrt_prod_var = np.sqrt(prod_var)
        pearson = cov[0,1]/sqrt_prod_var
        '''
        '''Funcao pearsonr 
        state_vector = np.reshape(state_vector,(-1,1))
        daily_cases = np.reshape(daily_cases,(-1, 1))
        pearson = pearsonr(daily_cases,state_vector)[1]
        print('pearson: ' + str(pearson))
        '''
        arquivo.write(str(v)+';'+str(r)+';'+'\n'+str(df_corr_display)+';'+'\n\n')
        respostas.write("v:;"+str(v)+";r:;"+str(r)+"\n"+str(df_final)+"\n\n")
arquivo.close()
respostas.close()
