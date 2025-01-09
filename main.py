import logging
import os
import customtkinter as ctk
from tkinter import PhotoImage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import json
import requests

version = '0.1'

ctk.set_appearance_mode("dark")
logging.basicConfig(level=logging.INFO)

# Настройка параметров Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Запуск без графического интерфейса
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Список серверов с их соответствующими URL
server_urls = {
    "Downtown": "https://gta5rp.com/api/V2/users/chars/1",
    "Strawberry": "https://gta5rp.com/api/V2/users/chars/2",
    "Vinewood": "https://gta5rp.com/api/V2/users/chars/3",
    "Blackberry": "https://gta5rp.com/api/V2/users/chars/4",
    "Insquad": "https://gta5rp.com/api/V2/users/chars/5",
    "Sunrise": "https://gta5rp.com/api/V2/users/chars/6",
    "Rainbow": "https://gta5rp.com/api/V2/users/chars/7",
    "Richman": "https://gta5rp.com/api/V2/users/chars/8",
    "Eclipse": "https://gta5rp.com/api/V2/users/chars/9",
    "La Mesa": "https://gta5rp.com/api/V2/users/chars/10",
    "Burton": "https://gta5rp.com/api/V2/users/chars/11",
    "Rockford": "https://gta5rp.com/api/V2/users/chars/12",
    "Alta": "https://gta5rp.com/api/V2/users/chars/13",
    "Del Perro": "https://gta5rp.com/api/V2/users/chars/14",
    "Davis": "https://gta5rp.com/api/V2/users/chars/15",
    "Harmony": "https://gta5rp.com/api/V2/users/chars/16",
    "Redwood": "https://gta5rp.com/api/V2/users/chars/17",
    "Hawick": "https://gta5rp.com/api/V2/users/chars/18",
    "Grapeseed": "https://gta5rp.com/api/V2/users/chars/19",
    "Murrieta": "https://gta5rp.com/api/V2/users/chars/20",
    "Vespucci": "https://gta5rp.com/api/V2/users/chars/21"
}

def get_token_from_file():
    try:
        file_path = os.path.join(os.getcwd(), '__stk.json')
        with open(file_path, 'r', encoding='utf-8') as f:
            cookie_data = json.load(f)
            token = cookie_data.get("value")
            if token:
                print(f"Токен: {token}")
                return token
            else:
                print("Токен не найден в файле.")
                return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

def on_server_select(selected_server):
    print(f"Выбран сервер: {selected_server}")
    token = get_token_from_file()

    if token:
        headers = {
            "Authorization": f"Bearer {token}",
            "x-access-token": token,
            "x-lang": "ru",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0"
        }

        url = server_urls.get(selected_server)
        if url:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                user_info = ""

                for user in data:
                    vehicle_info = f"Машина: {user['vehicles'][0]['title'] if user['vehicles'] else 'Отсутствует'}"
                    house_info = f"Дом: {user['house'] if user['house'] else 'Отсутствует'}"
                    vip_info = f"VIP уровень: {user['vip_name']}"

                    user_info += f"""
                        Статик: {user['id']}
                        Ник: {user['name']}
                        Уровень: {user['lvl']}
                        Статус: {'Онлайн 🟢' if user['is_online'] else 'Оффлайн 🔴'}
                        Деньги: {user['cash']}
                        Фракция: {user['fraction'] or 'None'}
                        {vehicle_info}
                        {house_info}
                        {vip_info}
                        Часов отыграно: {user['hours_played']}
                        \n"""

                result_label.configure(text=user_info,font=("Arial", 16, "bold"), justify="left")
            else:
                print(f"Ошибка запроса: {response.status_code}")
        else:
            print("Сервер не найден.")
    else:
        print("Не удалось получить токен.")

def sign_up():
    login = loginEntry.get()
    password = passwordEntry.get()

    driver.get("https://gta5rp.com/login")
    login_field = driver.find_element(By.NAME, "login")
    password_field = driver.find_element(By.NAME, "password")

    login_field.send_keys(login)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    time.sleep(5)

    def save_cookie():
        try:
            cookies = driver.get_cookies()
            stk_cookie = next((cookie for cookie in cookies if cookie['name'] == '__stk'), None)
            if stk_cookie:
                file_path = os.path.join(os.getcwd(), '__stk.json')
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(stk_cookie, f, ensure_ascii=False, indent=4)
                logging.info(f"Куки '__stk' сохранены в {file_path}")
            else:
                logging.warning("Куки '__stk' не найдены.")
        except Exception as e:
            logging.error(f"Ошибка при сохранении куки: {e}")

    if driver.current_url == "https://gta5rp.com/user/stats":
        save_cookie()
        # Получение размера экрана
        screen_width = loginWindow.winfo_screenwidth()
        screen_height = loginWindow.winfo_screenheight()

        window_width = 500
        window_height = 800
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        loginWindow.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')
        loginWindow.title("Информация о персонаже | GTA 5 RP")
        version_label = ctk.CTkLabel(loginWindow, text=f"Developer: apache1337 | Version: {version}", font=("Arial", 9),text_color="#595858")
        version_label.pack(side="bottom", pady=5)

        for widget in loginWindow.winfo_children():
            widget.destroy()

        def on_arrow_key(event):
            current_index = servers.index(server_option_menu.get())
            if event.keysym == "Up":  # Обработка нажатия стрелки вверх
                new_index = (current_index - 1) % len(servers)
            elif event.keysym == "Down":  # Обработка нажатия стрелки вниз
                new_index = (current_index + 1) % len(servers)
            else:
                return
            server_option_menu.set(servers[new_index])

        servers = list(server_urls.keys())
        server_option_menu = ctk.CTkOptionMenu(loginWindow, values=servers, command=on_server_select)
        server_option_menu.pack(pady=10, anchor='w', padx=10)  # Привязка к левому краю

        server_option_menu.bind('<Up>', on_arrow_key)
        server_option_menu.bind('<Down>', on_arrow_key)

        global result_label
        result_label = ctk.CTkLabel(loginWindow, text="Выберите сервер", font=("Arial", 16, "bold"))
        result_label.pack(pady=20, anchor='w', padx=10, side = "top")  # Привязка к левому краю
    else:
        driver.quit()


# Создаем окно для логина
loginWindow = ctk.CTk()
loginWindow.title("Вход в аккаунт | GTA 5 RP")
# Получение размера экрана
screen_width = loginWindow.winfo_screenwidth()
screen_height = loginWindow.winfo_screenheight()

window_width = 255
window_height = 180
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
loginWindow.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')

version_label = ctk.CTkLabel(loginWindow, text="Введите данные", font = ("Arial", 16, "bold"))
version_label.pack(side="top", pady=3)

loginEntry = ctk.CTkEntry(loginWindow, placeholder_text="Введите логин...", corner_radius=12)
loginEntry.pack(pady=5)

passwordEntry = ctk.CTkEntry(loginWindow, placeholder_text="Введите пароль...", show="*",corner_radius=12)
passwordEntry.pack(pady=5)

signUpButton = ctk.CTkButton(loginWindow, text="Войти", command=sign_up, font=("Arial",16,"bold"),corner_radius=12)
signUpButton.pack(pady=5)
loginWindow.bind('<Return>', lambda event: sign_up())

version_label = ctk.CTkLabel(loginWindow, text=f"Developer: apache1337 | Version: {version} | All rights reserved", font=("Arial", 9), text_color='#595858')
version_label.pack(side="bottom", pady=3)


loginWindow.mainloop()
