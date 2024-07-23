import telebot
from telebot import types
import datetime
import json

API_TOKEN = '7242276895:AAG9iJTP1_5uQ6rgIjnNvPQq429OWs05XdU'
ADMIN_IDS = [6964973925]
ADMIN_USERNAME = '@AaravFrr'
qr_code = 'path_to_default_qr_image.png'

bot = telebot.TeleBot(API_TOKEN)

user_balances = {}
stocks = {'prepaid': {}, 'oldig': {}, 'indoig': {}, 'freshig': {}}
stock_counts = {'prepaid': 0, 'oldig': 0, 'indoig': 0, 'freshig': 0}
total_stock_sold = 0

user_ids = set()

def track_user(message):
    user_ids.add(message.from_user.id)
    if message.from_user.id not in user_balances:
        user_balances[message.from_user.id] = 0


def create_main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('ADD FUNDS')
    btn2 = types.KeyboardButton('BUY PREPAID IG')
    btn3 = types.KeyboardButton('BUY OLD IG')
    btn4 = types.KeyboardButton('BUY INDO IG')
    btn5 = types.KeyboardButton('MY BALANCE')
    btn6 = types.KeyboardButton('STOCK')
    btn7 = types.KeyboardButton('Fresh IG')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    return markup

def create_back_button():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(types.KeyboardButton('BACK'))
    return markup

def create_transparent_check_button():
    markup = types.InlineKeyboardMarkup()
    check_button = types.InlineKeyboardButton('CHECK ✅', callback_data='check_funds')
    markup.add(check_button)
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    track_user(message)
    markup = create_main_menu()
    bot.send_message(message.chat.id, "🔥WELCOME TO PREPAID/INDO IG/OLD IG/FRESH IG SELLER BOT\n\n😢ANY PROBLEM? CONTACT @AaravFrr", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'ADD FUNDS')
def add_funds(message):
    track_user(message)
    bot.send_message(message.chat.id, "PLEASE WAIT.. GENERATING QR🤖")
    bot.send_photo(message.chat.id, open(qr_code, 'rb'), "PAY ON THIS QR AND CLICK ON CHECK TO ADD YOUR BALANCE ✅\n\n❤️YOU CAN ADD BALANCE TO YOUR ACCOUNT BY CLICKING ON THE CHECK✅ BUTTON ❤️", reply_markup=create_transparent_check_button())

@bot.callback_query_handler(func=lambda call: call.data == 'check_funds')
def check_funds(call):
    bot.send_message(call.message.chat.id, f"Send transaction ID and screenshot of payment to {ADMIN_USERNAME} to add funds.")

@bot.message_handler(func=lambda message: message.text == 'BUY PREPAID IG')
def buy_prepaid_ig(message):
    track_user(message)
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    for i in range(1, 21):
        markup.add(types.KeyboardButton(f'BUY PREPAID {i}'))
    markup.add(types.KeyboardButton('BACK'))
    bot.send_message(message.chat.id, "PRICE PER PREPAID IG IS :- ₹50\n\nIF YOU WANT TO LEARN ABOUT GUARANTEE THEN DM @AaravFrr", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'BUY OLD IG')
def buy_old_ig(message):
    track_user(message)
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    for i in range(1, 21):
        markup.add(types.KeyboardButton(f'BUY OLD IG {i}'))
    markup.add(types.KeyboardButton('BACK'))
    bot.send_message(message.chat.id, "SELECT AN OLD IG ACCOUNT TO BUY", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'BUY INDO IG')
def buy_indo_ig(message):
    track_user(message)
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    for i in range(1, 21):
        markup.add(types.KeyboardButton(f'BUY INDO IG {i}'))
    markup.add(types.KeyboardButton('BACK'))
    bot.send_message(message.chat.id, "SELECT AN INDO IG ACCOUNT TO BUY", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'BACK')
def go_back(message):
    track_user(message)
    markup = create_main_menu()
    bot.send_message(message.chat.id, "Main Menu", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'MY BALANCE')
