import time                     # Импорт модуля time для работы с системным временем.
from datetime import datetime   # Импорт функции datetime из библиотеки datetime для работы с датами календаря.
import pygame                   # Импорт библиотеки pygame для создания игр.

pygame.mixer.init()             # Инициализация функции mixer проигрывателя муз.файлов.

alarm_time = 0                  # alarm_time - дата будильника в формате YYYY-MM-DD hh:mm.
a_t_sec = 0                     # a_t_sec - дата будильника в секундах от 01.01.1970 00:00.
t_sec = 0                       # t_sec - текущая дата в секундах от 01.01.1970 00:00.
mel_numb = 0                    # mel_numb - номер мелодии в музыкальном списке.
alarm_msg = 0                   # alarm_msg - сообщение будильника,  задаваемое пользователем.
alarm_time_list = []            # alarm_time_list - список будильников (времён побудки).

year = datetime.now().year      # year - текущий год.

# melody_list - музыкальный список
melody_list = \
    [
    "Беззвучная....",
    "Louis Armstrong - Go Down Moses.mp3",
    "Matia Bazar - Vacance Romane.mp3",
    "Fallout New Vegas Radio - Jazz Blues.mp3"
    ]

"""
str0 - создание двузначной строки "0d" из однозначного целого числа d. 
Для форматированного вывода времени побудки.
"""
def str0(d):
    if 0 <= d < 10:
        d = str(0) + str(d)
    else:
        d = str(d)
    return d

""""
alarm_time_set - установка времени будильника (будильников). 
Возвращает список будильников.
"""
def alarm_time_set():

    while True:             # Цикл для установки времени будильника (будильников)
        """
        Ввод времени будильника в формате для аргумента функции time.mktime(), т.е., в формате tuple -
        список целых чисел [год, месяц, день(число) месяца, час дня, минуты, 0, 0, 0, 0], 
        здесь нули - значения остальных аргументов.
        """
        print(f"Установите время будильника {year}-MM-DD hh:mm")
        try:
            a_t_list = \
                [year,
                int(input('месяц MM: ')),
                int(input('число DD: ')),
                int(input('час(24) hh: ')),
                int(input('минут mm: ')),
                0, 0, 0, 0
                ]
            """
            Проверка корректности введённых значений аргументов даты и времени будильника.
            """
            if         a_t_list[1] not in range(1, 13)\
                    or a_t_list[2] not in range(1, 32)\
                    or a_t_list[3] not in range(0, 24)\
                    or a_t_list[4] not in range(0, 60):
                print("Ошибка")
                raise ValueError                    # Вызов исключения ValueError в случае некорректного значения даты.
            """
            Проверка корректности времени будильника
            """
            t_sec = time.time()                     # Текущая дата в секундах от времени эпохи.
            a_t_sec = time.mktime(tuple(a_t_list))  # Перевод времени будильника из формата tuple в формат float секунд.
            if a_t_sec < t_sec:                     # Если True, то ввод будильника повоторяется.
                print("Ошибка. Установите время будильника больше текущего времени")
                raise ValueError                    # Вызов исключения ValueError, если будильник меньше текущей даты.
            else:
                print("Будильник будет установлен!")
                alarm_time_list.append(a_t_sec)     # Добавление будильника (времени побудки) в список будильников.

                """
                Запрос на добавление будильника
                """
                quest = input(
                    f"Добавить будильник?...введите 'yes'{'\n'}"
                    f"Продолжить - нажмите ENTER{'\n'}"
                    f"Ваш выбор:  "
                             )
                if quest == "yes":
                    continue
                else:
                    pass
        except Exception: continue      # Обработка любого исключения при ошибке ввода с возвращением в начало ввода.
        alarm_time_list.sort()          # Сортировка списка будильников по возрастанию (на случай хаотичного ввода).

        return alarm_time_list          # Возвращается список будильников
