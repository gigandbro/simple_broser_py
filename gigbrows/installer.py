
import subprocess
import importlib

# Функция для проверки и установки зависимостей
def check_and_install_dependencies():
    required_libraries = ['PyQt6 ', 'PyQtWebEngine']

    for library in required_libraries:
        try:
            importlib.import_module(library)
        except ImportError:
            print(f"Установка зависимости {library}...")
            result = subprocess.call(['pip', 'install', library])
            if result == 0:
                print(f"{library} успешно установлен.")
            else:
                print(f"Ошибка при установке {library}.")

if __name__ == "__main__":
    check_and_install_dependencies()
    # Ваш код приложения продолжается здесь
