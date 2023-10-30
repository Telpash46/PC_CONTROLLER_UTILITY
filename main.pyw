import os
import platform
import sys
import getpass
import time
import threading
import cv2
import requests
import telebot
import winreg
import tkinter as tk
from tkinter import simpledialog, messagebox
from pathlib import Path
import psutil
import pygetwindow
import subprocess
import pyautogui
import ctypes
import pymsgbox
from telebot import types
from pydub import AudioSegment
import sounddevice as sd
import winsound
import io
import subprocess
import winshell
from win32com.client import Dispatch
import sys


def check_user(message):
    try:
        # Открытие ключа реестра
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Pavelo\PC_CONTROLLER")

        # Чтение значения из ключа реестра
        accessmode, _ = winreg.QueryValueEx(key, "AccessMode")
        accesslist, _ = winreg.QueryValueEx(key, "AccessList")
        phonelist, _ = winreg.QueryValueEx(key, "PhoneList")
        phonelist = eval(phonelist)
        accesslist = eval(accesslist)
        ownerid, _ = winreg.QueryValueEx(key, "OwnerId")
        if accessmode != "off":
            print(True)
            if message.from_user.id != int(ownerid):
                if not message.from_user.username:
                    if message.from_user.id in phonelist:
                        if accessmode == "whitelist":
                            return True
                        elif accessmode == "blacklist":
                            bot.reply_to(message, "❌🚨 Вам запрещен доступ к этому боту, так как владелец включил чёрный список и внёс Вас туда (могут быть допущены все, кроме указанных). Мы сожалеем, что Вас заблокировали.")
                            return False
                        else:
                            return True
                    else:
                        if accessmode == "whitelist" or accessmode == "blacklist":
                            bot.reply_to(message, "👮‍♂️ Доступ в бота запрещён, так как настроены права пользователей. Мы обнаружили что у Вас нет username. Попробуйте поделиться с нами номером телефона тут: /sharephone и повторить свое действие.")
                            return False
                        else:
                            return True
                    
                else:
                    if "@"+str(message.from_user.username) in accesslist:
                        if accessmode == "whitelist":
                            return True
                        elif accessmode == "blacklist":
                            bot.reply_to(message, "❌🚨 Вам запрещен доступ к этому боту, так как владелец включил чёрный список и внёс Вас туда (могут быть допущены все, кроме указанных). Мы сожалеем, что Вас заблокировали.")
                            return False
                        else:
                            return True
                    else:
                        if accessmode == "whitelist":
                            bot.reply_to(message, "❌🚨 Вам запрещен доступ к этому боту, так как владелец включил белый список (могут быть допущены только одобренные).")
                            return False
                        elif accessmode == "blacklist":
                            return True
                        else:
                            return True
            else:
                return True
        else:
            return True

    except:
        pass


class MyCustomError(Exception):
    def __init__(self, message):
        super().__init__(message)


version = 3
answer = None
popuptitle = ""
popupmessage = ""
# Создание корневого окна Tkinter
root = tk.Tk()
root.withdraw()

# Установка пути к изображению логотипа
logo_path = "logo.png"  # Замените на фактический путь к вашему изображению

# Установка логотипа окна
root.iconphoto(True, tk.PhotoImage(file=logo_path))

ActivationStatus = False
try:
    # Открытие ключа реестра
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Pavelo\PC_CONTROLLER")

    # Чтение значения из ключа реестра
    valuee = winreg.QueryValueEx(key, "ActivationStatus")

    if valuee == "true":
        ActivationStatus = True

    # Закрытие ключа реестра
    winreg.CloseKey(key)
except FileNotFoundError:

    def ask_for_activation_key(mode):
        keys = requests.get("https://pc-controller.pp.ua/keys.cfg")
        keys = eval(str(keys.text))
        if mode == "again":
            messagebox.showerror(
                "ОШИБКА ВВОДА КЛЮЧА АКТИВАЦИИ",
                "Вы ввели неправильный ключ активации или с законченным сроком действия. Проверьте Ваш ключ активации и повторите попытку.",
            )
        value = simpledialog.askstring(
            "Первоначальная настройка",
            "Введите ключ активации программы, полученый при покупке приложения.\n\nФормат ключа: M5R8P-Q2B1S-G9L6J-V3S7K-WZ0YH.\nСОБЛЮДАЙТЕ СТРОГО ТАКОЙ ФОРМАТ С ДЕФИСАМИ",
        )
        if value in keys:
            # Открытие или создание ключа реестра
            key = winreg.CreateKey(
                winreg.HKEY_CURRENT_USER, r"Software\Pavelo\PC_CONTROLLER"
            )

            # Запись значения в ключ реестра
            winreg.SetValueEx(key, "ActivationStatus", 0, winreg.REG_SZ, "true")

            # Закрытие ключа реестра
            winreg.CloseKey(key)

            # Открытие или создание ключа реестра
            key = winreg.CreateKey(
                winreg.HKEY_CURRENT_USER, r"Software\Pavelo\PC_CONTROLLER"
            )

            # Запись значения в ключ реестра
            winreg.SetValueEx(key, "ActivationKey", 0, winreg.REG_SZ, value)

            # Закрытие ключа реестра
            winreg.CloseKey(key)
        else:
            ask_for_activation_key("again")

    ask_for_activation_key("first")
