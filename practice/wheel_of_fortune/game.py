import logging
from .decorators import timer
from .file_handler import random_word_generator, words_count
from .utils import input_word_or_letter
from .utils import input_difficulty
from .utils import input_yes_no
from .file_handler import best_score
from .file_handler import write_best_score

logging.basicConfig(filename='wheel_of_fortune/game.log', level=logging.INFO)


logger = logging


class Word:
    __slots__ = ('word', '_guessed_letters')

    def __init__(self, word):
        self.word = word
        self._guessed_letters = set()

    def is_guessed(self):
        return len(self._guessed_letters) == len(set(self.word))

    def guess(self, letter):
        if letter in self.word:
            self._guessed_letters.add(letter)
            return True
        return False

    def display(self):
        return ''.join(letter if letter in self._guessed_letters else '_' for letter in self.word)


class Stats:
    __slots__ = ('_total_words', '_guessed_words', '_time_played', '_best_score')

    def __init__(self):
        self._total_words = 0
        self._guessed_words = 0
        self._time_played = 0
        self._best_score = best_score('data/record.txt')

    def update(self, guessed):
        logger.info(f'Update stats: guessed "{guessed}"')
        self._guessed_words += 1
        if self._guessed_words > self._best_score:
            self._best_score = self._guessed_words
            write_best_score('data/record.txt', self._best_score)

    def set_total_words(self, words):
        self._total_words = words

    def set_time_played(self, time):
        self._time_played = time

    def display_results(self):
        print("Ваши результаты:")
        print(f"Всего слов: {self._total_words}")
        print(f"Угадано слов: {self._guessed_words} 🏅")
        print(f"Лучший рекорд: {self._best_score}")
        print(f"Время игры: {self._time_played // 60:.00f} минут {self._time_played % 60:.00f} секунд")


class Game:
    __slots__ = ('_lives', '_stats')

    def __init__(self):
        self._lives = 0
        self._stats = Stats()

    def decrease_lives(self):
        self._lives -= 1
        logger.info(f'Decreased lives: {self._lives}')
        return not self._lives

    def start(self):
        logger.info('Game started')
        print("🎉 Добро пожаловать в Поле Чудес! 🎉")

        while True:
            time = self.play()[1]
            self._stats.set_time_played(time)
            self._stats.display_results()

            print("")

            if not self.end_message():
                logger.info('Game ended by user')
                break

    @timer
    def play(self):
        self._lives = input_difficulty()
        logger.info(f'Set lives: {self._lives}')
        return self.game_loop()

    def end_message(self):
        print("Хотите сыграть еще?")
        return input_yes_no()

    def game_loop(self):
        current_word = 1
        count = words_count("data/words.txt")
        self._stats.set_total_words(count)

        for word in random_word_generator("data/words.txt"):
            word = Word(word)

            while True:
                print(f"Слово №{current_word} из {count}: {word.display()}")
                print(f"Осталось жизней: {self._lives}")
                print()

                guess = input_word_or_letter()
                logger.info(f'User guessed: "{guess}"')

                if guess == word.word:
                    logger.info(f'Guessed the word: "{word.word}"')
                    print("Загаданное слово:", word.word)
                    print("Вы угадали слово!")
                    self._stats.update(guess)
                    current_word += 1
                    break
                elif len(guess) == 1 and word.guess(guess):
                    if word.is_guessed():
                        logger.info(f'Guessed the word: "{word.word}"')
                        print("Загаданное слово:", word.word)
                        print("Вы угадали слово!")
                        self._stats.update(guess)
                        current_word += 1
                        break
                    logger.info(f'Guessed a letter: "{guess}"')
                    print("Вы угадали букву!")
                    continue
                else:
                    logger.warning(f'Failed to guess: "{guess}"')
                    print("Не угадали!")
                    
                    if len(guess) > 1:
                        logger.info('User lost the game')
                        print("Вы проиграли!")
                        print("Загаданное слово было:", word.word)
                        print()
                        print()
                        return

                if self.decrease_lives():
                    logger.info('User lost the game')
                    print("Вы проиграли!")
                    print("Загаданное слово было:", word.word)
                    print()
                    print()
                    return

            print()
            print()

        logger.info('User completed the game')
        print("🎊 ПОЗДРАВЛЯЕМ! 🎊")
        print(f"Вы прошли всю игру и угадали все {count} слов!")
        print("Вы настоящий ПОБЕДИТЕЛЬ игры \"Поле чудес\"! 🏆")
