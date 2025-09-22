# password_generator
Утилита для генерации устойчивых  к перебору паролей

# Запуск тестов
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r req.txt
python test.py
```
# Проверка типов
```bash
mypy src/ tests/
```
# Запуск линтера
```bash
pylint src/ tests/ test.py
```