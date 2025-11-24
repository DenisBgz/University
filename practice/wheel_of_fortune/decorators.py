import time
import logging
import sys

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
    
        return (result, elapsed_time)
    return wrapper

def log_errors(func):
   

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"[{func.__name__}: {e}")
            raise
    return wrapper
    
    
def handle_file_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            print(f"Файл {e.filename} не найден")
            sys.exit(1)
        except Exception as e:
            print(f"Произошла ошибка при работе с файлом: {e}")
            sys.exit(1)
    return wrapper
