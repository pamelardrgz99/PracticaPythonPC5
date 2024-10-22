import pandas as pd

# Cargar el conjunto de datos desde el archivo CSV
wine_data = pd.read_csv("./data/winemag-data-130k-v2.csv")

# Exploración inicial del DataFrame
print(wine_data.head())
print(wine_data.info())
print(wine_data.describe())

# Renombrar columnas
wine_data.rename(columns={
    'points': 'puntos',
    'price': 'costo',
    'country': 'pais',
    'variety': 'tipo'
}, inplace=True)

# Creación de nuevas columnas

wine_data['description_length'] = wine_data['description'].apply(len)

wine_data['price_category'] = pd.cut(wine_data['costo'], bins=[0, 20, 50, 100, 5000], labels=['Bajo', 'Medio', 'Alto', 'Muy Alto'])


# Descargar el archivo de países y continentes
countries_url = 'https://gist.githubusercontent.com/kintero/7d1db891401f56256c79/raw/a61f6d0dda82c3f04d2e6e76c3870552ef6cf0c6/paises.csv'
countries_continents = pd.read_csv(countries_url)

# Crear un diccionario para el mapeo de país a continente
continent_map = dict(zip(countries_continents['nombre'], countries_continents['continente']))

#Etiquetar según continente
wine_data['continent'] = wine_data['pais'].map(continent_map)

#Clasificación por puntuación
wine_data['score_category'] = pd.cut(wine_data['puntos'], bins=[0, 85, 90, 95, 100], labels=['Promedio', 'Bien', 'Muy bien', 'Excelente'])

# Reporte 1: Promedio de precio y cantidad de reviews por país
report1 = wine_data.groupby('pais').agg({'costo': 'mean', 'puntos': 'count'}).sort_values(by='costo', ascending=False)

# Reporte 2: Mejor vino por continente
report2 = wine_data.loc[wine_data.groupby('continent')['puntos'].idxmax()]

# Reporte 3: Número de vinos por tipo y categoría de precio
report3 = wine_data.groupby(['tipo', 'price_category']).size().unstack(fill_value=0)

# Reporte 4: Promedio de longitud de descripción y puntuación por país
report4 = wine_data.groupby('pais').agg({'description_length': 'mean', 'puntos': 'mean'}).sort_values(by='description_length', ascending=False)

# Exportar los reportes a diferentes formatos
report1.to_csv('report1.csv')
report2.to_excel('report2.xlsx', index=False)
report3.to_sql('report3', 'sqlite:///wine_reports.db', if_exists='replace')
report4.to_json('report4.json')

# Mostrar el primer reporte
print(report1.head())
