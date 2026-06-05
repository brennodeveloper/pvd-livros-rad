import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageDraw

from components.navbar import NavBar
from components.footer import Footer

from db.livros_repository import (
    buscar_livro_por_id,
    atualizar_livro,
    deletar_livro
)


# ---------- Paleta ----------
BG = "#242424"
PANEL = "#2b2b2b"
BORDER = "#4a4a4a"
FG = "#f0f0f0"
MUTED = "#a0a0a0"
ACCENT = "#1f6aa5"
ACCENT_HOVER = "#144870"
GOOD = "#16a34a"
DANGER = "#991b1b"
DANGER_HOVER = "#7f1d1d"
WARN = "#6b7280"


class DetalhesScreen(ctk.CTkFrame):
    def __init__(self, parent, id_livro):
        super().__init__(parent)

        self.parent = parent
        self.id_livro = id_livro

        self.pack(fill="both", expand=True)

        self.categorias = {
            "Romance": 1,
            "Aventura": 2,
            "Tecnologia": 3,
            "Terror": 4
        }

        self.livro = buscar_livro_por_id(self.id_livro)

        if self.livro is None:
            messagebox.showerror("Erro", "Livro não encontrado.")
            self.voltar_consulta()
            return

        self.criar_layout()

    def criar_layout(self):
        NavBar(
            self,
            title="Livraria PDV — Detalhes do Livro",
            operator="OP: ADMIN",
            back_command=self.voltar_consulta
        )

        Footer(
            self,
            shortcuts=("F1 Ajuda", "F2 Editar", "F3 Excluir", "F4 Salvar"),
            status_text="ITEM CARREGADO"
        )

        body = ctk.CTkFrame(self, fg_color=BG)
        body.pack(fill="both", expand=True, padx=12, pady=6)

        body.grid_columnconfigure(0, weight=14)
        body.grid_columnconfigure(1, weight=10)
        body.grid_rowconfigure(0, weight=1)

        self.criar_lado_esquerdo(body)
        self.criar_lado_direito(body)

    def criar_lado_esquerdo(self, parent):
        (
            id_livro,
            codigo_isbn,
            titulo,
            descricao,
            imagem_capa,
            autor,
            preco,
            qtd_estoque,
            num_paginas,
            id_categoria,
            nome_categoria
        ) = self.livro

        left = ctk.CTkFrame(
            parent,
            fg_color=PANEL,
            border_color=BORDER,
            border_width=1,
            corner_radius=6
        )
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        header = ctk.CTkFrame(left, fg_color="transparent")
        header.pack(fill="x", padx=14, pady=(12, 6))

        ctk.CTkLabel(
            header,
            text="[F2] DETALHES DO ITEM",
            text_color=MUTED,
            font=("Arial", 11, "bold")
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text=f"ID: {id_livro}",
            text_color=MUTED,
            font=("Consolas", 11)
        ).pack(side="right")

        content = ctk.CTkFrame(left, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=14, pady=10)

        # Capa / placeholder
        cover_frame = ctk.CTkFrame(
            content,
            fg_color=BG,
            border_color=BORDER,
            border_width=1,
            corner_radius=4,
            width=160,
            height=230
        )
        cover_frame.pack(side="left", padx=(0, 14), anchor="n")
        cover_frame.pack_propagate(False)

        self.cover_img = self.criar_placeholder_capa(titulo, autor)

        ctk.CTkLabel(
            cover_frame,
            image=self.cover_img,
            text=""
        ).pack(expand=True)

        info = ctk.CTkFrame(content, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(
            info,
            text="TÍTULO",
            text_color=MUTED,
            font=("Arial", 9, "bold")
        ).pack(anchor="w")

        self.entry_titulo = ctk.CTkEntry(info, height=38)
        self.entry_titulo.insert(0, titulo)
        self.entry_titulo.pack(fill="x", pady=(2, 10))

        ctk.CTkLabel(
            info,
            text="AUTOR",
            text_color=MUTED,
            font=("Arial", 9, "bold")
        ).pack(anchor="w")

        self.entry_autor = ctk.CTkEntry(info, height=38)
        self.entry_autor.insert(0, autor)
        self.entry_autor.pack(fill="x", pady=(2, 10))

        # KPIs
        kpis = ctk.CTkFrame(info, fg_color="transparent")
        kpis.pack(fill="x", pady=(0, 12))

        self.criar_kpi(kpis, "ESTOQUE", f"{qtd_estoque} un", GOOD).pack(
            side="left",
            expand=True,
            fill="x",
            padx=(0, 4)
        )

        self.criar_kpi(kpis, "PÁGINAS", f"{num_paginas}", FG).pack(
            side="left",
            expand=True,
            fill="x",
            padx=4
        )

        self.criar_kpi(kpis, "CATEGORIA", nome_categoria or "Sem categoria", WARN).pack(
            side="left",
            expand=True,
            fill="x",
            padx=(4, 0)
        )

        self.criar_label_campo(info, "ISBN")
        self.entry_isbn = ctk.CTkEntry(info, height=34)
        self.entry_isbn.insert(0, codigo_isbn)
        self.entry_isbn.pack(fill="x", pady=(2, 8))

        self.criar_label_campo(info, "DESCRIÇÃO")
        self.entry_descricao = ctk.CTkTextbox(info, height=120)
        self.entry_descricao.insert("1.0", descricao or "")
        self.entry_descricao.pack(fill="x", pady=(2, 8))

        self.imagem_capa = imagem_capa

    def criar_lado_direito(self, parent):
        (
            id_livro,
            codigo_isbn,
            titulo,
            descricao,
            imagem_capa,
            autor,
            preco,
            qtd_estoque,
            num_paginas,
            id_categoria,
            nome_categoria
        ) = self.livro

        right = ctk.CTkFrame(parent, fg_color=BG)
        right.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

        # Painel preço
        price = ctk.CTkFrame(
            right,
            fg_color=PANEL,
            border_color=BORDER,
            border_width=1,
            corner_radius=6
        )
        price.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            price,
            text="PREÇO DE VENDA",
            text_color=MUTED,
            font=("Arial", 10, "bold")
        ).pack(anchor="w", padx=14, pady=(12, 0))

        self.entry_preco = ctk.CTkEntry(
            price,
            height=42,
            font=("Consolas", 24, "bold")
        )
        self.entry_preco.insert(0, f"{preco:.2f}")
        self.entry_preco.pack(fill="x", padx=14, pady=(6, 12))

        # Estoque e páginas
        campos = ctk.CTkFrame(
            right,
            fg_color=PANEL,
            border_color=BORDER,
            border_width=1,
            corner_radius=6
        )
        campos.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            campos,
            text="ESTOQUE",
            text_color=MUTED,
            font=("Arial", 10, "bold")
        ).pack(anchor="w", padx=14, pady=(12, 0))

        self.entry_estoque = ctk.CTkEntry(campos, height=36)
        self.entry_estoque.insert(0, str(qtd_estoque))
        self.entry_estoque.pack(fill="x", padx=14, pady=(6, 10))

        ctk.CTkLabel(
            campos,
            text="NÚMERO DE PÁGINAS",
            text_color=MUTED,
            font=("Arial", 10, "bold")
        ).pack(anchor="w", padx=14)

        self.entry_paginas = ctk.CTkEntry(campos, height=36)
        self.entry_paginas.insert(0, str(num_paginas))
        self.entry_paginas.pack(fill="x", padx=14, pady=(6, 10))

        ctk.CTkLabel(
            campos,
            text="CATEGORIA",
            text_color=MUTED,
            font=("Arial", 10, "bold")
        ).pack(anchor="w", padx=14)

        self.combo_categoria = ctk.CTkComboBox(
            campos,
            values=list(self.categorias.keys()),
            height=36
        )
        self.combo_categoria.set(nome_categoria or "Romance")
        self.combo_categoria.pack(fill="x", padx=14, pady=(6, 14))

        # Ações
        actions = ctk.CTkFrame(
            right,
            fg_color=PANEL,
            border_color=BORDER,
            border_width=1,
            corner_radius=6
        )
        actions.pack(fill="x", pady=(0, 8))

        ctk.CTkButton(
            actions,
            text="[F4] SALVAR ALTERAÇÕES",
            height=44,
            fg_color=GOOD,
            hover_color="#15803d",
            text_color="white",
            font=("Arial", 12, "bold"),
            command=self.salvar_alteracoes
        ).pack(fill="x", padx=12, pady=(12, 6))

        ctk.CTkButton(
            actions,
            text="[F3] EXCLUIR LIVRO",
            height=42,
            fg_color=DANGER,
            hover_color=DANGER_HOVER,
            text_color="white",
            font=("Arial", 12, "bold"),
            command=self.excluir_livro
        ).pack(fill="x", padx=12, pady=(0, 6))

        ctk.CTkButton(
            actions,
            text="[ESC] VOLTAR",
            height=38,
            fg_color=BG,
            hover_color=BORDER,
            text_color=FG,
            border_color=BORDER,
            border_width=1,
            command=self.voltar_consulta
        ).pack(fill="x", padx=12, pady=(0, 12))

        # Informações extras
        stats = ctk.CTkFrame(
            right,
            fg_color=PANEL,
            border_color=BORDER,
            border_width=1,
            corner_radius=6
        )
        stats.pack(fill="x")

        self.criar_stat(stats, "Código interno", str(id_livro), MUTED)
        self.criar_stat(stats, "Imagem", imagem_capa or "Sem capa", MUTED)
        self.criar_stat(stats, "Status", "Ativo", GOOD)

    # ---------- Componentes internos ----------
    def criar_placeholder_capa(self, titulo, autor):
        img = Image.new("RGB", (140, 200), BG)
        d = ImageDraw.Draw(img)

        d.rectangle([6, 6, 134, 194], outline=ACCENT, width=2)

        titulo_curto = titulo[:18].upper()
        autor_curto = autor[:15].upper()

        d.text((18, 60), titulo_curto, fill=FG)
        d.text((18, 160), autor_curto, fill=MUTED)

        return ctk.CTkImage(
            light_image=img,
            dark_image=img,
            size=(140, 200)
        )

    def criar_kpi(self, parent, label, value, color):
        f = ctk.CTkFrame(
            parent,
            fg_color=PANEL,
            border_color=BORDER,
            border_width=1,
            corner_radius=4
        )

        ctk.CTkLabel(
            f,
            text=label,
            text_color=MUTED,
            font=("Arial", 9, "bold")
        ).pack(anchor="w", padx=8, pady=(6, 0))

        ctk.CTkLabel(
            f,
            text=value,
            text_color=color,
            font=("Consolas", 14, "bold")
        ).pack(anchor="w", padx=8, pady=(0, 6))

        return f

    def criar_label_campo(self, parent, texto):
        ctk.CTkLabel(
            parent,
            text=texto,
            text_color=MUTED,
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(4, 0))

    def criar_stat(self, parent, label, value, color):
        r = ctk.CTkFrame(parent, fg_color="transparent")
        r.pack(fill="x", padx=14, pady=5)

        ctk.CTkLabel(
            r,
            text=label,
            text_color=MUTED,
            font=("Consolas", 11)
        ).pack(side="left")

        ctk.CTkLabel(
            r,
            text=value,
            text_color=color,
            font=("Consolas", 11)
        ).pack(side="right")

    # ---------- Ações ----------
    def salvar_alteracoes(self):
        isbn = self.entry_isbn.get().strip()
        titulo = self.entry_titulo.get().strip()
        autor = self.entry_autor.get().strip()
        descricao = self.entry_descricao.get("1.0", "end").strip()
        categoria_nome = self.combo_categoria.get()

        try:
            preco = float(self.entry_preco.get().replace(",", "."))
            estoque = int(self.entry_estoque.get())
            paginas = int(self.entry_paginas.get())
        except ValueError:
            messagebox.showerror(
                "Erro",
                "Preço, estoque e páginas precisam ser valores válidos."
            )
            return

        if isbn == "" or titulo == "" or autor == "":
            messagebox.showerror(
                "Erro",
                "ISBN, título e autor são obrigatórios."
            )
            return

        if preco <= 0:
            messagebox.showerror("Erro", "O preço precisa ser maior que zero.")
            return

        if estoque < 0:
            messagebox.showerror("Erro", "O estoque não pode ser negativo.")
            return

        if paginas <= 0:
            messagebox.showerror("Erro", "O número de páginas precisa ser maior que zero.")
            return

        id_categoria = self.categorias.get(categoria_nome)

        try:
            sucesso = atualizar_livro(
                id_livro=self.id_livro,
                codigo_isbn=isbn,
                titulo=titulo,
                descricao=descricao,
                imagem_capa=self.imagem_capa,
                autor=autor,
                preco=preco,
                qtd_estoque=estoque,
                num_paginas=paginas,
                id_categoria=id_categoria
            )

            if sucesso:
                messagebox.showinfo("Sucesso", "Livro atualizado com sucesso!")
                self.livro = buscar_livro_por_id(self.id_livro)
            else:
                messagebox.showwarning("Aviso", "Nenhuma alteração foi feita.")

        except Exception as erro:
            messagebox.showerror(
                "Erro ao atualizar",
                f"Não foi possível atualizar o livro.\n\nDetalhe: {erro}"
            )

    def excluir_livro(self):
        confirmar = messagebox.askyesno(
            "Excluir livro",
            "Tem certeza que deseja excluir este livro?\n\nEssa ação não pode ser desfeita."
        )

        if not confirmar:
            return

        try:
            sucesso = deletar_livro(self.id_livro)

            if sucesso:
                messagebox.showinfo("Sucesso", "Livro excluído com sucesso!")
                self.voltar_consulta()
            else:
                messagebox.showwarning("Aviso", "Livro não encontrado para exclusão.")

        except Exception as erro:
            messagebox.showerror(
                "Erro ao excluir",
                "Não foi possível excluir o livro.\n\n"
                "Talvez ele já esteja vinculado a uma venda.\n\n"
                f"Detalhe: {erro}"
            )

    def voltar_consulta(self):
        self.parent.voltar_tela()