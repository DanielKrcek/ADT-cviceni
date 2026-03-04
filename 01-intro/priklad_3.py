#tvorba párů:

def main():
        names: list = ["Daniel", "Petr", "Adam", "Bobek", "Karel", "Bobik"]
        pary: list = []
        for i in range(0, len(names), 2):
            if (i + 1) < len(names):
                pary.append(names[i] + " - " + names[(i+1)])
        print(pary)

if __name__ == "__main__":
    main()
