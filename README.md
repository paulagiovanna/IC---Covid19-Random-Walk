# IC - Random Walk Project


## Passo a passo para rodar o projeto:

### Passo 1.

    O arquivo 'archives.ipynb' é o primeiro arquivo que deve ser rodado:
    Ele contabiliza quantos voos foram feitos de um país para o outro e tira uma média diária (como são 2 anos divide a soma por 730). 
    Esse código gera o arquivo 'international_graph.csv' com a média de voos diários de um país para outro.
    
### Passo 2.
    Para fazer o random walk deve-se rodar o arquivo 'random_walk.ipynb':
    Ele pega os dados do arquivo 'international_graph.csv' e do arquivo 'total_cases_countries_normalized.csv', se houver algum país no primeiro arquivo que não esteja presente no dia escolhido para análise no segundo arquivo ele considera que o total de casos naquele país e naquele dia foi 0.
    Esse código gera o arquivo 'transition_matrix_edge_list.csv' com uma normalização da média de voos diários de um país para outro e o arquivo 'state_vector.csv' gerado com os melhores parâmetros encontrados pelo grid search.
    
### Passo 3.
    Para gerar graficos da matriz de transição e do vetor de estados deve-se rodar o arquivo 'draw_graph.ipynb'.
    Ele pega os dados dos arquivos 'transition_matrix_edge_list.csv' e 'state_vector.csv' e gera dois gráficos: um que representa a matriz de transição no mapa mundi com seus respectivos pesos e um que representa o vetor de estados, também no mapa mundi com seus respectivos pesos.
    Esse código gera os arquivos 'uncolored_graph_edges.png' e 'colored_graph_nodes.png'.
