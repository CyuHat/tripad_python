# Importing all the functions I created
from functions import *

# Get all the main links for the collection (nt complete)
all_links = get_all_links("palermo")

print("\nGet all the main links needed for the collection (not complete)\n")

for i in all_links:
	print(i)

# ATTENTION!!! 
# La sélection des liens pour les 4 type est une mauvaise idée
# preuve: https://www.tripadvisor.com/Tourism-g60763-New_York_City_New_York-Vacations.html
# Se baser plutôt sur le contenu du href

# Pour tourner les page il y a un oa0 pour toutes les pages (30 résultats par pages)
# Exemple: https://www.tripadvisor.com/Attractions-g60763-Activities-oa0-New_York_City_New_York.html
# S'il n'y en a pas, l'ajouter manuellement

iterable_list = list(all_links[i] for i in [0,1,2,3,5])

iterable_list

iterable_list[4].replace("a0", "a30", 1)

test = iterable_list

max_list = [5,5,5,5,5]