try:
    # Открытие ключа реестра
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Pavelo\PC_CONTROLLER")

    # Чтение значения из ключа реестра
    valuee = winreg.QueryValueEx(key, "BotToken")

    token = valuee[0]

    # Закрытие ключа реестра
    winreg.CloseKey(key)
    bot = telebot.TeleBot(str(token))

    try:
        newest_version = requests.get("https://pc-controller.pp.ua/newest_version.cfg")
        if int(str(newest_version.text)) > version:
            # Определение типов данных для функции MessageBox
            MessageBox = ctypes.windll.user32.MessageBoxW
            HWND = 0  # Окно по умолчанию

            popuptitle = "Проверка обновлений"
            popupmessage = "Вышла новая версия программы PC CONTROLLER, Вы хотите поставить её? (нужно будет Ваше участие)"
            # Вывод всплывающего окна
            result = MessageBox(
                HWND, popupmessage, popuptitle, 4, 0x00000001 | 0x00000040
            )
            if result == 6:
                print("yes")
            else:
                print("no")
    except Exception as e:
        print(str(e))

    @bot.message_handler(commands=["defaultinfopopup"])
    def info_popup(message):
        a=check_user(message)
        if a:
            pass
        else:
            return 0
        x = bot.reply_to(message, "ОК, введите заголовок окна")
        bot.register_next_step_handler(x, g)

    def g(message):
        global popuptitle, popupmessage
        popuptitle = str(message.text)
        n = bot.reply_to(
            message, "Хорошо, заголовок задан, задайте текст всплывающего сообщения"
        )
        bot.register_next_step_handler(n, h)

    def h(message):
        global popuptitle, popupmessage
        popupmessage = str(message.text)

        # Определение типов данных для функции MessageBox
        MessageBox = ctypes.windll.user32.MessageBoxW
        HWND = 0  # Окно по умолчанию

        # Вывод всплывающего окна
        MessageBox(HWND, popupmessage, popuptitle, 0, 0x00000001 | 0x00000040)

        # Получение скриншота с помощью pyautogui
        screenshot = pyautogui.screenshot()

        # Сохранение скриншота в файл
        screenshot_path = "screenshot.png"
        screenshot.save(screenshot_path)

        # Отправка скриншота через Telegram
        with open(screenshot_path, "rb") as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption="✔ Popup выскочил",
                reply_to_message_id=message.message_id,
            )

        # Удаление временного файла скриншота
        os.remove(screenshot_path)

    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback(call):
        message = call.message
        if call.data == "block_input":
            user32 = ctypes.windll.user32
            user32.BlockInput(True)
            markup = types.InlineKeyboardMarkup(row_width=2)
            button1 = types.InlineKeyboardButton(
                "🚫⚠ Заблокировать ввод на компьютере от слова совсем (кроме физ. кнопок)",
                callback_data="block_input",
            )
            button2 = types.InlineKeyboardButton(
                "✔⚠ Разблокировать ввод на компьютере", callback_data="allow_input"
            )
            markup.add(button1, button2)
            try:
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text="🚨 Вы зашли в пульт управления вводом на своем компьютере. Выберите действие ниже. ВВОД СЕЙЧАС ЗАКРЫТ",
                    reply_markup=markup,
                )
            except:
                pass

        elif call.data == "allow_input":
            user32 = ctypes.windll.user32
            user32.BlockInput(False)
            markup = types.InlineKeyboardMarkup(row_width=2)
            button1 = types.InlineKeyboardButton(
                "🚫⚠ Заблокировать ввод на компьютере от слова совсем (кроме физ. кнопок)",
                callback_data="block_input",
            )
            button2 = types.InlineKeyboardButton(
                "✔⚠ Разблокировать ввод на компьютере", callback_data="allow_input"
            )
            markup.add(button1, button2)
            try:
                bot.edit_message_text(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    text="🚨 Вы зашли в пульт управления вводом на своем компьютере. Выберите действие ниже. ВВОД СЕЙЧАС ОТКРЫТ",
                    reply_markup=markup,
                )
            except:
                pass
        elif call.data == "disable_access_list":
            dir = winreg.HKEY_CURRENT_USER  # Вы можете изменить на нужный раздел
            tree = r"Software\Pavelo\PC_CONTROLLER"  # Укажите путь к подразделу
            try:
                key = winreg.OpenKey(dir, tree, 0, winreg.KEY_WRITE)
                winreg.SetValue(key, "AccessMode", winreg.REG_SZ, 0, "off")
                bot.edit_message_text(
                    "Вы отключили список доступа (теперь бот доступен всем)",
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                )
            except:
                key = winreg.CreateKey(
                    winreg.HKEY_CURRENT_USER, r"Software\Pavelo\PC_CONTROLLER"
                )

                # Запись значения в ключ реестра
                winreg.SetValueEx(key, "AccessMode", 0, winreg.REG_SZ, "off")

                # Закрытие ключа реестра
                winreg.CloseKey(key)
                bot.edit_message_text(
                    "Вы отключили список доступа (теперь бот доступен всем)",
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                )
        elif call.data == "white_list_mode":
            dir = winreg.HKEY_CURRENT_USER  # Вы можете изменить на нужный раздел
            tree = r"Software\Pavelo\PC_CONTROLLER"  # Укажите путь к подразделу
            try:
                key = winreg.OpenKey(dir, tree, 0, winreg.KEY_WRITE)
                winreg.SetValue(key, "AccessMode", winreg.REG_SZ, 0, "whitelist")
                bot.edit_message_text(
                    "Вы включили список доступа в белый режим (теперь бот доступен только определённым аккаунтам и Вам в том числе)",
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                )
            except:
                key = winreg.CreateKey(
                    winreg.HKEY_CURRENT_USER, r"Software\Pavelo\PC_CONTROLLER"
                )

                # Запись значения в ключ реестра
                winreg.SetValueEx(key, "AccessMode", 0, winreg.REG_SZ, "whitelist")

                # Закрытие ключа реестра
                winreg.CloseKey(key)
                bot.edit_message_text(
                    "Вы включили список доступа в белый режим (теперь бот доступен только определённым аккаунтам и Вам в том числе)",
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                )
        elif call.data == "black_list_mode":
            dir = winreg.HKEY_CURRENT_USER  # Вы можете изменить на нужный раздел
            tree = r"Software\Pavelo\PC_CONTROLLER"  # Укажите путь к подразделу
            try:
                key = winreg.OpenKey(dir, tree, 0, winreg.KEY_WRITE)
                winreg.SetValue(key, "AccessMode", winreg.REG_SZ, 0, "blacklist")
                bot.edit_message_text(
                    "Вы включили список доступа в черный режим (теперь бот доступен всем, кроме указанных в списке)",
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                )
            except:
                key = winreg.CreateKey(
                    winreg.HKEY_CURRENT_USER, r"Software\Pavelo\PC_CONTROLLER"
                )

                # Запись значения в ключ реестра
                winreg.SetValueEx(key, "AccessMode", 0, winreg.REG_SZ, "blacklist")

                # Закрытие ключа реестра
                winreg.CloseKey(key)
                bot.edit_message_text(
                    "Вы включили список доступа в черный режим (теперь бот доступен всем, кроме указанных в списке)",
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                )

    @bot.message_handler(commands=["sharephone"])
    def handle_sharephone(message):
        markup = telebot.types.ReplyKeyboardMarkup(
            one_time_keyboard=True, resize_keyboard=True
        )
        item = telebot.types.KeyboardButton(
            "Отправить номер телефона", request_contact=True
        )
        markup.add(item)
        bot.reply_to(
            message,
            "👇 Поделитесь кнопкой ниже Вашим номером телефона, эта процедура для Вашего аккаунта единоразовая и нужна только для аунтефикации",
            reply_markup=markup,
        )

    @bot.message_handler(content_types=["contact"])
    def contact_received(message):
        contact = message.contact
        phones = {}
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Pavelo\PC_CONTROLLER")
        try:
            phones, _ = winreg.QueryValueEx(key, "PhoneList")
            phones = eval(phones)
        except:
            pass
        winreg.CloseKey(key)
        phones[message.from_user.id] = contact.phone_number
        # Открытие или создание ключа реестра
        key = winreg.CreateKey(
            winreg.HKEY_CURRENT_USER, r"Software\Pavelo\PC_CONTROLLER"
        )
        winreg.CreateKey(key, "PhoneList")
        # Запись значения в ключ реестра
        winreg.SetValueEx(key, "PhoneList", 0, winreg.REG_SZ, str(phones))
        # Закрытие ключа реестра
        winreg.CloseKey(key)
        bot.reply_to(message, "✔ Номер телефона для Вашего аккаунта обновлён успешно")

    @bot.message_handler(commands=["iamowner"])
    def handle_iamowner(message):
        a=check_user(message)
        if a:
            pass
        else:
            return 0
        try:
            # Открытие ключа реестра
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, r"Software\Pavelo\PC_CONTROLLER"
            )

            # Чтение значения из ключа реестра
            owner_id, _ = winreg.QueryValueEx(key, "OwnerId")
            if int(owner_id) == message.from_user.id:
                bot.reply_to(message, "❌ Вы и так владелец.")
            else:
                bot.reply_to(
                    message,
                    "👮‍♂️ К сожалению, Вы не имеете право стать владельцем, так как им стал уже другой человек.",
                )
        except:
            # Открытие или создание ключа реестра
            key = winreg.CreateKey(
                winreg.HKEY_CURRENT_USER, r"Software\Pavelo\PC_CONTROLLER"
            )

            # Запись значения в ключ реестра
            winreg.SetValueEx(
                key, "OwnerId", 0, winreg.REG_SZ, str(message.from_user.id)
            )

            # Закрытие ключа реестра
            winreg.CloseKey(key)
            bot.reply_to(
                message,
                "🥳 Поздравляю! Теперь Вы владелец (доступно управление правами и в дальнейших версиях будет большее) и больше никто не сможет им стать, даже при переустановке программы. Чтобы настроить, напишите /settings",
            )

    @bot.message_handler(commands=["settings"])
    def handle_settings(message):
        a=check_user(message)
        if a:
            pass
        else:
            return 0
        try:
            # Открытие ключа реестра
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, r"Software\Pavelo\PC_CONTROLLER"
            )

            # Чтение значения из ключа реестра
            owner_id, _ = winreg.QueryValueEx(key, "OwnerId")
            if int(owner_id) == message.from_user.id:
                bot.reply_to(
                    message,
                    "👮‍♂️ Добро пожаловать в меню настройки, "
                    + str(message.from_user.first_name)
                    + ".\n\n/changeaccessmode - Поменять режим между черным и белым списком.\n/editlist - Посмотреть и поменять список (независимо от того белый или черный он).\n\nОстальные команды будут добавляться со временем.",
                )
            else:
                bot.reply_to(
                    message,
                    "❌ Произошла ошибка. К сожалению, Вы не имеете доступа к этому меню, так как Вы не являетесь владельцем.",
                )
        except Exception as e:
            print(e)
            bot.reply_to(
                message,
                "❌ Произошла ошибка. К сожалению, Вы не имеете доступа к этому меню, так как владелец еще не настроен. Чтобы настроить владельца, напишите /iamowner",
            )

    @bot.message_handler(commands=["changeaccessmode"])
    def handle_accessmode(message):
        a=check_user(message)
        if a:
            pass
        else:
            return 0
        try:
            # Открытие ключа реестра
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, r"Software\Pavelo\PC_CONTROLLER"
            )

            # Чтение значения из ключа реестра
            accessMode, _ = winreg.QueryValueEx(key, "AccessMode")
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(
                "🏳 Белый список", callback_data="white_list_mode"
            )
            button2 = types.InlineKeyboardButton(
                "🏴 Чёрный список", callback_data="black_list_mode"
            )
            button3 = types.InlineKeyboardButton(
                "🔕 Отключить", callback_data="disable_access_list"
            )
            markup.add(button1, button2, button3)

            if accessMode == "whitelist":
                bot.reply_to(
                    message,
                    "⚠ Сейчас режим доступа стоит: белый список.\n\nЭто значит, что пользоваться ботом смогут только указанные в списке аккаунты\nВыберите режим доступа кнопками ниже.",
                    reply_markup=markup,
                )
            elif accessMode == "blacklist":
                bot.reply_to(
                    message,
                    "⚠ Сейчас режим доступа стоит: чёрный список.\n\nЭто значит, что пользоваться ботом смогут все, кроме указаных в списке аккаунтов.\nВыберите режим доступа кнопками ниже.",
                    reply_markup=markup,
                )
            elif accessMode == "off":
                bot.reply_to(
                    message,
                    "⚠ Сейчас режим доступа не настроен, то есть список не будет работать. Выберите режим доступа кнопками ниже",
                    reply_markup=markup,
                )

        except:
            markup1 = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(
                "🏳 Белый список", callback_data="white_list_mode"
            )
            button2 = types.InlineKeyboardButton(
                "🏴 Чёрный список", callback_data="black_list_mode"
            )
            button3 = types.InlineKeyboardButton(
                "🔕 Отключить", callback_data="disable_access_list"
            )
            markup1.add(button1, button2, button3)
            bot.reply_to(
                message,
                "⚠ Сейчас режим доступа не настроен, то есть список не будет работать. Выберите режим доступа кнопками ниже",
                reply_markup=markup1,
            )

    def listeditortrue(message):
        # Чтение значения из ключа реестра

        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, r"Software\Pavelo\PC_CONTROLLER", winreg.KEY_READ
        )
        accesslist, _ = winreg.QueryValueEx(key, "AccessList")
        accesslist = eval(accesslist)
        winreg.CloseKey(key)  # Закрыть ключ после чтения

        listtoout = ""
        counter = 0
        for i in accesslist:
            counter += 1
            listtoout += str(counter) + ". " + str(i) + "\n"

        if (
            message.reply_to_message
            and counter >= 1
            and message.reply_to_message.text
            == "📃 Вот список тех, кто внесен в либо в чёрный либо в белый список: \n\n"
            + str(listtoout)
            + "\n\nЧтобы произвести операции над списком, напишите сообщение в ответ в таком формате:\n+ @username  (добавить в список юзернэйм)\n- @username  (удалить из списка юзернэйм)\n+ +1234567890  (добавить в список по номеру)\n- +1234567890  (удалить из списка номер).\n\n‼ В случае смены юзернэйма, система не сможет распознать аккаунт, а в случае с номером - им придется делиться с ботом для проверки личности."
        ):
            operator, person = map(str, message.text.split())
            print(operator)
            print(person)

            # Опять открываем ключ для записи
            key = winreg.CreateKey(
                winreg.HKEY_CURRENT_USER, r"Software\Pavelo\PC_CONTROLLER"
            )

            if operator == "+":
                accesslist.append(person)
                accesslist_str = ",".join(map(str, accesslist))
                winreg.SetValueEx(key, "AccessList", 0, winreg.REG_SZ, str(accesslist))
                bot.reply_to(
                    message,
                    "✅ Вы успешно добавили "
                    + person
                    + " в список. Список уже изменён и ждет дальнейшего ввода",
                )
                # Чтение значения из ключа реестра
                accesslist, _ = winreg.QueryValueEx(key, "AccessList")
                accesslist = eval(accesslist)
                listtoout = ""
                counter = 1
                for i in accesslist:
                    listtoout += str(counter) + ". " + str(i) + "\n"
                    counter += 1
                txt = (
                    "📃 Вот список тех, кто внесен в либо в чёрный либо в белый список: \n\n"
                    + str(listtoout)
                    + "\n\nЧтобы произвести операции над списком, напишите сообщение в ответ в таком формате:\n+ @username  (добавить в список юзернэйм)\n- @username  (удалить из списка юзернэйм)\n+ +1234567890  (добавить в список по номеру)\n- +1234567890  (удалить из списка номер).\n\n‼ В случае смены юзернэйма, система не сможет распознать аккаунт, а в случае с номером - им придется делиться с ботом для проверки личности."
                )
                g = bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=message.reply_to_message.id,
                    text=txt,
                )
                bot.register_next_step_handler(g, listeditortrue)
            elif operator == "-":
                try:
                    accesslist.remove(person)
                    winreg.SetValueEx(
                        key, "AccessList", 0, winreg.REG_SZ, str(accesslist)
                    )
                    bot.reply_to(
                        message,
                        "✅ Вы успешно удалили "
                        + person
                        + " из списка. Список уже изменён и ждет дальнейшего ввода",
                    )
                    # Чтение значения из ключа реестра
                    accesslist, _ = winreg.QueryValueEx(key, "AccessList")
                    accesslist = eval(accesslist)
                    listtoout = ""
                    counter = 1
                    for i in accesslist:
                        listtoout += str(counter) + ". " + str(i) + "\n"
                        counter += 1
                    txt = (
                        "📃 Вот список тех, кто внесен в либо в чёрный либо в белый список: \n\n"
                        + str(listtoout)
                        + "\n\nЧтобы произвести операции над списком, напишите сообщение в ответ в таком формате:\n+ @username  (добавить в список юзернэйм)\n- @username  (удалить из списка юзернэйм)\n+ +1234567890  (добавить в список по номеру)\n- +1234567890  (удалить из списка номер).\n\n‼ В случае смены юзернэйма, система не сможет распознать аккаунт, а в случае с номером - им придется делиться с ботом для проверки личности."
                    )
                    g = bot.edit_message_text(
                        chat_id=message.chat.id,
                        message_id=message.reply_to_message.id,
                        text=txt,
                    )
                except:
                    g = bot.reply_to(
                        message, "❌ Не найден аккаунт для удаления. Повторите попытку"
                    )
                bot.register_next_step_handler(g, listeditortrue)

            winreg.CloseKey(key)  # Закрываем ключ после записи

    def listeditorfalse(message):
        accesslist = []
        if (
            message.reply_to_message
            and message.reply_to_message.text
            == "❗ Никого не найдено в списках."
            + "\n\nЧтобы произвести операции над списком, напишите сообщение в ответ в таком формате:\n+ @username  (добавить в список юзернэйм)\n+ +1234567890  (добавить в список по номеру).\n\n‼ В случае смены юзернэйма, система не сможет распознать аккаунт, а в случае с номером - им придется делиться с ботом для проверки личности."
        ):
            operator, person = map(str, message.text.split())
            print(operator)
            print(person)

            # Опять открываем ключ для записи
            key = winreg.CreateKey(
                winreg.HKEY_CURRENT_USER, r"Software\Pavelo\PC_CONTROLLER"
            )

            if operator == "+":
                accesslist.append(person)
                accesslist_str = ",".join(map(str, accesslist))
                winreg.SetValueEx(key, "AccessList", 0, winreg.REG_SZ, str(accesslist))
                bot.reply_to(
                    message,
                    "✅ Вы успешно добавили "
                    + person
                    + " в список. Список уже изменён и ждет дальнейшего ввода",
                )
                # Чтение значения из ключа реестра
                accesslist, _ = winreg.QueryValueEx(key, "AccessList")
                accesslist = eval(accesslist)
                listtoout = ""
                counter = 1
                for i in accesslist:
                    listtoout += str(counter) + ". " + str(i) + "\n"
                    counter += 1
                txt = (
                    "📃 Вот список тех, кто внесен в либо в чёрный либо в белый список: \n\n"
                    + str(listtoout)
                    + "\n\nЧтобы произвести операции над списком, напишите сообщение в ответ в таком формате:\n+ @username  (добавить в список юзернэйм)\n- @username  (удалить из списка юзернэйм)\n+ +1234567890  (добавить в список по номеру)\n- +1234567890  (удалить из списка номер).\n\n‼ В случае смены юзернэйма, система не сможет распознать аккаунт, а в случае с номером - им придется делиться с ботом для проверки личности."
                )
                g = bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=message.reply_to_message.id,
                    text=txt,
                )
                bot.register_next_step_handler(g, listeditortrue)
            elif operator == "-":
                g = bot.reply_to(
                    message,
                    "❌ Вы не можете использовать удаление из пустого списка. Повторите попытку",
                )
                bot.register_next_step_handler(g, listeditorfalse)
            winreg.CloseKey(key)  # Закрываем ключ после записи

    @bot.message_handler(commands=["editlist"])
    def handle_listeditor(message):
        a=check_user(message)
        if a:
            pass
        else:
            return 0
        try:
            # Открытие ключа реестра
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, r"Software\Pavelo\PC_CONTROLLER"
            )

            # Чтение значения из ключа реестра
            accesslist, _ = winreg.QueryValueEx(key, "AccessList")
            accesslist = eval(accesslist)
            listtoout = ""
            counter = 1
            for i in accesslist:
                listtoout += str(counter) + ". " + str(i) + "\n"
                counter += 1
            if len(accesslist) > 0:
                pass
            else:
                raise MyCustomError("Никого не найдено в списке!")
            x = bot.reply_to(
                message,
                "📃 Вот список тех, кто внесен в либо в чёрный либо в белый список: \n\n"
                + str(listtoout)
                + "\n\nЧтобы произвести операции над списком, напишите сообщение в ответ в таком формате:\n+ @username  (добавить в список юзернэйм)\n- @username  (удалить из списка юзернэйм)\n+ +1234567890  (добавить в список по номеру)\n- +1234567890  (удалить из списка номер).\n\n‼ В случае смены юзернэйма, система не сможет распознать аккаунт, а в случае с номером - им придется делиться с ботом для проверки личности.",
            )
            bot.register_next_step_handler(x, listeditortrue)
        except:
            x = bot.reply_to(
                message,
                "❗ Никого не найдено в списках."
                + "\n\nЧтобы произвести операции над списком, напишите сообщение в ответ в таком формате:\n+ @username  (добавить в список юзернэйм)\n+ +1234567890  (добавить в список по номеру).\n\n‼ В случае смены юзернэйма, система не сможет распознать аккаунт, а в случае с номером - им придется делиться с ботом для проверки личности.",
            )
            bot.register_next_step_handler(x, listeditorfalse)

    @bot.message_handler(commands=["warningpopup"])
    def info_popup(message):
        a=check_user(message)
        if a:
            pass
        else:
            return 0
        x = bot.reply_to(message, "ОК, введите заголовок окна")
        bot.register_next_step_handler(x, gc)

    def gc(message):
        global popuptitle, popupmessage
        popuptitle = str(message.text)
        n = bot.reply_to(
            message,
            "Хорошо, заголовок задан, задайте текст всплывающего предупреждения",
        )
        bot.register_next_step_handler(n, hc)

    def hc(message):
        global popuptitle, popupmessage
        popupmessage = str(message.text)

        # Загрузка библиотеки user32.dll
        user32 = ctypes.windll.user32

        # Константы для типа окна и кнопок
        MB_OK = 0x00000000
        MB_ICONWARNING = 0x00000030

        # Вызов функции MessageBoxW из user32.dll
        result = user32.MessageBoxW(
            None, popupmessage, popuptitle, MB_OK | MB_ICONWARNING
        )

        # Получение скриншота с помощью pyautogui
        screenshot = pyautogui.screenshot()

        # Сохранение скриншота в файл
        screenshot_path = "screenshot.png"
        screenshot.save(screenshot_path)

        # Отправка скриншота через Telegram
        with open(screenshot_path, "rb") as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption="✔ Предупреждающий Popup выскочил",
                reply_to_message_id=message.message_id,
            )

        # Удаление временного файла скриншота
        os.remove(screenshot_path)

    @bot.message_handler(commands=["controlinput"])
    def control_input(message):
        a=check_user(message)
        if a:
            pass
        else:
            return 0
        markup = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton(
            "🚫⚠ Заблокировать ввод на компьютере от слова совсем (кроме физ. кнопок)",
            callback_data="block_input",
        )
        button2 = types.InlineKeyboardButton(
            "✔⚠ Разблокировать ввод на компьютере", callback_data="allow_input"
        )
        markup.add(button1, button2)
        bot.reply_to(
            message,
            "🚨 Вы зашли в пульт управления вводом на своем компьютере. Выберите действие ниже. НЕИЗВЕСТНО ОТКРЫТ ЛИ СЕЙЧАС ВВОД",
            reply_markup=markup,
        )

    @bot.message_handler(commands=["inputpopup"])
    def info_popup(message):
        a=check_user(message)
        if a:
            pass
        else:
            return 0
        x = bot.reply_to(message, "ОК, введите заголовок окна")
        bot.register_next_step_handler(x, gcc)

    def gcc(message):
        
        global popuptitle, popupmessage
        popuptitle = str(message.text)
        n = bot.reply_to(
            message, "Хорошо, заголовок задан, задайте текст всплывающего ввода"
        )
        bot.register_next_step_handler(n, hcc)

    def hcc(message):
        
        global popuptitle, popupmessage, answer
        popupmessage = str(message.text)
        user_input = pymsgbox.prompt(popupmessage, popuptitle)
        user_id = message.from_user.id

        print(user_input)
        if user_input == None:
            user_input = "ответа не последовало"

        # Получение скриншота с помощью pyautogui
        screenshot = pyautogui.screenshot()

        # Сохранение скриншота в файл
        screenshot_path = "screenshot.png"
        screenshot.save(screenshot_path)

        # Отправка скриншота через Telegram
        with open(screenshot_path, "rb") as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption="✔ Popup для ввода текста выскочил, ответ: " + str(user_input),
                reply_to_message_id=message.message_id,
            )

        # Удаление временного файла скриншота
        os.remove(screenshot_path)

    @bot.message_handler(commands=["okcancelpopup"])
    def info_popup(message):
        a=check_user(message)
        if a:
            pass
        else:
            return 0
        x = bot.reply_to(message, "ОК, введите заголовок окна")
        bot.register_next_step_handler(x, gb)

    def gb(message):
        
        global popuptitle, popupmessage
        popuptitle = str(message.text)
        n = bot.reply_to(
            message,
            "Хорошо, заголовок задан, задайте текст всплывающего сообщения с кнопками ОК / ОТМЕНА",
        )
        bot.register_next_step_handler(n, hb)

    def hb(message):
        
        global popuptitle, popupmessage
        popupmessage = str(message.text)

        # Определение типов данных для функции MessageBox
        MessageBox = ctypes.windll.user32.MessageBoxW
        HWND = 0  # Окно по умолчанию

        # Вывод всплывающего окна
        result = MessageBox(HWND, popupmessage, popuptitle, 1, 0x00000001 | 0x00000040)

        # Получение скриншота с помощью pyautogui
        screenshot = pyautogui.screenshot()

        # Сохранение скриншота в файл
        screenshot_path = "screenshot.png"
        screenshot.save(screenshot_path)

        # Проверка результата
        if result == 1:  # Если нажата кнопка "OK"
            btn = "ОК"
        elif result == 2:  # Если нажата кнопка "Cancel"
            btn = "ОТМЕНА / ЗАКРЫТИЕ"
        else:  # Если окно закрыто без нажатия кнопок
            btn = "НИКАКАЯ"
        # Отправка скриншота через Telegram
        with open(screenshot_path, "rb") as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption="✔ Popup с кнопками ОК / ОТМЕНА выскочил, нажата кнопка "
                + str(btn),
                reply_to_message_id=message.message_id,
            )

        # Удаление временного файла скриншота
        os.remove(screenshot_path)

    @bot.message_handler(commands=["reboot"])
    def reboot(message):
        a=check_user(message)
        if a:
            pass
        else:
            return 0
        os.system("shutdown /r /t 0")
        time.sleep(1)
        # Получение скриншота с помощью pyautogui
        screenshot = pyautogui.screenshot()

        # Сохранение скриншота в файл
        screenshot_path = "screenshot.png"
        screenshot.save(screenshot_path)

        # Отправка скриншота через Telegram
        with open(screenshot_path, "rb") as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption="✔ Команда на перезагрузку компьютера отправлена",
                reply_to_message_id=message.message_id,
            )

        # Удаление временного файла скриншота
        os.remove(screenshot_path)

    @bot.message_handler(commands=["shutdown"])
    def reboot(message):
        a=check_user(message)
        if a:
            pass
        else:
            return 0
        os.system("shutdown /s /t 0")
        time.sleep(1)
        # Получение скриншота с помощью pyautogui
        screenshot = pyautogui.screenshot()

        # Сохранение скриншота в файл
        screenshot_path = "screenshot.png"
        screenshot.save(screenshot_path)

        # Отправка скриншота через Telegram
        with open(screenshot_path, "rb") as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption="✔ Команда на выключение компьютера отправлена",
                reply_to_message_id=message.message_id,
            )

        # Удаление временного файла скриншота
        os.remove(screenshot_path)

    @bot.message_handler(commands=["lock"])
    def lock_workstation(message):
        a=check_user(message)
        if a:
            pass
        else:
            return 0
        subprocess.call("rundll32.exe user32.dll,LockWorkStation")
        time.sleep(2)
        # Получение скриншота с помощью pyautogui
        screenshot = pyautogui.screenshot()

        # Сохранение скриншота в файл
        screenshot_path = "screenshot.png"
        screenshot.save(screenshot_path)

        # Отправка скриншота через Telegram
        with open(screenshot_path, "rb") as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption="✔ Компьютер заблокирован",
                reply_to_message_id=message.message_id,
            )

        # Удаление временного файла скриншота
        os.remove(screenshot_path)

    @bot.message_handler(commands=["system_info"])
    def send_sys_info(message):
        global version
        a=check_user(message)
        if a:
            pass
        else:
            return 0
        # Информация о системе
        system_info = platform.uname()
        system_info_str = (
            f"Версия программы: {version}\n"
            f"Система: {system_info.system}\n"
            f"Узел: {system_info.node}\n"
            f"Выпуск: {system_info.release}\n"
            f"Версия: {system_info.version}\n"
            f"Машина: {system_info.machine}\n"
            f"Процессор: {system_info.processor}\n"
        )

        # Информация о CPU
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)

        cpu_info_str = (
            f"Количество процессоров: {cpu_count}\n"
            f"Максимальная частота: {cpu_freq.max:.2f} МГц\n"
            f"Минимальная частота: {cpu_freq.min:.2f} МГц\n"
            f"Средняя загрузка CPU: {sum(cpu_percent) / cpu_count:.2f}%\n"
        )

        # Информация о памяти
        memory_info = psutil.virtual_memory()
        memory_info_str = (
            f"Всего памяти: {memory_info.total / 2 ** 30:.2f} ГБ\n"
            f"Доступно памяти: {memory_info.available / 2 ** 30:.2f} ГБ\n"
            f"Использовано памяти: {memory_info.percent:.2f}%\n"
        )

        # Формирование сообщения
        message_text = f"{system_info_str}\n{cpu_info_str}\n{memory_info_str}"

        # Если сообщение превышает ограничение в 1024 символа, обрезаем его
        if len(message_text) > 1024:
            message_text = message_text[:1020] + "..."

        message_text = message_text + "\n\nОткрытые приложения:\n"
        # Получение списка всех открытых окон
        open_windows = pygetwindow.getAllTitles()

        # Вывод списка открытых приложений
        for window in open_windows:
            message_text = message_text + str(window) + "\n"

        bot.reply_to(message, str(message_text))

    @bot.message_handler(commands=["camera"])
    def send_photo(message):
        a=check_user(message)
        if a:
            pass
        else:
            return 0
        # Захват изображения с камеры
        camera = cv2.VideoCapture(0)
        return_value, image = camera.read()
        camera.release()

        # Сохранение изображения на диск
        image_path = "photo.jpg"
        cv2.imwrite(image_path, image)

        # Отправка изображения через Telegram
        with open(image_path, "rb") as photo:
            bot.send_photo(
                message.chat.id, photo, reply_to_message_id=message.message_id
            )

        # Удаление временного файла
        os.remove(image_path)

    # Handle '/start' command
    @bot.message_handler(commands=["start"])
    def handle_start(message):
        a=check_user(message)
        if a:
            pass
        else:
            return 0
        bot.reply_to(
            message,
            "Добро пожаловать, "
            + str(message.from_user.first_name)
            + "!\n\n🥳 Все работает замечательно, Ваш компьютер сейчас включен и работает под учетной записью <em>"
            + str(getpass.getuser())
            + "</em>. Тут Вы полноценно можете управлять своим компьютером абсолютно безопасно. Ниже написаны возможные команды. Выберите нужную.\n\n/camera - сделать снимок с основной камеры компьютера и отправить сюда\n/system_info - информация о системе\n/lock - заблокировать компьютер удалённо\n/defaultinfopopup - вывести информационное всплывающее сообщение с кнопкой ОК\n/okcancelpopup - вывести информационное всплывающее сообщение с кнопкой ОК / ОТМЕНА (нажатая кнопка прийдет сюда)\n/warningpopup - вывести предупреждающее всплывающее сообщение с кнопкой ОК\n/inputpopup - вывести всплывающее окно с вводом данных на ПК (ответ прийдет сюда)\n/shutdown - выключить компьютер\n/reboot - перезагрузить компьютер\n/controlinput - пульт управления разрешением ввода на компьютере",
            parse_mode="HTML",
        )
    bot.set_my_commands([
                types.BotCommand("start", "Главное меню бота"),
                types.BotCommand("iamowner", "Я владелец"),
                types.BotCommand("settings", "Настройки"),
                types.BotCommand("sharephone", "Поделиться номером телефона с ботом"),
                types.BotCommand("camera", "сделать снимок с основной камеры компьютера и отправить сюда"),
                types.BotCommand("system_info", "Информация о системе"),
                types.BotCommand("lock", "заблокировать компьютер удалённо"),
                types.BotCommand("defaultinfopopup", "Вывести информационное всплывающее сообщение с кнопкой ОК"),
                types.BotCommand("okcancelpopup", "Вывести информационное всплывающее сообщение с кнопкой ОК / ОТМЕНА (нажатая кнопка прийдет сюда)"),
                types.BotCommand("warningpopup", "Вывести предупреждающее всплывающее сообщение с кнопкой ОК"),
                types.BotCommand("inputpopup", "Вывести всплывающее окно с вводом данных на ПК (ответ прийдет сюда)"),
                types.BotCommand("shutdown", "Выключить компьютер"),
                types.BotCommand("reboot", "Перезагрузить компьютер"),
                types.BotCommand("controlinput", "Пульт управления разрешением ввода на компьютере"),
                
                ])
    # Start the bot
    bot.polling()
