import time
import datetime
import pygame

def ustanovka_vremeni():
    while True:
        time_user = input('Введите время будильника (часы минуты через пробел, например 07 30): ').strip().split()
        if len(time_user) != 2:
            print("Ошибка: формат 'часы минуты'")
            continue
        hours, minutes = time_user
        if not (hours.isdigit() and minutes.isdigit()):
            print("Ошибка: часы и минуты должны быть числами")
            continue
        hours, minutes = int(hours), int(minutes)
        if not (0 <= hours < 24 and 0 <= minutes < 60):
            print("Ошибка: часы 0-23, минуты 0-59")
            continue
        return f"{hours:02d}:{minutes:02d}"

def vybor_zvuka():
    print("Выберите звук будильника:")
    print("1. Звуковой сигнал beep")
    print("2. Текстовое сообщение")
    print("3. Простая мелодия (несколько beep подряд)")
    choice = input("Введите номер (1-3): ").strip()
    return choice if choice in {"1", "2", "3"} else "1"

def vybor_povtoreniya():
    print("Выберите режим повторения будильника:")
    print("1. Однократный (будет срабатывать один раз)")
    print("2. Ежедневный (будет срабатывать каждый день)")
    choice = input("Введите номер (1 или 2): ").strip()
    return "daily" if choice == "2" else "once"

def play_sound(choice):
    pygame.mixer.init()
    if choice == "1":  # beep
        # простой короткий beep.wav
        sound = pygame.mixer.Sound("beep.wav")
        sound.play()
        while pygame.mixer.get_busy():
            time.sleep(0.1)
    elif choice == "3":  # melody - несколько beep подряд
        beep = pygame.mixer.Sound("beep.wav")
        for _ in range(3):
            beep.play()
            while pygame.mixer.get_busy():
                time.sleep(0.1)
            time.sleep(0.2)
    elif choice == "2":  # текстовое сообщение
        print("[Будильник]: Время просыпаться!")

def budilnik():
    alarms = []
    try:
        n = int(input("Сколько будильников хотите установить? "))
    except ValueError:
        print("Ошибка: введите число")
        return

    for i in range(n):
        print(f"\nНастройка будильника {i+1}:")
        alarm_time = ustanovka_vremeni()
        alarm_sound = vybor_zvuka()
        alarm_repeat = vybor_povtoreniya()
        alarms.append({"time": alarm_time, "sound": alarm_sound, "repeat": alarm_repeat, "active": True})

    print("\nБудильники установлены:")
    for i, alarm in enumerate(alarms, 1):
        print(f"{i}. Время: {alarm['time']} - Звук: {alarm['sound']} - Повтор: {alarm['repeat']}")

    print("\nОжидание срабатывания будильников...\n")

    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        for alarm in alarms:
            if alarm['active'] and now == alarm['time']:
                play_sound(alarm['sound'])
                if alarm['repeat'] == "once":
                    alarm['active'] = False
                    if not any(a['active'] for a in alarms):
                        print("Все однократные будильники сработали. Завершение")
                        return
                    time.sleep(60)
                    time.sleep(1)

if __name__ == "__main__":
    budilnik()