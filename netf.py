from datetime import datetime, timedelta
email.utils import parsedate_to_datetime
import email
from email import message_from_bytes
from io import BytesIO
import json
import imaplib
import os
import re
import threading
import time
from dotenv import load_dotenv
from flask import Flask
from PIL import Image, ImageDraw, ImageFont
import requests
import telebot
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

# --- إعداد خادم الويب لإبقاء البوت مستيقظاً على Render ---
app = Flask('')


@app.route('/')
def home():
  return 'I am alive!'


def run():
  port = int(os.environ.get('PORT', 10000))
  app.run(host='0.0.0.0', port=port)


def keep_alive():
  t = threading.Thread(target=run)
  t.start()


load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv(
    'TELEGRAM_BOT_TOKEN', '8415364406:AAGBVGsuVkQ6VBQN1ao8D_dh0fRKR3QJfgg'
)
IMAP_SERVER = 'imap.gmail.com'
EMAIL_ACCOUNT = os.getenv('EMAIL_ACCOUNT', 'hrdwrermdy@gmail.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'yxiycsytfwnztwzy')

IMAP_YAHOO_SERVER = 'imap.mail.yahoo.com'
IMAP_AOL_SERVER = 'imap.aol.com'

YAHOO_ACCOUNTS = {
    'bibozd@yahoo.com': 'jljigwcrjxkuyeao',
    'hamzausmh267@yahoo.com': 'cozqfgxssbkrhcnq',
    'zikomycanal1@yahoo.com': 'pagwxvirzkxvlqul',
    'icknause@yahoo.com': 'oryqtcogihjabkim',
    'zikomycanal@yahoo.com': 'jpwjkmwfqqxbuhmv',
    'zazabenmebarek@aol.com': 'xjejcqhvzhkgasbk',
}

admin_env = os.getenv('ADMIN_IDS', '6786498950')
ADMIN_IDS = [
    int(admin_id.strip())
    for admin_id in admin_env.split(',')
    if admin_id.strip().isdigit()
]

NETFLIX_IMAGE_URL = 'https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?q=80&w=1000&auto=format&fit=crop'
SUBSCRIPTIONS_FILE = 'subscriptions.json'
LOG_FILE = 'activity.log'
LAST_BROADCAST_FILE = 'last_broadcast.json'
USERS_FILE = 'users.json'
STATS_FILE = 'stats.json'

RAW_ALLOWED_EMAILS = [
    'ALOK2000X@outlook.fr',
    'hamzausmh267@yahoo.com',
    'zaki10000007@gmail.com',
    'znetflix903@gmail.com',
    'X1000ZAK@outlook.fr',
    'fredomax29@hotmail.fr',
    'zazio1990@gmail.com',
    'sfr-22222@outlook.fr',
    'zaki065853@gmail.com',
    'alokza05@gmail.com',
    'x2netflix101@gmail.com',
    'zazazabrlo@gmail.com',
    'Zak1.1@outlook.fr',
    'papyclaude@live.fr',
    'zdz49132@gmail.com',
    'zaza055272@gmail.com',
    'nalbgz723@gmail.com',
    'saint_paul@hotmail.fr',
    'znetflix802@gmail.com',
    'zaki10000004@gmail.com',
    'rx104net@gmail.com',
    'znetflix900@gmail.com',
    'zaki100000003@gmail.com',
    'znetflix403@gmail.com',
    'znetflix804@gmail.com',
    'zk.2009@outlook.fr',
    'bibo--@outlook.com',
    'bibo.zaza@yandex.com',
    'netflix10zak@gmail.com',
    'gefloem1@hotmail.fr',
    'alfx895@gmail.com',
    'zatil101.10@gmail.com',
    'zess0301@gmail.com',
    'zo2121112@gmail.com',
    'zaki10000006@gmail.com',
    'zaza1992X@outlook.fr',
    'zaki100000002@gmail.com',
    'x3zaza@gmail.com',
    'remagelbisivni@gmail.com',
    'sfr-33333@outlook.fr',
    'Zaza1997X@outlook.fr',
    'lmza73940@gmail.com',
    'zqa10ut@gmail.com',
    'mechalalba140@gmail.com',
    'dido444444444@gmail.com',
    'x4netflix103@gmail.com',
    'Zaza1994X@outlook.fr',
    'benzaki331@gmail.com',
    'x17netflix17@gmail.com',
    'Zak.16.16@outlook.fr',
    'crdon631@gmail.com',
    'ragnarzad@gmail.com',
    'zazausma673@gmail.com',
    'Drago.60.zk@outlook.com',
    'bibo150000@gmail.com',
    'dido555555555@gmail.com',
    'Drago.10.zk@hotmail.com',
    'benmebarekzaki2@gmail.com',
    'sfr-55555@outlook.fr',
    'ben898352@gmail.com',
    'Cr7-900@outlook.com',
    'xza70392@gmail.com',
    '10trdut@gmail.com',
    'aemb72888@gmail.com',
    'ALOK2004X@outlook.fr',
    'acques.berthier30@gmail.com',
    'zaki10000005@gmail.com',
    'carson474444@gmail.com',
    'zk.2005@outlook.fr',
    'Zaza1996X@outlook.fr',
    'madridess17@gmail.com',
    'zakbza54@gmail.com',
    'moumounedu59@hotmail.fr',
    'zaki01115@outlook.com',
    'Zaki1Netflix2@gmail.com',
    'pilipaviciusmiss@gmail.com',
    'zizazakiki@gmail.com',
    'dz7283983@gmail.com',
    'znetflix801@gmail.com',
    'zaza065992@gmail.com',
    'x5netflix104@gmail.com',
    'znetflix402@gmail.com',
    'rosline.grellier85@gmail.com',
    'fqsere@gmail.com',
    'zk.2006@outlook.fr',
    'itajvi2@gmail.com',
    'zaz72171@gmail.com',
    'Drago.50.zk@outlook.com',
    'zaki01113@outlook.fr',
    'x4zaza10@gmail.com',
    'zaki01116@outlook.com',
    'sfr-44444@outlook.fr',
    'la.tribale@hotmail.fr',
    'zaki01114@outlook.com',
    'juoz4209@gmail.com',
    'Zaza1995X@outlook.fr',
    'zaza1993X@outlook.fr',
    'zaakak373@gmail.com',
    'zazabibo09@gmail.com',
    'znetflix904@gmail.com',
    'znetflix902@gmail.com',
    'zess280@gmail.com',
    'zntflix405@gmail.com',
    'znetflix803@gmail.com',
    'kza61487@gmail.com',
    'zaza-12-13-14@hotmail.com',
    'Zaza1991X@outlook.fr',
    'zaki100000001@gmail.com',
    'zaza1000000009@gmail.com',
    'zaza100000010@gmail.com',
    'zak244441@gmail.com',
    'x1netflix100@gmail.com',
    'Cr7-400@hotmail.com',
    'X20netflix20@gmail.com',
    'yhhjiaze28@gmail.com',
    'zazkak102@gmail.com',
    'dzkoki54@gmail.com',
    'zaki10000008@gmail.com',
    'znetflix901@gmail.com',
    'zaki1190000@gmail.com',
    'zaza.3636@outlook.fr',
    'X16netflix16@gmail.com',
    'zbe8274@gmail.com',
    'zddz848@gmail.com',
    'chclement1@hotmail.fr',
    'rx102net@gmail.com',
    'Cr7-800@outlook.com',
    'zk.2007@outlook.fr',
    'dhaimi.28@outlook.fr',
    'X19netflix19@gmail.com',
    'melanie91580@hotmail.fr',
    'zaki01112@outlook.fr',
    'zakimestr@gmail.com',
    'greg59245@hotmail.fr',
    'nkbbvn@gmail.com',
    'zakimadridbibo@gmail.com',
    'zk.2008@outlook.fr',
    'taliamathias@hotmail.fr',
    'zoro17816@gmail.com',
    'dido333333333@gmail.com',
    'zaqsdqa@gmail.com',
    'qsqszaz10@gmail.com',
    'zaki01111@outlook.fr',
    'ALOK2001X@outlook.fr',
    'benbz4533@gmail.com',
    'sasukefans@hotmail.fr',
    'zaki1999001@gmail.com',
    'zaki1999000@gmail.com',
    'cheifdido@gmail.com',
    'zazabibo306@gmail.com',
    'X12netflix12@gmail.com',
    'sfr-66666@outlook.fr',
    'ffbibo051@gmail.com',
    'zaki069843@gmail.com',
    'oku69134@gmail.com',
    'zaza10236@gmail.com',
    'zaza.netflix@yandex.com',
    'zak1.ben@yandex.com',
    'bibo.zaza@yandex.com',
    'bibozd@yahoo.com',
    'hamzausmh267@yahoo.com',
    'zikomycanal1@yahoo.com',
    'icknause@yahoo.com',
    'zikomycanal@yahoo.com',
    'zazabenmebarek@aol.com',
]

WHATSAPP_NUMBER = '+213552725828'

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
user_selected_emails = {}
user_bot_messages = {}
admin_waiting_broadcast = set()
user_cooldowns = {}

DEFAULT_USERS = {
    '5789291272': 'Farouk',
    '5022811857': 'Muslim',
    '5393880306': 'AZ STORE',
    '5638977180': 'moh',
}


def notify_admin_error(error_msg):
  if ADMIN_IDS and error_msg:
    for admin_id in ADMIN_IDS:
      try:
        bot.send_message(
            admin_id,
            f'🚨 <b>تنبيه خطأ في النظام:</b>\n<code>{error_msg}</code>',
            parse_mode='HTML',
        )
      except:
        pass


def log_user_action_detail(user_obj, email_addr, service_type, result_status):
  try:
    user_id = (
        user_obj.id if user_obj and hasattr(user_obj, 'id') else 'Unknown_ID'
    )
    first_name = (
        user_obj.first_name
        if user_obj and hasattr(user_obj, 'first_name') and user_obj.first_name
        else ''
    )
    last_name = (
        user_obj.last_name
        if user_obj and hasattr(user_obj, 'last_name') and user_obj.last_name
        else ''
    )
    full_name = f'{first_name} {last_name}'.strip()
    if not full_name:
      full_name = f'User_{user_id}'

    username = (
        user_obj.username
        if user_obj and hasattr(user_obj, 'username') and user_obj.username
        else ''
    )
    username_str = f'@{username}' if username else 'بدون اسم مستخدم'

    date_formatted = datetime.now().strftime('%d/%m/%Y')

    log_entry = (
        f'========================================\n'
        f'📅 التاريخ : {date_formatted}\n'
        f'👤 اسم المستخدم : {full_name}\n'
        f'🆔 معرف التليجرام : {user_id}\n'
        f'🔗 اليوزرنيم     : {username_str}\n'
        f'📧 البريد المطلوب : {email_addr}\n'
        f'🛠 الخدمة المطلوبة : {service_type}\n'
        f'📝 حالة النتيجة    : {result_status}\n'
        f'========================================\n\n'
    )

    with open(LOG_FILE, 'a', encoding='utf-8') as f:
      f.write(log_entry)
  except:
    pass


def save_sale_to_client_file(
    client_name, client_id, email_addr, days, start_time, expiry_time
):
  try:
    folder_name = 'clients_folder'
    if not os.path.exists(folder_name):
      os.makedirs(folder_name)

    safe_filename = (
        ''.join(
            c
            for c in client_name
            if c.isalnum() or c in (' ', '_', '-')
        )
        .strip()
        .replace(' ', '_')
    )
    if not safe_filename:
      safe_filename = 'Unknown_Client'

    file_path = os.path.join(folder_name, f'{safe_filename}_{client_id}.txt')

    start_dt_obj = (
        datetime.fromisoformat(str(start_time))
        if isinstance(start_time, str)
        else start_time
    )
    expiry_dt_obj = (
        datetime.fromisoformat(str(expiry_time))
        if isinstance(expiry_time, str)
        else expiry_time
    )

    start_formatted = start_dt_obj.strftime('%d/%m/%Y')
    expiry_formatted = expiry_dt_obj.strftime('%d/%m/%Y')

    sale_entry = (
        f'========================================\n'
        f'🛒 عملية بيع / تفعيل حساب جديدة\n'
        f'👤 اسم الزبون : {client_name}\n'
        f'🆔 معرف التليجرام : {client_id}\n'
        f'📧 البريد المباع : {email_addr}\n'
        f'⏳ المدة : {days} يوماً\n'
        f'🟢 من تاريخ : {start_formatted}\n'
        f'🔴 إلى تاريخ : {expiry_formatted}\n'
        f'========================================\n\n'
    )

    with open(file_path, 'a', encoding='utf-8') as f:
      f.write(sale_entry)
  except:
    pass


def load_users():
  users = DEFAULT_USERS.copy()
  if os.path.exists(USERS_FILE):
    try:
      with open(USERS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if isinstance(data, dict):
          users.update(data)
    except:
      pass
  return users


all_bot_users = load_users()


def save_users(users_dict):
  try:
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
      json.dump(users_dict, f, ensure_ascii=False, indent=4)
  except:
    pass


def register_user_from_user_obj(user_obj):
  if user_obj and hasattr(user_obj, 'id'):
    chat_id_str = str(user_obj.id)
    first = user_obj.first_name if user_obj.first_name else ''
    last = user_obj.last_name if user_obj.last_name else ''
    full_name = f'{first} {last}'.strip()
    if not full_name:
      full_name = 'Unknown'
    all_bot_users[chat_id_str] = full_name
    save_users(all_bot_users)


def register_user(message):
  if message and hasattr(message, 'from_user') and message.from_user:
    register_user_from_user_obj(message.from_user)


def save_subscriptions(subs_dict):
  try:
    with open(SUBSCRIPTIONS_FILE, 'w', encoding='utf-8') as f:
      json.dump(subs_dict, f, ensure_ascii=False, indent=4)
  except:
    pass


def load_subscriptions():
  subs = {}
  default_expiry = (datetime.now() + timedelta(days=31)).replace(
      hour=0, minute=0, second=0, microsecond=0
  )
  for email_addr in RAW_ALLOWED_EMAILS:
    subs[email_addr.strip().lower()] = {
        'active': True,
        'expiry': default_expiry.isoformat(),
        'owner_id': None,
        'client_name': 'مشترك',
        'notified_expiry': False,
    }
  if os.path.exists(SUBSCRIPTIONS_FILE):
    try:
      with open(SUBSCRIPTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if isinstance(data, dict):
          for k, v in data.items():
            clean_k = k.strip().lower()
            if clean_k in subs and isinstance(v, dict):
              subs[clean_k] = v
    except:
      pass
  return subs


subscriptions = load_subscriptions()


def check_expirations_loop():
  while True:
    try:
      now = datetime.now()
      for email_addr, data in subscriptions.items():
        if data and data.get('active') and data.get('expiry'):
          exp_date = datetime.fromisoformat(data['expiry'])
          if (
              0 < (exp_date - now).days <= 3
              and not data.get('notified_expiry')
          ):
            owner_id = data.get('owner_id')
            if owner_id:
              try:
                bot.send_message(
                    owner_id,
                    f'⚠️ <b>تنبيه:</b> اشتراكك للبريد <code>{email_addr}</code> سينتهي خلال 3 أيام.',
                    parse_mode='HTML',
                )
                data['notified_expiry'] = True
                save_subscriptions(subscriptions)
              except:
                pass
    except:
      pass
    time.sleep(86400)


threading.Thread(target=check_expirations_loop, daemon=True).start()


def load_stats():
  if os.path.exists(STATS_FILE):
    try:
      with open(STATS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if isinstance(data, dict):
          return data
    except:
      pass
  return {'requests_count': 0, 'top_emails': {}}


stats_data = load_stats()


def increment_request_stat(email_addr):
  if email_addr:
    stats_data['requests_count'] = stats_data.get('requests_count', 0) + 1
    top = stats_data.get('top_emails', {})
    top[email_addr] = top.get(email_addr, 0) + 1
    stats_data['top_emails'] = top
    try:
      with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats_data, f, ensure_ascii=False, indent=4)
    except:
      pass


def is_subscription_active(email_addr, user_id):
  if not email_addr:
    return 'not_found'
  email_lower = email_addr.strip().lower()
  if email_lower not in subscriptions:
    return 'not_found'
  sub_data = subscriptions[email_lower]
  if not sub_data.get('active', True):
    return 'inactive'
  expiry_str = sub_data.get('expiry')
  try:
    if expiry_str and datetime.now() > datetime.fromisoformat(expiry_str):
      sub_data['active'] = False
      sub_data['owner_id'] = None
      save_subscriptions(subscriptions)
      return 'expired'
  except:
    pass
  owner_id = sub_data.get('owner_id')
  if ADMIN_IDS and user_id in ADMIN_IDS:
    return 'active'
  if owner_id is None:
    sub_data['owner_id'] = user_id
    save_subscriptions(subscriptions)
    return 'active'
  elif str(owner_id) != str(user_id):
    return 'wrong_owner'
  return 'active'


def create_banner_with_text(text, image_url, output_path='banner.jpg'):
  try:
    response = requests.get(image_url)
    if response.status_code == 200:
      img = Image.open(BytesIO(response.content)).convert('RGB')
      draw = ImageDraw.Draw(img)
      try:
        font = ImageFont.truetype('arial.ttf', 45)
      except:
        font = ImageFont.load_default()
      width, height = img.size
      bbox = draw.textbbox((0, 0), text, font=font)