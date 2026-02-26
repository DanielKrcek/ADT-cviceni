"Cílem je odstranit z listu všechna čísla menší než 50. "

scores = [50, 80, 45, 90, 30, 60]
for i in range(len(scores)-1):
    if scores[i] < 50:
        scores.pop(i)
print(scores)

