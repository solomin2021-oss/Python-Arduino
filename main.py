import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import os
import random
import subprocess
import time

# Киберпанк цвета
NEON_BLUE = "#0ff0fc"
NEON_PINK = "#f205cb"
NEON_GREEN = "#00ff41"
NEON_PURPLE = "#bc13fe"
DARK_BG = "#0a0a12"
GLITCH_BLUE = "#1c7ce0"
GLITCH_PINK = "#ff00ff"
GRID_COLOR = "#1a1a2e"

# Конфигурация
FONT_MAIN = ("Courier New", 11, "bold")
FONT_DIGITAL = ("OCR A Extended", 12)
FONT_TITLE = ("Bank Gothic", 16, "bold")
FONT_HUD = ("Seven Segment", 14)

# Состояния светофора
traffic_states = {
    "RED": {"color": "#ff0033", "text": "СТОП", "time": 5},
    "YELLOW": {"color": "#ffff00", "text": "ВНИМАНИЕ", "time": 2},
    "GREEN": {"color": "#00ff41", "text": "ИДТИ", "time": 5},
    "OFF": {"color": "#333333", "text": "ОФФЛАЙН", "time": 0}
}

current_state = "OFF"
pedestrian_request = False
system_online = False
scan_pos = 0
glitch_active = False

# Пути к ресурсам (замени на свои или используй заглушки)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cyber_boy_path = os.path.join(BASE_DIR, "cyber_boy.png")
glitch_sound = os.path.join(BASE_DIR, "glitch.wav")
power_sound = os.path.join(BASE_DIR, "power.wav")

# Заглушка для звуков
def play_sound(sound_type):
    try:
        if sound_type == "power":
            os.system("afplay /System/Library/Sounds/Submarine.aiff 2>/dev/null || echo 'beep'")
        elif sound_type == "glitch":
            os.system("say 'glitch' 2>/dev/null")
        elif sound_type == "switch":
            os.system("afplay /System/Library/Sounds/Pop.aiff 2>/dev/null")
    except:
        pass

class CyberTrafficLight:
    def __init__(self, canvas, x, y, size=80):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.state = "OFF"
        
        # Создаем светофор
        self.frame = canvas.create_rectangle(
            x, y, x + size, y + size * 3,
            fill="#111122", outline=NEON_BLUE, width=2
        )
        
        # Светодиоды
        self.lights = {
            "RED": canvas.create_oval(
                x + size*0.2, y + size*0.2,
                x + size*0.8, y + size*0.8 + size*0,
                fill="#333333", outline=NEON_PINK, width=1
            ),
            "YELLOW": canvas.create_oval(
                x + size*0.2, y + size*1.2,
                x + size*0.8, y + size*1.8,
                fill="#333333", outline=NEON_PINK, width=1
            ),
            "GREEN": canvas.create_oval(
                x + size*0.2, y + size*2.2,
                x + size*0.8, y + size*2.8,
                fill="#333333", outline=NEON_PINK, width=1
            )
        }
        
        # Глитч-эффекты
        self.glitch_overlay = canvas.create_rectangle(
            x, y, x + size, y + size * 3,
            fill="", outline="", width=0
        )
        
        # Текст состояния
        self.text = canvas.create_text(
            x + size/2, y + size*3 + 20,
            text="ОФФЛАЙН",
            fill=NEON_BLUE,
            font=FONT_DIGITAL
        )
    
    def set_state(self, state):
        self.state = state
        color = traffic_states[state]["color"]
        text = traffic_states[state]["text"]
        
        # Выключаем все лампы
        for light in self.lights.values():
            self.canvas.itemconfig(light, fill="#333333")
        
        # Включаем нужную
        if state == "RED":
            self.canvas.itemconfig(self.lights["RED"], fill=color)
        elif state == "YELLOW":
            self.canvas.itemconfig(self.lights["YELLOW"], fill=color)
        elif state == "GREEN":
            self.canvas.itemconfig(self.lights["GREEN"], fill=color)
        
        self.canvas.itemconfig(self.text, text=text)
        
        # Глитч-эффект при переключении
        if state != "OFF":
            self.glitch_effect()

    def glitch_effect(self):
        for _ in range(3):
            offset_x = random.randint(-3, 3)
            offset_y = random.randint(-3, 3)
            color = random.choice([NEON_PINK, NEON_BLUE, GLITCH_BLUE])
            
            self.canvas.itemconfig(self.glitch_overlay, 
                outline=color, width=1)
            self.canvas.move(self.glitch_overlay, offset_x, offset_y)
            
            self.canvas.update()
            time.sleep(0.05)
            
            self.canvas.itemconfig(self.glitch_overlay, 
                outline="", width=0)
            self.canvas.move(self.glitch_overlay, -offset_x, -offset_y)

