from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .storage import web_data, split_list, plugins_list, users_txt, retry_on_flood, queue, asyncio

from pyrogram.errors import FloodWait
import pyrogram.errors

from bot import Bot, Vars, logger

import random
from Tools.db import *
from Tools.my_token import *

from pyrogram.handlers import MessageHandler
import time

from asyncio import create_subprocess_exec
from os import execl
from sys import executable

import shutil, psutil, time, os, platform
import asyncio

HELP_MSG = """
<b>To download a manga just type the name of the manga you want to keep up to date.</b>

For example:
`One Piece`

<blockquote expandable><i>Then you will have to choose the language of the manga. Depending on this language, you will be able to choose the website where you could download the manga. Here you will have the option to subscribe, or to choose a chapter to download. The chapters are sorted according to the website.</i></blockquote>

<blockquote><b>Updates Channel : @AnimeNexusNetwork</b></blockquote>
"""



@Bot.on_message(filters.command("start"))
async def start(client, message):
  if Vars.IS_PRIVATE:
    if message.chat.id not in Vars.ADMINS:
      return await message.reply("<code>You cannot use me baby </code>")

  if len(message.command) > 1:
    if message.command[1] != "start":
      user_id = message.from_user.id
      token = message.command[1]
      if verify_token_memory(user_id, token):
        sts = await message.reply("Token verified! You can now use the bot.")
        save_token(user_id, token)
        global_tokens.pop(user_id, None)
        await asyncio.sleep(8)
        await sts.delete()
      else:
        sts = await message.reply("Invalid or expired token. Requesting a new one...")
        await get_token(message, user_id)
        await sts.delete()
      return

  photo = random.choice(Vars.PICS)
  ping = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - Vars.PING))
  await message.reply_photo(
    photo,
    caption=(
      "<b><i>Welcome to the best manga pdf bot in telegram!!</i></b>\n"
      "\n"
      "<b><i>How to use? Just type the name of some manga you want to keep up to date.</i></b>\n"
      "\n"
      "<b><i>For example:</i></b>\n"
      "<i><code>One Piece</i></code>\n"
      "\n"
      f"<b><i>Ping:- {ping}</i></b>"
      "\n"
      "<b><i>Check /help for more information.</i></b>"),
    reply_markup=InlineKeyboardMarkup([[        
                                         InlineKeyboardButton('* More Channel *', url = "https://t.me/AnimeNexusNetwork/158"),
                                         InlineKeyboardButton("* Support *", url = "https://t.me/EternalsHelplineBot")
                                     ]]))

@Bot.on_message(filters.private)
async def on_private_message(client, message):
  if client.SHORTENER:
    if not await premium_user(message.from_user.id):
      if not verify_token(message.from_user.id):
        if not message.from_user.id in client.ADMINS:
          return await get_token(message, message.from_user.id)
  
  channel = client.FORCE_SUB_CHANNEL
  if not channel:
    return message.continue_propagation()

  try:
    if await client.get_chat_member(channel, message.from_user.id):
      return message.continue_propagation()

  except pyrogram.errors.UsernameNotOccupied:
    await message.reply("Channel does not exist, therefore bot will continue to operate normally")
    return message.continue_propagation()

  except pyrogram.errors.ChatAdminRequired:
    await message.reply("Bot is not admin of the channel, therefore bot will continue to operate normally")
    return message.continue_propagation()

  except pyrogram.errors.UserNotParticipant:
    await message.reply("<b>In order to use the bot you must join it's channel.</b>",
            reply_markup=InlineKeyboardMarkup([
              [InlineKeyboardButton(' Join Channel ! ', url=f't.me/{channel}')]]))

  except pyrogram.ContinuePropagation:
    raise
  except pyrogram.StopPropagation:
    raise
  except BaseException as e:
    await message.reply(e)
    return message.continue_propagation()

@Bot.on_message(filters.command(["add", "add_premium"]) & filters.user(Bot.ADMINS))
async def add_handler(_, msg):
  sts = await msg.reply_text("<code>Processing...</code>")
  try:
    user_id = int(msg.text.split(" ")[1])
    time_limit_days = int(msg.text.split(" ")[2])
    await add_premium(user_id, time_limit_days)
    await retry_on_flood(sts.edit)("<code>User added to premium successfully.</code>")
  except Exception as err:
    await retry_on_flood(sts.edit)(err)

