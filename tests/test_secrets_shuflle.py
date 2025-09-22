import unittest
from unittest.mock import patch

from src.core import secrets_shuffle


class TestSecretsShuffle(unittest.IsolatedAsyncioTestCase):

    def test_empty_list(self):
        """Тест: пустой список не должен вызывать ошибок."""
        lst = []
        secrets_shuffle(lst)
        self.assertEqual(lst, [])

    def test_single_element(self):
        """Тест: список из одного элемента не изменяется."""
        lst = [42]
        secrets_shuffle(lst)
        self.assertEqual(lst, [42])

    def test_two_elements(self):
        """Тест: два элемента должны иметь шанс поменяться местами."""
        lst = [1, 2]
        # Запустим несколько раз, чтобы убедиться, что меняются
        found_swapped = False
        for _ in range(100):
            test_lst = lst.copy()
            secrets_shuffle(test_lst)
            if test_lst == [2, 1]:
                found_swapped = True
                break
        self.assertTrue(found_swapped, "Два элемента должны иногда меняться местами")

    def test_preserves_elements(self):
        """Перемешивание не теряет и не добавляет элементы."""
        original = [1, 2, 3, 4, 5]
        shuffled = original.copy()
        secrets_shuffle(shuffled)
        self.assertCountEqual(original, shuffled)  # Проверка, что элементы те же
        self.assertNotEqual(original, shuffled)

    def test_in_place_modification(self):
        """Функция изменяет список на месте."""
        lst = [1, 2, 3]
        original_id = id(lst)
        secrets_shuffle(lst)
        self.assertEqual(id(lst), original_id)

    @patch('secrets.randbelow')
    def test_uses_secrets_randbelow(self, mock_randbelow):
        """Функция использует secrets.randbelow."""
        mock_randbelow.side_effect = [1, 0, 2]  # Подделываем возврат для списка из 4 элементов
        lst = ['a', 'b', 'c', 'd']
        secrets_shuffle(lst)
        # Проверяем, что randbelow вызывался с правильными аргументами
        mock_randbelow.assert_any_call(4)  # i=3 → i+1=4
        mock_randbelow.assert_any_call(3)  # i=2 → i+1=3
        mock_randbelow.assert_any_call(2)  # i=1 → i+1=2
        self.assertEqual(mock_randbelow.call_count, 3)

    def test_deterministic_with_mocked_secrets(self):
        """При подмене randbelow можно получить детерминированное поведение."""
        with patch('secrets.randbelow', side_effect=[1, 0, 1]):
            lst = [10, 20, 30, 40]
            secrets_shuffle(lst)
            # i=3: j = 1 → swap(40, 20) → [10, 40, 30, 20]
            # i=2: j = 0 → swap(30, 10) → [30, 40, 10, 20]
            # i=1: j = 1 → swap(40, 40) → [30, 40, 10, 20]
            expected = [30, 40, 10, 20]
            self.assertEqual(lst, expected)