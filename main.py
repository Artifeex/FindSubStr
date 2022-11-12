import random
import string
import time
import numpy as np
import matplotlib.pyplot as plt


def naive_string_matcher(text, pattern):
    len_pattern = len(pattern)
    len_text = len(text)
    result = [0] * len_text
    # всевозможные позиции начала нашей рамки
    for i in range(0, len_text - len_pattern + 1):
        s = 0
        # сравнение подстроки, которую ищем и текста внутри рамки со смещением i
        while s < len_pattern and text[i + s] == pattern[s]:
            s += 1
        # полное совпадение, значит, внутри рассматриваемой рамки оказался искомый паттерн
        if s == len_pattern:
            result[i + len_pattern - 1] = len_pattern
        else:
            result[i + len_pattern - 1] = 0
    return result


def KMP(pattern):
    # всегда 0
    pattern_length = len(pattern)
    result = [0] * pattern_length
    # инициалиация счетчиков
    i = 1
    j = 0
    # пока не закончился паттерн
    while i < pattern_length:
        # если совпало, значит, нашли совпадающий суффикс и префикс, увеличиваем счетчики и записываем полученное значение
        # в функцию-откатов
        if pattern[i] == pattern[j]:
            result[i] = j + 1
            i += 1
            j += 1
        # совпадения не было, при этом, до этого совпадений так же не было, так как j = 0
        elif j == 0:
            result[i] = 0
            i += 1
        else:
            j = result[j - 1] # берем длину меньшего префикс-суффикса
    return result


def SFT_KMP(text, pattern):
    i = 0 # индекс по тексту
    l = 0 # индекс внутри шаблона
    len_text = len(text)
    len_pattern = len(pattern)
    f_pattern = KMP(pattern)
    result = [0] * len_text
    while i < len_text:
        if text[i] == pattern[l]:
            i += 1
            l += 1
            # нашли в тексте шаблон
            if l == len_pattern:
                result[i-1] = len_pattern
                l = 0
        # дошли до момента, когда нужно начать проверять шаблон с самого начала
        elif l == 0:
            i += 1
        else:
            l = f_pattern[l - 1]
    return result


def gen_normal_word(len_word, valid_letters):
    result = ''
    for i in range(len_word):
        result += valid_letters[random.randint(0, len(valid_letters) - 1)]
    return result


def gen_repeated(k, word):
    result = ''
    for i in range(k):
        result += word
    return result