def check_balance(message):
    track_user(message)
    balance = user_balances.get(message.from_user.id, 0)
    bot.send_message(message.chat.id, f"Your balance is: ₹{balance}")

@bot.message_handler(func=lambda message: message.text == 'STOCK')
def check_stock(message):
    track_user(message)
    stock_msg = "►   𝐀𝐕𝐀𝐈𝐋𝐀𝐁𝐋𝐄 𝐒𝐓𝐎𝐂𝐊   ◄\n\n"
    stock_msg += f"IG+CC  ► {stock_counts['prepaid']}\n"
    stock_msg += f"𝙸𝙽𝙳𝙾 𝙸𝙶           ► {stock_counts['indoig']}\n"
    stock_msg += f"𝙾𝙻𝙳 𝙸𝙶           ► {stock_counts['oldig']}\n"
    stock_msg += f"𝙵𝚁𝙴𝚂𝙷 𝙸𝙶         ► {stock_counts['freshig']}\n"
    bot.send_message(message.chat.id, stock_msg)

@bot.message_handler(func=lambda message: message.text == 'Fresh IG')
def fresh_ig_menu(message):
    track_user(message)
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    for i in range(1, 21):
        markup.add(types.KeyboardButton(f'BUY FRESH IG {i}'))
    markup.add(types.KeyboardButton('BACK'))
    bot.send_message(message.chat.id, "SELECT A FRESH IG ACCOUNT TO BUY", reply_markup=markup)

@bot.message_handler(commands=['addstock'])
def add_stock_command(message):
    if message.from_user.id in ADMIN_IDS:
        try:
            _, category, submenu = message.text.split()
            submenu = int(submenu)
            bot.send_message(message.chat.id, f"Adding stock to {category} submenu {submenu}. Please send the stock message.")
            bot.register_next_step_handler(message, lambda msg: process_stock_message(msg, category, submenu))
        except:
            bot.send_message(message.chat.id, "Usage: /addstock <category> <submenu>")
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this command.")

def process_stock_message(message, category, submenu):
    stock_message = message.text
    bot.send_message(message.chat.id, f"Stock message received: {stock_message}\nPlease enter the price in INR.")
    bot.register_next_step_handler(message, lambda msg: set_stock_price(msg, category, submenu, stock_message))

def set_stock_price(message, category, submenu, stock_message):
    try:
        price = int(message.text)
        if submenu not in stocks[category]:
            stocks[category][submenu] = []
        stocks[category][submenu].append({'message': stock_message, 'price': price})
        stock_counts[category] += 1
        bot.send_message(message.chat.id, f"Stock added to {category} submenu {submenu} with price ₹{price}.")
    except:
        bot.send_message(message.chat.id, "Invalid price. Please try again.")

@bot.message_handler(func=lambda message: message.text.startswith('BUY PREPAID '))
def handle_buy_prepaid(message):
    track_user(message)
    submenu = int(message.text.split()[2])
    if submenu in stocks['prepaid'] and stocks['prepaid'][submenu]:
        show_stock_options(message, 'prepaid', submenu)
    else:
        bot.send_message(message.chat.id, "Stock is empty in this submenu. Please try another one.", reply_markup=create_back_button())

@bot.message_handler(func=lambda message: message.text.startswith('BUY OLD IG '))
def handle_buy_old_ig(message):
    track_user(message)
    submenu = int(message.text.split()[3])
    if submenu in stocks['oldig'] and stocks['oldig'][submenu]:
        show_stock_options(message, 'oldig', submenu)
    else:
        bot.send_message(message.chat.id, "Stock is empty in this submenu. Please try another one.", reply_markup=create_back_button())

