import sys
from engine import GameEngine


class GameApp:
    """Консольный интерфейс приложения. Реализует циклическое меню и взаимодействие с пользователем."""
    def __init__(self):
        self.engine = GameEngine()

    def _get_valid_int(self, prompt: str, min_val: int = None, max_val: int = None) -> int:
        """Безопасный ввод целого числа с проверкой диапазона."""
        while True:
            try:
                val = int(input(prompt).strip())
                if min_val is not None and val < min_val:
                    print(f"Значение должно быть ≥ {min_val}.")
                    continue
                if max_val is not None and val > max_val:
                    print(f"Значение должно быть ≤ {max_val}.")
                    continue
                return val
            except ValueError:
                print("Ошибка: введите корректное целое число.")

    def run(self) -> None:
        """Главный циклический цикл приложения."""
        print("Игра «Добрые дела» | Языки программирования")
        while True:
            self._print_menu()
            choice = input("\n▶ Ваш выбор (1-5): ").strip()
            if choice == '1':
                self._cmd_load()
            elif choice == '2':
                self._cmd_create_file()
            elif choice == '3':
                self._cmd_play()
            elif choice == '4':
                self._cmd_results()
            elif choice == '5':
                print("Завершение работы. Спасибо за использование!")
                sys.exit(0)
            else:
                print("Неверный пункт. Выберите число от 1 до 5.")

    def _print_menu(self) -> None:
        """Вывод главного меню."""
        print("\n" + "="*35)
        print("              ГЛАВНОЕ МЕНЮ")
        print("1. Загрузить существующий файл")
        print("2. Создать новый файл с учениками")
        print("3. Начать игру")
        print("4. Показать итоговый рейтинг")
        print("5. Выход")
        print("="*35)

    def _cmd_load(self) -> None:
        """Загрузка списка из существующего файла."""
        path = input("Путь к файлу с фамилиями: ").strip()
        try:
            self.engine.load_from_file(path)
            print(f"Успешно загружено учеников: {self.engine._circle.size}")
        except FileNotFoundError:
            print("Ошибка: файл не найден. Проверьте путь.")
        except Exception as e:
            print(f"Ошибка чтения: {e}")

    def _cmd_create_file(self) -> None:
        """Создание нового текстового файла со списком учеников."""
        print("\nСоздание нового списка учеников")
        filename = input("Введите имя файла (например, class9a.txt): ").strip()
        if not filename:
            print("Имя файла не может быть пустым.")
            return
        if not filename.endswith('.txt'):
            filename += '.txt'

        try:
            count = self._get_valid_int("Введите количество учеников: ", min_val=1, max_val=500)
            with open(filename, 'w', encoding='utf-8') as f:
                for i in range(1, count + 1):
                    while True:
                        surname = input(f"Введите фамилию ученика {i}: ").strip()
                        if surname:
                            break
                        print("Фамилия не может быть пустой. Повторите ввод.")
                    f.write(surname + '\n')
            print(f"\nФайл '{filename}' успешно создан.")
            auto_load = input("Загрузить его в игру сразу? (y/n): ").strip().lower()
            if auto_load == 'y':
                self.engine.load_from_file(filename)
                print(f"Загружено учеников: {self.engine._circle.size}")
        except PermissionError:
            print("Ошибка: нет прав на запись в указанную директорию.")
        except Exception as e:
            print(f"Ошибка при создании файла: {e}")

    def _cmd_play(self) -> None:
        """Запуск игрового цикла."""
        if not self.engine.is_ready():
            print("Сначала загрузите или создайте список учеников (пункты 1 или 2).")
            return
        rounds = self._get_valid_int("Количество раундов: ", min_val=1)
        print("\nПРОТОКОЛ ИГРЫ")
        print(f"{'#':<4} | {'Число':<6} | {'Направление':<14} | {'Ученик':<15} | {'Рейтинг'}")
        print("-" * 62)
        for i in range(1, rounds + 1):
            res = self.engine.play_round()
            print(f"{i:<4} | {res['step']:<6} | {res['direction']:<14} | {res['student']:<15} | {res['rating']}")
        print("Игра завершена.")

    def _cmd_results(self) -> None:
        """Вывод отсортированного рейтинга."""
        if not self.engine.is_ready():
            print("Список пуст. Загрузите или создайте данные.")
            return
        sorted_list = self.engine.get_sorted_results()
        print("\nИТОГОВЫЙ РЕЙТИНГ")
        print(f"{'Место':<6} | {'Фамилия':<20} | {'Рейтинг'}")
        print("-" * 35)
        for i, st in enumerate(sorted_list, 1):
            print(f"{i:<6} | {st.surname:<20} | {st.rating}")


if __name__ == "__main__":
    app = GameApp()
    app.run()