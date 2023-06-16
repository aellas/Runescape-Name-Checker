from concurrent.futures import ThreadPoolExecutor
import requests
from rs3_api.hiscores import Hiscore
from osrs_api import Hiscores
from typing import List
import customtkinter as ctk
import aiohttp
import asyncio
import json

class RunescapeNameChecker:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("600x355")
        self.root.title("RS Name Checker")
        self.root.resizable(False, False)
        self.frame = ctk.CTkFrame(self.root, width=140, height=110)
        self.frame.place(x=15, y=11)
        self.name_label = ctk.CTkLabel(self.frame, text="Name Checker", font=("Helvetica", 14, 'bold'), text_color="white")
        self.name_label.place(x=15, y=10)
        self.name_label1 = ctk.CTkLabel(self.frame, text="Version 1.0", font=("Helvetica", 12), text_color="white")
        self.name_label1.place(x=35, y=30)
        self.set_appearance_var = ctk.StringVar(value="Theme")
        self.set_appearance_menu = ctk.CTkOptionMenu(self.frame, values=["Dark", "Light"], font=("Helvetica", 12,),
                                                    variable=self.set_appearance_var, command=self.update_appearance,
                                                    width=110, text_color="white")
        self.set_appearance_menu.place(x=13, y=65)
        self.main_frame = ctk.CTkFrame(self.root, width=415, height=110)
        self.main_frame.place(x=170, y=11)
        self.main_frame1 = ctk.CTkFrame(self.main_frame, width=250, height=30)
        self.main_frame1.place(x=10, y=70)
        self.result_label = ctk.CTkLabel(self.main_frame1, text="", font=("Helvetica", 12), text_color="white")
        self.result_label.place(x=10, y=1)
        self.source_var = ctk.StringVar(value="OSRS Hiscores")
        self.source_options: List[str] = ["OSRS Hiscores", "RS3 Hiscores", "RunePixels"]
        self.source_menu = ctk.CTkOptionMenu(self.main_frame, values=self.source_options, variable=self.source_var,font=("Helvetica", 12), text_color="white")
        self.source_menu.place(x=265, y=70)
        self.name_entry = ctk.CTkEntry(self.main_frame, width=250, placeholder_text="Enter username", font=("Helvetica", 12))
        self.name_entry.place(x=10, y=35)
        self.button = ctk.CTkButton(self.main_frame, text="Check", command=self.check_name, text_color="white")
        self.button.place(x=265, y=35)
        self.text = ctk.CTkLabel(self.main_frame, text="Search", font=("Helvetica", 12, "bold"), text_color="white")
        self.text.place(x=10, y=5)
        self.text_box = ctk.CTkTextbox(self.root,width=280, height=180, activate_scrollbars=True)
        self.text_box.place(x=15, y=160)
        self.label1 = ctk.CTkLabel(self.root, text="Input", font=("Helvetica", 14, "bold"), text_color="white")
        self.label1.place(x=120, y=128)
        self.output_result = ctk.CTkTextbox(self.root,width=280, height=180, activate_scrollbars=True)
        self.output_result.place(x=305, y=160)
        self.label2 = ctk.CTkLabel(self.root, text="Output", font=("Helvetica", 14, "bold"), text_color="white")
        self.label2.place(x=410, y=128) 
        self.root.bind("<Return>", lambda event: self.check_name())
        self.root.bind("<Escape>", lambda event: self.root.destroy())
        
    async def check_name_availability(self, name: str, source: str) -> bool:
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
        
    async def check_name_async(self):
     name_entry_text = self.name_entry.get().strip()
     text_box_text = self.text_box.get("1.0", "end-1c").strip()

     if name_entry_text and text_box_text:
        raise ValueError("Can't use both search entries, use one.")

     input_text = name_entry_text or text_box_text
     input_text: str = self.name_entry.get().strip()
     if not input_text:
        input_text: str = self.text_box.get("1.0", "end-1c")
     if not input_text:
        return
     names: List[str] = input_text.split(",")
     source: str = self.source_var.get()
     if len(names) == 1:
        stripped_name = names[0].strip()
        if not stripped_name:
            return
        if len(stripped_name) < 1:
            self.result_label.configure(text=f"'{stripped_name}': Name cannot be empty")
        elif len(stripped_name) > 12:
            self.result_label.configure(text=f"'{stripped_name}': Name is too long")
        elif not all(
            char.isalnum() or char.isspace() or char == "_" for char in stripped_name
        ):
            self.result_label.configure(
                text=f"'{stripped_name}': Name contains invalid characters"
            )
        elif stripped_name == "_":
            self.result_label.configure(
                text=f"'{stripped_name}': Name cannot be just underscores"
            )
        else:
            available = await self.check_name_availability(stripped_name, source)
            if available:
                self.result_label.configure(
                    text=f"May be available"
                )
            else:
                self.result_label.configure(
                    text=f"Not available"
                )
     else:
        available_names = []
        async with aiohttp.ClientSession() as session:
            tasks = []
            for name in names:
                stripped_name_loop = name.strip()
                if not stripped_name_loop:
                    continue
                if len(stripped_name_loop) < 1:
                    available_names.append(f"'{stripped_name_loop}': Name cannot be empty")
                elif len(stripped_name_loop) > 12:
                    available_names.append(f"'{stripped_name_loop}': Name is too long")
                elif not all(
                    char.isalnum() or char.isspace() or char == "_" for char in stripped_name_loop
                ):
                    available_names.append(
                        f"'{stripped_name_loop}': Name contains invalid characters"
                    )
                elif stripped_name_loop == "_":
                    available_names.append(
                        f"'{stripped_name_loop}': Name cannot be just underscores"
                    )
                else:
                    task = asyncio.create_task(self.check_name_availability(stripped_name_loop, source))
                    tasks.append(task)
            results = await asyncio.gather(*tasks)
            for i, result in enumerate(results):
                if result:
                    available_names.append(f"{names[i].strip()} may be available")
            self.output_result.insert(1.0, "\n".join(available_names))




    def update_appearance(self, mode):
     if mode == "Dark":
        ctk.set_appearance_mode("dark")
        self.name_label.configure(text_color="white")
        self.set_appearance_menu.configure(text_color="white")
        self.name_label1.configure(text_color="white")
        self.result_label.configure(text_color="white")
        self.source_menu.configure(text_color="white")
        self.button.configure(text_color="white")
        self.text.configure(text_color="white")
     else:
        ctk.set_appearance_mode("light")
        self.name_label.configure(text_color="black")
        self.set_appearance_menu.configure(text_color="black")
        self.name_label1.configure(text_color="black")
        self.result_label.configure(text_color="black")
        self.source_menu.configure(text_color="black")
        self.button.configure(text_color="black")
        self.text.configure(text_color="black")
        
    def check_name(self):
        try:
         asyncio.get_event_loop().run_until_complete(self.check_name_async())
        except ValueError as e:
         self.result_label.configure(text=str(e))
        
    def run(self):
        self.root.mainloop()     

def main():
    checker = RunescapeNameChecker()
    checker.run()

if __name__ == '__main__':
    main()