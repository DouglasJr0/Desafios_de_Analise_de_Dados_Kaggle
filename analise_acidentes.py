import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. CARREGAMENTO DOS DADOS ---
nome_do_arquivo = 'US_Accidents_March23.csv'
print("Carregando uma AMOSTRA de 1 milhão de linhas do arquivo...")
df = pd.read_csv(nome_do_arquivo, nrows=1000000)
print("Amostra carregada com sucesso!")

# --- 2. LIMPEZA DOS DADOS ---
print("\nIniciando a limpeza dos dados...")

# 1. Colunas para remover (com nomes CORRIGIDOS)
# Removemos 'Number' pois não existe na amostra e corrigimos 'Wind_Chill(F)'
colunas_para_remover = ['Wind_Chill(F)'] 
df_limpo = df.drop(columns=colunas_para_remover)

# 2. Remover linhas onde colunas importantes estão com valores faltantes (com nome CORRIGIDO)
# Corrigimos 'Wind_Speed(mph)'
colunas_importantes = ['City', 'Zipcode', 'Sunrise_Sunset', 'Weather_Condition', 'Wind_Speed(mph)']
df_limpo = df_limpo.dropna(subset=colunas_importantes)

print("Limpeza concluída com sucesso!")

# --- 3. VERIFICAÇÃO PÓS-LIMPEZA ---
print("\n--- Informações Após a Limpeza ---")
print(f"Número de linhas inicial: {df.shape[0]}")
print(f"Número de linhas restantes: {df_limpo.shape[0]}")
print("\nVerificando se ainda há valores faltantes nas colunas importantes:")
print(df_limpo[colunas_importantes].isnull().sum())

# --- 4. ANÁLISE EXPLORATÓRIA ---
print("\nIniciando a Análise Exploratória...")

# Pergunta 1: Quais são os 10 estados com mais acidentes?

# Contando o número de acidentes por estado e pegando os 10 maiores
top_10_estados = df_limpo['State'].value_counts().head(10)

print("\nTop 10 Estados com mais acidentes:")
print(top_10_estados)

# Criando o gráfico
plt.figure(figsize=(12, 6)) # Define o tamanho da imagem do gráfico
sns.barplot(x=top_10_estados.values, y=top_10_estados.index, palette='viridis')

# Adicionando título e rótulos aos eixos
plt.title('Top 10 Estados por Número de Acidentes', fontsize=16)
plt.xlabel('Número de Acidentes', fontsize=12)
plt.ylabel('Estado', fontsize=12)
plt.tight_layout() # Ajusta o gráfico para não cortar os rótulos

# Mostrando o gráfico
print("\nExibindo o gráfico de acidentes por estado...")
plt.show()

# --- 5. ANÁLISE TEMPORAL ---
print("\nIniciando a Análise Temporal...")

# Pergunta 2: Em quais dias e horários os acidentes são mais frequentes?

# Primeiro, precisamos converter a coluna 'Start_Time' para um formato de data/hora
df_limpo['Start_Time'] = pd.to_datetime(df_limpo['Start_Time'])

# Extrair a hora do dia e o dia da semana
df_limpo['Hour'] = df_limpo['Start_Time'].dt.hour
df_limpo['DayOfWeek'] = df_limpo['Start_Time'].dt.day_name()

# Organizar os dias da semana na ordem correta
dias_da_semana = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Criar uma tabela para o heatmap (contando acidentes por dia e hora)
heatmap_data = df_limpo.groupby(['DayOfWeek', 'Hour']).size().unstack()
heatmap_data = heatmap_data.loc[dias_da_semana] # Ordena as linhas

# Criando o heatmap
plt.figure(figsize=(15, 8))
sns.heatmap(heatmap_data, cmap='YlGnBu', annot=False) # annot=False para não mostrar os números

plt.title('Concentração de Acidentes por Dia da Semana e Hora', fontsize=16)
plt.xlabel('Hora do Dia', fontsize=12)
plt.ylabel('Dia da Semana', fontsize=12)
plt.tight_layout()

print("\nExibindo o heatmap de acidentes por tempo...")
plt.show()

import plotly.express as px

# --- 6. VISUALIZAÇÃO INTERATIVA ---
print("\nIniciando a criação do mapa interativo...")

# Pergunta 3: Onde ocorrem os acidentes mais graves?

# Para o mapa não ficar pesado, vamos pegar uma amostra menor dos dados
# e focar apenas nos acidentes de maior gravidade (Severity 3 e 4)
df_mapa = df_limpo[df_limpo['Severity'] >= 3].sample(15000, random_state=42)

print(f"Criando mapa com {len(df_mapa)} pontos de acidentes graves...")

# Criando o mapa interativo com plotly
fig = px.scatter_mapbox(df_mapa,
                        lat="Start_Lat",
                        lon="Start_Lng",
                        color="Severity",
                        size_max=10,
                        zoom=3,
                        mapbox_style="open-street-map",
                        title="Mapa Interativo de Acidentes Graves nos EUA")

# Mostrando o mapa
# O plotly geralmente abre o resultado em uma nova aba do seu navegador
print("\nExibindo o mapa interativo... Isso pode abrir uma nova aba no seu navegador.")
fig.show()