@Bot.on_message(filters.command(["del", "del_premium"]) & filters.user(Bot.ADMINS))
async def del_handler(_, msg):
  sts = await msg.reply_text("<code>Processing...</code>")
  try:
    user_id = int(msg.text.split(" ")[1])
    await remove_premium(user_id)
    await retry_on_flood(sts.edit)("<code>User removed from premium successfully.</code>")
  except Exception as err:
    await retry_on_flood(sts.edit)(err)

@Bot.on_message(filters.command(["del_expired", "del_expired_premium"]) & filters.user(Bot.ADMINS))
async def del_expired_handler(_, msg):
  sts = await msg.reply_text("<code>Processing...</code>")
  try:
    await remove_expired_users()
    await retry_on_flood(sts.edit)("<code>Expired users removed successfully.</code>")
  except Exception as err:
    await retry_on_flood(sts.edit)(err)

@Bot.on_message(filters.command(["premium", "premium_users"]) & filters.user(Bot.ADMINS))
async def premium_handler(_, msg):
  sts = await msg.reply_text("<code>Processing...</code>")
  try:
    premium_users = acollection.find()
    txt = "<b>Premium Users:-</b>\n"
    for user in premium_users:
      user_ids = user["user_id"]
      user_info = await _.get_users(user_ids)
      username = user_info.username
      first_name = user_info.first_name
      expiration_timestamp = user["expiration_timestamp"]
      xt = (expiration_timestamp-(time.time()))
      x = round(xt/(24*60*60))
      txt += f"User id: <code>{user_ids}</code>\nUsername: @{username}\nName: <code>{first_name}</code>\nExpiration Timestamp: {x} days\n"

    await retry_on_flood(sts.edit)(txt[:1024])
  except Exception as err:
    await retry_on_flood(sts.edit)(err)
  
@Bot.on_message(filters.command(["broadcast", "b"]) & filters.user(Bot.ADMINS))
async def b_handler(_, msg):
  return await borad_cast_(_, msg)

@Bot.on_message(filters.command(["pbroadcast", "pb"]) & filters.user(Bot.ADMINS))
async def pb_handler(_, msg):
  return await borad_cast_(_, msg, True)

async def borad_cast_(_, message, pin=None):
  def del_users(user_id):
    try:
      user_id = str(user_id)
      del uts[user_id]
      sync(_.DB_NAME, 'uts')
    except:
      pass
    
  sts = await message.reply_text("<code>Processing...</code>")
  if message.reply_to_message:
    user_ids = get_users()
    msg = message.reply_to_message
    total = 0
    successful = 0
    blocked = 0
    deleted = 0
    unsuccessful = 0
    await retry_on_flood(sts.edit)("<code>Broadcasting...</code>")
    for user_id in user_ids:
      try:
        docs = await msg.copy(int(user_id))
        if pin:
          await docs.pin(both_sides=True)
        
        successful += 1
      except FloodWait as e:
        await asyncio.sleep(e.value)
        
        docs = await msg.copy(int(user_id))
        if pin:
          await docs.pin(both_sides=True)
        
        successful += 1
      except pyrogram.errors.UserIsBlocked:
        del_users(user_id)
        blocked += 1
      except pyrogram.errors.PeerIdInvalid:
        del_users(user_id)
        unsuccessful += 1
      except pyrogram.errors.InputUserDeactivated:
        del_users(user_id)
        deleted += 1
      except pyrogram.errors.UserNotParticipant:
        del_users(user_id)
        blocked += 1
      except:
        unsuccessful += 1
    
    status = f"""<b><u>Broadcast Completed</u>

    Total Users: <code>{total}</code>
    Successful: <code>{successful}</code>
    Blocked Users: <code>{blocked}</code>
    Deleted Accounts: <code>{deleted}</code>
    Unsuccessful: <code>{unsuccessful}</code></b>"""
    
    await retry_on_flood(sts.edit)(status)
  else:
    await retry_on_flood(sts.edit)("<code>Reply to a message to broadcast it.</code>")
          

    
@Bot.on_message(filters.command("restart") & filters.user(Bot.ADMINS))
async def restart_(client, message):
  msg = await message.reply_text("<code>Restarting.....</code>", quote=True)
  with open("restart_msg.txt", "w") as file:
    file.write(str(msg.chat.id) + ":" + str(msg.id))
    file.close()
  
  await (await create_subprocess_exec("python3", "update.py")).wait()
  execl(executable, executable, "-B", "main.py")