@bot.message_handler(func=lambda message: message.text.startswith('BUY INDO IG '))
def handle_buy_indo_ig(message):
    track_user(message)
    submenu = int(message.text.split()[3])
    if submenu in stocks['indoig'] and stocks['indoig'][submenu]:
        show_stock_options(message, 'indoig', submenu)
    else:
        bot.send_message(message.chat.id, "Stock is empty in this submenu. Please try another one.", reply_markup=create_back_button())

@bot.message_handler(func=lambda message: message.text.startswith('BUY FRESH IG '))
def handle_buy_fresh_ig(message):
    track_user(message)
    submenu = int(message.text.split()[3])
    if submenu in stocks['freshig'] and stocks['freshig'][submenu]:
        show_stock_options(message, 'freshig', submenu)
    else:
        bot.send_message(message.chat.id, "Stock is empty in this submenu. Please try another one.", reply_markup=create_back_button())

def show_stock_options(message, category, submenu):
    stock_list = stocks[category][submenu]
    if not stock_list:
        bot.send_message(message.chat.id, "No stock available in this submenu.")
        return
    price = stock_list[0]['price']
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(types.KeyboardButton('BUY'))
    bot.send_message(message.chat.id, f"Price: ₹{price}", reply_markup=markup)
    bot.register_next_step_handler(message, lambda msg: handle_purchase(msg, category, submenu, price))

def handle_purchase(message, category, submenu, price):
    user_balance = user_balances.get(message.from_user.id, 0)
    if message.text == 'BUY':
        if user_balance >= price:
            user_balances[message.from_user.id] = user_balance - price
            purchased_stock = stocks[category][submenu].pop(0)
            stock_counts[category] -= 1
            global total_stock_sold
            total_stock_sold += 1
            bot.send_message(message.chat.id, f"Purchased for ₹{price}. Your new balance is ₹{user_balances[message.from_user.id]}.")
            bot.send_message(message.chat.id, purchased_stock['message'], reply_markup=create_main_menu())
        else:
            bot.send_message(message.chat.id, "Insufficient balance. Please add funds and try again.", reply_markup=create_main_menu())
            add_funds(message)
    else:
        bot.send_message(message.chat.id, "Purchase cancelled.", reply_markup=create_main_menu())

@bot.message_handler(commands=['backup'])
def backup_command(message):
    if message.from_user.id in ADMIN_IDS:
        backup_data = {
            'user_balances': user_balances,
            'stocks': stocks,
            'stock_counts': stock_counts,
            'total_stock_sold': total_stock_sold,
        }
        backup_filename = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(backup_filename, 'w') as backup_file:
            json.dump(backup_data, backup_file)
        with open(backup_filename, 'rb') as backup_file:
            bot.send_document(message.chat.id, backup_file)
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this command.")

@bot.message_handler(commands=['restore'])
def restore_command(message):
    if message.from_user.id in ADMIN_IDS:
        msg = bot.reply_to(message, "Please send the backup file to restore.")
        bot.register_next_step_handler(msg, process_restore_file)
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this command.")

def process_restore_file(message):
    if message.content_type == 'document':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("restore_backup.json", 'wb') as restore_file:
            restore_file.write(downloaded_file)
        with open("restore_backup.json", 'r') as restore_file:
            backup_data = json.load(restore_file)
            global user_balances, stocks, stock_counts, total_stock_sold
            user_balances.update(backup_data.get('user_balances', {}))
            for category, stock in backup_data.get('stocks', {}).items():
                for submenu, items in stock.items():
                    if submenu in stocks[category]:
                        stocks[category][submenu].extend(items)
                    else:
                        stocks[category][submenu] = items
            stock_counts.update(backup_data.get('stock_counts', {}))
            total_stock_sold += backup_data.get('total_stock_sold', 0)
        bot.send_message(message.chat.id, "Backup restored successfully.")
    else:
        bot.send_message(message.chat.id, "Please send a valid backup file.")

