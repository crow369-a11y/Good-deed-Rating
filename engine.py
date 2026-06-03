import random
from structures import StudentCircle, Student


class GameEngine:
    """Управляет состоянием игры, раундами и протоколом."""
    def __init__(self):
        self._circle = StudentCircle()
        self._current: Student = None
        self._protocol: list[dict] = []

    def load_from_file(self, filepath: str) -> None:
        """Загружает фамилии из файла и инициализирует круг."""
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                name = line.strip()
                if name:
                    self._circle.add_student(name)
        if not self._circle.is_empty():
            self._current = self._circle.head

    def is_ready(self) -> bool:
        """Проверяет готовность к запуску."""
        return not self._circle.is_empty() and self._current is not None

    def play_round(self) -> dict:
        """Выполняет один раунд. Возвращает данные для протокола."""
        step = random.randint(-10, 10)
        direction = 1 if step >= 0 else -1
        moves = abs(step) % self._circle.size if self._circle.size > 0 else 0

        target = self._current
        for _ in range(moves):
            target = target.next if direction == 1 else target.prev

        target.rating += 1
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
        """Возвращает учеников, отсортированных по убыванию рейтинга."""
        return sorted(
            self._circle.get_all(),
            key=lambda s: (-s.rating, s.original_index)
        )

    def get_protocol(self) -> list[dict]:
        return self._protocol.copy()