def humanbytes(size):    
  if not size:
      return ""
  units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
  size = float(size)
  i = 0
  while size >= 1024.0 and i < len(units):
      i += 1
      size /= 1024.0
  return "%.2f %s" % (size, units[i])

def GET_PROVIDER():
  provider = "Unknown"
  try:
      if os.path.exists('/sys/hypervisor/uuid'):
          with open('/sys/hypervisor/uuid', 'r') as f:
              uuid = f.read().lower()
              if uuid.startswith('ec2'): provider = "AWS EC2"
              elif 'azure' in uuid: provider = "Microsoft Azure"

      elif os.path.exists('/etc/google-cloud-environment'):
          provider = "Google Cloud"

      elif os.path.exists('/etc/digitalocean'):
          provider = "DigitalOcean"

      elif os.path.exists('/dev/disk/by-id/scsi-0Linode'):
          provider = "Linode"

      elif os.path.exists('/etc/vultr'):
          provider = "Vultr"

  except Exception:
      pass
  
  return provider
  
@Bot.on_message(filters.command('stats'))
async def show_ping(_, message):
  total, used, free = shutil.disk_usage(".")
  total = humanbytes(total)
  used = humanbytes(used)
  free = humanbytes(free)
  net_start = psutil.net_io_counters()

  time.sleep(2)
  net_end = psutil.net_io_counters()

  bytes_sent = net_end.bytes_sent - net_start.bytes_sent
  bytes_recv = net_end.bytes_recv - net_start.bytes_recv
  #pkts_sent = net_end.packets_sent - net_start.packets_sent
  #pkts_recv = net_end.packets_recv - net_start.packets_recv
  
  cpu_cores = os.cpu_count()
  cpu_usage = psutil.cpu_percent()
  ram_usage = psutil.virtual_memory().percent
  disk_usage = psutil.disk_usage('/').percent
  try: uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - _.PING))
  except: uptime = None

  start_t = time.time()
  st = await message.reply('**Aᴄᴄᴇꜱꜱɪɴɢ Tʜᴇ Dᴇᴛᴀɪʟꜱ.....**')    
  end_t = time.time()
  time_taken_s = (end_t - start_t) * 1000 
  
  await message.reply_text(
    text=(f"<b><i>Total Disk Space: {total} \n"
          f"Used Space: {used}({disk_usage}%) \n"
          f"Free Space: {free} \n"
          f"CPU Cores: {cpu_cores} \n"
          f"CPU Usage: {cpu_usage}% \n"
          f"RAM Usage: {ram_usage}%\n"
          f"Uptime {uptime}\n"
          f"Cloud Provider: {GET_PROVIDER()}\n"
          f"OS: {platform.system()} \n"
          f"OS Version: {platform.release()} \n"
          f"Python Version: {platform.python_version()} \n"
          f"Pyrogram Version: {_.__version__} \n"
          f"Total I/O Data: {humanbytes(net_end.bytes_sent + net_end.bytes_recv)} \n"
          f"Upload Rate: {humanbytes(bytes_sent/2)}/s \n"
          f"Download Rate: {humanbytes(bytes_recv/2)}/s \n"
          f"Current Ping: {time_taken_s:.3f} ᴍꜱ\n"
          f"Queue: {queue.qsize()}</i></b>\n"),
    quote=True
    )
  await st.delete()


@Bot.on_message(filters.command("shell") & filters.user(Bot.ADMINS))
async def shell(_, message):
  cmd = message.text.split(maxsplit=1)
  if len(cmd) == 1:
    return await message.reply("<code>No command to execute was given.</code>")

  cmd = cmd[1]
  proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
  stdout, stderr = await proc.communicate()
  stdout = stdout.decode().strip()
  stderr = stderr.decode().strip()
  reply = ""
  if len(stdout) != 0:
    reply += f"<b>Stdout</b>\n<blockquote>{stdout}</blockquote>\n"
  if len(stderr) != 0:
    reply += f"<b>Stderr</b>\n<blockquote>{stderr}</blockquote>"

  if len(reply) > 3000:
    file_name = "shell_output.txt"
    with open(file_name) as out_file:
      await message.reply_document(out_file)
      out_file.close()
    os.remove(file_name)
  elif len(reply) != 0:
    await message.reply(reply)
  else:
    await message.reply("No Reply")
  
