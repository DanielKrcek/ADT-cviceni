import random
from collections import deque
from dataclasses import dataclass


@dataclass
class Worker:
    name: str
    source: deque
    dest: deque
    period: int
    spread_factor: float = 0.0
    timer: int = 0


def get_delay(period: int, spread_factor: float) -> int:
    return int(random.gauss(period, period * spread_factor))



def worker_tick(worker: Worker) -> None:
    if worker.timer > 0:
        worker.timer -= 1
    elif len(worker.source) > 0:
        clovek = worker.source.popleft() # Vyjmutí zákazníka zezačátku fronty
        worker.dest.append(clovek) # Poslání tohoto zákazníka dál
        worker.timer = get_delay(worker.period, worker.spread_factor)#"Uspání" workeru po obsloužení zákazníka  
        print(f"{worker.name} právě obsloužil zákazníka, dalšího zvládne za:{worker.timer} sekund.")

def print_snapshot(time: int, queues: list[tuple[str, deque]]) -> None:  # noqa: ARG001
    for name, q in queues:
        print(f"{name}: ({len(q)}) lidí")

def main() -> None:
    people_number = 1000
    people_in_the_city = deque(list(range(people_number)))

    # 1. Vytvoření front
    gate_q: deque[int] = deque()
    vege_q: deque[int] = deque()
    cash_q: deque[int] = deque()
    final_q: deque[int] = deque()

    # Seznam pro výpis (jméno, fronta)
    queues_to_observe: list[tuple[str, deque]] = [
        ("Street", people_in_the_city),
        ("Gate", gate_q),
        ("Vege", vege_q),
        ("Cashier", cash_q), 
        ("Final", final_q)]

    # Parametry simulace (střední hodnoty časů v sekundách)
    day_m = 30  # Každých 30s přijde někdo z ulice
    gate_m = 15  # Gate keeper každého odbavuje 5s
    vege_m = 45  # Vážení zeleniny trvá 45s
    final_m = 2 * 60  # Pokladna zabere 2 minuty

    # 2. Vytvoření pracovníků (Worker)
    # Worker(jméno, zdroj, cíl, perioda, spread_factor)
    street_worker = Worker("StreetWorker", people_in_the_city, gate_q, day_m, 0.5)
    gate_worker = Worker("GateWorker", gate_q, vege_q, gate_m, 0.2)
    vege_worker = Worker("VegeWorker", vege_q, cash_q, vege_m, 0.2)
    cash_worker = Worker("CashWorker", cash_q, final_q, final_m, 0.1)

    # 3. Hlavní smyčka simulace
    i = 1
    while i <= 7200:
        for worker in [street_worker, gate_worker, vege_worker, cash_worker]:
            worker_tick(worker)
        if i % 60 == 0:# Každých 60 vteřin zavoláme výpis
            print_snapshot(0, queues_to_observe)
        i +=1


if __name__ == "__main__":
    main()
