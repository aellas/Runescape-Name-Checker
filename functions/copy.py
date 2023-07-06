import pyperclip

def copy_maybe_available(maybe_available_frame, copy_button):
    text = maybe_available_frame.get("1.0", "end-1c")
    pyperclip.copy(text)
    copy_button.configure(text="Copied!")
    copy_button.after(2000, lambda: copy_button.configure(text="Copy to Clipboard"))
        

