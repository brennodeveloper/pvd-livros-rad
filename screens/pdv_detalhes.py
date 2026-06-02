"""
PDV Livraria — Detalhes do Item
Paleta: CustomTkinter dark theme (#242424 / #2b2b2b / azul CTk #1f6aa5)
Requer: pip install customtkinter pillow
"""

import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk

# ---------- Paleta ----------
BG = "#242424"
PANEL = "#2b2b2b"
BORDER = "#4a4a4a"
FG = "#f0f0f0"
MUTED = "#a0a0a0"
ACCENT = "#1f6aa5"
ACCENT_HOVER = "#144870"
GOOD = "#16a34a"
WARN = "#6b7280"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------- Dados ----------
item = {
    "sku": "LIV-0001-DCM",
    "ean": "7891234567890",
    "titulo": "Dom Casmurro",
    "autor": "Machado de Assis",
    "editora": "Páginas Edições",
    "categoria": "Ficção / Clássicos",
    "preco": 39.92,
    "estoque": 14,
}


class PdvApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PDV — Livraria Páginas")
        self.geometry("1100x720")
        self.configure(fg_color=BG)

        self.qtd = 1
        self._build_topbar()
        self._build_body()
        self._build_footer()
        self._bind_shortcuts()

    # ---------- Topbar ----------
    def _build_topbar(self):
        top = ctk.CTkFrame(self, fg_color=PANEL, border_color=BORDER,
                           border_width=1, corner_radius=6, height=42)
        top.pack(fill="x", padx=12, pady=(12, 6))

        ctk.CTkButton(top, text="← Voltar", width=90, height=28,
                      fg_color=BG, hover_color=BORDER, text_color=FG,
                      border_color=BORDER, border_width=1,
                      command=self._voltar).pack(side="left", padx=10, pady=8)

        ctk.CTkLabel(top, text=" PDV ", fg_color=ACCENT, text_color="white",
                     font=("Arial", 12, "bold"),
                     corner_radius=4).pack(side="left", padx=6)

        ctk.CTkLabel(top, text="Livraria Páginas — Caixa 02",
                     text_color=MUTED).pack(side="left", padx=10)

        ctk.CTkLabel(top, text="● ONLINE", text_color=GOOD,
                     font=("Consolas", 11, "bold")).pack(side="right", padx=10)
        ctk.CTkLabel(top, text="22/05/2026 14:37  OP: ANA.M",
                     text_color=MUTED,
                     font=("Consolas", 11)).pack(side="right", padx=6)

    # ---------- Body ----------
    def _build_body(self):
        body = ctk.CTkFrame(self, fg_color=BG)
        body.pack(fill="both", expand=True, padx=12, pady=6)
        body.grid_columnconfigure(0, weight=14)
        body.grid_columnconfigure(1, weight=10)
        body.grid_rowconfigure(0, weight=1)

        self._build_left(body)
        self._build_right(body)

    def _build_left(self, parent):
        left = ctk.CTkFrame(parent, fg_color=PANEL, border_color=BORDER,
                            border_width=1, corner_radius=6)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        header = ctk.CTkFrame(left, fg_color="transparent")
        header.pack(fill="x", padx=14, pady=(12, 6))
        ctk.CTkLabel(header, text="[F2] DETALHES DO ITEM",
                     text_color=MUTED,
                     font=("Arial", 11, "bold")).pack(side="left")
        ctk.CTkLabel(header, text=f"SKU: {item['sku']}",
                     text_color=MUTED,
                     font=("Consolas", 11)).pack(side="right")

        content = ctk.CTkFrame(left, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=14, pady=10)

        # Capa
        cover_frame = ctk.CTkFrame(content, fg_color=BG,
                                   border_color=BORDER, border_width=1,
                                   corner_radius=4, width=150, height=210)
        cover_frame.pack(side="left", padx=(0, 14))
        cover_frame.pack_propagate(False)

        img = Image.new("RGB", (140, 200), BG)
        d = ImageDraw.Draw(img)
        d.rectangle([6, 6, 134, 194], outline=ACCENT, width=2)
        d.text((20, 60), "DOM\nCASMURRO", fill=FG)
        d.text((20, 160), "MACHADO", fill=MUTED)
        self._cover_img = ImageTk.PhotoImage(img)
        ctk.CTkLabel(cover_frame, image=self._cover_img, text="").pack(
            expand=True)

        info = ctk.CTkFrame(content, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(info, text="TÍTULO", text_color=MUTED,
                     font=("Arial", 9, "bold")).pack(anchor="w")
        ctk.CTkLabel(info, text=item["titulo"], text_color=FG,
                     font=("Arial", 22, "bold")).pack(anchor="w")
        ctk.CTkLabel(info, text=f"{item['autor']} • {item['editora']}",
                     text_color=MUTED).pack(anchor="w", pady=(0, 12))

        # KPIs
        kpis = ctk.CTkFrame(info, fg_color="transparent")
        kpis.pack(fill="x", pady=(0, 12))
        self._kpi(kpis, "ESTOQUE", f"{item['estoque']} un", GOOD).pack(
            side="left", expand=True, fill="x", padx=(0, 4))
        self._kpi(kpis, "RESERVADO", "2 un", FG).pack(
            side="left", expand=True, fill="x", padx=4)
        self._kpi(kpis, "MÍNIMO", "5 un", WARN).pack(
            side="left", expand=True, fill="x", padx=(4, 0))

        self._field(info, "EAN", item["ean"])
        self._field(info, "CATEGORIA", item["categoria"])

    def _kpi(self, parent, label, value, color):
        f = ctk.CTkFrame(parent, fg_color=PANEL, border_color=BORDER,
                         border_width=1, corner_radius=4)
        ctk.CTkLabel(f, text=label, text_color=MUTED,
                     font=("Arial", 9, "bold")).pack(anchor="w", padx=8,
                                                     pady=(6, 0))
        ctk.CTkLabel(f, text=value, text_color=color,
                     font=("Consolas", 16, "bold")).pack(anchor="w", padx=8,
                                                         pady=(0, 6))
        return f

    def _field(self, parent, label, value):
        row = ctk.CTkFrame(parent, fg_color="transparent", height=28)
        row.pack(fill="x", pady=2)
        ctk.CTkLabel(row, text=label, text_color=MUTED,
                     font=("Arial", 10)).pack(side="left")
        ctk.CTkLabel(row, text=value, text_color=FG,
                     font=("Consolas", 11)).pack(side="right")
        ctk.CTkFrame(parent, fg_color=BORDER, height=1).pack(fill="x")

    def _build_right(self, parent):
        right = ctk.CTkFrame(parent, fg_color=BG)
        right.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

        # Preço
        price = ctk.CTkFrame(right, fg_color=PANEL, border_color=BORDER,
                             border_width=1, corner_radius=6)
        price.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(price, text="PREÇO DE VENDA", text_color=MUTED,
                     font=("Arial", 10, "bold")).pack(anchor="w", padx=14,
                                                      pady=(12, 0))
        ctk.CTkLabel(price,
                     text=f"R$ {item['preco']:.2f}".replace(".", ","),
                     text_color=ACCENT,
                     font=("Consolas", 32, "bold")).pack(anchor="w", padx=14)

        # Quantidade
        qrow = ctk.CTkFrame(price, fg_color="transparent")
        qrow.pack(fill="x", padx=14, pady=10)
        ctk.CTkLabel(qrow, text="QUANTIDADE", text_color=MUTED,
                     font=("Arial", 10, "bold")).pack(side="left")

        qbox = ctk.CTkFrame(qrow, fg_color=BG, border_color=BORDER,
                            border_width=1, corner_radius=4)
        qbox.pack(side="right")
        ctk.CTkButton(qbox, text="−", width=32, fg_color="transparent",
                      hover_color=PANEL, text_color=FG,
                      command=lambda: self._set_qtd(-1)).pack(side="left")
        self.lbl_qtd = ctk.CTkLabel(qbox, text="1", text_color=FG, width=40,
                                    font=("Consolas", 14, "bold"))
        self.lbl_qtd.pack(side="left")
        ctk.CTkButton(qbox, text="+", width=32, fg_color="transparent",
                      hover_color=PANEL, text_color=FG,
                      command=lambda: self._set_qtd(1)).pack(side="left")

        ctk.CTkFrame(price, fg_color=BORDER, height=1).pack(fill="x", padx=14)

        sub = ctk.CTkFrame(price, fg_color="transparent")
        sub.pack(fill="x", padx=14, pady=10)
        ctk.CTkLabel(sub, text="SUBTOTAL", text_color=MUTED,
                     font=("Arial", 10, "bold")).pack(side="left")
        self.lbl_subtotal = ctk.CTkLabel(
            sub, text=self._subtotal_text(), text_color=FG,
            font=("Consolas", 20, "bold"))
        self.lbl_subtotal.pack(side="right")

        # Ações
        actions = ctk.CTkFrame(right, fg_color=PANEL, border_color=BORDER,
                               border_width=1, corner_radius=6)
        actions.pack(fill="x", pady=(0, 8))

        ctk.CTkButton(actions, text="[F4] ADICIONAR À VENDA", height=44,
                      fg_color=ACCENT, hover_color=ACCENT_HOVER,
                      text_color="white",
                      font=("Arial", 12, "bold"),
                      command=self._adicionar).pack(fill="x", padx=12,
                                                    pady=(12, 6))

        srow = ctk.CTkFrame(actions, fg_color="transparent")
        srow.pack(fill="x", padx=12, pady=(0, 12))
        for text in ("[F6] Reservar", "[F7] Etiqueta", "[ESC] Voltar"):
            cmd = self._voltar if "Voltar" in text else (
                lambda t=text: self._msg(t))
            ctk.CTkButton(srow, text=text, fg_color=BG, hover_color=BORDER,
                          text_color=FG, border_color=BORDER, border_width=1,
                          command=cmd).pack(side="left", expand=True,
                                            fill="x", padx=3)

        # Stats
        stats = ctk.CTkFrame(right, fg_color=PANEL, border_color=BORDER,
                             border_width=1, corner_radius=6)
        stats.pack(fill="x")
        for label, value, color in (
            ("Últ. venda", "21/05 • 11:02", MUTED),
            ("Vendas (30d)", "23 un", MUTED),
            ("Margem", "+38%", GOOD),
        ):
            r = ctk.CTkFrame(stats, fg_color="transparent")
            r.pack(fill="x", padx=14, pady=3)
            ctk.CTkLabel(r, text=label, text_color=MUTED,
                         font=("Consolas", 11)).pack(side="left")
            ctk.CTkLabel(r, text=value, text_color=color,
                         font=("Consolas", 11)).pack(side="right")

    # ---------- Footer ----------
    def _build_footer(self):
        foot = ctk.CTkFrame(self, fg_color=PANEL, border_color=BORDER,
                            border_width=1, corner_radius=6, height=34)
        foot.pack(fill="x", padx=12, pady=(6, 12))
        for k in ("F1 Ajuda", "F2 Item", "F3 Cliente", "F4 Adicionar",
                  "F8 Finalizar"):
            ctk.CTkLabel(foot, text=k, text_color=MUTED,
                         font=("Consolas", 10)).pack(side="left", padx=10,
                                                     pady=6)
        ctk.CTkLabel(foot, text="SCANNER PRONTO", text_color=GOOD,
                     font=("Consolas", 10, "bold")).pack(side="right", padx=12)

    # ---------- Lógica ----------
    def _subtotal_text(self):
        return f"R$ {item['preco'] * self.qtd:.2f}".replace(".", ",")

    def _set_qtd(self, delta):
        self.qtd = max(1, self.qtd + delta)
        self.lbl_qtd.configure(text=str(self.qtd))
        self.lbl_subtotal.configure(text=self._subtotal_text())

    def _adicionar(self):
        messagebox.showinfo("PDV",
                            f"{self.qtd}× {item['titulo']} adicionado "
                            f"({self._subtotal_text()})")

    def _voltar(self):
        if messagebox.askyesno("Voltar", "Sair desta tela?"):
            self.destroy()

    def _msg(self, t):
        messagebox.showinfo("PDV", f"Ação: {t}")

    def _bind_shortcuts(self):
        self.bind("<F4>", lambda e: self._adicionar())
        self.bind("<F6>", lambda e: self._msg("[F6] Reservar"))
        self.bind("<F7>", lambda e: self._msg("[F7] Etiqueta"))
        self.bind("<Escape>", lambda e: self._voltar())


if __name__ == "__main__":
    PdvApp().mainloop()
