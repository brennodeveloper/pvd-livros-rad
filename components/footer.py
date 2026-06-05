import customtkinter as ctk

# ---------- Paleta ----------
PANEL = "#2b2b2b"
BORDER = "#4a4a4a"
MUTED = "#a0a0a0"
GOOD = "#16a34a"


class Footer(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        shortcuts=None,
        status_text="SCANNER PRONTO"
    ):
        super().__init__(
            parent,
            fg_color=PANEL,
            border_color=BORDER,
            border_width=1,
            corner_radius=6,
            height=34
        )

        self.pack(fill="x", side="bottom", padx=12, pady=(6, 12))
        self.pack_propagate(False)

        if shortcuts is None:
            shortcuts = (
                "F1 Ajuda",
                "F2 Item",
                "F3 Cliente",
                "F4 Adicionar",
                "F8 Finalizar"
            )

        for shortcut in shortcuts:
            ctk.CTkLabel(
                self,
                text=shortcut,
                text_color=MUTED,
                font=("Consolas", 10)
            ).pack(side="left", padx=10, pady=6)

        ctk.CTkLabel(
            self,
            text=status_text,
            text_color=GOOD,
            font=("Consolas", 10, "bold")
        ).pack(side="right", padx=12)