def create_grid(canvas, width, height, step=20):
    """Создает сетку в стиле киберпанк"""
    for x in range(0, width, step):
        canvas.create_line(x, 0, x, height, fill=GRID_COLOR, width=1, tags="grid")
    for y in range(0, height, step):
        canvas.create_line(0, y, width, y, fill=GRID_COLOR, width=1, tags="grid")

def glitch_text(canvas, text_id):
    """Эффект глитча для текста"""
    original_text = canvas.itemcget(text_id, "text")
    glitch_chars = "█▓▒░╬╫╪╨╧╦╥╤╣╢╡╠╟╞╝╜╛╚╙╘╗╖╕╔╓╒║═╬"
    
    for _ in range(5):
        glitched = ''.join(random.choice(glitch_chars) if random.random() > 0.7 else c 
                          for c in original_text)
        canvas.itemconfig(text_id, text=glitched)
        canvas.update()
        time.sleep(0.03)
    
    canvas.itemconfig(text_id, text=original_text)

def scanline_effect(canvas, width, height):
    """Движущаяся сканирующая линия"""
    global scan_pos
    canvas.delete("scanline")
    
    # Основная линия
    canvas.create_rectangle(
        0, scan_pos, width, scan_pos + 2,
        fill=NEON_BLUE, outline="", alpha=0.3, tags="scanline"
    )
    
    # Свечение
    for i in range(1, 4):
        alpha = 0.2 - i*0.05
        canvas.create_rectangle(
            0, scan_pos - i, width, scan_pos - i + 1,
            fill=NEON_BLUE, outline="", alpha=alpha, tags="scanline"
        )
        canvas.create_rectangle(
            0, scan_pos + i, width, scan_pos + i + 1,
            fill=NEON_BLUE, outline="", alpha=alpha, tags="scanline"
        )
    
    scan_pos = (scan_pos + 3) % height
    canvas.after(50, lambda: scanline_effect(canvas, width, height))

def random_glitch(canvas):
    """Случайные глитч-эффекты"""
    if not system_online:
        return
    
    if random.random() < 0.1:  # 10% шанс на глитч
        # Мигание экрана
        canvas.config(bg=random.choice([GLITCH_BLUE, GLITCH_PINK, "#000000"]))
        canvas.after(50, lambda: canvas.config(bg=DARK_BG))
        
        # Случайные линии
        for _ in range(random.randint(1, 3)):
            x1 = random.randint(0, 320)
            y1 = random.randint(0, 240)
            x2 = random.randint(0, 320)
            y2 = random.randint(0, 240)
            canvas.create_line(x1, y1, x2, y2, 
                             fill=random.choice([NEON_PINK, NEON_BLUE]),
                             width=1, tags="temp_glitch")
        
        canvas.after(100, lambda: canvas.delete("temp_glitch"))
        play_sound("glitch")
    
    canvas.after(1000, lambda: random_glitch(canvas))

