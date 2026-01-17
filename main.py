import tkinter as tk
from tkinter import messagebox
from pyfirmata import Arduino, PWM
from time import sleep

def blueLED():
   delay = float(LEDtime.get())
   brightness = float(LEDbright.get())
   blueBtn.config(state = tk.DISABLED)
   board.digital[3].write(brightness/100.0)
   sleep(delay)
   board.digital[3].write(0)
   blueBTN.config(state = tk.ACTIVE)
def redLED():
    delay = float(LEDtime.get())
    brightness = float(LEDbright.get())
    redBtn.config(state = tk.DISABLED)
    board.digital[3].write(brightness/100.0)
    sleep(delay)
    board.digital[3].write(0)
    redBTN.config(state = tk.ACTIVE)
def aboutMsg():
    messagebox.showinfo("Это программа обеспечение, которому все равно на логику\nLED Контроллер Вер 1.0\nJanuary 2026")



board = Arduino("COM3")

board.digital[3].mode = PWM
board.digital[5].mode = PWM

win = tk.Tk()
# Инициализация окна
win.title("Dimmer LED")
win.minsize(235, 150)

LEDtime = tk.Entry(win, bd=6, width=8)
LEDtime.grid(column=1, row=1)
# Создаем надписи label ну тип текст
label = tk.Label(win, text="LED ВКЛ Время (сек)").grid(column=2, row=1)

LEDbright = tk.Scale(win, bd=5, from_=0, to=100, orient=tk.HORIZONTAL)
LEDbright.grid(column=1, row=2)

tk.Label(win, text="Яркость LED")

#кнопки вкл выкл делаем
blueBtn = tk.Button(win, bd=5, text="Blue LED", command=blueLED)
blueBtn.grid (column=1, row=3)
redBtn = tk.Button(win, bd=5, text="Red LED", command=redLED)
redBtn.grid (column=2, row=3)
aboutBtn = tk.Button(win, text="Справка", command=aboutMsg)
aboutBtn.grid(column=1, row=4)
quitBtn = tk.Button(win, text="Закрыть", command=win.quit)
quitBtn.grid(column=2, row= 4)


win.mainloop()