"""
music_set функция выбора варианта побудки:
- если будет ведён 0, то побудка будет беззвучная с заданным сообщением alarm_msg;
- если будет введён не 0, то побудка будет мелодией с введённым номером.
Возвращает номер варианта побудки mel_numb и сообщение при варианте беззвучной побудки alarm_msg.
Музыкальные файлы расположены вместе с программой clockalarm.py в директории проекта .venv/Scripts/
"""
def music_set():
    while True:                                             # Цикл для выбора варианта побудки
        try:
            print("ВАРИАНТЫ ПОБУДКИ:")                      # вывод списка вариантов побудки
            for i in range(len(melody_list)):
                print(f"{i} -  {melody_list[i][:-4]}{'\n'}")
            mel_numb = int(input(f"№ варианта: "))
            if mel_numb not in range(0, len(melody_list)):    # Проверка корректности введённого номера варианта.
                print("Ошибка. Мелодии с таким номером нет")
                raise ValueError                              # Вызов исключения ValueError при ошибке ввода.
            else:
                print(f"Вы выбрали {melody_list[mel_numb][:-4]}{'\n'}")

            if mel_numb == 0:  # Если выбран вариант 0, то можно задать своё сообщение. По умолчанию "Время вставать!"
                alarm_msg = input(f"Задайте сообщение будильника или нажмите ENTER{'\n'} Сообщение: ")
                if alarm_msg == "":
                    alarm_msg = "Время вставать!"
                print("Сообщение: ", alarm_msg)
            alarm_msg = " "
            return mel_numb, alarm_msg
        except ValueError: continue


mel_numb, alarm_msg = music_set()                       # Выбор варианта побудки.
alarm_time_list = alarm_time_set()                      # Создание списка будильников.

for i in range(len(alarm_time_list)):       # Цикл по списку будильников alarm_time_list.

    a_t_sec = alarm_time_list[i]            # Установленное время очередного будильника, в секундах от эпохи.
    a_t = time.localtime(a_t_sec)           # Преобразование времени a_t_sec в формат tuple.

    # Преобразование установки времени из формата tuple в строку alarm_time = "year-MM-DD hh:mm"
    alarm_time = (
            str0(a_t[0]) + "-" +
            str0(a_t[1]) + "-" +
            str0(a_t[2]) + " " +
            str0(a_t[3]) + ":" +
            str0(a_t[4])
                 )
    print("alarm_time", alarm_time)         # Вывод установки времени очередного будильника "year-MM-DD hh:mm"
    """
    Отсрочка запуска программы будильника нужна, чтобы не занимать ресурсы 
    циклами сравнения текущего времени с временем будильника. 
    Используется функция time.sleep() модуля time.
    Программа продолжит выполняться за 1 секунду до времени побудки a_t_sec.
    
    Записанное время будильника a_t_sec из-за задержек при создании будильника 
    или при продолжительной предыдущей побудке может не превышать больше 
    чем на 1 секунду текущее время t_sec. Тогда аргумент функции time.sleep() отрицательный 
    и при обработке исключения ValueError запускается следующий будильник.
    """
    try:
        t_sec = time.time()  # Текущее время на момент запуска очередного будильника, секунды от эпохи.
        time.sleep((a_t_sec - t_sec) - 1)
    except ValueError:
        if True:
            print("Время этого будильника прошло")
            continue
    """
    Запуск очередного установленного будильника.
    """
    while a_t_sec > t_sec:      # Цикл сравнения продолжается, пока время побудки a_t_sec не превысит текущее время
        t_sec = time.time()     # Текущее время, секунды от эпохи.
        continue
    else:
        if mel_numb == 0:       # При беззвучной побудке выводится сообщение alarm_msg.
            print(alarm_msg)
        else:                   # При выборе музыкальной побудки
            count = 0           # включается count счётчик повторов (отложенных на 5 мин. побудок) count.
            while True:         # Цикл для повторов побудки. Выход из цикла или по счётчику count или принудительно.
                pygame.mixer.music.load(melody_list[mel_numb])
                pygame.mixer.music.play()
                stop = input(f"Чтобы остановить этот будильник, введите 'stop'.{'\n'}"
                             f"Чтобы отложить на 5 минут нажмите ENTER. {'\n'}")
                if stop == 'stop':
                    pygame.mixer.music.stop()
                    break
                else:
                    pygame.mixer.music.stop()
                    if count < 5:
                        time.sleep(10)              # Побудка откладывается - работа будильника прерывается на 5 мин.
                        pygame.mixer.music.play()   # Побудка включается, если счётчик повторов count < 5.
                        count += 1
                    else:
                        print("Этот будильник остановлен")
                        break
                    continue
    stop = input(
        f"Чтобы остановить все будильники, введите 'stop'.{'\n'}"
        f"Чтобы продолжить, нажмите ENTER. {'\n'}"
                )
    if stop == 'stop':
        break
    else:
        pass








