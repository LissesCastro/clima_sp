import pandas as pd

dataset = pd.read_csv('dataset/southeast.csv', encoding='utf-8') # Arquivo original
dataset.columns = dataset.columns.str.strip()

#REALIZANDO LIMPEZA DA BASE - RETIRANDO CATEGORIAS QUE NÃO ME SÃO INTERESSANTES PARA ESSA ANÁLISE
dataset.drop(['PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)','PRESSÃO ATMOSFERICA MAX.NA HORA ANT. (AUT) (mB)', 'PRESSÃO ATMOSFERICA MIN. NA HORA ANT. (AUT) (mB)','TEMPERATURA DO PONTO DE ORVALHO (°C)', 'TEMPERATURA ORVALHO MIN. NA HORA ANT. (AUT) (°C)', 'TEMPERATURA ORVALHO MAX. NA HORA ANT. (AUT) (°C)','VENTO, RAJADA MAXIMA (m/s)', 'VENTO, DIREÇÃO HORARIA (gr) (° (gr))', 'region', 'station'], axis=1,  inplace=True)
dataset.to_csv('dataset/southeast_modificado.csv', index=False)

dataset = pd.read_csv('dataset/southeast_modificado.csv', encoding='utf-8') #Arquivo modificado

#FILTRANDO APENAS PARA O ESTADO DE SÃO PAULO
dataset_sp = dataset[dataset['state'] == 'SP']
print(dataset_sp.head())
dataset_sp.to_csv('dataset/southeast_modificado_sp.csv', index=False)