@Bot.on_message(filters.command("export") & filters.user(Bot.ADMINS))
async def export_(_, message):
  cmd = message.text.split(maxsplit=1)
  if len(cmd) == 1:
    return await message.reply("<code>File Name Not given.</code>")
  
  sts = await message.reply("<code>Processing...</code>")
  try:
    file_name = cmd[1]
    if "*2" in file_name:
      file_name = file_name.replace("*2", "")
      file_name = f"__{file_name}__"
    
    if os.path.exists(file_name):
      await message.reply_document(file_name)
    else:
      await sts.edit("<code>File Not Found</code>")
  except Exception as err:
    await sts.edit(err)
  

@Bot.on_message(filters.command("import") & filters.user(Bot.ADMINS))
async def import_(_, message):
  cmd = message.text.split(maxsplit=1)
  if len(cmd) == 1:
    return await message.reply("<code>File Name Not given.</code>")

  sts = await message.reply("<code>Processing...</code>")
  try:
    file_name = cmd[1]
    if "*2" in file_name:
      file_name = file_name.replace("*2", "")
      file_name = f"__{file_name}__"

    if not os.path.exists(file_name):
      await message.download(file_name, file_name=file_name)
    else:
      await sts.edit("<code>File Path Found</code>")
  except Exception as err:
    await sts.edit(err)

@Bot.on_message(filters.command(["clean", "c"]) & filters.user(Bot.ADMINS))
async def clean(_, message):
  directory = '/app'
  ex = (".mkv", ".mp4", ".zip", ".pdf", ".png", ".epub", ".temp")
  protected_dirs = (".git", "venv", "env", "__pycache__")  # Directories to SKIP
  sts = await message.reply_text("🔍 Cleaning files...")
  deleted_files = []
  removed_dirs = []
  
  if os.path.exists("Process"):
    shutil.rmtree("Process")
  elif os.path.exists("./Process"):
    shutil.rmtree("./Process")
    
  try:
    for root, dirs, files in os.walk(directory, topdown=False):
      # Skip protected directories (e.g., .git)
      dirs[:] = [d for d in dirs if d not in protected_dirs]
      for file in files:
        if file.lower().endswith(ex):
          file_path = os.path.join(root, file)
          try:
            os.remove(file_path)
            deleted_files.append(file_path)
          except Exception as e:
            pass

        elif file.lower().startswith("vol"):
          file_path = os.path.join(root, file)
          try:
            os.remove(file_path)
            deleted_files.append(file_path)
          except Exception as e:
            pass

      for dir_name in dirs:
        dir_path = os.path.join(root, dir_name)
        try:
          if not os.listdir(dir_path):  # Check if empty
            os.rmdir(dir_path)
            removed_dirs.append(dir_path)

          elif dir_path == "/app/Downloads":
            os.rmdir("/app/Downloads")
            removed_dirs.append("/app/Downloads")

          elif dir_path == "/app/downloads":
            os.rmdir("/app/downloads")
            removed_dirs.append("/app/downloads")

          try:
            dir_path = int(dir_path)
            os.rmdir(dir_path)
            removed_dirs.append(dir_path)
          except:
            pass
        except Exception as e:
          pass

    msg = "**🧹 Cleaning Logs:**\n"
    if deleted_files:
      msg += f"🗑 **Deleted {len(deleted_files)} files:**\n" + "\n".join(deleted_files[:10])  # Show first 10
      if len(deleted_files) > 10:
        msg += f"\n...and {len(deleted_files) - 10} more."
      else:
        msg += "✅ No files deleted."

    if removed_dirs:
      msg += f"\n\n📁 **Removed {len(removed_dirs)} empty directories:**\n" + "\n".join(removed_dirs[:5])
      if len(removed_dirs) > 5:
        msg += f"\n...and {len(removed_dirs) - 5} more."

    await sts.edit(msg[:4096])  # Telegram's max message length
  except Exception as err:
    await sts.edit(f"❌ Error: {str(err)}")

def remove_dir(path):
    try:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path, topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                    for dir in dirs:
                        os.rmdir(os.path.join(root, dir))
            os.rmdir(path)
    except Exception as err:
        return err


