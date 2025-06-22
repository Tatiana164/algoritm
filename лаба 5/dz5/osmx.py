import osmnx as ox

# Скачиваем граф по названию города
G = ox.graph_from_place('Белград, Сербия', network_type='drive')
# Сохраняем в файл для последующего использования
ox.save_graphml(G, 'belgrad_serbia.graphml')
