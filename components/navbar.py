import customtkinter as ctk
from datetime import datetime

# ---------- Paleta ----------
BG = "#242424"
PANEL = "#2b2b2b"
BORDER = "#4a4a4a"
FG = "#f0f0f0"
MUTED = "#a0a0a0"
ACCENT = "#1f6aa5"
GOOD = "#16a34a"


class NavBar(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        title="Livraria Páginas — Caixa 02",
        operator="OP: ADMIN",
        date_text=None,
        back_command=None,
        show_back=True
    ):
        super().__init__(
            parent,
            fg_color=PANEL,
            border_color=BORDER,
            border_width=1,
            corner_radius=6,
            height=42
        )

        if date_text is None:
            date_text = datetime.now().strftime("%d/%m/%Y %H:%M")

        self.pack(fill="x", padx=12, pady=(12, 6))
        self.pack_propagate(False)

        if show_back:
            ctk.CTkButton(
                self,
                text="← Voltar",
                width=90,
                height=28,
                fg_color=BG,
                hover_color=BORDER,
                text_color=FG,
                border_color=BORDER,
                border_width=1,
                command=back_command
            ).pack(side="left", padx=10, pady=8)

        ctk.CTkLabel(
            self,
            text=" PDV ",
            fg_color=ACCENT,
            text_color="white",
            font=("Arial", 12, "bold"),
            corner_radius=4
        ).pack(side="left", padx=6)

        ctk.CTkLabel(
            self,
            text=title,
            text_color=MUTED
        ).pack(side="left", padx=10)

        ctk.CTkLabel(
            self,
            text="● ONLINE",
            text_color=GOOD,
            font=("Consolas", 11, "bold")
        ).pack(side="right", padx=10)

        ctk.CTkLabel(
            self,
            text=f"{date_text}  {operator}",
            text_color=MUTED,
            font=("Consolas", 11)
        ).pack(side="right", padx=6)