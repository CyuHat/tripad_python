# Importing all the functions I created
from new_code.functions import *

# Get all the main links for the collection (nt complete)
all_links = get_all_links("palermo")

print("\nGet all the main links needed for the collection (not complete)\n")

for i in all_links:
	print(i)