import customtkinter as ctk
from tkinter import messagebox

# ---------- Constantes visuais (padrão Livraria PDV) ----------
BG_MAIN   = "#2A2C30"
BG_CARD   = "#333333"
BG_INPUT  = "#3a3a3a"
FG_MAIN   = "#ffffff"
FG_MUTED  = "#a0a0a0"
GREEN     = "#2ecc71"
GREEN_HV  = "#27ae60"
GRAY_BTN  = "#4a4a4a"
GRAY_HV   = "#5a5a5a"
ACCENT    = "#4a6fa5"

CATS       = ["Todas", "Ficção", "Romance", "Tecnologia", "História", "Infantil", "Autoajuda"]
POR_PAGINA = 8

COL_SPECS = [
    ("ID",            1, "center"),
    ("Nome do Livro", 5, "w"),
    ("Autor",         4, "w"),
    ("Categoria",     3, "w"),
    ("Estoque",       1, "center"),
    ("Preço",         2, "center"),
    ("Ações",         4, "center"),
]

livros     = []
proximo_id = 1


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Livraria PDV — Consulta de Livros")
        self.geometry("1180x720")
        self.minsize(960, 600)
        self.configure(fg_color=BG_MAIN)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.pagina = 1
        self.tela_consulta()

    # ---------- Utilitários ----------
    def _limpar(self):
        for w in self.winfo_children():
            w.destroy()

    def _modal(self, titulo, w, h):
        top = ctk.CTkToplevel(self)
        top.title(titulo)
        top.configure(fg_color=BG_MAIN)
        top.transient(self)
        top.grab_set()
        self.update_idletasks()
        x = self.winfo_x() + (self.winfo_width()  - w) // 2
        y = self.winfo_y() + (self.winfo_height() - h) // 2
        top.geometry(f"{w}x{h}+{x}+{y}")
        ctk.CTkLabel(
            top, text=titulo,
            font=ctk.CTkFont("Segoe UI", 20, "bold"),
            text_color=FG_MAIN
        ).pack(pady=(24, 8))
        return top

    # ---------- Tela principal ----------
    def tela_consulta(self):
        self._limpar()
        self.pagina = 1

        # ── Cabeçalho ──────────────────────────────────────────
        header = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=0, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Botão ← Início (canto esquerdo)
        ctk.CTkButton(
            header, text="← Início", width=100, height=34,
            fg_color="#374151", hover_color="#4b5563",
            text_color=FG_MAIN, font=ctk.CTkFont("Segoe UI", 13, "bold"),
            corner_radius=8, command=lambda: None   # trocar pela navegação real
        ).place(x=16, rely=0.5, anchor="w")

        # Título central com ícone
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(
            title_frame, text="🗂  LIVRARIA PDV",
            font=ctk.CTkFont("Segoe UI", 22, "bold"),
            text_color=FG_MAIN
        ).pack()

        # ── Subtítulo / filtros ─────────────────────────────────
        sub = ctk.CTkFrame(self, fg_color="transparent")
        sub.pack(fill="x", padx=24, pady=(14, 0))

        ctk.CTkLabel(
            sub, text="Livros cadastrados",
            font=ctk.CTkFont("Segoe UI", 13),
            text_color=FG_MUTED
        ).pack(side="left")

        ctk.CTkButton(
            sub, text="+ Adicionar novo livro",
            fg_color=GREEN, hover_color=GREEN_HV,
            text_color="white", font=ctk.CTkFont("Segoe UI", 13, "bold"),
            corner_radius=8, height=34,
            command=self.adicionar
        ).pack(side="right")

        # ── Card de filtros ─────────────────────────────────────
        fc = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=12)
        fc.pack(fill="x", padx=24, pady=10)

        ctk.CTkLabel(fc, text="🔍", font=ctk.CTkFont(size=15),
                     text_color=FG_MUTED).pack(side="left", padx=(14, 4), pady=12)

        self.var_busca = ctk.StringVar()
        ctk.CTkEntry(
            fc, textvariable=self.var_busca,
            placeholder_text="Buscar por nome ou autor...",
            fg_color=BG_INPUT, border_color=BG_INPUT,
            text_color=FG_MAIN, placeholder_text_color=FG_MUTED,
            font=ctk.CTkFont("Segoe UI", 13),
            corner_radius=8, height=36, width=0
        ).pack(side="left", fill="x", expand=True, padx=(0, 14), pady=10)

        ctk.CTkLabel(fc, text="Categoria:",
                     font=ctk.CTkFont("Segoe UI", 12),
                     text_color=FG_MUTED).pack(side="left", padx=(0, 6))

        self.var_cat = ctk.StringVar(value="Todas")
        ctk.CTkOptionMenu(
            fc, variable=self.var_cat, values=CATS,
            fg_color=BG_INPUT, button_color=ACCENT, button_hover_color=GRAY_HV,
            text_color=FG_MAIN, font=ctk.CTkFont("Segoe UI", 12),
            corner_radius=8, width=150,
            command=lambda _: self._atualizar(reset=True)
        ).pack(side="left", padx=(0, 14), pady=10)

        self.var_busca.trace_add("write", lambda *_: self._atualizar(reset=True))

        # ── Tabela ──────────────────────────────────────────────
        self.tabela_container = ctk.CTkScrollableFrame(
            self, fg_color=BG_CARD, corner_radius=12,
            scrollbar_button_color=GRAY_BTN,
            scrollbar_button_hover_color=GRAY_HV
        )
        self.tabela_container.pack(fill="both", expand=True, padx=24, pady=(0, 6))

        self._montar_cabecalho()

        self.linhas_frame = ctk.CTkFrame(self.tabela_container, fg_color="transparent")
        self.linhas_frame.pack(fill="both", expand=True)

        # ── Rodapé / paginação ──────────────────────────────────
        rod = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=0, height=52)
        rod.pack(fill="x")
        rod.pack_propagate(False)

        self.lbl_info = ctk.CTkLabel(
            rod, text="", text_color=FG_MUTED,
            font=ctk.CTkFont("Segoe UI", 12)
        )
        self.lbl_info.pack(side="left", padx=24)

        nav = ctk.CTkFrame(rod, fg_color="transparent")
        nav.pack(side="right", padx=16)

        self.btn_prev = ctk.CTkButton(
            nav, text="← Anterior", width=110, height=32,
            fg_color=GRAY_BTN, hover_color=GRAY_HV,
            text_color=FG_MAIN, font=ctk.CTkFont("Segoe UI", 12),
            corner_radius=8, command=lambda: self._mudar_pagina(-1)
        )
        self.btn_prev.pack(side="left", padx=4)

        self.lbl_pag = ctk.CTkLabel(
            nav, text="", text_color=FG_MAIN,
            font=ctk.CTkFont("Segoe UI", 13, "bold")
        )
        self.lbl_pag.pack(side="left", padx=12)

        self.btn_next = ctk.CTkButton(
            nav, text="Próxima →", width=110, height=32,
            fg_color=GREEN, hover_color=GREEN_HV,
            text_color="white", font=ctk.CTkFont("Segoe UI", 12, "bold"),
            corner_radius=8, command=lambda: self._mudar_pagina(1)
        )
        self.btn_next.pack(side="left", padx=4)

        self._atualizar()

    # ---------- Tabela ----------
    def _montar_cabecalho(self):
        head = ctk.CTkFrame(self.tabela_container, fg_color=BG_MAIN, corner_radius=8, height=42)
        head.pack(fill="x", pady=(4, 2))
        head.pack_propagate(False)

        for i, (_, peso, _) in enumerate(COL_SPECS):
            head.columnconfigure(i, weight=peso, minsize=30)

        for i, (titulo, peso, anchor) in enumerate(COL_SPECS):
            cell = ctk.CTkFrame(head, fg_color="transparent", corner_radius=0)
            cell.grid(row=0, column=i, sticky="nsew")
            ctk.CTkLabel(
                cell, text=titulo.upper(),
                font=ctk.CTkFont("Segoe UI", 11, "bold"),
                text_color=FG_MUTED, anchor=anchor
            ).pack(fill="both", expand=True, padx=10)

    def _filtrados(self):
        busca = self.var_busca.get().strip().lower()
        cat   = self.var_cat.get()
        return [
            l for l in livros
            if (cat == "Todas" or l["categoria"] == cat)
            and (not busca or busca in l["nome"].lower() or busca in l["autor"].lower())
        ]

    def _atualizar(self, reset=False):
        if reset:
            self.pagina = 1
        dados = self._filtrados()
        total = len(dados)
        n_pag = max(1, (total + POR_PAGINA - 1) // POR_PAGINA)
        self.pagina = min(self.pagina, n_pag)

        for w in self.linhas_frame.winfo_children():
            w.destroy()

        if not dados:
            ctk.CTkLabel(
                self.linhas_frame,
                text="🗃  Nenhum livro encontrado",
                font=ctk.CTkFont("Segoe UI", 14),
                text_color=FG_MUTED
            ).pack(expand=True, pady=40)
        else:
            for i, l in enumerate(dados[(self.pagina - 1) * POR_PAGINA: self.pagina * POR_PAGINA]):
                self._criar_linha(l, i)

        self.lbl_info.configure(text=f"Itens: {total}")
        self.lbl_pag.configure(text=f"Página {self.pagina} de {n_pag}")
        self.btn_prev.configure(state="normal" if self.pagina > 1     else "disabled")
        self.btn_next.configure(state="normal" if self.pagina < n_pag else "disabled")

    def _criar_linha(self, l, idx):
        bg  = BG_INPUT if idx % 2 == 0 else BG_CARD
        row = ctk.CTkFrame(self.linhas_frame, fg_color=bg, corner_radius=6, height=48)
        row.pack(fill="x", pady=(0, 2))
        row.pack_propagate(False)

        for i, (_, peso, _) in enumerate(COL_SPECS):
            row.columnconfigure(i, weight=peso, minsize=30)

        valores = [
            (str(l["id"]),             "center"),
            (l["nome"],                "w"),
            (l["autor"],               "w"),
            (l["categoria"],           "w"),
            (str(l["estoque"]),        "center"),
            (f"R$ {l['preco']:.2f}",   "center"),
        ]

        for i, (val, anchor) in enumerate(valores):
            cell = ctk.CTkFrame(row, fg_color="transparent", corner_radius=0)
            cell.grid(row=0, column=i, sticky="nsew")
            ctk.CTkLabel(
                cell, text=val,
                font=ctk.CTkFont("Segoe UI", 13),
                text_color=FG_MAIN, anchor=anchor
            ).pack(fill="both", expand=True, padx=10)

        # Coluna de ações
        cell = ctk.CTkFrame(row, fg_color="transparent", corner_radius=0)
        cell.grid(row=0, column=6, sticky="nsew")
        inner = ctk.CTkFrame(cell, fg_color="transparent")
        inner.pack(expand=True)

        for txt, cmd, cor, hcor in [
            ("👁 Ver",    lambda lid=l["id"]: self._abrir_detalhes(lid), ACCENT,    GRAY_HV),
            ("✏ Editar",  lambda lid=l["id"]: self._editar(lid),         GRAY_BTN,  GRAY_HV),
            ("🗑 Excluir", lambda lid=l["id"]: self._excluir(lid),        "#c0392b", "#e74c3c"),
        ]:
            ctk.CTkButton(
                inner, text=txt, width=78, height=28,
                fg_color=cor, hover_color=hcor, text_color="white",
                font=ctk.CTkFont("Segoe UI", 11, "bold"),
                corner_radius=6, command=cmd
            ).pack(side="left", padx=2)

    def _mudar_pagina(self, delta):
        self.pagina += delta
        self._atualizar()

    # ---------- Ações CRUD ----------
    def _achar(self, lid):
        return next((l for l in livros if l["id"] == lid), None)

    def _abrir_detalhes(self, lid):
        l = self._achar(lid)
        if not l:
            return
        top = self._modal(f"Detalhes — {l['nome']}", 460, 400)

        card = ctk.CTkFrame(top, fg_color=BG_CARD, corner_radius=12)
        card.pack(fill="x", padx=26, pady=8)

        for label, val in [
            ("ID", l["id"]), ("Nome", l["nome"]), ("Autor", l["autor"]),
            ("Categoria", l["categoria"]), ("Estoque", l["estoque"]),
            ("Preço", f"R$ {l['preco']:.2f}"),
        ]:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=16, pady=5)
            ctk.CTkLabel(
                row, text=label, width=90, anchor="w",
                font=ctk.CTkFont("Segoe UI", 12),
                text_color=FG_MUTED
            ).pack(side="left")
            ctk.CTkLabel(
                row, text=str(val), anchor="w",
                font=ctk.CTkFont("Segoe UI", 13, "bold"),
                text_color=FG_MAIN
            ).pack(side="left", fill="x", expand=True)

        ctk.CTkButton(
            top, text="Fechar", width=120, height=36,
            fg_color=GRAY_BTN, hover_color=GRAY_HV,
            text_color=FG_MAIN, corner_radius=8,
            command=top.destroy
        ).pack(pady=16)

    def _editar(self, lid):
        l = self._achar(lid)
        if l:
            self._formulario("Editar Livro", l)

    def adicionar(self):
        self._formulario("Cadastro de Livro", None)

    def _excluir(self, lid):
        l = self._achar(lid)
        if l and messagebox.askyesno("Excluir", f"Excluir '{l['nome']}'?"):
            livros.remove(l)
            self._atualizar()

    # ---------- Formulário ----------
    def _formulario(self, titulo, livro):
        global proximo_id
        top    = self._modal(titulo, 500, 560)
        campos = {}

        card = ctk.CTkFrame(top, fg_color=BG_CARD, corner_radius=12)
        card.pack(fill="both", expand=True, padx=20, pady=(0, 8))

        for label, valor, eh_combo in [
            ("Título da Obra", livro["nome"]          if livro else "", False),
            ("Autor(es)",      livro["autor"]          if livro else "", False),
            ("Categoria",      livro["categoria"]      if livro else "Ficção", True),
            ("Preço",          f"{livro['preco']:.2f}" if livro else "0.00", False),
            ("Estoque",        livro["estoque"]        if livro else 0, False),
        ]:
            ctk.CTkLabel(
                card, text=label, anchor="w",
                font=ctk.CTkFont("Segoe UI", 12),
                text_color=FG_MUTED
            ).pack(fill="x", padx=20, pady=(10, 2))

            if eh_combo:
                var = ctk.StringVar(value=valor or "Ficção")
                ctk.CTkOptionMenu(
                    card, variable=var,
                    values=[c for c in CATS if c != "Todas"],
                    fg_color=BG_INPUT, button_color=ACCENT,
                    button_hover_color=GRAY_HV, text_color=FG_MAIN,
                    font=ctk.CTkFont("Segoe UI", 13),
                    corner_radius=8, height=36
                ).pack(fill="x", padx=20)
                campos[label] = var
            else:
                e = ctk.CTkEntry(
                    card,
                    fg_color=BG_INPUT, border_color=BG_INPUT,
                    text_color=FG_MAIN,
                    font=ctk.CTkFont("Segoe UI", 13),
                    corner_radius=8, height=36
                )
                e.insert(0, str(valor))
                e.pack(fill="x", padx=20)
                campos[label] = e

        def salvar():
            global proximo_id
            try:
                nome  = campos["Título da Obra"].get().strip()
                autor = campos["Autor(es)"].get().strip()
                cat   = campos["Categoria"].get()
                preco = float(str(campos["Preço"].get()).replace(",", "."))
                est   = int(campos["Estoque"].get())
                if not nome or not autor:
                    raise ValueError("Título e autor são obrigatórios.")
            except Exception as ex:
                messagebox.showerror("Erro", str(ex), parent=top)
                return

            if livro:
                livro.update(nome=nome, autor=autor, categoria=cat, estoque=est, preco=preco)
                top.destroy()
                self._atualizar()
            else:
                livros.append({
                    "id": proximo_id, "nome": nome, "autor": autor,
                    "categoria": cat, "estoque": est, "preco": preco
                })
                proximo_id += 1
                top.destroy()
                self.var_busca.set("")
                self.var_cat.set("Todas")
                self.pagina = max(1, (len(livros) + POR_PAGINA - 1) // POR_PAGINA)
                self._atualizar()

        botoes = ctk.CTkFrame(top, fg_color="transparent")
        botoes.pack(pady=10)

        ctk.CTkButton(
            botoes, text="Limpar", width=130, height=38,
            fg_color=GRAY_BTN, hover_color=GRAY_HV,
            text_color=FG_MAIN, font=ctk.CTkFont("Segoe UI", 13),
            corner_radius=8,
            command=lambda: [e.delete(0, "end") for e in campos.values()
                             if isinstance(e, ctk.CTkEntry)]
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            botoes, text="Salvar", width=130, height=38,
            fg_color=GREEN, hover_color=GREEN_HV,
            text_color="white", font=ctk.CTkFont("Segoe UI", 13, "bold"),
            corner_radius=8, command=salvar
        ).pack(side="left", padx=8)


if __name__ == "__main__":
    App().mainloop()
