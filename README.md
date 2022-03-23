# Análise exploratória do clima em São Paulo

<p class="text-justify">Projeto de análise exploratória de dados, feito em Python, com o intuíto de explorar as ferramentas de organização e limpeza de dados em csv através da biblioteca Pandas, bem como potenciais de plotagem dos dados por meio de gráficos gerados por Seaborn e Matplotlib. 
 
A planilha explorada no projeto é referente aos dados horários do clima no Brasil a partir da medição realizada pelo [INMET](https://portal.inmet.gov.br/) entre 2000 e 2021. Os dados foram agrupados anteriormente e limpados por Jonh Holz e estão disponíveis [aqui](https://www.kaggle.com/datasets/PROPPG-PPG/hourly-weather-surface-brazil-southeast-region?resource=download). O arquivo base para esse projeto (intitulado 'Southeast.csv') é referente aos dados climatológicos disponíveis para a região sudeste do Brasil e foi filtrado de modo a manter apenas os dados climáticos localizados no Estado de São Paulo.
 
 O código do projeto foi separado em dois arquivos, o arquivo [Base_data_cleaning](clima_sp/Base_data_cleaning.py) contém o trabalho filtro do csv base e escrita dos novos csvs para trabalho, o arquivo [climate_analysis](clima_sp/climate_analysis.py) possui as correções nos valores da planilha trabalhada, os resumos estatísticos e a obtenção gráfica de relações entre as variáveis 
 ## Arquivo "base_data_cleaning.py"
O arquivo possui os códigos de limpeza do csv primário, transformando-o no dataframe de trabalho do projeto através de duas etapas:
 1. Alteração do modelo original do csv, onde foram retiradas as variáveis que não seriam consideradas e/ou trabalhadas na análise exploratória, a saber:
 
```python
 	dataset.drop(['PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)','PRESSÃO ATMOSFERICA MAX.NA HORA ANT. (AUT) (mB)', 'PRESSÃO ATMOSFERICA MIN. NA HORA ANT. (AUT) (mB)','TEMPERATURA DO PONTO DE ORVALHO (°C)', 'TEMPERATURA ORVALHO MIN. NA HORA ANT. (AUT) (°C)', 'TEMPERATURA ORVALHO MAX. NA HORA ANT. (AUT) (°C)','VENTO, RAJADA MAXIMA (m/s)', 'VENTO, DIREÇÃO HORARIA (gr) (° (gr))', 'region', 'station'], axis=1,  inplace=True)
```
	
2. Delimitação de filtro para área de trabalho apenas para os dados referentes ao Estado de São Paulo
```python
	dataset_sp = dataset[dataset['state'] == 'SP']
```
	
## Arquivo "climate_analysis"
No arquivo foi escrito todo o código referente às modificações necessárias para retirar erros numéricos/outliers e mitigar os possíveis erros no dataframe, o código obedece uma ordem onde foi realizada:
	
1. O resumo estatístico de algumas das colunas interessantes para trabalho, como exemplo:
```python
	sum_chuva = dataset_sp['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'].describe()
```
2. Identificação dos valores errados (como -9999 para o caso da falta de dados sobre o clima no horário) e substituição desses valores pela mediana da coluna:
```python
	corrigido_Tmin = dataset_sp.loc[(dataset_sp['TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)'] > -10)] 
	mediana_Tmin = sts.median(corrigido_Tmin['TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)']) #mediana = 20.09 C°
	dataset_sp.loc[dataset_sp['TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)'] < -4.1, 'TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)'] = mediana_Tmin
```
3. Dissolução da variável "Date" do tipo datetime em três variáveis (Ano, mês e dia) para a utilização das temperaturas máximas e mínimas por recorte de ano. O filtro foi realizado porque as medições eram horárias e, assim, a leitura por hora entre o período de 2000-2021 se mostrava muito poluída e pouco prática para o entendimento da dinâmica climatológica
```python
	dataset_sp['Data'] = pd.to_datetime(dataset_sp['Data'])
	dataset_sp['dia'] = dataset_sp['Data'].dt.day
	dataset_sp['mes'] = dataset_sp['Data'].dt.month
	dataset_sp['ano'] = dataset_sp['Data'].dt.year
	dataset_sp['Tmax_ano'] = dataset_sp.groupby(['ano'])['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'].transform(max)
	dataset_sp['Tmin_ano'] = dataset_sp.groupby(['ano'])['TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)'].transform(min)									       
```	
4. Plotagem dos dados obtidos em formato de linha (para entender a diferença entre duas variáveis, como as temperaturas máximas e mínimas, assim obtendo simultaneamente os valores dessas e uma noção da amplitude térmica ano a ano) e pontos (para o entendimento da distribuição de uma determinada variável no tempo ou de sua relação com outra variável)
```python
	#2 LINHAS (TEMP MAX E MIN) AO LONGO DO TEMPO
	fig, ax = plt.subplots()
	ax = srn.lineplot(x='ano', y='Tmin_ano', data=dataset_sp, palette='blue', label='Temperatura mínima')
	ax1 = srn.lineplot(x='ano', y = 'Tmax_ano', data=dataset_sp, palette='red', label='Temperatura máxima')
	plt.xlabel('Ano')
	plt.ylabel('Temperatura (C°)')
	plt.title('Temperaturas máximas e mínimas anuais (2000-2021)')
	plt.show()
										       
	#SCATTER DA RELAÇÃO ENTRE PRECIPITAÇÃO NO ANO
	srn.scatterplot(x = 'ano', y= 'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)', data=dataset_sp, palette='green', label='Chuva', linewidth=0)
	plt.xlabel('Ano')
	plt.ylabel('Precipitação (mm)')
	plt.title('Quantidade de precipitação por dias de chuva no ano (2000 - 2021)')
	plt.show()									       
```						
										       
## Resultados	
Esse projeto foi realizado com intuito principalmente exploratório dos dados e com fins de prática para limpeza e organização dos desses. Logo, apresenta relações simples entre temperatura e chuva ao longo do ano, sem que análises mais específicas sejam realizadas. É possível verificar o aumento de temperatura e amplitude térmica ao longo do tempo, bem como da quantidade de chuva no período. Alguns exemplos de gráficos resultantes do código são apresentados a seguir
										       
<p align='center'>
	<img
	width="1280"
    	height="754"
	src="https://i.ibb.co/qMckHCC/Gr-fico-temperatura-anual.png"	
	>
</p>

<p align='center'>
	<img
	width="1280"
    	height="754"
	src="https://i.ibb.co/7Jjf9ZL/Precipita-o-por-dias-do-ano.png"	
	>
</p>

<p align='center'>
	<img
	width="1280"
    	height="754"
	src="https://i.ibb.co/r381Qts/Chuva-por-temperatura.png"	
	>
</p>

<p align='center'>
	<img
	width="1280"
    	height="754"
	src="https://i.ibb.co/g7xfR6L/Radia-o-solar-ao-longo-do-tempo.png"	
	>
</p>