@Bot.on_message(filters.command("updates"))
async def updates_(_, message):
  if Vars.IS_PRIVATE:
    if message.chat.id not in Vars.ADMINS:
      return await message.reply("<code>You cannot use me baby </code>")
  try:
    await message.reply_photo(
      photo=random.choice(Vars.PICS),
      caption="<b>Choose Sites</b>",
      reply_markup=plugins_list("updates"),
      quote=True,
    )
  except FloodWait as err:
    await asyncio.sleep(err.value)
    await message.reply_photo(
      photo=random.choice(Vars.PICS),
      caption="<b>Choose Sites</b>",
      reply_markup=plugins_list("updates"),
      quote=True,
    )
  except:
    await message.reply_photo(
      photo=random.choice(Vars.PICS),
      caption="<b>Choose Sites</b>",
      reply_markup=plugins_list("updates"),
      quote=True,
    )
  
@Bot.on_message(filters.command("queue"))
async def queue_msg_handler(client, message):
  if Vars.IS_PRIVATE:
    if message.chat.id not in Vars.ADMINS:
      return await message.reply("<code>You cannot use me baby </code>")

  await message.reply(f"<blockquote><b><i>Your Queue: {queue.get_count_(message.from_user.id)}\nTotal Queue Size: {int(queue.qsize())+1}</i></b></blockquote>")

@Bot.on_message(filters.command(["us", "user_setting", "user_panel"]))
async def userxsettings(client, message):
  if Vars.IS_PRIVATE:
    if message.chat.id not in Vars.ADMINS:
      return await message.reply("<code>You cannot use me baby </code>")
  
  sts = await message.reply("<code>Processing...</code>")
  try:
    db_type = "uts"
    name = Vars.DB_NAME
    user_id = str(message.from_user.id)
    if not user_id in uts:
      uts[user_id] = {}
      sync(name, db_type)

    if not "setting" in uts[user_id]:
      uts[user_id]['setting'] = {}
      sync(name, db_type)

    thumbnali = uts[user_id]['setting'].get("thumb", None)
    if thumbnali:
      thumb = "True" if not thumbnali.startswith("http") else thumbnali
    else:
      thumb = thumbnali

    banner1 = uts[user_id]['setting'].get("banner1", None)
    banner2 = uts[user_id]['setting'].get("banner2", None)
    if banner1:
      banner1 = "True" if not banner1.startswith("http") else banner1

    if banner2:
      banner2 = "True" if not banner2.startswith("http") else banner2

    txt = users_txt.format(
      id=user_id,
      file_name=uts[user_id]['setting'].get("file_name", "None"),
      caption=uts[user_id]['setting'].get("caption", "None"),
      thumb=thumb,
      banner1=banner1,
      banner2=banner2,
      dump=uts[user_id]['setting'].get("dump", "None"),
      type=uts[user_id]['setting'].get("type", "None"),
      megre=uts[user_id]['setting'].get("megre", "None"),
      regex=uts[user_id]['setting'].get("regex", "None"),
      len=uts[user_id]['setting'].get("file_name_len", "None"),
      password=uts[user_id]['setting'].get("password", "None"),
    )

    button = [
      [
        InlineKeyboardButton("🪦 File Name 🪦", callback_data="ufn"),
        InlineKeyboardButton("🪦 Caption‌ 🪦", callback_data="ucp")
      ],
      [
        InlineKeyboardButton("🪦 Thumbnali 🪦", callback_data="uth"),
        InlineKeyboardButton("🪦 Regex 🪦", callback_data="uregex")
      ],
      [
        InlineKeyboardButton("⚒ Banner ⚒", callback_data="ubn"),
      ],
      [
        InlineKeyboardButton("⚙️ Password ⚙️", callback_data="upass"),
        InlineKeyboardButton("⚙️ Megre Size ⚙️", callback_data="umegre")
      ],
      [
        InlineKeyboardButton("⚒ File Type ⚒", callback_data="u_file_type"),
      ],
    ]
    if not Vars.CONSTANT_DUMP_CHANNEL:
      button[-1].append(InlineKeyboardButton("⚒ Dump Channel ⚒", callback_data="udc"))
    
    button.append([InlineKeyboardButton("❄️ Close ❄️", callback_data="close")])
    if not thumbnali:
      thumbnali = random.choice(Vars.PICS)
    try:
      await message.reply_photo(thumbnali, caption=txt, reply_markup=InlineKeyboardMarkup(button))
    except FloodWait as err:
      await asyncio.sleep(err.value)
      await message.reply_photo(thumbnali, caption=txt, reply_markup=InlineKeyboardMarkup(button))
    except:
      await message.reply_photo(photo=random.choice(Vars.PICS), caption=txt, reply_markup=InlineKeyboardMarkup(button))

    await sts.delete()
  except Exception as err:
    logger.exception(err)
    await sts.edit(err)


