import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

nome_do_arquivo = 'US_Accidents_March23.csv'
print("Carregando uma AMOSTRA de 1 milhão de linhas do arquivo...")
df = pd.read_csv(nome_do_arquivo, nrows=1000000)
print("Amostra carregada com sucesso!")
print("\nIniciando a limpeza dos dados...")

colunas_para_remover = ['Wind_Chill(F)'] 
df_limpo = df.drop(columns=colunas_para_remover)

colunas_importantes = ['City', 'Zipcode', 'Sunrise_Sunset', 'Weather_Condition', 'Wind_Speed(mph)']
df_limpo = df_limpo.dropna(subset=colunas_importantes)

print("Limpeza concluída com sucesso!")

print("\n--- Informações Após a Limpeza ---")
print(f"Número de linhas inicial: {df.shape[0]}")
print(f"Número de linhas restantes: {df_limpo.shape[0]}")
print("\nVerificando se ainda há valores faltantes nas colunas importantes:")
print(df_limpo[colunas_importantes].isnull().sum())

print("\nIniciando a Análise Exploratória...")
top_10_estados = df_limpo['State'].value_counts().head(10)

print("\nTop 10 Estados com mais acidentes:")
print(top_10_estados)

plt.figure(figsize=(12, 6))
sns.barplot(x=top_10_estados.values, y=top_10_estados.index, palette='viridis')

plt.title('Top 10 Estados por Número de Acidentes', fontsize=16)
plt.xlabel('Número de Acidentes', fontsize=12)
plt.ylabel('Estado', fontsize=12)
plt.tight_layout() 
print("\nExibindo o gráfico de acidentes por estado...")
plt.show()

print("\nIniciando a Análise Temporal...")

df_limpo['Start_Time'] = pd.to_datetime(df_limpo['Start_Time'])
df_limpo['Hour'] = df_limpo['Start_Time'].dt.hour
df_limpo['DayOfWeek'] = df_limpo['Start_Time'].dt.day_name()

dias_da_semana = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

heatmap_data = df_limpo.groupby(['DayOfWeek', 'Hour']).size().unstack()
heatmap_data = heatmap_data.loc[dias_da_semana] # Ordena as linhas

# Criando o heatmap
plt.figure(figsize=(15, 8))
sns.heatmap(heatmap_data, cmap='YlGnBu', annot=False)

plt.title('Concentração de Acidentes por Dia da Semana e Hora', fontsize=16)
plt.xlabel('Hora do Dia', fontsize=12)
plt.ylabel('Dia da Semana', fontsize=12)
plt.tight_layout()

print("\nExibindo o heatmap de acidentes por tempo...")
plt.show()

import plotly.express as px

print("\nIniciando a criação do mapa interativo...")

df_mapa = df_limpo[df_limpo['Severity'] >= 3].sample(15000, random_state=42)

print(f"Criando mapa com {len(df_mapa)} pontos de acidentes graves...")

fig = px.scatter_mapbox(df_mapa,
                        lat="Start_Lat",
                        lon="Start_Lng",
                        color="Severity",
                        size_max=10,
                        zoom=3,
                        mapbox_style="open-street-map",
                        title="Mapa Interativo de Acidentes Graves nos EUA")

# Mostrando o mapa
print("\nExibindo o mapa interativo... Isso pode abrir uma nova aba no seu navegador.")
fig.show()