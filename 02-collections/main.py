from dataclasses import dataclass
from collections import defaultdict

# Testovací data: Jméno, Osobní číslo, Předmět
# Takto vypadají data načtená například z CSV souboru nebo databáze.
raw_data = [
    ("Jan Novák", "A01N001", "Matematika"),
    ("Petr Svoboda", "A01N002", "Fyzika"),
    ("Jan Novák", "A01N001", "Fyzika"),
    ("Marie Dvořáková", "A01N003", "Informatika"),
    ("Petr Svoboda", "A01N002", "Matematika"),
    ("Jana Černá", "A01N004", "Matematika"),
    ("Karel Nový", "A01N005", "Angličtina"),
    ("Marie Dvořáková", "A01N003", "Angličtina"),
]

@dataclass(frozen=True)
class Student:
    name: str
    os_cislo: str

    def __eq__(self, other) -> bool:
        if self.name == other.name and self.os_cislo == other.os_cislo:
            return True
        return False
    

    def __hash__(self) -> int:
        return (len(self.name) * len(self.os_cislo)) % 5


def get_unique_subjects(data: list[tuple[str, str, str]]) -> set[str]:
    mnozina: set[str] = set()
    for _, _, subject in data:
        mnozina.add(subject)
    return mnozina


def group_students_by_subject(data: list[tuple[str, str, str]]) -> dict[str, list[Student]]: 
    
    """
    slovnik: dict[str, list[Student]] = {}
    for name, id, subject in data:
        st = Student(name, id)
        if subject in slovnik:
            slovnik[subject].append(st)
        else:
            slovnik[subject] = [st]
    return slovnik
    """
    
    subject_stud : dict[str, list[Student]] = {}

    for data_line in data:
        student = Student(name=data_line[0], os_cislo=data_line[1])
        if data_line[2] in subject_stud:
            subject_stud[data_line[2]].

    rozvrh: dict[str, list[Student]] = defaultdict(list)
    for name, id, subject in data:
        st = Student(name, id)
        rozvrh[subject].append(st)

    return rozvrh


def get_unique_students(data: list[tuple[str, str, str]]) -> set[Student]:
    """
    Vrátí množinu unikátních studentů.
    Pozor: Data obsahují duplicity (jeden student může mít více předmětů).
    Cílem je získat množinu fyzických osob.
    """
    studenti: set[Student] = set()
    for name, id_c, _ in data:
        stu = Student(name, id_c)
        studenti.add(stu)
    return studenti



def main() -> None:
    print("--- ÚKOL 1: Unikátní předměty ---")
    subjects = get_unique_subjects(raw_data)
    print(f"Nalezené předměty: {subjects}")

    print("\n--- ÚKOL 2: Studenti dle předmětů ---")
    by_subject = group_students_by_subject(raw_data)
    for subject, students in by_subject.items():
        print(f"{subject}: {len(students)} studentů")
        # print(f"  {students}") # Pro detailní výpis

    print("\n--- ÚKOL 3: Unikátní studenti (Množina) ---")
    unique_students = get_unique_students(raw_data)
    print(f"Počet unikátních studentů: {len(unique_students)}")
    print(unique_students)

    # Kontrola správnosti implementace __eq__ a __hash__
    # V raw_data je 8 záznamů, ale jen 5 unikátních studentů (A101, A102, A103, A104, A105)
    expected_count = 5
    if len(unique_students) == expected_count:
        print(f"\n[OK] Počet studentů odpovídá očekávání ({expected_count}).")
    else:
        print(f"\n[CHYBA] Očekáváno {expected_count} studentů, nalezeno {len(unique_students)}.")
        print("Tip: Funguje správně porovnávání instancí třídy Student v množině?")

if __name__ == "__main__":
    main()
