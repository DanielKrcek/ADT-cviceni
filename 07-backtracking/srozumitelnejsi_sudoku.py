import numpy as np
class SudokuSolver:
    def __init__(self):
        self.field = np.zeros([9, 9], dtype=int)

    def load(self, file_path:str) -> None:
        with open(file_path, "r", encoding="UTF-8") as f:
            loaded_rows: list [list[int]] = []
            lines = f.readlines()
            for line in lines:
                new_line = line.strip().split(";")
                numbers: list[int] = []
                for num in new_line:
                    number = int(num)
                    numbers.append(number)
                loaded_rows.append(numbers)
        self.field = np.array(loaded_rows)

    def check_sequence(self, sequence: np.ndarray) -> bool:
        # Kontroluje zda v dodané sekvenci se nachází duplicity
        # Nula se jako duplicita nepočítá, protože značí prázdnou buňku
        # True === OK
        # False === Not OK

        mnozina: set[int] = set()
        for i in sequence:
            if i == 0:
                continue
            if i not in mnozina:
                mnozina.add(i)
                continue
            return False
        return True

    def check_row(self, row_index: int) -> bool:
    # pomoci řezu matice dodá ke kontrole celý řádek
        row_data = self.field[row_index, :]
        if self.check_sequence(row_data):  # noqa: SIM103
            return True
        return False

    def check_column(self, col_index: int) -> bool:
        # pomoci řezu matice dodá ke kontrole celý sloupec
        col_data = self.field[:, col_index]
        return self.check_sequence(col_data)

    def check_block(self, row_index: int, col_index: int) -> bool:
    # zjištění do kterého bloku daná buňka patří
        row_start = (row_index // 3) * 3
        col_start = (col_index // 3) * 3

    # získání daného bloku (podmatice) dat
        podmatice = self.field[row_start: row_start + 3, col_start : col_start + 3]
    
    # zploštění podmatice (3x3) na pole (9x1)
    # tvar můžete zjistit pomocí .shape
        zplostela_podm = podmatice.reshape(-1)
        return self.check_sequence(zplostela_podm)
    
    def check_one_cell(self, row_index: int, col_index: int) -> bool:
        row = self.check_row(row_index)
        col = self.check_column(col_index)
        block = self.check_block(row_index, col_index)

         # Metoda vrátí True pouze pokud všechny 3 pravdla sudoku jsou splněna
        return row and col and block 
    
    def get_empty_cell(self) -> tuple[int, int] | None:
        """ Gets the coordinates of the next empty field. """
        for r in range(self.field.shape[0]):
            for c in range(self.field.shape[1]):
                if self.field[r, c] == 0:
                    return r, c
        return None
    
    def solve(self) -> bool:
        """Recursively solves the sudoku"""

        # Zastavovací podmínka
        next_cell = self.get_empty_cell()
        if next_cell == None:
            return True
        
        row, col = next_cell
        
        for num in range(1, 10):
            self.field[row, col] = num # Zkoušení různých kandidátů
            is_valid = self.check_one_cell(row, col)# Je kandidát validní?
            if not is_valid:
                continue # Pokud není, tak skočím na dalšího kandidáta
                         # a ani nebudu zkoušet doplňovat jiné prázdné buňky (spuštěním další úrovně zanoření = rekurze)
            solved = self.solve()

            # Aktuální kandidát je zatím dobrý, zkusím s ním pokračovat dál
            # a doplnit ostatní prázdné buňky
            if solved:      
            # Podařilo se to vyřešit -> chci se postupně vynořit z rekurze a nic dalšího nedělat
                return True
            
        self.field[row, col] = 0
        return False
        # Sem se dostanu, pouze pokud další zanoření byly neúspěšné 
        # a to znamená, že jsem v úplně slepé uličce -> chci tedy vynulovat co jsem vyplnit a vynořit se     
        

def main() -> None:
    sudoku_solver = SudokuSolver()
    sudoku_solver.load("07-backtracking/sudoku.csv")
    sudoku_solver.solve()
    print(sudoku_solver.field)
if __name__ == "__main__":
    main()
