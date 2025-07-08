import pyrogram
from time import time 
from loguru import logger

from pyrogram import idle
import random, os, shutil, asyncio

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class Vars:
  API_ID = int(os.environ.get("API_ID", "29245477"))
  API_HASH = os.environ.get("API_HASH", "0abc83883262245c90ca337b7a0375c4")
  
  BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
  plugins = dict(
    root="TG",
    #include=["TG.users"]
  )
  
  LOG_CHANNEL = os.environ.get("LOG_CHANNEL", "-1002456565415")
  UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL", "-1001607131442")
  DB_URL = os.environ.get("DB_URL", "mongodb+srv://Kafka:Au3OoWzCDYJKeuHU@cluster0.lz2m8iy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
  
  PORT = int(os.environ.get("PORT", "8080"))
  ADMINS = [7654385403]
  
  IS_PRIVATE = os.environ.get("IS_PRIVATE", None) #True Or None  Bot is for admins only
  CONSTANT_DUMP_CHANNEL = os.environ.get("CONSTANT_DUMP_CHANNEL", None)
  WEBS_HOST = os.environ.get("WEBS_HOST", True) # For Render and Koyeb
  
  DB_NAME = "cluster0"
  PING = time()
  FORCE_SUB_CHANNEL = os.environ.get("FORCE_SUB_CHANNEL", "-1001457313028")
  SHORTENER = os.environ.get("SHORTENER", "shortxlinks.com")
  SHORTENER_API = os.environ.get("SHORTENER_API", "64d631b036df348caab852591a09288cbf5b6809") # put {} for url, ex: shornter.api?url={}
  DURATION = int(os.environ.get("DURATION", "20")) # hrs
  PICS = (
    "https://ik.imagekit.io/jbxs2z512/hd-anime-prr1y1k5gqxfcgpv.jpg?updatedAt=1748487947183",
    "https://ik.imagekit.io/jbxs2z512/naruto_GxcPgSeOy.jpg?updatedAt=1748486799631",
    "https://ik.imagekit.io/jbxs2z512/dazai-osamu-sunset-rooftop-anime-wallpaper-cover.jpg?updatedAt=1748488276069",
    "https://ik.imagekit.io/jbxs2z512/thumb-1920-736461.png?updatedAt=1748488419323",
    "https://ik.imagekit.io/jbxs2z512/116847-3840x2160-desktop-4k-bleach-background-photo.jpg?updatedAt=1748488510841",
    "https://ik.imagekit.io/jbxs2z512/images_q=tbn:ANd9GcSjvt9DcrLXzGYEwwOpxwCSFXTfKEhXhVB-Zg&s?updatedAt=1748488611032",
    "https://ik.imagekit.io/jbxs2z512/thumb-1920-777955.jpg?updatedAt=1748488978230",
    "https://ik.imagekit.io/jbxs2z512/thumb-1920-1361035.jpeg?updatedAt=1748488911202",
    "https://ik.imagekit.io/jbxs2z512/akali-wallpaper-960x540_43.jpg?updatedAt=1748489275125",
    "https://ik.imagekit.io/jbxs2z512/robin-honkai-star-rail-497@1@o?updatedAt=1748490140360",
    "https://ik.imagekit.io/jbxs2z512/wallpapersden.com_tian-guan-ci-fu_1920x1080.jpg?updatedAt=17484902552770000",
    "https://ik.imagekit.io/jbxs2z512/1129176.jpg?updatedAt=1748491905419",
    "https://ik.imagekit.io/jbxs2z512/wp14288215.jpg?updatedAt=1748492348766",
    "https://ik.imagekit.io/jbxs2z512/8k-anime-girl-and-flowers-t4bj6u55nmgfdrhe.jpg?updatedAt=1748493169919",
    "https://ik.imagekit.io/jbxs2z512/anime_Fuji_Choko_princess_anime_girls_Sakura_Sakura_Woman_in_Red_mask_palace-52030.png!d?updatedAt=1748493259665",
    "https://ik.imagekit.io/jbxs2z512/1187037bb1d8aaf14a631f7b813296f1.jpg?updatedAt=1748493396756",
    "https://ik.imagekit.io/jbxs2z512/yor_forger_by_senku_07_dgifqh7-fullview.jpg_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9ODAzIiwicGF0aCI6IlwvZlwvNDAxZDdlYTYtOGEyZi00ZTFiLTkxYTAtNjA3YmRlYTgzZmE4XC9kZ2lmcWg3LWNlMjY3Mzc2LWQ4NWYtNGMzZS1iNWY1LWU0OTZhYWM3ZmUyNC5wbmciLCJ3aWR0aCI6Ijw9MTI4MCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.FVwtt0HGKv6UQqWHkEbxmE1qkI5CFNNS5SzAYj4EVUs?updatedAt=1748493490929",
    "https://ik.imagekit.io/jbxs2z512/attack-on-titan-mikasa-cover-image-ybt96t1e1041qdt3.jpg?updatedAt=1748493720903",
    "https://ik.imagekit.io/jbxs2z512/tsunade-at-her-desk-bakoh4jeg42sjn3c.jpg?updatedAt=1748493962363",
    "https://ik.imagekit.io/jbxs2z512/9aab3a2fba4bd0117b990e4ca453cb61.jpg?updatedAt=1748494616359",
    "https://ik.imagekit.io/jbxs2z512/3bf8ed2f8f1acacd5451444ba6e7842a.jpg?updatedAt=1748494817874",
    "https://ik.imagekit.io/jbxs2z512/5f10d5eeab91c46b2b442d170998a10e.jpg?updatedAt=1748494936535",
    "https://ik.imagekit.io/jbxs2z512/18a02ef5ab71d0df7a1b4f854c214dfb.jpg?updatedAt=1748495170887",
    "https://ik.imagekit.io/jbxs2z512/3860e6e91d9cc88b4579d096e4edaaf3.jpg?updatedAt=1748495479043",
    "https://ik.imagekit.io/jbxs2z512/d367f6d6d22f4ead7c359e9f091db94e.jpg?updatedAt=1748495852427",
    "https://ik.imagekit.io/jbxs2z512/9c989e113f6ba997e417a436cde4a387.jpg?updatedAt=1748496068439",
    "https://ik.imagekit.io/jbxs2z512/8750ba474fb938b94d6b1a4093e5c104.jpg?updatedAt=1748496295001",
    "https://ik.imagekit.io/jbxs2z512/2e6937e9d7c6fb4c179c3e92684bb7f4.jpg?updatedAt=1748496479835",
    "https://ik.imagekit.io/jbxs2z512/99ce9434aed7b5785cae1d784aee3d72.jpg?updatedAt=1748497104463",
    "https://ik.imagekit.io/jbxs2z512/stycc.jpg?updatedAt=1748497475612",
    "https://ik.imagekit.io/jbxs2z512/9bba360ebd71d6086e19d5729b80a5b8.jpg?updatedAt=1748497751053",
    "https://ik.imagekit.io/jbxs2z512/94f23c5b9055846db8047565bbb8cd70.jpg?updatedAt=1748497975473",
    "https://ik.imagekit.io/jbxs2z512/eec7ff7238553179fb4236da3537d19d.jpg?updatedAt=1748498058373",
    "https://ik.imagekit.io/jbxs2z512/Fight-Break-Sphere.png?updatedAt=1750042299023",
    "https://ik.imagekit.io/jbxs2z512/doupocangqiong-medusa-queen-hd-wallpaper-preview.jpg?updatedAt=1750042397343",
    "https://ik.imagekit.io/jbxs2z512/wp5890248.jpg?updatedAt=1750042498187",
    "https://ik.imagekit.io/jbxs2z512/sacffc_uu-T1F5AC?updatedAt=1750042873876",
    "https://ik.imagekit.io/jbxs2z512/1345216.jpeg?updatedAt=1750042982858",
    "https://ik.imagekit.io/jbxs2z512/shanks-divine-departure-attack-in-one-piece-sn.jpg?updatedAt=1750043121252",
    "https://ik.imagekit.io/jbxs2z512/1a74aff1d81a1af5f3e25b9b30282e06.jpg?updatedAt=1750043251516",
    "https://ik.imagekit.io/jbxs2z512/a7241b95829a685f99a900e509e39591.jpg?updatedAt=1750043398842",
    "https://ik.imagekit.io/jbxs2z512/2dff5d8b43c34b8bdc6b2064e0917123_low.webp?updatedAt=1751077578776",
    "https://ik.imagekit.io/jbxs2z512/1217847739e4bf310076a217bb4c4762_low.webp?updatedAt=1751077642452",
    "https://ik.imagekit.io/jbxs2z512/44ba8229f62d7f7b9251ff8839a1d8ea_low.webp?updatedAt=1751077714921",
    "https://ik.imagekit.io/jbxs2z512/a6d39692ba169fc142a410995878408d_low.webp?updatedAt=1751077802364",
    "https://ik.imagekit.io/jbxs2z512/367c7d7031988b2b06a56e7096a734153fab2284_low.webp?updatedAt=1751077891589",
    "https://ik.imagekit.io/jbxs2z512/22219.jpg?updatedAt=1751107408410",
    "https://ik.imagekit.io/jbxs2z512/21418.jpg?updatedAt=1751107452919",
    "https://ik.imagekit.io/jbxs2z512/mythical-dragon-beast-anime-style_23-2151112835.jpg?updatedAt=1751107574210",
    "https://ik.imagekit.io/jbxs2z512/halloween-scene-illustration-anime-style_23-2151794288.jpg?updatedAt=1751107676806",
    "https://ik.imagekit.io/jbxs2z512/5823589-2920x1640-desktop-hd-boy-programmer-wallpaper-image.jpg_id=1726666227?updatedAt=1751107911063",
    "https://ik.imagekit.io/jbxs2z512/thumbbig-1345576.webp?updatedAt=1751108065802",
    "https://ik.imagekit.io/jbxs2z512/thumb-440-1340473.webp?updatedAt=1751108159970",
    "https://ik.imagekit.io/jbxs2z512/thumb-440-1250445.webp?updatedAt=1751108243962",
    "https://ik.imagekit.io/jbxs2z512/wp3084738.jpg?updatedAt=1751108326075",
    "https://ik.imagekit.io/jbxs2z512/wp12362449.png?updatedAt=1751108554882",
    "https://ik.imagekit.io/jbxs2z512/wp7627005.jpg?updatedAt=1751108634878",
    "https://ik.imagekit.io/jbxs2z512/thumbbig-1335194.webp?updatedAt=1751108710765",
    "https://ik.imagekit.io/jbxs2z512/thumbbig-1373976.webp?updatedAt=1751108748746",
    "https://ik.imagekit.io/jbxs2z512/thumbbig-1065277.webp?updatedAt=1751108877871",
    "https://ik.imagekit.io/jbxs2z512/thumbbig-877141.webp?updatedAt=1751108916209",
    "https://ik.imagekit.io/jbxs2z512/thumbbig-856517.webp?updatedAt=1751108984376",
    "https://ik.imagekit.io/jbxs2z512/thumbbig-722181.webp?updatedAt=1751109016670",
    "https://ik.imagekit.io/jbxs2z512/thumbbig-1337392.webp?updatedAt=1751109084903",
    "https://ik.imagekit.io/jbxs2z512/anime-4k-pc-hd-download-wallpaper-preview%20(1).jpg?updatedAt=1751109522060",
    "https://ik.imagekit.io/jbxs2z512/876145-3840x2160-desktop-4k-konan-naruto-background-image%20(1).jpg?updatedAt=1751109523353",
    "https://ik.imagekit.io/jbxs2z512/tumblr_9663cff78634f174f81b41b64fc450df_66ebd999_1280%20(1).png?updatedAt=1751109523759",
    "https://ik.imagekit.io/jbxs2z512/anime-girl-demon-horn-art-4k-wallpaper-uhdpaper.com-714@2@b%20(1).jpg?updatedAt=1751109524369",
    "https://ik.imagekit.io/jbxs2z512/wp14771453.png?updatedAt=1751110776400",
    "https://ik.imagekit.io/jbxs2z512/dbbb586df338d55d340ec650bcdd74fe.jpg?updatedAt=1751110984735",
    "https://ik.imagekit.io/jbxs2z512/5bf388947f00a495089a892729e30eff.jpg?updatedAt=1751111093184",
    "https://ik.imagekit.io/jbxs2z512/70c6b3a1007864c703eee8161de10b16.jpg?updatedAt=1751111171988",
    "https://ik.imagekit.io/jbxs2z512/8f27da8d6616d8f80af36c8b765a149b.jpg?updatedAt=1751111431360",
    "https://ik.imagekit.io/jbxs2z512/2bbc87d73d2aeefb70c5ab9cc7f5d9d4.jpg?updatedAt=1751111480775",
    "https://ik.imagekit.io/jbxs2z512/1fa6825ca849a55808e112371721cfe4.jpg?updatedAt=1751111592964",
    "https://ik.imagekit.io/jbxs2z512/67a32939a3510571e08ef949ac9209e6.jpg?updatedAt=1751111647854",
    "https://ik.imagekit.io/jbxs2z512/a5f26efcc42a213a64eda0a2a15fc26c.jpg?updatedAt=1751111705093",
    "https://ik.imagekit.io/jbxs2z512/4d8f713943c109c88130118b12803cc7.jpg?updatedAt=1751111768586",
    "https://ik.imagekit.io/jbxs2z512/c02aecb70c3c6a5b1f51ba09e4d2cc70.jpg?updatedAt=1751111979586",
    "https://ik.imagekit.io/jbxs2z512/6c2618a1eea58d22e2d1a5ba99c95a1c.jpg?updatedAt=1751112051082",
    "https://ik.imagekit.io/jbxs2z512/7a82750e26bf451ab1775993279e2c64.jpg?updatedAt=1751112189297",
    "https://ik.imagekit.io/jbxs2z512/a469262476f60456dd4aceb8a75deed5.jpg?updatedAt=1751112263336",
  )



class Manhwa_Bot(pyrogram.Client, Vars):
  def __init__(self):
    super().__init__(
      "ManhwaBot",
      api_id=self.API_ID,
      api_hash=self.API_HASH,
      bot_token=self.BOT_TOKEN,
      plugins=self.plugins,
      workers=50,
    )
    self.logger = logger
    self.__version__ = pyrogram.__version__
    
  async def start(self):
    await super().start()
    
    async def run_flask():
      cmds = ("gunicorn", "app:app")
      process = await asyncio.create_subprocess_exec(
        *cmds,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
      )
      stdout, stderr = await process.communicate()

      if process.returncode != 0:
        logger.error(f"Flask app failed to start: {stderr.decode()}")
      
      logger.info("Webs app started successfully")
    
    usr_bot_me = await self.get_me()
    
    if os.path.exists("restart_msg.txt"):
      with open("restart_msg.txt", "r") as f:
        chat_id, message_id = f.read().split(":")
        f.close()

      try: await self.edit_message_text(int(chat_id), int(message_id), "<code>Restarted Successfully</code>")
      except Exception as e: logger.exception(e)

      os.remove("restart_msg.txt")
    
    if os.path.exists("Process"):
      shutil.rmtree("Process")
    
    self.logger.info("""
    
     ___       __   ___  ________  ________  ________  ________          ________  ________  _________  ________      
    |\  \     |\  \|\  \|\_____  \|\   __  \|\   __  \|\   ___ \        |\   __  \|\   __  \|\___   ___\\   ____\     
    \ \  \    \ \  \ \  \\|___/  /\ \  \|\  \ \  \|\  \ \  \_|\ \       \ \  \|\ /\ \  \|\  \|___ \  \_\ \  \___|_    
     \ \  \  __\ \  \ \  \   /  / /\ \   __  \ \   _  _\ \  \ \\ \       \ \   __  \ \  \\\  \   \ \  \ \ \_____  \   
      \ \  \|\__\_\  \ \  \ /  /_/__\ \  \ \  \ \  \\  \\ \  \_\\ \       \ \  \|\  \ \  \\\  \   \ \  \ \|____|\  \  
       \ \____________\ \__\\________\ \__\ \__\ \__\\ _\\ \_______\       \ \_______\ \_______\   \ \__\  ____\_\  \ 
        \|____________|\|__|\|_______|\|__|\|__|\|__|\|__|\|_______|        \|_______|\|_______|    \|__| |\_________\
                                                                                                          \|_________|


    """)
    self.username = usr_bot_me.username
    self.logger.info("Make By https://t.me/Wizard_Bots ")
    self.logger.info(f"Manhwa Bot Started as {usr_bot_me.first_name} | @{usr_bot_me.username}")
    
    if self.WEBS_HOST:
      await run_flask()
    
    MSG = """<blockquote><b>🔥 SYSTEMS ONLINE. READY TO RUMBLE. 🔥
Sleep mode deactivated. Neural cores at 100%. Feed me tasks, and watch magic happen. Let’s. Get. Dangerous.</b></blockquote>"""
    
    PICS = random.choice(Vars.PICS)
    
    button = [[
      InlineKeyboardButton('*Start Now*', url= f"https://t.me/{usr_bot_me.username}?start=start"),
      InlineKeyboardButton("*Channel*", url = "telegram.me/Wizard_Bots")
    ]]
    
    try: await self.send_photo(self.UPDATE_CHANNEL, photo=PICS, caption=MSG, reply_markup=InlineKeyboardMarkup(button))
    except: pass

    
  async def stop(self):
    await super().stop()
    self.logger.info("Manhwa Bot Stopped")


Bot = Manhwa_Bot()
    
