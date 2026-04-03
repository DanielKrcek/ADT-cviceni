from collections import defaultdict
import os
import sys
from dataclasses import dataclass

@dataclass
class Record:
    time: int
    id_cust: int

def load_data(data_path: str, city: str, shop: str, day: str = "1-Mon") -> \
        dict[str, list[Record]] | None:
    """ Funkce načte data z daného souboru a vrátí je jako slovník.
    Klíčem je název checkpointu a hodnotou je list záznamů.

    Args:
        data_path (str): cesta k adresáři se všemi daty
        city (str): název města, které chceme načíst
        shop (str): název obchodu, který chceme načíst
        day (str, optional): Konkrétní den, který chceme načíst. Defaults to "1-Mon".

    Returns:
        dict[str, list[Record]] | None: slovník s načtenými daty nebo None pokud soubor neexistuje
    """

    city_data: dict[str, list[Record]] = defaultdict(list) # Použití vylepšené slovníku defaultdict
    print("loading", city)

    # Skládání cesty k souboru a přidání .txt koncovky k souboru shop_X.txt
    path = os.path.join(data_path, city, day, shop + ".txt")

    # Otevření souboru v režimu čtení - "r"
    with open(path, "r", encoding="utf-8") as file:
        try:
            _ = file.readline() # Zbavení se prvního řádku obsahující názvy sloupců v souborech
            lines = file.readlines()
            for line in lines:
                line = line.strip() # Odstranění neviditelných znaků z okrajů řetězce
                splitted = line.split(";") # Rozdělení řádku podle oddělovače -> zde středníku
                time, ckpt, cid, price = splitted
                rec = Record(int(time), int(cid)) # Vytvoření objektu Record
                city_data[ckpt].append(rec)
        except Exception as e:
            # V případě výskytu chyby v try-bloku, proběhne tento kód
            # Zde konkrétně ošetřuji všechny možné výjimky pomocí obecné Exception
            # Je možné specifikovat pouze na (ValueError, IndexError, ...)
            print(f"Something went wrong: {e}")

    return city_data

def get_passed_set(data: dict[str, list[Record]], key_words: list[str]) -> set[int]:
    """Funkce vrátí množinu zákazníků, kteří prošli alespoň jedním z checkpointů s prefixem
    předaných jako key_words. Do funkce tedy nevstupuje celé jméno checkpointu ale pouze
    jeho prefix (např. vege místo vege_1).

    Args:
        data (dict[str, list[Record]]): data načtená z datového souboru funkcí load_data
        key_words (list[str]): prefixové označení checkpointů, které chceme sledovat

    Returns:
        set[int]: Funkce vrací množinu identifikačních čísel zákazníků.
    """
    customers: set[int] = set()

    for key, value in data.items():
        norm_key = key.split("_")[0] # Chci pouze tu část checkpointu před podtržítkem
        if norm_key in key_words:
            for rec in value:
                customers.add(rec.id_cust)

    return customers

def filter_data_time(data: dict[str, list[Record]], cond_time: int) -> dict[str, list[Record]]:
    """Funkce vrátí data omezená na záznamy s časem menším nebo rovným než je cond_time.
    Args:
        data (dict[str, list[Record]]): data načtená z datového souboru funkcí load_data
        cond_time (int): časový limit v sekundách
    Returns:
        dict[str, list[Record]]: vrací data omezená na záznamy s časem menším nebo rovným cond_time.
    """
    ret: dict[str, list[Record]] = defaultdict(list)

    for ckpt, records in data.items():
        for record in records:
            if record.time <= cond_time:
                ret[ckpt].append(record)

    return ret

def get_q_size(data: dict[str, list[Record]], seconds: int) -> int:
    """Funkce vrátí velikost fronty v daném čase.
    Velikost fronty je dána počtem zákazníků, kteří prošli některým z checkpointů
    (vege, frui, meat) a ještě neprošli pokladnou.
    """
    filtered_data = filter_data_time(data, seconds)
    paid = get_passed_set(filtered_data, ["final-crs"])
    before_payment = get_passed_set(filtered_data, ["vege", "frui", "meat"])
    
    diff = len(before_payment) - len(paid) # Jeden způsob výpočtu pouze pomocí velikosti množin

    # Použití množinové operace rozdílu na získání množiny zákazníků ve frontě
    # diff_set tedy obsahuje konkrétní id zákazníků čekajících ve frontě -> získání velikosti lze pomocí len()
    diff_set = before_payment.difference(paid)

    # diff a len(diff_set) BY SE MĚLY ROVNAT!!!
    return diff

def histogram(data: dict[str, list[Record]]) -> None:
    print("-" * 20)
    print("Výpis po celých hodinách")
    for i in range(8, 21):
        q_size = get_q_size(data, i*60*60)
        print(f"{i}:00 --- {q_size}")

    print("-" * 20)
    print("Výpis po půl hodinách")

    for i in range(16, 42):
        hour = (i/2)
        q_size = get_q_size(data, hour*60*60)
        print(f"{hour} --- {q_size}")

def main(data_path: str) -> None:
    while True:
        city = input("Zadejte město (Plzeň): ")
        shop = input("Zadejte obchod (shop_a): ")

        if city == "":
            city = "Plzeň"
        if shop == "":
            shop = "shop_a"

        data = load_data(data_path, city, shop)


        in_cust_set = get_passed_set(data, ["gate-keeper"])
        in_cust = len(in_cust_set) # Použití len() abych získal pouze velikost množiny zákazníků
        print(f"Počet zákazníků, kteří přišli do obchodu za celý den: {in_cust}")

        out_cust = len(get_passed_set(data, ["final-crs"])) # Stejné jako in_cust, akorát kratší zápis
        print(f"Počet zákazníků, kteří odešli z obchodu za celý den: {out_cust}")

        # Velikost fronty v 15 hodin
        q_size = get_q_size(data, 15*60*60)


        if data is None:
            continue

        histogram(data)

if __name__ == "__main__":
    print(sys.argv) # Kontrolní výpis systémových argumentů
    if len(sys.argv) < 2:
        print("Usage: python main.py <data_path>")
        sys.exit(1)
    main(sys.argv[1])

