import customtkinter as ctk

def BackButton(parent, command, text="← Início"):
    return ctk.CTkButton(
        parent,
        text=text,
        width=100,
        height=35,
        font=("Arial", 14, "bold"),
        fg_color="#374151",
        hover_color="#4b5563",
        command=command
    )