import linecache
import random

from .decorators import log_errors
from .decorators import handle_file_errors

@handle_file_errors
@log_errors
def words_count(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        total_lines = sum(1 for _ in f)
    return total_lines

@handle_file_errors
@log_errors
def best_score(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            best_score = int(f.readline().strip())
    except Exception:
        best_score = 0
    return best_score
    
@handle_file_errors
@log_errors
def write_best_score(filename, score):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(str(score))

@handle_file_errors
@log_errors
def random_word_generator(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        total_lines = sum(1 for _ in f)
    
    cache = set()
    while len(cache) < total_lines:
        random_line = random.randint(1, total_lines)
        if random_line in cache:
            continue
        
        yield linecache.getline(filename, random_line).strip().replace("\n", "")
        cache.add(random_line)