from concurrent.futures import ThreadPoolExecutor
from rs3_api.hiscores import Hiscore
from typing import List
import customtkinter as ctk
import requests
import aiohttp
import asyncio
import json

class RunescapeNameChecker:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("600x300")
        self.root.title("RS Name Checker")
        self.root.resizable(False, False)

        # Side bar
        self.frame = ctk.CTkFrame(self.root, width=140, height=280)
        self.frame.place(x=15, y=10)

        self.name_label = ctk.CTkLabel(self.frame, text="Name Checker", font=("Helvetica", 16, 'bold'), text_color="white")
        self.name_label.place(x=15, y=10)

        self.name_label1 = ctk.CTkLabel(self.frame, text="Version 1.0", font=("Helvetica", 12), text_color="white")
        self.name_label1.place(x=35, y=35)

        self.set_apperance = ctk.CTkLabel(self.frame, text="Theme", font=("Helvetica", 12, 'bold'), text_color="white")
        self.set_apperance.place(x=45, y=205)

        self.set_appearance_var = ctk.StringVar(value="Dark")
        self.set_appearance_menu = ctk.CTkOptionMenu(self.frame, values=["Dark", "Light"], font=("Helvetica", 12,),
                                                    variable=self.set_appearance_var, command=self.update_appearance,
                                                    width=110, text_color="white")
        self.set_appearance_menu.place(x=12, y=235)

        # main search
        self.main_frame = ctk.CTkFrame(self.root, width=415, height=110)
        self.main_frame.place(x=170, y=11)

        self.main_frame1 = ctk.CTkFrame(self.main_frame, width=250, height=30)
        self.main_frame1.place(x=10, y=70)

        self.result_label = ctk.CTkLabel(self.main_frame1, text="", font=("Helvetica", 12), text_color="white")
        self.result_label.place(x=10, y=1)

        self.source_label = ctk.CTkLabel(self.main_frame, text="Source", font=("Helvetica", 12, 'bold'), text_color="white")
        self.source_label.place(x=55, y=150)

        self.source_var = ctk.StringVar(value="RS Hiscores")
        self.source_options: List[str] = ["RS Hiscores", "RunePixels"]
        self.source_menu = ctk.CTkOptionMenu(self.main_frame, values=self.source_options, variable=self.source_var,
                                             font=("Helvetica", 12), text_color="white")
        self.source_menu.place(x=265, y=70)
        
        self.name_entry = ctk.CTkEntry(self.main_frame, width=250, placeholder_text="Enter username", font=("Helvetica", 12))
        self.name_entry.place(x=10, y=35)

        self.button = ctk.CTkButton(self.main_frame, text="Check", command=self.check_name, text_color="white")
        self.button.place(x=265, y=35)

        self.text = ctk.CTkLabel(self.main_frame, text="Search", font=("Helvetica", 12, "bold"), text_color="white")
        self.text.place(x=10, y=5)

        self.hiscore = Hiscore()

    @staticmethod
    def check_name_availability(name: str, source: str) -> bool:
        if source == "RS Hiscores":
            try:
                Hiscore().user(name)
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

    def check_name(self):
        name: str = self.name_entry.get()
        source: str = self.source_var.get()
        if len(name) < 1:
            self.result_label.configure(text="Name cannot be empty")
        elif len(name) > 12:
            self.result_label.configure(text="Name is too long")
        elif not name.isalnum():
            self.result_label.configure(text="Name contains invalid characters")
        else:
            available = asyncio.run(self.check_name_availability_async(name, source))
            if available:
                self.result_label.configure(text="Username may be available")
            else:
                self.result_label.configure(text="Username is not available")

    async def check_name_availability_async(self, name: str, source: str) -> bool:
     if source == "RS Hiscores":
        try:
            await self.hiscore.user(name)
            return False
        except Exception:
            return True
     elif source == "RunePixels":
        url = f"https://runepixels.com:5000/players/{name}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                try:
                    response_json = await response.json()
                except aiohttp.client_exceptions.ContentTypeError:
                    return True
        try:
            if response_json['name'].lower() == name.lower():
                return False
            else:
                return True
        except json.JSONDecodeError:
            return True
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")
     else:
        raise ValueError(f"Unsupported source: {source}")
    def update_appearance(self, mode):
        if mode == "Dark":
            ctk.set_appearance_mode("dark")
            self.name_label.configure(text_color="white")
            self.set_apperance.configure(text_color="white")
            self.set_appearance_menu.configure(text_color="white")
            self.name_label1.configure(text_color="white")

        else:
            ctk.set_appearance_mode("light")
            self.name_label.configure(text_color="black")
            self.set_apperance.configure(text_color="black")
            self.set_appearance_menu.configure(text_color="black")
            self.name_label1.configure(text_color="black")

    def run(self):
        self.root.mainloop()

def main():
    checker = RunescapeNameChecker()
    checker.run()

if __name__ == '__main__':
    main()