def toggle_system():
    """Включение/выключение системы"""
    global system_online, current_state
    
    system_online = not system_online
    
    if system_online:
        play_sound("power")
        power_btn.config(text="■ СИСТЕМА ОНЛАЙН", 
                        bg=NEON_GREEN, 
                        fg="black",
                        activebackground=NEON_GREEN)
        status_label.config(text="[ СТАТУС: ОНЛАЙН ]", fg=NEON_GREEN)
        canvas.itemconfig(system_indicator, fill=NEON_GREEN)
        
        # Запускаем светофор
        current_state = "RED"
        traffic_light.set_state("RED")
        cycle_traffic_light()
        
        # Активируем эффекты
        scanline_effect(canvas, 320, 240)
        random_glitch(canvas)
    else:
        play_sound("power")
        power_btn.config(text="▶ СИСТЕМА ОФФЛАЙН", 
                        bg="#222233", 
                        fg=NEON_BLUE,
                        activebackground=NEON_BLUE)
        status_label.config(text="[ СТАТУС: ОФФЛАЙН ]", fg=NEON_BLUE)
        canvas.itemconfig(system_indicator, fill="#222233")
        
        # Выключаем светофор
        current_state = "OFF"
        traffic_light.set_state("OFF")

def cycle_traffic_light():
    """Цикл работы светофора"""
    global current_state
    
    if not system_online:
        return
    
    states = ["RED", "GREEN", "YELLOW"]
    current_idx = states.index(current_state) if current_state in states else 0
    next_idx = (current_idx + 1) % 3
    current_state = states[next_idx]
    
    traffic_light.set_state(current_state)
    play_sound("switch")
    
    # Обновляем информацию
    info_text = f"[ ФАЗА: {traffic_states[current_state]['text']} ]\n"
    info_text += f"[ ВРЕМЯ: {traffic_states[current_state]['time']}сек ]\n"
    info_text += f"[ СИГНАЛ: {current_state} ]"
    info_display.config(text=info_text)
    
    # Планируем следующее переключение
    delay = traffic_states[current_state]['time'] * 1000
    canvas.after(delay, cycle_traffic_light)

def request_pedestrian():
    """Запрос пешеходного перехода"""
    global pedestrian_request
    
    if not system_online:
        return
    
    pedestrian_request = True
    pedestrian_btn.config(bg=NEON_PINK, text="ЗАПРОС ОТПРАВЛЕН")
    play_sound("glitch")
    
    # Мигание зеленого для пешеходов
    def blink_green():
        for _ in range(6):
            traffic_light.set_state("GREEN")
            canvas.update()
            time.sleep(0.3)
            traffic_light.set_state("OFF")
            canvas.update()
            time.sleep(0.3)
        
        traffic_light.set_state("RED")
        pedestrian_btn.config(bg="#222233", text="ПЕШЕХОДНЫЙ ЗАПРОС")
    
    canvas.after(1000, blink_green)

def show_about():
    """Окно информации"""
    about_window = tk.Toplevel(win)
    about_window.title("■ СИСТЕМНАЯ ИНФОРМАЦИЯ")
    about_window.geometry("300x200")
    about_window.configure(bg=DARK_BG)
    about_window.resizable(False, False)
    
    tk.Label(about_window, 
             text="╔════════════════════════╗\n"
                  "  КИБЕРПАНК СВЕТОФОР v2.0\n"
                  "╚════════════════════════╝\n\n"
                  "■ СИСТЕМА: TRAFFIC_OS\n"
                  "■ ВЕРСИЯ: 2077.2.1\n"
                  "■ ЛИЦЕНЗИЯ: NIGHT_CITY_TECH\n"
                  "■ СТАТУС: OPERATIONAL",
             font=FONT_DIGITAL,
             fg=NEON_BLUE,
             bg=DARK_BG).pack(pady=20)
    
    tk.Button(about_window,
              text="[ ЗАКРЫТЬ ]",
              font=FONT_MAIN,
              fg=NEON_PINK,
              bg="#222233",
              command=about_window.destroy).pack()

# Создание главного окна
win = tk.Tk()
win.title("■ КИБЕРПАНК СВЕТОФОР ■ NIGHT CITY TRAFFIC CONTROL")
win.geometry("400x500")
win.configure(bg=DARK_BG)
win.resizable(False, False)

