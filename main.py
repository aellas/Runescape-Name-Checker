from rs3_api.hiscores import Hiscore
from osrs_api import Hiscores
from typing import List
import customtkinter as ctk
import aiohttp
import asyncio
import functions.clear
import functions.copy
import functions.time
import generate.random

class RunescapeNameChecker:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("570x395")
        self.root.title("RSNChecker")
        self.root.resizable(False, False)
        
        # ======= Search Frame =========
        
        self.search_frame = ctk.CTkFrame(self.root, width=355, height=110)
        self.search_frame.place(x=10, y=10)
        
        # Search Label
        self.search_label = ctk.CTkLabel(
            self.search_frame,
            text="Search",
            font=("Roboto Medium", 14, "bold"),
        )
        self.search_label.place(x=10, y=3)
        
        # Search entry
        self.name_entry = ctk.CTkEntry(
            self.search_frame,
            width=220,
            font=("Roboto Medium", 12),
            placeholder_text="Enter username",
        )
        self.name_entry.place(x=10, y=35)
        
        # Search button
        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Check",
            command=self.check_name,
            font=("Roboto Medium", 12),
            text_color="white",
            width=100,
            height=30,
            
        )
        self.search_button.place(x=240, y=33)
        
        # Stop button
        self.stop_button = ctk.CTkButton(
            self.search_frame,
            text="Stop",
            command=self.stop_search,
            font=("Roboto Medium", 12),
            text_color="white",
            width=100,
            height=30,
            
        )
        self.stop_button.place(x=240, y=70)
        
        # Progress bar
        self.progress_bar = ctk.CTkFrame(
            self.search_frame,
            width=220,
            height=30
        )
        self.progress_bar.place(x=10, y=70)
        
        self.progress_label = ctk.CTkLabel(
            self.progress_bar,
            text="",
            font=("Roboto Medium", 12),
            text_color="white",
        )
        self.progress_label.place(x=5, y=0)
        
        
        # ========= Source (Right) Frame =========
        
        self.source_frame = ctk.CTkFrame(self.root, width=177, height=110)
        self.source_frame.place(x=380, y=10)
        
        self.configure_label = ctk.CTkLabel(
            self.source_frame,
            text="Search Options",
            font=("Roboto Medium", 14, "bold"),
        )
        self.configure_label.place(x=32, y=18)
        
        # Source Selection
        self.selection_var = ctk.StringVar(value="OSRS Hiscores")
        self.selection_options = ["OSRS Hiscores", "RS3 Hiscores"]
        self.source_selection = ctk.CTkOptionMenu(
            self.source_frame,
            values = self.selection_options,
            variable= self.selection_var,
            font=("Roboto Medium", 12),
        )
        self.source_selection.place(x=18, y=55)
        
        # ========= Guide (Left) Frame =========
        
        self.guide_textbox = ctk.CTkTextbox(
            self.root,
            width=178,
            height=181,
            border_color="white",
            border_width=1,
            font=("Roboto Medium", 12),
        )
        self.guide_textbox.place(x=380, y=130)
                
        self.copy_button = ctk.CTkButton(
            self.root,
            text="Copy to Clipboard",
            text_color="white",
            command=lambda: functions.copy.copy_maybe_available(
                self.guide_textbox, self.copy_button
            ),
            font=("Roboto Medium", 12),
            width=178,
            fg_color="#2F8C56",
        )     
        self.copy_button.place(x=380, y=320)
        
        self.clear_button = ctk.CTkButton(
            self.root,
            text="Clear Results",
            text_color="white",
            command=lambda: functions.clear.clear_search_results(self.guide_textbox),
            width=178
        )
        self.clear_button.place(x=380, y=355)

        self.random_frame = ctk.CTkFrame(self.root, width=355, height=90)
        self.random_frame.place(x=10, y=130)

        self.two_letter = ctk.CTkButton(
            self.random_frame,
            text="Two Letters",
            command=lambda: generate.random.two_letter_func(self.name_entry),
            font=("Helvetica", 12),
            text_color="white",
            width=90,
        )
        self.two_letter.place(x=10, y=10)

        self.three_letter = ctk.CTkButton(
            self.random_frame,
            text="Three Letters",
            command=lambda: generate.random.three_letter_func(self.name_entry),
            font=("Helvetica", 12),
            text_color="white",
            width=90,
        )
        self.three_letter.place(x=10, y=50)

        self.two_letter_numbers = ctk.CTkButton(
            self.random_frame,
            text="(Two) L + N",
            command=lambda: generate.random.two_letter_and_number_func(self.name_entry),
            font=("Helvetica", 12),
            text_color="white",
            width=100,
        )
        self.two_letter_numbers.place(x=240, y=10)

        self.three_letter_numbers = ctk.CTkButton(
            self.random_frame,
            text="(Three) L + N",
            command=lambda: generate.random.three_letter_and_number_func(
                self.name_entry
            ),
            font=("Helvetica", 12),
            text_color="white",
            width=100,
        )
        self.three_letter_numbers.place(x=240, y=50)

        self.placeholder_button = ctk.CTkButton(
            self.random_frame,
            text="Two Numbers",
            command=lambda: generate.random.two_number_func(self.name_entry),
            font=("Helvetica", 12),
            text_color="white",
            width=105,
        )
        self.placeholder_button.place(x=117, y=10)

        self.placeholder2_button = ctk.CTkButton(
            self.random_frame,
            text="Three Numbers",
            command=lambda: generate.random.three_number_func(self.name_entry),
            font=("Helvetica", 12),
            text_color="white",
            width=105,
        )
        self.placeholder2_button.place(x=117, y=50)
        
        # Logs text
        self.logs_text = ctk.CTkTextbox(
            self.root,
            width=355,
            height=152,
            font=("Roboto Medium", 10),
            border_color="white",
            border_width=1
        )
        self.logs_text.insert('end', f"RSNChecker v1.5\n")
        self.logs_text.insert('end', f"https://github.com/Aellas/RSNChecker\n")
        self.logs_text.insert('end', f"\n{functions.time.get_time()}: GUI started\n")

        self.logs_text.place(x=10, y=230)
        
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

    async def search_name(self):
        self.stop_flag = False

        name_entry_text = self.name_entry.get().strip()
        names: List[str] = name_entry_text.split(",")
        source: str = self.selection_var.get()
        
        maybe_available_names = []

        for name in names:
            stripped_name_loop = name.strip()
            if not stripped_name_loop:
                continue
            if len(stripped_name_loop) < 1:
                self.progress_label.configure(text="Name cannot be empty")
                continue
            elif len(stripped_name_loop) > 12:
                self.progress_label.configure(text="Name is too long")
                continue
            elif not all(
                char.isalnum() or char.isspace() or char == "_" or char == "-"
                for char in stripped_name_loop
            ):
                self.progress_label.configure(text="invalid characters detected")
                continue
            elif stripped_name_loop == "_":
                self.progress_label.configure(text="Name cannot be just underscores")
                continue
            else:
                self.progress_label.configure(
                    text=f"Checking [ {stripped_name_loop} ] is available..."
                )

                self.logs_text.insert("end", f"{functions.time.get_time()}: checking {stripped_name_loop} via {source}\n")
                self.root.update()
                async with aiohttp.ClientSession() as session:
                    task = asyncio.create_task(
                        self.check_name_availability(
                            stripped_name_loop, source, session
                        )
                    )
                    tasks = [task]
                    results = await asyncio.gather(*tasks)

                    if self.stop_flag:
                        break

                    if results[0]:
                        maybe_available_names.append(stripped_name_loop)
                        self.guide_textbox.insert(
                            "end", stripped_name_loop + "\n"
                        )
                        if source == "RS3 Hiscores" or "OSRS Hiscores":
                         self.logs_text.insert("end", f"[result] {stripped_name_loop} not found on {source} -> added to output\n")
                        else:
                         self.logs_text.insert("end", f"[result] {stripped_name_loop} found on {source} -> rsn taken\n")
                    self.progress_label.configure(text="")
                    if self.stop_flag:
                        break
        if len(maybe_available_names) == 0:
            if len(names) == 1:
                self.progress_label.configure(text="Username not available")
            else:
                self.progress_label.configure(text="Usernames not available")
        else:
            self.progress_label.configure(text="")
            

    def check_name(self):
        self.guide_textbox.delete(1.0, "end")
        asyncio.run(self.search_name())
        self.search_button.configure(state="normal")        

    def stop_search(self):
        self.stop_flag = True

    def run(self):
        self.root.mainloop()

def main():
    checker = RunescapeNameChecker()
    checker.run()

if __name__ == "__main__":
    main()
