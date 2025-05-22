import telebot
import psycopg2
from datetime import datetime

TOKEN = '🐱‍👤'  
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'YOUR_PASSWORD'
DB_HOST = 'localhost'
DB_PORT = '5432'

ADMIN_LOGIN = "admin"
ADMIN_PASSWORD = "1234"
admin_logged_in_users = set()  

bot = telebot.TeleBot(TOKEN)

try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        options='-c client_encoding=UTF8'
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS banned_users (
            user_id BIGINT PRIMARY KEY
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            deadline DATE,
            priority TEXT CHECK (priority IN ('past', 'o‘rta', 'yuqori')),
            status TEXT DEFAULT 'Bajarilmoqda'
        );
    """)
    conn.commit()
except Exception as e:
    print(f"❌ Ma'lumotlar bazasiga ulanishda xato: {e}")
    exit()

def is_banned(user_id):
    cursor.execute("SELECT 1 FROM banned_users WHERE user_id = %s", (user_id,))
    return cursor.fetchone() is not None

@bot.message_handler(commands=['start'])
def start(message):
    if is_banned(message.from_user.id):
        bot.send_message(message.chat.id, "🚫 Siz bloklangansiz.")
        return
    bot.send_message(message.chat.id, "👋 Salom! Bu vazifalarni boshqarish botidir.\n/help buyruqni ishlatib, buyruqlar ro'yxatini ko'ring.")

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "Bot buyruqlari:\n"
        "/start - Botni ishga tushirish\n"
        "/mytasks - Mening vazifalarim\n"
        "/newtask - Yangi vazifa yaratish\n"
        "/updatetask - Vazifani yangilash\n"
        "/deletetask - Vazifani o'chirish\n"
        "/manage_task - Vazifani boshqarish\n"
        "/admin_login - Administrator sifatida kirish\n"
        "/alltasks - Barcha vazifalar (admin)\n"
        "/ban - Foydalanuvchini bloklash (admin)\n"
        "/unban - Foydalanuvchini blokdan chiqarish (admin)\n"
        "/admin_manage - Foydalanuvchilar vazifalarini boshqarish (admin)\n"
    )
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['admin_login'])
def admin_login(message):
    msg = bot.send_message(message.chat.id, "Login va parolni login:parol formatida kiriting.")
    bot.register_next_step_handler(msg, process_admin_login)

def process_admin_login(message):
    try:
        login, password = message.text.split(":")
        if login == ADMIN_LOGIN and password == ADMIN_PASSWORD:
            admin_logged_in_users.add(message.from_user.id)
            bot.send_message(message.chat.id, "✅ Siz administrator sifatida kirdingiz.")
        else:
            bot.send_message(message.chat.id, "❌ Noto'g'ri login yoki parol.")
    except Exception:
        bot.send_message(message.chat.id, "❗ Noto'g'ri format. Login:parol formatida kiriting.")

def is_admin(user_id):
    return user_id in admin_logged_in_users

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if not is_admin(message.from_user.id):
        bot.send_message(message.chat.id, "❌ Faqat admin bu buyruqni ishlatishi mumkin.")
        return
    msg = bot.send_message(message.chat.id, "Bloklash uchun foydalanuvchi ID'sini kiriting:")
    bot.register_next_step_handler(msg, process_ban_user)

def process_ban_user(message):
    try:
        user_id = int(message.text)
        cursor.execute("INSERT INTO banned_users (user_id) VALUES (%s) ON CONFLICT DO NOTHING", (user_id,))
        conn.commit()
        bot.send_message(message.chat.id, f"✅ Foydalanuvchi {user_id} bloklandi.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Xato: {e}")

@bot.message_handler(commands=['unban'])
def unban_user(message):
    if not is_admin(message.from_user.id):
        bot.send_message(message.chat.id, "❌ Faqat admin bu buyruqni ishlatishi mumkin.")
        return
    msg = bot.send_message(message.chat.id, "Blokdan chiqarish uchun foydalanuvchi ID'sini kiriting:")
    bot.register_next_step_handler(msg, process_unban_user)

def process_unban_user(message):
    try:
        user_id = int(message.text)
        cursor.execute("DELETE FROM banned_users WHERE user_id = %s", (user_id,))
        conn.commit()
        bot.send_message(message.chat.id, f"✅ Foydalanuvchi {user_id} blokdan chiqarildi.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Xato: {e}")

@bot.message_handler(commands=['alltasks'])
def all_tasks(message):
    if not is_admin(message.from_user.id):
        bot.send_message(message.chat.id, "❌ Siz admin emassiz.")
        return
    cursor.execute('SELECT id, user_id, name, description, deadline, priority, status FROM tasks ORDER BY id')
    tasks = cursor.fetchall()
    if not tasks:
        bot.send_message(message.chat.id, "📭 Hozircha vazifalar yo'q.")
        return
    response = "🗂 Barcha vazifalar:\n\n"
    for t in tasks:
        task_id, user_id, name, desc, deadline, priority, status = t
        response += (
            f"👤 Foydalanuvchi ID: {user_id}\n"
            f"🔹 Vazifa ID: {task_id}\n"
            f"📌 Nomi: {name}\n"
            f"📄 Tavsifi: {desc}\n"
            f"📅 Deddline: {deadline}\n"
            f"⚙️ Prioritet: {priority}\n"
            f"📍 Status: {status}\n\n"
        )
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['newtask'])
def new_task(message):
    if is_banned(message.from_user.id):
        bot.send_message(message.chat.id, "🚫 Siz bloklangansiz.")
        return
    msg = bot.send_message(message.chat.id, "Vazifaning nomini kiriting:")
    bot.register_next_step_handler(msg, process_task_name)

def process_task_name(message):
    task_name = message.text
    msg = bot.send_message(message.chat.id, "Vazifaning tavsifini kiriting:")
    bot.register_next_step_handler(msg, process_task_description, task_name)

def process_task_description(message, task_name):
    task_description = message.text
    msg = bot.send_message(message.chat.id, "Deddline kiriting (format YYYY-MM-DD):")
    bot.register_next_step_handler(msg, process_task_deadline, task_name, task_description)

def process_task_deadline(message, task_name, task_description):
    task_deadline_str = message.text
    try:
        deadline_date = datetime.strptime(task_deadline_str, "%Y-%m-%d").date()
        msg = bot.send_message(message.chat.id, "Prioritetni tanlang (past / o‘rta / yuqori):")
        bot.register_next_step_handler(msg, process_task_priority, task_name, task_description, deadline_date)
    except ValueError:
        msg = bot.send_message(message.chat.id, "❌ Noto'g'ri sana formati! YYYY-MM-DD formatida kiriting:")
        bot.register_next_step_handler(msg, process_task_deadline, task_name, task_description)

def process_task_priority(message, task_name, task_description, deadline_date):
    task_priority = message.text.lower()
    if task_priority not in ['past', "o‘rta", 'yuqori']:
        msg = bot.send_message(message.chat.id, "❌ Noto'g'ri prioritet! past / o‘rta / yuqori dan tanlang:")
        bot.register_next_step_handler(msg, process_task_priority, task_name, task_description, deadline_date)
        return

    try:
        cursor.execute(
            'INSERT INTO tasks (user_id, name, description, deadline, priority, status) VALUES (%s, %s, %s, %s, %s, %s)',
            (message.from_user.id, task_name, task_description, deadline_date, task_priority, 'Bajarilmoqda')
        )
        conn.commit()
        bot.send_message(message.chat.id, "✅ Vazifa yaratildi!")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Xato: {e}")

@bot.message_handler(commands=['mytasks'])
def my_tasks(message):
    if is_banned(message.from_user.id):
        bot.send_message(message.chat.id, "🚫 Siz bloklangansiz.")
        return
    user_id = message.from_user.id
    cursor.execute('SELECT id, name, description, deadline, priority, status FROM tasks WHERE user_id = %s ORDER BY id', (user_id,))
    tasks = cursor.fetchall()
    if not tasks:
        bot.send_message(message.chat.id, "Sizda hozircha vazifalar yo'q.")
        return
    response = "📝 Sizning vazifalaringiz:\n\n"
    for task in tasks:
        task_id, name, desc, deadline, priority, status = task
        response += (
            f"🔹 ID: {task_id}\n"
            f"📌 Nomi: {name}\n"
            f"📄 Tavsifi: {desc}\n"
            f"📅 Deddline: {deadline}\n"
            f"⚙️ Prioritet: {priority}\n"
            f"📍 Status: {status}\n\n"
        )
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['updatetask'])
def update_task(message):
    if is_banned(message.from_user.id):
        bot.send_message(message.chat.id, "🚫 Siz bloklangansiz.")
        return
    msg = bot.send_message(message.chat.id, "Yangilanishi kerak bo'lgan vazifa ID'sini kiriting:")
    bot.register_next_step_handler(msg, process_update_id)

def process_update_id(message):
    task_id = message.text
    msg = bot.send_message(message.chat.id, "Yangi vazifa nomini kiriting:")
    bot.register_next_step_handler(msg, process_update_name, task_id)

def process_update_name(message, task_id):
    new_name = message.text
    msg = bot.send_message(message.chat.id, "Yangi vazifa tavsifini kiriting:")
    bot.register_next_step_handler(msg, process_update_description, task_id, new_name)

def process_update_description(message, task_id, new_name):
    new_desc = message.text
    try:
        cursor.execute('UPDATE tasks SET name = %s, description = %s WHERE id = %s AND user_id = %s', (new_name, new_desc, task_id, message.from_user.id))
        conn.commit()
        bot.send_message(message.chat.id, "✅ Vazifa yangilandi!")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Xato: {e}")

@bot.message_handler(commands=['deletetask'])
def delete_task(message):
    if is_banned(message.from_user.id):
        bot.send_message(message.chat.id, "🚫 Siz bloklangansiz.")
        return
    msg = bot.send_message(message.chat.id, "O'chirilishi kerak bo'lgan vazifa ID'sini kiriting:")
    bot.register_next_step_handler(msg, process_delete_task)

def process_delete_task(message):
    task_id = message.text
    try:
        cursor.execute('DELETE FROM tasks WHERE id = %s AND user_id = %s', (task_id, message.from_user.id))
        conn.commit()
        bot.send_message(message.chat.id, "✅ Vazifa o'chirildi.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Xato: {e}")

print("🚀 Bot ishga tushirildi!")
bot.infinity_polling()
