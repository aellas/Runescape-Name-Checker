from rs3_api.hiscores import Hiscore
from osrs_api import Hiscores
from typing import List
import customtkinter as ctk
import aiohttp
import asyncio
import json

class RunescapeNameChecker:
    def __init__(self):
        self.app = None
        self.root = ctk.CTk()
        self.root.geometry("600x355")
        self.root.title("RSNChecker")
        self.root.resizable(False, False)
        self.frame = ctk.CTkFrame(self.root, width=140, height=330)
        self.frame.place(x=15, y=11)
        self.name_label = ctk.CTkLabel(self.frame, text="RSNChecker", font=("Helvetica", 14, 'bold'), text_color="white")
        self.name_label.place(x=25, y=15)
        self.name_label1 = ctk.CTkLabel(self.frame, text="Version 1.1", font=("Helvetica", 12), text_color="white")
        self.name_label1.place(x=37, y=38)
        self.set_appearance_var = ctk.StringVar(value="Theme")
        self.set_appearance_menu = ctk.CTkOptionMenu(self.frame, values=["Dark", "Light"], font=("Helvetica", 12,),
                                                    variable=self.set_appearance_var, command=self.update_appearance,
                                                    width=110, text_color="white")
        self.set_appearance_menu.configure(width=100)
        self.set_appearance_menu.place(x=17, y=285)
        self.main_frame = ctk.CTkFrame(self.root, width=415, height=110)
        self.main_frame.place(x=170, y=11)
        self.status_label = ctk.CTkLabel(self.main_frame, text="", font=("Helvetica", 12, "bold"), text_color="white")
        self.status_label.place(x=265, y=60)
        self.source_var = ctk.StringVar(value="OSRS Hiscores")
        self.source_options: List[str] = ["OSRS Hiscores", "RS3 Hiscores", "RunePixels"]
        self.source_menu = ctk.CTkOptionMenu(self.main_frame, values=self.source_options, variable=self.source_var,font=("Helvetica", 12), text_color="white")
        self.source_menu.place(x=265, y=70)
        self.name_entry = ctk.CTkEntry(self.main_frame, width=250, placeholder_text="Enter usernames", font=("Helvetica", 12))
        self.name_entry.place(x=10, y=35)
        self.button = ctk.CTkButton(self.main_frame, text="Check", command=self.check_name, text_color="white")
        self.button.place(x=265, y=35)
        self.main_frame1 = ctk.CTkFrame(self.main_frame, width=250, height=30)
        self.main_frame1.place(x=10, y=70)
        self.checking_name = ctk.CTkLabel(self.main_frame1, text="", font=("Helvetica", 12), text_color="white")
        self.checking_name.place(x=10, y=1)
        self.text = ctk.CTkLabel(self.main_frame, text="Search", font=("Helvetica", 12, "bold"), text_color="white")
        self.text.place(x=10, y=5)
        
        
        self.not_available = ctk.CTkTextbox(self.root,width=200, height=170, activate_scrollbars=True)
        self.not_available.place(x=170, y=170)  
        self.available = ctk.CTkTextbox(self.root,width=200, height=170, activate_scrollbars=True)
        self.available.place(x=383, y=170)
        
        self.textbox1 = ctk.CTkTextbox(self.root,width=200, height=30)
        self.textbox1.insert("0.0", "                 Not Available")
        self.textbox1.place(x=171, y=131)
        self.textbox1.configure(state="disabled")
        
        self.textbox2 = ctk.CTkTextbox(self.root,width=200, height=30)
        self.textbox2.insert("0.0", "                 Maybe Available")
        self.textbox2.place(x=380, y=131)   
        self.textbox2.configure(state="disabled")

        self.available_text = ctk.CTkLabel(self.textbox1, text="Not Available", font=("Helvetica", 12, "bold"), text_color="white")
        self.available_text.place(x=240, y=132)
             
        self.root.bind("<Return>", lambda event: self.check_name())
        self.root.bind("<Escape>", lambda event: self.root.destroy())
                


    async def check_name_availability(self, name: str, source: str, session: aiohttp.ClientSession) -> bool:
        if source == "RS3 Hiscores":
            try:
                Hiscore().user(name)
                return False
            except Exception:
                return True
        elif source == "OSRS Hiscores":
            try:
                Hiscores(username=name)
                return False
            except Exception:
                return True
        elif source == "RunePixels":
            url = f"https://runepixels.com:5000/players/{name}"
            async with session.get(url, timeout=10) as response:
                try:
                    data = await response.json()
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

    async def search_name(self):
        name_entry_text = self.name_entry.get().strip()
        names: List[str] = name_entry_text.split(",")
        source: str = self.source_var.get()
        tasks = []
        for name in names:
            stripped_name_loop = name.strip()
            if not stripped_name_loop:
                continue
            if len(stripped_name_loop) < 1:
                self.not_available.insert(
                    "end", f"Name cannot be empty\n"
                )
                continue
            elif len(stripped_name_loop) > 12:
                self.not_available.insert(
                    "end", f"Name is too long\n"
                )
                continue
            elif not all(
                char.isalnum() or char.isspace() or char == "_" or char == "-" for char in stripped_name_loop
            ):
                self.not_available.insert(
                    "end", f"invalid characters detected\n"
                )
                continue
            elif stripped_name_loop == "_":
                self.not_available.insert(
                    "end", f"'Name cannot be just underscores\n"
                )
                continue
            else:
                async with aiohttp.ClientSession() as session:
                    self.checking_name.configure(text=f"Checking availability for {stripped_name_loop}")
                    self.root.update()
                    await asyncio.sleep(0.5)
                    tasks.append(
                        asyncio.create_task(
                            self.check_name_availability(stripped_name_loop, source, session)
                        )
                    )
        if tasks:
            results = await asyncio.gather(*tasks)
            for name, result in zip(names, results):
                if result:
                    self.available.insert(
                        "end", f"{name.strip()}\n"
                    )
                else:
                    self.not_available.insert(
                        "end", f"{name.strip()}\n"
                    )

        self.checking_name.configure(text="")

                
    def update_appearance(self, mode):
     if mode == "Dark":
        ctk.set_appearance_mode("dark")
        self.name_label.configure(text_color="white")
        self.set_appearance_menu.configure(text_color="white")
        self.name_label1.configure(text_color="white")
        self.source_menu.configure(text_color="white")
        self.button.configure(text_color="white")
        self.text.configure(text_color="white")
     else:
        ctk.set_appearance_mode("light")
        self.name_label.configure(text_color="black")
        self.set_appearance_menu.configure(text_color="black")
        self.name_label1.configure(text_color="black")
        self.source_menu.configure(text_color="black")
        self.button.configure(text_color="black")
        self.text.configure(text_color="black")
        
    def check_name(self):
        self.button.configure(state="disabled")
        self.available.delete(1.0, "end")
        self.not_available.delete(1.0, "end")
        asyncio.run(self.search_name())
        self.button.configure(state="normal")
        
    def run(self):
        self.root.mainloop()     

def main():
    checker = RunescapeNameChecker()
    checker.run()

if __name__ == '__main__':
    main()