@Bot.on_message(filters.command("help"))
async def help(client, message):
  if Vars.IS_PRIVATE:
    if message.chat.id not in Vars.ADMINS:
      return await message.reply("<code>You cannot use me baby </code>")

  return await message.reply(HELP_MSG)


@Bot.on_message(filters.command(["deltask", "cleantasks", "del_tasks", "clean_tasks"]))
async def deltask(client, message):
  if Vars.IS_PRIVATE:
    if message.chat.id not in Vars.ADMINS:
      return await message.reply("<code>You cannot use me baby </code>")

  user_id = message.from_user.id
  numb = 0
  if user_id in queue._user_data:
    for task_id in queue._user_data[user_id]:
      await queue.delete_task(task_id)
      numb += 1
    await message.reply(f"All tasks deleted:- {numb}")
  else:
    await message.reply("No tasks found")


@Bot.on_message(filters.command("subs"))
async def subs(_, message):
  if _.IS_PRIVATE:
    if message.chat.id not in _.ADMINS:
      return await message.reply("<code>You cannot use me baby </code>")
  
  sts = await message.reply_text("<code>Getting Subs...</code>")
  txt = "<b>Subs List:-</b>\n"
  try:
    subs_list = get_subs(message.from_user.id)
    for sub in subs_list:
      txt += f"<blockquote>=> <code>{sub}</code></blockquote>\n"
    
    txt += f"<blockquote>=> <code>Total Subs:- {len(subs_list)}</code></blockquote>"
    txt += f"\n\n<b>To Unsubs:-</b>\n<blockquote><code>/unsubs url</code></blockquote>"
    await retry_on_flood(sts.edit)(txt[:1024])
  except Exception as err:
    await retry_on_flood(sts.edit)(err)

@Bot.on_message(filters.command("unsubs"))
async def unsubs(_, message):
  if _.IS_PRIVATE:
    if message.chat.id not in _.ADMINS:
      return await message.reply("<code>You cannot use me baby </code>")
  
  sts = await message.reply_text("<code>Processing to Unsubs...</code>")
  try:
    txt = message.text.split(" ")[1]
    if txt in dts:
      if message.from_user.id in dts[txt]['users']:
        dts[txt]['users'].remove(message.from_user.id)
        sync(_.DB_NAME, 'dts')
        await retry_on_flood(sts.edit)("<code>Sucessfully Unsubs</code>")
      else:
        await retry_on_flood(sts.edit)("<code>You are not subscribed to this manga</code>")
    else:
      await retry_on_flood(sts.edit)("<code>Manga not found</code>")
  except Exception as err:
    await retry_on_flood(sts.edit)(err)


@Bot.on_message(filters.command("search"))
async def search_group(client, message):
  if Vars.IS_PRIVATE:
    if message.chat.id not in Vars.ADMINS:
      return await message.reply("<code>You cannot use me baby </code>")
  
  if client.SHORTENER:
    if not await premium_user(message.from_user.id):
      if not verify_token(message.from_user.id):
        if not message.from_user.id in client.ADMINS:
          return await get_token(message, message.from_user.id)
    
  try: txt = message.text.split(" ")[1]
  except: return await message.reply("<code>Format:- /search Manga </code>")
  photo = random.choice(Vars.PICS)

  try: 
    await message.reply_photo(photo, caption="Select search Webs .", reply_markup=plugins_list(), quote=True)
  except ValueError: 
    await message.reply_photo(photo, caption="Select search Webs .", reply_markup=plugins_list(), quote=True)


@Bot.on_message(filters.text & filters.private)
async def search(client, message):
  if Vars.IS_PRIVATE:
    if message.chat.id not in Vars.ADMINS:
      return await message.reply("<code>You cannot use me baby </code>")

  txt = message.text
  photo = random.choice(Vars.PICS)
  button = []
  if not txt.startswith("/"):
    try: await message.reply_photo(photo, caption="Select search Webs .", reply_markup=plugins_list(), quote=True)
    except ValueError: await message.reply_photo(photo, caption="Select search Webs .", reply_markup=plugins_list(), quote=True)
