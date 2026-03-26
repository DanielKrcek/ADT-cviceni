from collections import deque

def main() -> None:
    print("--- Fronta (Queue) ---")
    # 1. Vytvořte prázdnou deque
    queue: deque[str] = deque()

    # 2. Přidejte prvky "A", "B", "C"
    queue.append("A")
    queue.append("B")
    queue.append("C")
    print(f"Fronta po naplnění: {queue}")

    # 3. Odeberte prvek ze začátku
    item = queue.popleft()
    print(f"Odebráno: {item}")

    # 4. Vypište zbytek
    print(f"Zbytek fronty: {queue}")

    print("\n--- Zásobník (Stack) ---")
    # 1. Vytvořte prázdnou deque
    stack: deque[int] = deque()

    # 2. Přidejte prvky 1, 2, 3
    stack.append(1)
    stack.append(2)
    stack.append(3)
    print(f"Zásobník po naplnění: {stack}")

    # 3. Odeberte prvek z konce
    item = stack.pop()
    print(f"Odebráno: {item}")

    # 4. Vypište zbytek
    print(f"Zbytek zásobníku: {stack}")

if __name__ == "__main__":
    main()
