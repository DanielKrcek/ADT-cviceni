import dataclasses
from dataclasses import dataclass

from collections import defaultdict

list = list(range(10))

"""řezání seznamů """
print(list)

print(list[2:5])
print(list[2:5])

print(list[0::2])
"""
@dataclass(frozen=True)
class Student:
    name: str
    os_cislo = str

student = Student(name="Daniel Krcek", os_cislo="AB9900")
print(hash(student))

student2 = Student(name="Daniel Krcek", os_cislo="AB9900")
print(hash(student2))
"""

slovnik : defaultdict[str, list[str]] = defaultdict(list)

slovnik["matematika"].append("martin")
slovnik["informatika"].append("Jana")
slovnik["fyzika"].append("martin")

print(slovnik)