@bot.message_handler(commands=['addfund'])
def add_fund_command(message):
    if message.from_user.id in ADMIN_IDS:
        try:
            _, user_id, amount = message.text.split()
            user_id = int(user_id)
            amount = int(amount)
            user_balances[user_id] = user_balances.get(user_id, 0) + amount
            bot.send_message(message.chat.id, f"Added ₹{amount} to user {user_id}")
            bot.send_message(user_id, f"₹{amount} has been credited to your balance.")
        except:
            bot.send_message(message.chat.id, "Usage: /addfund <user_id> <amount>")
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this command.")

@bot.message_handler(commands=['setqr'])
def set_qr_command(message):
    if message.from_user.id in ADMIN_IDS:
        msg = bot.reply_to(message, "Please send the new QR code image.")
        bot.register_next_step_handler(msg, process_qr_image)
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this command.")

def process_qr_image(message):
    if message.content_type == 'photo':
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("new_qr_code.png", 'wb') as new_file:
            new_file.write(downloaded_file)
        global qr_code
        qr_code = "new_qr_code.png"
        bot.send_message(message.chat.id, "New QR code has been set.")
    else:
        bot.send_message(message.chat.id, "Please send a valid image.")

@bot.message_handler(commands=['admin'])
def admin_command(message):
    if message.from_user.id in ADMIN_IDS:
        admin_commands = (
            "/addfund <user_id> <amount> - Add funds to a user's balance.\n"
            "Usage: /addfund 12345678 100\n\n"
            "/setqr - Set a new QR code for adding funds.\n"
            "Usage: /setqr\n\n"
            "/addstock <category> <submenu> - Add stock to a specific submenu.\n"
            "Categories: prepaid, oldig, indoig, freshig\n"
            "Usage: /addstock prepaid 2\n\n"
            "/broadcast - Send a broadcast message or document to all users.\n"
            "Usage: /broadcast\n\n"
            "/stat - Show total users, total user balance, and total stock sold.\n"
            "Usage: /stat\n\n"
            "/statlist - Generate a text file with details of all users.\n"
            "Usage: /statlist\n\n"
            "/backup - Create a backup of the current data.\n"
            "Usage: /backup\n\n"
            "/restore - Restore data from a backup file.\n"
            "Usage: /restore\n\n"
        )
        bot.send_message(message.chat.id, f"Admin Commands:\n\n{admin_commands}")
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this command.")

@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    if message.from_user.id in ADMIN_IDS:
        msg = bot.reply_to(message, "What would you like to broadcast? Send the message or document.")
        bot.register_next_step_handler(msg, process_broadcast)
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this command.")

def process_broadcast(message):
    for user_id in user_ids:
        try:
            if message.content_type == 'text':
                bot.send_message(user_id, message.text)
            elif message.content_type == 'document':
                bot.send_document(user_id, message.document.file_id, caption=message.caption if message.caption else "")
            elif message.content_type == 'photo':
                bot.send_photo(user_id, message.photo[-1].file_id, caption=message.caption if message.caption else "")
            print(f"Broadcast sent to {user_id}")
        except Exception as e:
            print(f"Failed to send broadcast to {user_id}: {e}")

@bot.message_handler(commands=['stat'])
def stat_command(message):
    if message.from_user.id in ADMIN_IDS:
        total_users = len(user_ids)
        total_balance = sum(user_balances.values())
        stats = (
            f"Total Users: {total_users}\n"
            f"Total User Balance: ₹{total_balance}\n"
            f"Total Stock Sold: {total_stock_sold}\n"
        )
        bot.send_message(message.chat.id, stats)
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this command.")

@bot.message_handler(commands=['statlist'])
def statlist_command(message):
    if message.from_user.id in ADMIN_IDS:
        with open("user_stats.txt", "w") as file:
            for user_id, balance in user_balances.items():
                file.write(f"UserID: {user_id}, Balance: ₹{balance}\n")
        with open("user_stats.txt", "rb") as file:
            bot.send_document(message.chat.id, file)
    else:
        bot.send_message(message.chat.id, "You are not authorized to use this command.")

bot.infinity_polling()
