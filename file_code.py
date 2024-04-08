from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command, StateFilter
from aiogram.fsm.storage.memory import MemoryStorage
import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
import sqlite3
from sqlite3 import Error
import logging

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="6907302907:AAGTeedN1-vEm1hy5qf3V9iBLhPUQWPUYgw")
# Диспетчер
dp = Dispatcher(storage=MemoryStorage())
f = ''
PAYMENTS_PROVIDER_TOKEN = '381764678:TEST:81209'
PRICE = types.LabeledPrice(label='Онлайн-консультация', amount=10000)


async def send_main_menu(message: types.Message):
    """
    Функция для отправки главного меню
    """
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="ученик", callback_data="button1"))
    builder.add(types.InlineKeyboardButton(text="преподаватель", callback_data="button2"))
    builder.adjust(1)  # Регулирует количество кнопок в ряду
    await message.answer("Выберите свою роль",
                         reply_markup=builder.as_markup())


@dp.callback_query(F.data == 'button1')
async def process_marketplace(callback: CallbackQuery):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Химия", callback_data="button2"))
    builder.add(types.InlineKeyboardButton(text="Физика",
                                           callback_data="button3"))
    builder.add(types.InlineKeyboardButton(text="Русский язык",
                                           callback_data="button4"))
    builder.add(types.InlineKeyboardButton(text="ОБЖ",
                                           callback_data="button5"))
    builder.add(types.InlineKeyboardButton(text="Математика",
                                           callback_data="button6"))
    builder.add(types.InlineKeyboardButton(text="История",
                                           callback_data="button7"))
    builder.add(types.InlineKeyboardButton(text="Обществознание",
                                           callback_data="button8"))
    builder.add(types.InlineKeyboardButton(text="География",
                                           callback_data="button9"))
    builder.add(types.InlineKeyboardButton(text="Биология",
                                           callback_data="button10"))
    builder.add(types.InlineKeyboardButton(text="Английский язык",
                                           callback_data="button11"))
    builder.add(types.InlineKeyboardButton(text="Информатика",
                                           callback_data="button12"))
    builder.add(types.InlineKeyboardButton(text="Физкультура",
                                           callback_data="button13"))
    builder.add(types.InlineKeyboardButton(text="Литература",
                                           callback_data="button14"))
    builder.add(types.InlineKeyboardButton(text="Технология",
                                           callback_data="button15"))
    # Кнопка "Назад"
    builder.add(types.InlineKeyboardButton(text="Назад", callback_data="back1"))
    builder.adjust(1)  # Регулирует количество кнопок в ряду
    await callback.message.answer("Ниже представлен список предметов:", reply_markup=builder.as_markup())

"""
@dp.callback_query(F.data == 'button2')
async def process_marketplace(callback: CallbackQuery):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="удалить предмет", callback_data="button3"))
    builder.add(types.InlineKeyboardButton(text="добавить предмет", callback_data="button4"))
    builder.add(types.InlineKeyboardButton(text="удалить тему", callback_data="button5"))
    builder.add(types.InlineKeyboardButton(text="добавить тему", callback_data="button6"))
    builder.add(types.InlineKeyboardButton(text="удалить лекцию", callback_data="button7"))
    builder.add(types.InlineKeyboardButton(text="добавить лекцию", callback_data="button8"))
    builder.add(types.InlineKeyboardButton(text="удалить запись лекции", callback_data="button9"))
    builder.add(types.InlineKeyboardButton(text="добавить запись лекции", callback_data="button10"))
    builder.adjust(2)  # Регулирует количество кнопок в ряду
    await callback.message.answer("Ниже представлен список доступных команд:", reply_markup=builder.as_markup())
"""

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await send_main_menu(message)


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


CREATE_DATABASE_QUERY1 = """
CREATE TABLE IF NOT EXISTS lectures (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  subject TEXT NOT NULL,
  theme TEXT NOT NULL,
  number INTEGER NOT NULL,
  text_file TEXT NOT NULL,
  video_file TEXT NOT NULL
);
"""

DROP_DATABASE_QUERY1 = """
DROP TABLE lectures;
"""

logging.basicConfig(level=logging.INFO, filename="../../../Downloads/logs.log", filemode="a")


def create_connection(path):
    conn = None
    try:
        conn = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return conn


def execute_query(conn, query):
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
        print("Query executed successfully -", query.replace("\n", " "))
        logging.info("Query executed successfully -" + query.replace("\n", " "))
    except Error as e:
        print(query)
        print(f"The error '{e}' occurred")
        logging.info(f"The error '{e}' occurred in '" + query + "'")


def execute_read_query(conn, query):
    cursor = conn.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
        return result
    except Error as e:
        print(query)
        print(f"The error '{e}' occurred")


def INIT(conn):
    """Creating database if not created"""
    print("***********\nDB initialization!\n***********")
    execute_query(conn, CREATE_DATABASE_QUERY1)


def DROP_ALL(conn):
    """Dropping database. Warning, may remove something important"""
    print("***********\nDB dropping!\n***********")
    execute_query(conn, DROP_DATABASE_QUERY1)


def RECREATE(conn):
    """Just... dropping database and creating it again"""
    DROP_ALL(conn)
    INIT(conn)


def load_lecture(conn, subject, theme, number, text_file, video_file):
    """Loading a lecture into database"""\
    "загрузка лекции в бд"
    execute_query(conn,
                  f"INSERT INTO lectures (subject, theme, number, text_file, video_file) VALUES (\"{subject}\", \"{theme}\", {number}, \"{text_file}\", \"{video_file}\")")


def get_lectures(conn, subject):
    """Reading all the lectures with given subject"""
    'получение лекции'
    return execute_read_query(conn, f"SELECT * FROM lectures WHERE subject=\"{subject}\"")


if __name__ == "__main__":
    conn = create_connection("../../../Downloads/db.db")
    INIT(conn)
    load_lecture(conn, "Математика", "Дифференциальные уравнения", 1, "./say.gex", "../../..")
    print(get_lectures(conn, 'Математика'))
    asyncio.run(main())