except FileNotFoundError:

    def token_ask_after_install(mode):
        if mode == "again":
            messagebox.showerror(
                "ОШИБКА ПЕРВОНАЧАЛЬНОЙ НАСТРОЙКИ",
                "Введенный токен не соответствует токену ботов в Telegram.\n\nПример токена ботов в Telegram: 1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890\n\nПроверьте Ваш токен на правильность и повторите ввод, нажав кнопку ниже",
            )
        value = simpledialog.askstring(
            "Первоначальная настройка",
            "Введите токен для Вашего бота, полученый в @BotFather в Telegram. Этот токен будет храниться ТОЛЬКО на Вашем устройстве, мы не сможем получить к нему доступ",
        )

        if value == None or len(value) < 46:
            token_ask_after_install("again")
        else:
            # Открытие или создание ключа реестра
            key = winreg.CreateKey(
                winreg.HKEY_CURRENT_USER, r"Software\Pavelo\PC_CONTROLLER"
            )

            # Запись значения в ключ реестра
            winreg.SetValueEx(key, "BotToken", 0, winreg.REG_SZ, value)



            # Запись значения в ключ реестра
            phonelist = {}
            winreg.SetValueEx(key, "PhoneList", 0, winreg.REG_SZ, str("{}"))

            
            winreg.SetValueEx(key, "AccessMode", 0, winreg.REG_SZ, str("off"))

            
            accesslist = []
            winreg.SetValueEx(key, "AccessList", 0, winreg.REG_SZ, str(accesslist))
            winreg.SetValueEx(key, "OwnerId", 0, winreg.REG_SZ, str(""))

            result = messagebox.askyesno(
                "Первоначальная настройка",
                "Вы хотите чтобы программа запускалась вместе с системой?!",
            )
            if result:
                script_path = os.path.realpath(__file__)
                desktop_path = (
                    str(os.getenv("APPDATA"))
                    + "\Microsoft\Windows\Start Menu\Programs\Startup"
                )
                shell = Dispatch("WScript.Shell")
                shortcut = shell.CreateShortcut(desktop_path + "\\PC_CONTROLLER.lnk")
                shortcut.TargetPath = script_path
                shortcut.WorkingDirectory = desktop_path
                shortcut.IconLocation = str(os.getcwd()) + "/logo.ico"
                shortcut.Save()
                messagebox.showwarning(
                    "Внимание",
                    "Произошли небольшие изменения в программе. Если Вы ставите эту программу впервые на эту систему, скорее всего, у Вас не указан Владелец (тот, кто сможет настраивать доступы и многое другое в будущем). Это очень опасно, если Вы дадите доступ к этому боту другому человеку без настройки прав. Мы настоятельно рекомендуем прямо сейчас настроить права.\n\nДля выполнения настройки владельца (он может быть только один), перейдите в бота и введите /iamowner. После этого у Вас будут настроены права на этой системе и только с Вашего аккаунта Telegram можно будет управлять всеми.",
                )
                messagebox.showinfo(
                    "Первоначальная настройка",
                    "Поздравляем! Первоначальная настройка закончена, перезапустите компьютер",
                )
            else:
                result = messagebox.askyesno(
                    "Первоначальная настройка",
                    "В таком случае, Вы хотите создать ярлык на рабочем столе?!",
                )
                if result:
                    script_path = os.path.realpath(__file__)
                    desktop_path = winshell.desktop()
                    shell = Dispatch("WScript.Shell")
                    shortcut = shell.CreateShortcut(
                        desktop_path + "\\PC_CONTROLLER.lnk"
                    )
                    shortcut.TargetPath = script_path
                    shortcut.WorkingDirectory = desktop_path
                    shortcut.IconLocation = str(os.getcwd()) + "/logo.ico"
                    shortcut.Save()

                else:
                    pass
                messagebox.showwarning(
                    "Внимание",
                    "Произошли небольшие изменения в программе. Если Вы ставите эту программу впервые на эту систему, скорее всего, у Вас не указан Владелец (тот, кто сможет настраивать доступы и многое другое в будущем). Это очень опасно, если Вы дадите доступ к этому боту другому человеку без настройки прав. Мы настоятельно рекомендуем прямо сейчас настроить права.\n\nДля выполнения настройки владельца (он может быть только один), перейдите в бота и введите /iamowner. После этого у Вас будут настроены права на этой системе и только с Вашего аккаунта Telegram можно будет управлять всеми.",
                )
                
                messagebox.showinfo(
                    "Первоначальная настройка",
                    "Поздравляем! Первоначальная настройка закончена, перезапустите программу",
                )

    token_ask_after_install("first")