# Основной холст
canvas = tk.Canvas(win, width=400, height=500, bg=DARK_BG, highlightthickness=0)
canvas.pack()

# Сетка
create_grid(canvas, 400, 500)

# Заголовок
title = canvas.create_text(200, 30,
    text="╔══════════════════════════════╗\n"
         "   NIGHT CITY TRAFFIC CONTROL   \n"
         "╚══════════════════════════════╝",
    font=("Courier New", 14, "bold"),
    fill=NEON_BLUE,
    justify="center")

# Индикатор системы
canvas.create_text(200, 80,
    text="[ СИСТЕМНЫЙ МОНИТОР ]",
    font=FONT_DIGITAL,
    fill=NEON_PURPLE)

status_label = tk.Label(win,
    text="[ СТАТУС: ОФФЛАЙН ]",
    font=FONT_DIGITAL,
    fg=NEON_BLUE,
    bg=DARK_BG)
status_label.place(x=120, y=100)

# Индикатор в виде неонового круга
canvas.create_oval(360, 75, 380, 95, outline=NEON_BLUE, width=2)
system_indicator = canvas.create_oval(362, 77, 378, 93, fill="#222233")

# Создаем светофор
traffic_light = CyberTrafficLight(canvas, 160, 150, 60)

# Панель информации
info_frame = tk.Frame(win, bg="#111122", bd=2, relief="ridge")
info_frame.place(x=50, y=400, width=300, height=80)

info_display = tk.Label(info_frame,
    text="[ СИСТЕМА ОФФЛАЙН ]\n"
         "[ ОЖИДАНИЕ АКТИВАЦИИ ]\n"
         "[ --- ]",
    font=FONT_DIGITAL,
    fg=NEON_GREEN,
    bg="#111122",
    justify="left")
info_display.pack(pady=10)

# Кнопки управления
button_frame = tk.Frame(win, bg=DARK_BG)
button_frame.place(x=50, y=320, width=300, height=70)

power_btn = tk.Button(button_frame,
    text="▶ СИСТЕМА ОФФЛАЙН",
    font=FONT_TITLE,
    fg=NEON_BLUE,
    bg="#222233",
    bd=3,
    relief="raised",
    width=25,
    command=toggle_system,
    activebackground=NEON_BLUE,
    activeforeground="black")
power_btn.pack(pady=5)

pedestrian_btn = tk.Button(button_frame,
    text="ПЕШЕХОДНЫЙ ЗАПРОС",
    font=("Courier New", 10),
    fg=NEON_PINK,
    bg="#222233",
    bd=2,
    relief="ridge",
    width=20,
    command=request_pedestrian)
pedestrian_btn.pack()

# Меню
menu_bar = tk.Menu(win, bg=DARK_BG, fg=NEON_BLUE, activebackground=NEON_BLUE)
win.config(menu=menu_bar)

system_menu = tk.Menu(menu_bar, tearoff=0, bg="#111122", fg=NEON_BLUE)
menu_bar.add_cascade(label="■ СИСТЕМА", menu=system_menu)
system_menu.add_command(label="АКТИВИРОВАТЬ", command=toggle_system)
system_menu.add_separator()
system_menu.add_command(label="ВЫХОД", command=win.quit)

help_menu = tk.Menu(menu_bar, tearoff=0, bg="#111122", fg=NEON_BLUE)
menu_bar.add_cascade(label="■ ПОМОЩЬ", menu=help_menu)
help_menu.add_command(label="ИНФОРМАЦИЯ", command=show_about)

# Горячие клавиши
win.bind("<Escape>", lambda e: win.quit())
win.bind("<space>", lambda e: toggle_system())
win.bind("<p>", lambda e: request_pedestrian())
win.bind("<F1>", lambda e: show_about())

# Запуск
win.after(100, lambda: glitch_text(canvas, title))
win.mainloop()
