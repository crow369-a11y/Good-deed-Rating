from typing import Optional
from structures import StudentCircle, Student

class CustomRandom:
    def __init__(self, seed: Optional[int] = None):
        self.state = seed if seed is not None else 123456789 

    def randint(self, a: int, b: int) -> int:
        m = 2**31
        a_mult = 1103515245
        c = 12345
        
        self.state = (a_mult * self.state + c) % m
        range_size = b - a + 1
        return a + (self.state % range_size)


class GameEngine:
    def __init__(self):
        self._circle = StudentCircle()
        self._current: Optional[Student] = None
        self._protocol: list[dict] = []
        self._rng = CustomRandom()

    def load_from_file(self, filepath: str) -> None:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    name = line.strip()
                    if name:
                        self._circle.add_student(name)
            
            if not self._circle.is_empty():
                self._current = self._circle.head
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл '{filepath}' не найден.")
        except PermissionError:
            raise PermissionError(f"Нет прав на чтение файла '{filepath}'.")
        except UnicodeDecodeError:
            raise ValueError(f"Ошибка кодировки файла '{filepath}'. Используйте UTF-8.")

    def is_ready(self) -> bool:
        return not self._circle.is_empty() and self._current is not None

    def play_round(self) -> dict:
        step = self._rng.randint(-10, 10)
        direction = 1 if step >= 0 else -1
        moves = abs(step) % self._circle.size if self._circle.size > 0 else 0

        target = self._current
        for _ in range(moves):
            target = target.next if direction == 1 else target.prev
        target.rating += 1
        # Согласно заданию: следующий отсчет начинается с соседа 
        # текущего ученика в направлении движения (target.next или target.prev)
        self._current = target.next if direction == 1 else target.prev

        round_data = {
            'step': step,
            'direction': 'по часовой' if direction == 1 else 'против часовой',
            'student': target.surname,
            'rating': target.rating
        }
        self._protocol.append(round_data)
        return round_data

    def get_sorted_results(self) -> list[Student]:
        return sorted(
            self._circle.get_all(),
            key=lambda s: (-s.rating, s.original_index)
        )

    def get_protocol(self) -> list[dict]:
        return self._protocol.copy()