from cProfile import label
from pydoc import describe
from turtle import color, title
import pandas as pd
import seaborn as srn
from matplotlib import pyplot as plt
import datetime as dt
import statistics as sts
pd.set_option('display.max_columns', None)


#ABRINDO A BASE
dataset_sp = pd.read_csv('dataset/southeast_modificado_sp.csv', encoding='utf-8')
#print(dataset_sp.dtypes)


#ANÁLISE EXPLORATÓRIA DOS DADOS - RESUMO ESTATÍSTICO DAS COLUNAS
sum_chuva = dataset_sp['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'].describe()
sum_tempMAX = dataset_sp['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'].describe()
sum_tempMIN = dataset_sp['TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)'].describe()


#IDENTIFICANDO OS VALORES ERRADOS DE TEMPERATURA (VALORES -9999 OU OUTLIERS) E SUBSTITUINDO-OS PELAS MEDIANAS DE TEMPERATURA MÍNIMA OU MÁXIMA
corrigido_Tmin = dataset_sp.loc[(dataset_sp['TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)'] > -10)] 
mediana_Tmin = sts.median(corrigido_Tmin['TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)']) #mediana = 20.09 C°
dataset_sp.loc[dataset_sp['TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)'] < -4.1, 'TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)'] = mediana_Tmin

corrigido_Tmax = dataset_sp.loc[(dataset_sp['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'] > 0)]
mediana_Tmax = sts.median(corrigido_Tmax['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'])
dataset_sp.loc[dataset_sp['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'] < 0, 'TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'] = mediana_Tmax

corrigido_precipitacao = dataset_sp.loc[(dataset_sp['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'] > 0)]
mediana_precipitacao = sts.median(corrigido_precipitacao['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'])
dataset_sp.loc[dataset_sp['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'] < 0, 'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'] = mediana_precipitacao


#AGRUPANDO DADOS POR ANO - TRANSFORMANDO FORMATO DATETIME EM COLUNAS DE DIA, MÊS E ANO
dataset_sp['Data'] = pd.to_datetime(dataset_sp['Data'])
dataset_sp['dia'] = dataset_sp['Data'].dt.day
dataset_sp['mes'] = dataset_sp['Data'].dt.month
dataset_sp['ano'] = dataset_sp['Data'].dt.year
#dataset_sp.to_csv('dataset/southeast_modificado_sp.csv', index=False)

#AGRUPANDO DADOS POR ANO - PEGANDO OS MAIORES E MENORES VALORES DE TEMP. MAX OU MIN POR ANO E CRIANDO UMA NOVA COLUNA COM O NÚMERO
dataset_sp['Tmax_ano'] = dataset_sp.groupby(['ano'])['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'].transform(max)
dataset_sp['Tmin_ano'] = dataset_sp.groupby(['ano'])['TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)'].transform(min)
dataset_sp['precMax_ano'] = dataset_sp.groupby(['ano'])['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'].transform(max)


#PLOTANDO - 
#2 LINHAS (TEMP MAX E MIN) AO LONGO DO TEMPO
# fig, ax = plt.subplots()
# ax = srn.lineplot(x='ano', y='Tmin_ano', data=dataset_sp, palette='blue', label='Temperatura mínima')
# ax1 = srn.lineplot(x='ano', y = 'Tmax_ano', data=dataset_sp, palette='red', label='Temperatura máxima')
# plt.xlabel('Ano')
# plt.ylabel('Temperatura (C°)')
# plt.title('Temperaturas máximas e mínimas anuais (2000-2021)')
# plt.show()

#SCATTER DA RELAÇÃO ENTRE PRECIPITAÇÃO NO ANO
# srn.scatterplot(x = 'ano', y= 'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)', data=dataset_sp, palette='green', label='Chuva', linewidth=0)
# plt.xlabel('Ano')
# plt.ylabel('Precipitação (mm)')
# plt.title('Quantidade de precipitação por dias de chuva no ano (2000 - 2021)')
# plt.show()

#SCATTER DA RELAÇÃO ENTRE TEMPERATURA MÁXIMA E CHUVA
srn.scatterplot(x = 'TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)', y= 'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)', data=dataset_sp, hue='PRECIPITAÇÃO TOTAL, HORÁRIO (mm)', palette='Blues', label='Chuva', linewidth=0)
plt.xlabel('Temperatura máxima registrada no dia da chuva')
plt.ylabel('Precipitação (mm)')
plt.title('Quantidade de precipitação por máxima da temperatura (2000 - 2021)')
plt.show()






