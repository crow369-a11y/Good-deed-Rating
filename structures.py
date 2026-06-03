class Student:
    """Узел двусвязного списка. Хранит данные ученика и указатели."""
    def __init__(self, surname: str, original_index: int):
        self.surname = surname
        self.original_index = original_index
        self.rating = 0
        self.next = None
        self.prev = None


class StudentCircle:
    """Двусвязный циклический список для моделизации круга учеников."""
    def __init__(self):
        self._head = None
        self._size = 0

    @property
    def size(self) -> int:
        return self._size

    @property
    def head(self):
        return self._head

    def is_empty(self) -> bool:
        return self._size == 0

    def add_student(self, surname: str) -> None:
        """Добавляет ученика в конец круга."""
        new_node = Student(surname, self._size)
        if self._size == 0:
            self._head = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            tail = self._head.prev
            tail.next = new_node
            new_node.prev = tail
            new_node.next = self._head
            self._head.prev = new_node
        self._size += 1

    def get_all(self) -> list[Student]:
        """Возвращает список всех узлов в порядке обхода."""
        if self.is_empty():
            return []
        result = []
        current = self._head
        while True:
            result.append(current)
            current = current.next
            if current is self._head:
                break
        return result