def first_experiment():
    experiment_range = 101
    k_array = np.array(list(range(1, experiment_range, 10)))
    T1_array = np.empty(experiment_range // 10)
    T2_array = np.empty(experiment_range // 10)
    i = 0
    for k in range(1, experiment_range, 10):
        print(k)
        text = 'ab' * 1000 * k
        pattern = 'ab'* k
        start_time = time.time_ns()
        naive_string_matcher(text, pattern)
        end_time = time.time_ns()
        T1_array[i] = end_time - start_time
        start_time = time.time_ns()
        SFT_KMP(text, pattern)
        end_time = time.time_ns()
        T2_array[i] = end_time - start_time
        i += 1
    plt.plot(k_array, T1_array, label=r'$T_1(k) - Наивный$')
    plt.plot(k_array, T2_array, label=r'$T_2(k) - KMP$')
    plt.xlabel(r'$k$', fontsize=14)
    plt.ylabel(r'$T(k)$', fontsize=14)
    plt.legend(loc='best', fontsize=12)
    plt.show()


def second_experiment():
    m_array = np.array(list(range(1, 10**5 * 4, 10**4)))
    T1_array = np.array(list(range(1, 10**5 * 4, 10**4)))
    T2_array = np.array(list(range(1, 10**5 * 4, 10**4)))
    alphabet = 'ab'
    i = 0
    text = gen_normal_word(10**5 * 4, alphabet)
    for m in range(1, 10**5 * 4, 10**4):
        pattern = 'a' * m
        print(m)
        start_time = time.time_ns()
        naive_string_matcher(text, pattern)
        end_time = time.time_ns()
        T1_array[i] = (end_time - start_time)
        start_time = time.time_ns()
        SFT_KMP(text, pattern)
        end_time = time.time_ns()
        T2_array[i] = (end_time - start_time)
        i += 1
    plt.plot(m_array, T1_array, label=r'$T_1(m) - Наивный$')
    plt.plot(m_array, T2_array, label=r'$T_2(m) - KMP$')
    plt.xlabel(r'$m$', fontsize=14)
    plt.ylabel(r'$T(m)$', fontsize=14)
    plt.legend(loc='best', fontsize=12)
    plt.show()


def third_experiment():
    pattern = 'aaaaa'
    h_array = np.array(list(range(1, 10**5 * 3, 10**4)))
    T1_array = np.array(list(range(1, 10**5 * 3, 10**4)))
    T2_array = np.array(list(range(1, 10**5 * 3, 10**4)))
    i = 0
    for h in range(1, 10**5 * 3, 10**4):
        print(h)
        text = 'aaaaab' * h
        start_time = time.time_ns()
        naive_string_matcher(text, pattern)
        end_time = time.time_ns()
        T1_array[i] = (end_time - start_time)
        start_time = time.time_ns()
        SFT_KMP(text, pattern)
        end_time = time.time_ns()
        T2_array[i] = (end_time - start_time)
        i += 1
    plt.plot(h_array, T1_array, label=r'$T_1(h) - Наивный$')
    plt.plot(h_array, T2_array, label=r'$T_2(h) - KMP$')
    plt.xlabel(r'$h$', fontsize=14)
    plt.ylabel(r'$T(h)$', fontsize=14)
    plt.legend(loc='best', fontsize=12)
    plt.show()


def print_main_menu():
    print('Главное меню')
    print('1) Задать размер алфавита и сам алфавит')
    print('2) Задать текст')
    print('3) Задать шаблон для поиска')
    print('4) Сгенерировать текст с помощью')
    print('5) Сгенерировать шаблон')
    print('6) Сгенерировать повторяющийся текст')
    print('7) Сгенерировать повторяющийся шаблон')
    print('8) Исполнить алгоритм для заданных слов')
    print('9) Вывести текст и шаблон поиска')
    print('0) К экспериментам')


def main():
    T1 = 0
    T2 = 0
    count_letters = 0
    alphabet = string.ascii_lowercase
    text = ''
    pattern = ''
    print_main_menu()
    while True:
        choice = int(input('Ваш выбор:'))
        if choice == 1:
            count_letters = int(input('Введите число букв в алфавите: '))
            alphabet = input('Введите символы алфавита: ')
        elif choice == 2:
            text = input('Введите текст: ')
            print('Текст {} успешно сформирован'.format(text))
        elif choice == 3:
            pattern = input('Введите шаблон: ')
            print('Шаблон {} успешно сформирован'.format(pattern))
        elif choice == 4:
            len_word = int(input('Введите длину слова'))
            valid_letters = input('Введите допустимые буквы алфавита: ')
            text = gen_normal_word(len_word, valid_letters)
            print('Текст успешно сгенерирован')
        elif choice == 5:
            len_word = int(input('Введите длину шаблона'))
            valid_letters = input('Введите допустимые буквы алфавита: ')
            pattern = gen_normal_word(len_word, valid_letters)
            print('Шаблон успешно сгенерирован')
        elif choice == 6:
            word = input('Введите слово')
            k = int(input('Введите число повторений слова {} '.format(word)))
            text = gen_repeated(k, word)
            print('Повторяющийся текст успешно сгенерирован')
        elif choice == 7:
            word = input('Введите шаблон для поиска')
            k = int(input('Введите число повторений шаблона {} '.format(word)))
            pattern = gen_repeated(k, word)
            print('Повторяющийся шаблон успешно сгенерирован')
        elif choice == 8:
            start_time = time.time_ns()
            naive_string_matcher(text, pattern)
            end_time = time.time_ns()
            T1 = end_time - start_time
            print('Время работы наивного {}(наносекунд)'.format(T1))
            start_time = time.time_ns()
            SFT_KMP(text, pattern)
            end_time = time.time_ns()
            T2 = end_time - start_time
            print('Время работы Кнута-Морриса-Пратта {}(наносекунд)'.format(T2))
        elif choice == 9:
            print('Текст: ' + text)
            print('Шаблон: ' + pattern)
        elif choice == 0:
            break
        else:
            print('Нет такой команды')
    choice = int(input('Выберите эксперимент(1-3): '))
    if choice == 1:
        first_experiment()
    elif choice == 2:
        second_experiment()
    elif choice == 3:
        third_experiment()
    else:
        print('Нет такого эксперимента!')


if __name__ == '__main__':
    main()
