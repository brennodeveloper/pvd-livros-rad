import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont

# Dados do item
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
        self.title("PDV Livraria Páginas — Detalhes do Item")
        self.geometry("900x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.qtd = 1
        self._build_ui()

    def _build_ui(self):
        # Topbar
        top = ctk.CTkFrame(self, height=40)
        top.pack(fill="x", padx=10, pady=(10, 0))
        top.pack_propagate(False)

        btn_voltar = ctk.CTkButton(top, text="← Voltar", width=80, command=self._voltar)
        btn_voltar.pack(side="left", padx=5, pady=5)

        ctk.CTkLabel(top, text="PDV", font=("Courier", 12, "bold"), fg_color="#3B82F6", text_color="white", corner_radius=4).pack(side="left", padx=5)
        ctk.CTkLabel(top, text="Livraria Páginas — Caixa 02", font=("Courier", 11)).pack(side="left", padx=10)

        ctk.CTkLabel(top, text="22/05/2026 14:37   ● ONLINE", font=("Courier", 11), text_color="#4ade80").pack(side="right", padx=10)

        # Corpo
        body = ctk.CTkFrame(self)
        body.pack(fill="both", expand=True, padx=10, pady=10)

        # Esquerda: Detalhes
        left = ctk.CTkFrame(body)
        left.pack(side="left", fill="both", expand=True, padx=(0, 5))

        ctk.CTkLabel(left, text="[F2] Detalhes do Item", font=("Courier", 10), text_color="gray").pack(anchor="w", padx=10, pady=(10, 0))
        ctk.CTkLabel(left, text=f"SKU: {item['sku']}", font=("Courier", 10), text_color="gray").pack(anchor="e", padx=10)

        # Capa (imagem gerada)
        cover = self._make_cover()
        cover_label = ctk.CTkLabel(left, text="", image=ctk.CTkImage(cover, size=(120, 160)))
        cover_label.pack(pady=10)

        ctk.CTkLabel(left, text=item["titulo"], font=("Arial", 18, "bold")).pack()
        ctk.CTkLabel(left, text=f"{item['autor']} • {item['editora']}", font=("Arial", 12), text_color="gray").pack(pady=(0, 10))

        # KPIs
        kpi_frame = ctk.CTkFrame(left)
        kpi_frame.pack(fill="x", padx=10, pady=5)
        for label, value, color in [("Estoque", f"{item['estoque']} un", "#4ade80"), ("Reservado", "2 un", "gray"), ("Mínimo", "5 un", "#fbbf24")]:
            f = ctk.CTkFrame(kpi_frame, border_width=1)
            f.pack(side="left", expand=True, fill="x", padx=2)
            ctk.CTkLabel(f, text=label.upper(), font=("Courier", 9), text_color="gray").pack(pady=(5, 0))
            ctk.CTkLabel(f, text=value, font=("Courier", 14, "bold"), text_color=color).pack(pady=(0, 5))

        # Campos
        fields = ctk.CTkFrame(left)
        fields.pack(fill="x", padx=10, pady=10)
        for label, value in [("EAN", item["ean"]), ("Categoria", item["categoria"])]:
            row = ctk.CTkFrame(fields, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=label.upper(), font=("Courier", 10), text_color="gray").pack(side="left")
            ctk.CTkLabel(row, text=value, font=("Courier", 11)).pack(side="right")

        # Direita: Preço e Ações
        right = ctk.CTkFrame(body, width=320)
        right.pack(side="right", fill="y", padx=(5, 0))
        right.pack_propagate(False)

        ctk.CTkLabel(right, text="PREÇO DE VENDA", font=("Courier", 10), text_color="gray").pack(anchor="w", padx=15, pady=(15, 0))
        ctk.CTkLabel(right, text=f"R$ {item['preco']:.2f}".replace(".", ","), font=("Courier", 32, "bold"), text_color="#3B82F6").pack(anchor="w", padx=15)

        # Quantidade
        qtd_frame = ctk.CTkFrame(right, fg_color="transparent")
        qtd_frame.pack(fill="x", padx=15, pady=15)
        ctk.CTkLabel(qtd_frame, text="QUANTIDADE", font=("Courier", 10), text_color="gray").pack(side="left")

        self.qtd_label = ctk.CTkLabel(qtd_frame, text=str(self.qtd), font=("Courier", 14), width=40)
        self.qtd_label.pack(side="right", padx=5)
        ctk.CTkButton(qtd_frame, text="-", width=30, command=lambda: self._set_qtd(-1)).pack(side="right")
        ctk.CTkButton(qtd_frame, text="+", width=30, command=lambda: self._set_qtd(1)).pack(side="right", padx=(0, 2))

        # Subtotal
        self.sub_label = ctk.CTkLabel(right, text=f"Subtotal: R$ {item['preco']:.2f}".replace(".", ","), font=("Courier", 16, "bold"))
        self.sub_label.pack(anchor="w", padx=15, pady=(0, 15))

        # Botões de ação
        ctk.CTkButton(right, text="[F4] Adicionar à venda", fg_color="#3B82F6", command=self._adicionar).pack(fill="x", padx=15, pady=5)
        ctk.CTkButton(right, text="[F6] Reservar", command=lambda: self._msg("Reservado!")).pack(fill="x", padx=15, pady=5)
        ctk.CTkButton(right, text="[F7] Etiqueta", command=lambda: self._msg("Etiqueta impressa!")).pack(fill="x", padx=15, pady=5)
        ctk.CTkButton(right, text="[ESC] Voltar", command=self._voltar).pack(fill="x", padx=15, pady=5)

        # Estatísticas
        stats = ctk.CTkFrame(right)
        stats.pack(fill="x", padx=15, pady=15)
        for label, value in [("Últ. venda", "21/05 • 11:02"), ("Vendas (30d)", "23 un"), ("Margem", "+38%")]:
            row = ctk.CTkFrame(stats, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=label, font=("Courier", 10), text_color="gray").pack(side="left")
            ctk.CTkLabel(row, text=value, font=("Courier", 10), text_color="#4ade80" if label == "Margem" else "white").pack(side="right")

        # Rodapé
        footer = ctk.CTkFrame(self, height=30)
        footer.pack(fill="x", padx=10, pady=(0, 10))
        footer.pack_propagate(False)
        ctk.CTkLabel(footer, text="F1 Ajuda   F2 Item   F3 Cliente   F4 Adicionar   F8 Finalizar", font=("Courier", 9), text_color="gray").pack(side="left", padx=10)
        ctk.CTkLabel(footer, text="SCANNER PRONTO", font=("Courier", 9, "bold"), text_color="#4ade80").pack(side="right", padx=10)

        # Atalhos de teclado
        self.bind("<F4>", lambda e: self._adicionar())
        self.bind("<F6>", lambda e: self._msg("Reservado!"))
        self.bind("<F7>", lambda e: self._msg("Etiqueta impressa!"))
        self.bind("<Escape>", lambda e: self._voltar())

    def _make_cover(self):
        img = Image.new("RGB", (240, 320), "#1a1a2e")
        draw = ImageDraw.Draw(img)
        draw.rectangle([20, 80, 220, 240], fill="#16213e")
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
            small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        except:
            font = ImageFont.load_default()
            small = font
        draw.text((120, 140), "DOM\nCASMURRO", fill="white", font=font, anchor="mm", align="center")
        draw.text((120, 200), "Machado\nde Assis", fill="#94a3b8", font=small, anchor="mm", align="center")
        return img

    def _set_qtd(self, delta):
        self.qtd = max(1, self.qtd + delta)
        self.qtd_label.configure(text=str(self.qtd))
        sub = (item["preco"] * self.qtd)
        self.sub_label.configure(text=f"Subtotal: R$ {sub:.2f}".replace(".", ","))

    def _adicionar(self):
        self._msg(f"Adicionado {self.qtd}x '{item['titulo']}' à venda!")

    def _voltar(self):
        if ctk.CTkInputDialog(text="Deseja realmente voltar?", title="Confirmação").get_input():
            self.destroy()

    def _msg(self, texto):
        dlg = ctk.CTkToplevel(self)
        dlg.title("")
        dlg.geometry("300x100")
        ctk.CTkLabel(dlg, text=texto, font=("Arial", 14)).pack(expand=True)
        ctk.CTkButton(dlg, text="OK", command=dlg.destroy).pack(pady=5)

if __name__ == "__main__":
    app = PdvApp()
    app.mainloop()
