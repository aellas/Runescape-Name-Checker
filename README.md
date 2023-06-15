# RS Name Checker
<strong>RS Name Checker</strong> is a python script with a GUI that allows you to search for a username and see if it's still available. <br />
You can currently search the <strong>OSRS</strong> / <strong>RS3</strong> Hiscores & <strong>RunePixels</strong>.
<br />

![alt text](https://github.com/Arrayem/Runescape-Name-Checker/blob/main/images/Updated_UI.png?raw=true)

# Setup Instructions
+ Download [Python](https://www.python.org/)
+ Clone repo `git clone https://github.com/Arrayem/Runescape-Name-Checker.git`
+ Install requirements `pip install -r requirements.txt`
+ Run code `python3 main.py`

# Discord Bot
Want to setup the code for a discord bot? Here's an example you could use 
```python
import discord
from discord.ext import commands
from concurrent.futures import ThreadPoolExecutor
from rs3_api.hiscores import Hiscore
from osrs_api import Hiscores
from typing import List
import requests
import aiohttp
import asyncio
import json

@bot.command()
async def checkname(ctx, name: str, source: str):
    if len(name) < 1:
        await ctx.send('Name cannot be empty')
    elif len(name) > 12:
        await ctx.send('Name is too long')
    elif not name.isalnum():
        await ctx.send('Name contains invalid characters')
    else:
        available = await check_name_availability(name, source)
        if available:
            await ctx.send('Username may be available')
        else:
            await ctx.send('Username is not available')

async def check_name_availability(name: str, source: str) -> bool:
    if source == "RS3 Hiscores":
        try:
            Hiscore().user(name)
            return False
        except Exception:
            return True
    elif source == "OSRS Hiscores":
        try:
            Hiscores(username=name).skills.overall.rank
            return False
        except Exception:
            return True
    elif source == "RunePixels":
        url = f"https://runepixels.com:5000/players/{name}"
        with ThreadPoolExecutor() as executor:
            response = executor.submit(requests.get, url).result()
        try:
            data = json.loads(response)
            if data['name'].lower() == name.lower():
                return False
            else:
                return True
        except json.JSONDecodeError:
            return True
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")
    else:
        raise ValueError(f"Unsupported source: {source}")
```

# Future Updates
+ Add the option to search for every possible 2 or 3 letter usernames that may be available
+ Add an option to search a list of usernames you provide
+ (Maybe) make a function to add the ability to try and apply a username to your account
+ Release an executable version, code will remain open-source so you can run it yourself


# Credits
+ [Luciano Feder](https://github.com/lucianofeder) for the [RS3 API Wrapper](https://github.com/lucianofeder/runescape3-api-wrapper
+ [Chasesc](https://github.com/Chasesc) for the [OSRS API Wrapper](https://github.com/Chasesc/OSRS-API-Wrapper)

