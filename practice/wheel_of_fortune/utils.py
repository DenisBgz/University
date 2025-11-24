
def input_difficulty():
    lives = {
        "легкий": 7,
        "средний": 5,
        "сложный": 3
    }
    
    while True:
        difficulty = input("Введите уровень сложности (легкий, средний, сложный): ").strip().lower()
        
        if difficulty in ["легкий", "средний", "сложный"]:
            return lives[difficulty]
        print("Неверный ввод. Пожалуйста, выберите допустимый уровень сложности.")
        

def input_word_or_letter():
    while True:
        word = input("Введите слово или букву: ").strip().lower()
        if word.isalpha():
            return word
        print("Неверный ввод. Пожалуйста, введите слово без пробелов и символов.")


def input_yes_no():
    while True:
        answer = input("Введите 'да' или 'нет': ").strip().lower()
        if answer in ["да", "нет"]:
            return answer == "да"
        print("Неверный ввод. Пожалуйста, введите 'да' или 'нет'.")
