import customtkinter as ctk

from components.navbar import NavBar
from components.footer import Footer

from db.livros_repository import listar_livros, pesquisar_livros
from screens.cadastro_livros import CadastroScreen


class ConsultaScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.pack(fill="both", expand=True)

        self.livros = []

        self.criar_layout()
        self.carregar_livros()

    def criar_layout(self):
        NavBar(
            self,
            title="Livraria PDV — Consulta de Livros",
            operator="OP: ADMIN",
            back_command=self.voltar_inicio
        )

        Footer(
            self,
            shortcuts=("F1 Ajuda", "F2 Buscar", "F3 Detalhes", "F4 Novo Livro"),
            status_text="CONSULTA PRONTA"
        )

        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=15, pady=5)

        # =========================
        # CABEÇALHO DA CONSULTA
        # =========================

        topo = ctk.CTkFrame(container, fg_color="transparent")
        topo.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            topo,
            text="Livros cadastrados",
            font=("Arial", 22, "bold")
        ).pack(side="left")

        ctk.CTkButton(
            topo,
            text="+ Adicionar novo livro",
            height=40,
            fg_color="#16a34a",
            hover_color="#15803d",
            command=self.abrir_cadastro
        ).pack(side="right")

        # =========================
        # FILTROS / PESQUISA
        # =========================

        filtros = ctk.CTkFrame(container)
        filtros.pack(fill="x", padx=20, pady=10)

        self.entry_pesquisa = ctk.CTkEntry(
            filtros,
            placeholder_text="Pesquisar por título, autor ou ISBN...",
            height=40
        )
        self.entry_pesquisa.pack(side="left", fill="x", expand=True, padx=(15, 10), pady=15)

        ctk.CTkButton(
            filtros,
            text="Buscar",
            width=120,
            height=40,
            command=self.buscar_livros
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            filtros,
            text="Limpar",
            width=120,
            height=40,
            fg_color="#6b7280",
            hover_color="#4b5563",
            command=self.limpar_busca
        ).pack(side="left", padx=(0, 15))

        # Permite buscar apertando Enter
        self.entry_pesquisa.bind("<Return>", lambda event: self.buscar_livros())

        # =========================
        # TABELA
        # =========================

        tabela_container = ctk.CTkFrame(container)
        tabela_container.pack(fill="both", expand=True, padx=20, pady=(5, 15))

        header = ctk.CTkFrame(tabela_container)
        header.pack(fill="x", padx=10, pady=(10, 0))

        ctk.CTkLabel(header, text="ID", width=50, font=("Arial", 13, "bold")).pack(side="left", padx=3)
        ctk.CTkLabel(header, text="NOME DO LIVRO", width=240, font=("Arial", 13, "bold")).pack(side="left", padx=3)
        ctk.CTkLabel(header, text="AUTOR", width=170, font=("Arial", 13, "bold")).pack(side="left", padx=3)
        ctk.CTkLabel(header, text="CATEGORIA", width=110, font=("Arial", 13, "bold")).pack(side="left", padx=3)
        ctk.CTkLabel(header, text="ESTOQUE", width=75, font=("Arial", 13, "bold")).pack(side="left", padx=3)
        ctk.CTkLabel(header, text="PREÇO", width=90, font=("Arial", 13, "bold")).pack(side="left", padx=3)
        ctk.CTkLabel(header, text="AÇÕES", width=100, font=("Arial", 13, "bold")).pack(side="left", padx=3)

        self.lista_frame = ctk.CTkScrollableFrame(tabela_container)
        self.lista_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # =========================
        # RODAPÉ INTERNO DA CONSULTA
        # =========================

        info_bar = ctk.CTkFrame(container)
        info_bar.pack(fill="x", padx=20, pady=(0, 10))

        self.label_total_livros = ctk.CTkLabel(
            info_bar,
            text="Itens: 0",
            font=("Arial", 13, "bold")
        )
        self.label_total_livros.pack(side="left", padx=15, pady=10)

    # =========================
    # BANCO / CARREGAMENTO
    # =========================

    def carregar_livros(self):
        self.livros = listar_livros()
        self.renderizar_livros(self.livros)

    def buscar_livros(self):
        termo = self.entry_pesquisa.get().strip()

        if termo == "":
            self.carregar_livros()
            return

        self.livros = pesquisar_livros(termo)
        self.renderizar_livros(self.livros)

    def limpar_busca(self):
        self.entry_pesquisa.delete(0, "end")
        self.carregar_livros()

    # =========================
    # RENDERIZAÇÃO DA LISTA
    # =========================

    def renderizar_livros(self, livros):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()

        if len(livros) == 0:
            ctk.CTkLabel(
                self.lista_frame,
                text="📚 Nenhum livro encontrado",
                font=("Arial", 17)
            ).pack(pady=80)

            self.label_total_livros.configure(text="Itens: 0")
            return

        for livro in livros:
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
            ) = livro

            linha = ctk.CTkFrame(self.lista_frame)
            linha.pack(fill="x", padx=5, pady=5)

            ctk.CTkLabel(linha, text=str(id_livro), width=50).pack(side="left", padx=3)
            ctk.CTkLabel(linha, text=titulo, width=240, anchor="w").pack(side="left", padx=3)
            ctk.CTkLabel(linha, text=autor, width=170, anchor="w").pack(side="left", padx=3)
            ctk.CTkLabel(linha, text=nome_categoria or "Sem categoria", width=110).pack(side="left", padx=3)
            ctk.CTkLabel(linha, text=str(qtd_estoque), width=75).pack(side="left", padx=3)
            ctk.CTkLabel(linha, text=f"R$ {preco:.2f}", width=90).pack(side="left", padx=3)

            ctk.CTkButton(
                linha,
                text="Detalhes",
                width=90,
                height=30,
                fg_color="#1f6aa5",
                hover_color="#144870",
                command=lambda livro_id=id_livro: self.abrir_detalhes(livro_id)
            ).pack(side="left", padx=3)

        self.label_total_livros.configure(text=f"Itens: {len(livros)}")

    # =========================
    # NAVEGAÇÃO
    # =========================

    def abrir_cadastro(self):
        from screens.cadastro_livros import CadastroScreen
        self.parent.mostrar_tela(CadastroScreen)

    def abrir_detalhes(self, id_livro):
        from screens.pdv_detalhes import DetalhesScreen
        self.parent.mostrar_tela(DetalhesScreen, id_livro=id_livro)

    def voltar_inicio(self):
        self.parent.voltar_tela()