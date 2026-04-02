import numpy as np

matrix = np.arange(81).reshape(9,9)
print(matrix)
print(f"\n \nPrvní sloupec: {matrix[:,0]}")
print(f"\n \nPrvní řádka: {matrix[0,:]}")

print(f"\n\n Druhý blok zeshora:\n {matrix[0:3, 3:6]}")

print(np.size(matrix))
