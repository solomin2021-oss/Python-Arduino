import tkinter as tk  # Импорт библиотеки для создания графического интерфейса
from tkinter import messagebox  # Импорт модуля для отображения всплывающих сообщений
from pyfirmata import Arduino, PWM  # Импорт библиотеки для работы с Arduino (PWM - ШИМ-сигналы)
from time import sleep  # Импорт функции sleep для создания задержек

# Функция для управления синим светодиодом
def blueLED():
    delay = float(LEDtime.get())  # Получаем значение времени из поля ввода и преобразуем в число с плавающей точкой
    brightness = float(LEDbright.get())  # Получаем значение яркости из слайдера и преобразуем в число
    blueBtn.config(state=tk.DISABLED)  # Делаем кнопку синего светодиода неактивной на время работы
    board.digital[3].write(brightness / 100.0)  # Устанавливаем яркость на 3-м пине (преобразуем проценты в диапазон 0-1)
    sleep(delay)  # Ожидаем указанное количество секунд
    board.digital[3].write(0)  # Выключаем светодиод, устанавливая яркость в 0
    # ВНИМАНИЕ: Здесь ошибка в названии переменной - должно быть blueBtn вместо blueBTN
    blueBTN.config(state=tk.ACTIVE)  # Возвращаем кнопке активное состояние (ошибка в названии переменной)

# Функция для управления красным светодиодом
def redLED():
    delay = float(LEDtime.get())  # Получаем значение времени из поля ввода
    brightness = float(LEDbright.get())  # Получаем значение яркости из слайдера
    redBtn.config(state=tk.DISABLED)  # Делаем кнопку красного светодиода неактивной
    # ВНИМАНИЕ: Здесь ошибка - используется тот же пин (3), что и для синего светодиода
    board.digital[3].write(brightness / 100.0)  # Устанавливаем яркость на 3-м пине
    sleep(delay)  # Ожидаем указанное количество секунд
    board.digital[3].write(0)  # Выключаем светодиод
    # ВНИМАНИЕ: Здесь ошибка в названии переменной - должно быть redBtn вместо redBTN
    redBTN.config(state=tk.ACTIVE)  # Возвращаем кнопке активное состояние (ошибка в названии переменной)

# Функция для отображения информационного сообщения
def aboutMsg():
    # Показываем окно с информацией о программе
    messagebox.showinfo("Это программа обеспечение, которому все равно на логику\nLED Контроллер Вер 1.0\nJanuary 2026")

# Подключение к Arduino через COM3 порт
board = Arduino("COM3")

# Настройка пинов 3 и 5 в режим ШИМ (PWM) для управления яркостью светодиодов
board.digital[3].mode = PWM
board.digital[5].mode = PWM

# Создание главного окна приложения
win = tk.Tk()
# Настройка параметров окна
win.title("Dimmer LED")  # Установка заголовка окна
win.minsize(235, 150)  # Установка минимального размера окна

# Создание поля для ввода времени свечения светодиода
LEDtime = tk.Entry(win, bd=6, width=8)  # bd - толщина границы, width - ширина поля
LEDtime.grid(column=1, row=1)  # Размещение поля в сетке (столбец 1, строка 1)

# Создание надписи для поля ввода времени
label = tk.Label(win, text="LED ВКЛ Время (сек)").grid(column=2, row=1)  # Создание и размещение метки

# Создание слайдера для регулировки яркости светодиода
LEDbright = tk.Scale(win, bd=5, from_=0, to=100, orient=tk.HORIZONTAL)  # Слайдер от 0 до 100, горизонтальный
LEDbright.grid(column=1, row=2)  # Размещение слайдера в сетке

# ВНИМАНИЕ: Эта метка создана, но не размещена в сетке - вероятно, ошибка
tk.Label(win, text="Яркость LED")

# Создание кнопок управления

# Кнопка для включения синего светодиода
blueBtn = tk.Button(win, bd=5, text="Blue LED", command=blueLED)
blueBtn.grid(column=1, row=3)  # Размещение кнопки в сетке

# Кнопка для включения красного светодиода
redBtn = tk.Button(win, bd=5, text="Red LED", command=redLED)
redBtn.grid(column=2, row=3)  # Размещение кнопки в сетке

# Кнопка для вызова справки
aboutBtn = tk.Button(win, text="Справка", command=aboutMsg)
aboutBtn.grid(column=1, row=4)  # Размещение кнопки в сетке

# Кнопка для закрытия приложения
quitBtn = tk.Button(win, text="Закрыть", command=win.quit)
quitBtn.grid(column=2, row=4)  # Размещение кнопки в сетке

# Запуск главного цикла обработки событий приложения
win.mainloop()
