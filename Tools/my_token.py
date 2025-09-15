import time
import string
import random
import asyncio

import requests
import json

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait

from pymongo import MongoClient
from bot import Vars, Bot

import functools


db_client = MongoClient(Vars.DB_URL)
db = db_client[Vars.DB_NAME] 
token_db = db["tokens"]
dr = Vars.DURATION

tks = token_db.find_one({"_id": f"{Vars.DB_NAME}"})
if not tks:
    tks = {"_id": f"{Vars.DB_NAME}"}
    token_db.insert_one(tks)

def token_sync():
    token_db.replace_one({'_id': f"{Vars.DB_NAME}"}, tks)

def get_premuims():
    premuim_db = db["premium"]
    users_id_list = []
    for i in premuim_db.find():
        for j in i:
            try:
                users_id_list.append(int(j))
            except:
                pass
    
    users_id_list = users_id_list + Vars.ADMINS
    return users_id_list

def generate_random_alphanumeric():
    """Generate a random 8-letter alphanumeric string."""
    characters = string.ascii_letters + string.digits + "TOKEN" + string.ascii_uppercase
    random_chars = ''.join(random.choice(characters) for _ in range(8))
    return random_chars


def get_short(url):
    try:
        api_url = Vars.SHORTENER_API
        if not isinstance(api_url, str):
            api_url = random.choice(api_url)
        
        xurl = api_url.replace("{}", url)
        
        rjson = requests.get(xurl).json()
        
        return rjson["shortenedUrl"]

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return url


def generate_token():
    return generate_random_alphanumeric()


def save_token(user_id: str, token: str, _id: int, _cid: int, short_token_link: str):
    expiration_time = time.time() + (dr * 3600)  # Convert hours to seconds
    duration_ = time.time() + (0.0111111 * 3600) # adding 40 seconds to current time
    tks[str(user_id)] = {
        "token": token, 
        "expires_at": expiration_time, 
        "duration": duration_, 
        "msg_id": _id,
        "chat_id": _cid,
        "s_link": short_token_link,
        "verify": None,
    }
    token_sync()

def expired_token_():
    for user_id, data in tks.items():
        if data["expires_at"] < time.time():
            del tks[user_id]
            token_sync()


def check_token_(func):
    @functools.wraps(func)
    async def wrapper(client, message, *args, **kwargs):
        if Vars.SHORTENER not in ["None", None, False, "False", "OFF"]:
            if message.from_user.id in get_premuims():
                return await func(client, message, *args, **kwargs)
            else:
                if str(message.from_user.id) in tks:
                    if tks[str(message.from_user.id)]["verify"] == "True":
                        if tks[str(message.from_user.id)]["expires_at"] > time.time():
                            return await func(client, message, *args, **kwargs)
                        else:
                            return await get_token(message, message.from_user.id)
                    else:
                        return await message.reply(
                            f"<i> Verify Your Token First :- {tks[str(message.from_user.id)]['s_link']}</i>"
                        )
                else:
                    sts = await message.reply("<i>ㅤProcessing.....</i>")
                    return await get_token(sts, message.from_user.id)
        else:
            return await func(client, message, *args, **kwargs)
    
    return wrapper


async def verify_token(message, user_id, token):
    user_id = str(user_id)
    if user_id in tks:
        token_data = tks[user_id]
        if token_data["expires_at"] > time.time():
            if token_data['verify'] == "True":
                return await message.edit("<i> Token Already verified....</i>")
            if token_data["token"] == token:
                if token_data["duration"] < time.time():
                    tks[user_id]["verify"] = "True"
                    token_sync()
                    return await message.edit("<i> Token verified. Now, You Can Use Me</i>")
                else: 
                    keyboard = InlineKeyboardMarkup([
                        [InlineKeyboardButton("🖥 Get Token 🖥", url=token_data['s_link'])],
                        [InlineKeyboardButton("📺 Watch Tutorial 📺", url="https://t.me/+KymUiadSyutiZjM1")],
                        [
                            InlineKeyboardButton("💸 Bot Premuim 💸", callback_data="premuim"),
                            InlineKeyboardButton("⛓️‍💥 Close ⛓️‍💥", callback_data="close")
                        ],
                    ])
                    
                    return await message.edit(
                        Vars.BYPASS_TXT,
                        reply_markup=keyboard
                    )
            else:
                return await get_token(message, user_id)
        else:
            return await get_token(message, user_id)


async def get_token(message, user_id):
    user_id = str(user_id)
    if user_id in tks:
        if "msg_id" in tks[user_id] and "chat_id" in tks[user_id]:
            try:
                chat_id = tks[user_id]["chat_id"]
                await Bot.delete_messages(int(chat_id), int(tks[user_id]["msg_id"]))
            except FloodWait as e:
                await asyncio.sleep(e.value + 2)
                chat_id = tks[user_id]["chat_id"]
                await Bot.delete_messages(int(chat_id), int(tks[user_id]["msg_id"]))
            except:
                pass
    
    new_token = generate_token()
    
    token_link = f"https://telegram.me/{Bot.username}?start={new_token}"
    short_token_link = get_short(token_link)
    save_token(user_id, new_token, message.id, message.chat.id, short_token_link)
    
    button = InlineKeyboardButton("🖥 Get Token 🖥", url=short_token_link)
    button2 = InlineKeyboardButton("📺 Watch Tutorial 📺", url="https://t.me/+KymUiadSyutiZjM1")
    keyboard = InlineKeyboardMarkup([
        [button],
        [button2],
        [InlineKeyboardButton("💸 Bot Premuim 💸", callback_data="premuim")],
        [InlineKeyboardButton("⛓️‍💥 Close ⛓️‍💥", callback_data="close")],
    ])
    
    try:
        await message.edit_text("<i>Invalid or expired token. Here is your new token link. Click the button below to use it.\n\n **Valid Till 1 days.**</i>", reply_markup=keyboard)
    except FloodWait as e:
        await asyncio.sleep(e.value + 2)
        await message.edit_text("<i>Invalid or expired token. Here is your new token link. Click the button below to use it.\n\n **Valid Till 1 days.**</i>", reply_markup=keyboard)
