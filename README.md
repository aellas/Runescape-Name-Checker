# 🔎 RSNChecker [v1.5]
**RSNChecker** is an open-source project written in Python that allows you to search for a Runescape name to see if it's available. You can search for either a single username or enter multiple usernames (I've tested 500 usernames at once) with the added benefit of either checking OSRS Hiscores or RS3 Hiscores.

# 🧭 Demo 
![Image](/images/image.png?raw=true "Demo")

# ✍️ Manual Setup
+ Download [Python](https://www.python.org/)
+ Clone repo `https://github.com/aellas/testing.git`
+ Or download from [here](https://github.com/aellas/testing/archive/refs/heads/main.zip)
+ Install requirements `pip install -r requirements.txt`
+ Run code `python3 main.py` <br />

# ✏️ Generate
+ You can now generate (50) unique 2/3 letter /+ number RSN's to check

![Image](/images/generate.png?raw=true "Generate")

+ You can change how many names to generate by editing the generate functions
```python
def two_letter_func(name_entry):
    names = ["".join(random.choices(string.ascii_letters, k=2)) for _ in range(50)]
    name_entry.delete(0, "end")
    name_entry.insert(0, ",".join(names))
```
+ Where it says `for _ in range(50)` change `50` to your desired number output.

# ❤️ Credits
+ [Luciano Feder](https://github.com/lucianofeder) for [RS3 API Wrapper](https://github.com/lucianofeder/runescape3-api-wrapper)
+ [Chasesc](https://github.com/Chasesc) for [OSRS API Wrapper](https://github.com/Chasesc/OSRS-API-Wrapper)


