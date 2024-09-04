import requests
import time
import json
import os

def save_config(token, user_id):
    with open("config_user.py", "w") as config_file:
        config_file.write(f'TOKEN = "{token}"\n')
        config_file.write(f'USER_ID = "{user_id}"\n')

if os.path.exists("config_user.py"):
    from config_user import TOKEN, USER_ID
else:
    TOKEN = input("Введите ваш токен: ")
    USER_ID = input("Введите ваш USER_ID: ")

def get_thread_ids():
    url = f"https://api.zelenka.guru/threads?forum_id=8&creator_user_id={USER_ID}"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {TOKEN}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        thread_ids = [thread["thread_id"] for thread in data["threads"]]
        print(f"Кол-во айди найденное для удаления: {len(thread_ids)}")
        save_config(TOKEN, USER_ID)
        return thread_ids
    elif response.status_code == 403:
        print("Вы ввели не верный токен.")
        return []
    else:
        print(f"Ошибка: {response.status_code}")
        return []

def delete_thread(thread_id, current, total):
    url = f"https://api.zelenka.guru/threads/{thread_id}?reason=eblan"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {TOKEN}"
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print(f"Успешно удалили ({current}/{total})")
    else:
        print(f"Ошибка при удалении треда {thread_id}: {response.status_code}")

while True:
    thread_ids = get_thread_ids()
    if not thread_ids:
        break
    time.sleep(3)
    total_threads = len(thread_ids)
    for index, thread_id in enumerate(thread_ids, start=1):
        delete_thread(thread_id, index, total_threads)
        time.sleep(3)
    time.sleep(3)
