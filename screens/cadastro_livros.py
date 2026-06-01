import customtkinter as ctk
from tkinter import messagebox

from components.buttons import BackButton
from db.livros_repository import inserir_livro


class CadastroScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.pack(fill="both", expand=True)

        self.categorias = {
            "Romance": 1,
            "Aventura": 2,
            "Tecnologia": 3,
            "Terror": 4
        }

        self.criar_layout()

    def criar_layout(self):
        # Botão de voltar
        BackButton(
            self,
            command=self.voltar_inicio
        ).pack(anchor="nw", padx=15, pady=10)

        # Cabeçalho
        titulo = ctk.CTkLabel(
            self,
            text="📚 LIVRARIA PDV",
            font=("Arial", 30, "bold")
        )
        titulo.pack(pady=(5, 15))

        # Frame principal
        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.pack(fill="both", padx=30, pady=10, expand=True)

        # Título do formulário
        ctk.CTkLabel(
            frame,
            text="Cadastro de Livro",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        # Linha 1 - ISBN e categoria
        linha1 = ctk.CTkFrame(frame, fg_color="transparent")
        linha1.pack(fill="x", padx=20)

        self.entry_isbn = ctk.CTkEntry(
            linha1,
            width=250,
            placeholder_text="Código ISBN"
        )
        self.entry_isbn.pack(side="left", padx=10)

        self.combo_categoria = ctk.CTkComboBox(
            linha1,
            values=list(self.categorias.keys()),
            width=350
        )
        self.combo_categoria.set("Romance")
        self.combo_categoria.pack(side="left", padx=10)

        # Título
        ctk.CTkLabel(
            frame,
            text="Título da Obra"
        ).pack(anchor="w", padx=30, pady=(20, 5))

        self.entry_titulo = ctk.CTkEntry(
            frame,
            width=750
        )
        self.entry_titulo.pack(padx=30)

        # Autor
        ctk.CTkLabel(
            frame,
            text="Autor(es)"
        ).pack(anchor="w", padx=30, pady=(20, 5))

        self.entry_autor = ctk.CTkEntry(
            frame,
            width=750
        )
        self.entry_autor.pack(padx=30)

        # Descrição
        ctk.CTkLabel(
            frame,
            text="Descrição"
        ).pack(anchor="w", padx=30, pady=(20, 5))

        self.entry_descricao = ctk.CTkEntry(
            frame,
            width=750,
            placeholder_text="Descrição breve do livro"
        )
        self.entry_descricao.pack(padx=30)

        # Linha 2 - preço, estoque e páginas
        linha2 = ctk.CTkFrame(frame, fg_color="transparent")
        linha2.pack(fill="x", pady=20)

        self.entry_preco = ctk.CTkEntry(
            linha2,
            width=220,
            placeholder_text="Preço"
        )
        self.entry_preco.pack(side="left", padx=30)

        self.entry_estoque = ctk.CTkEntry(
            linha2,
            width=220,
            placeholder_text="Quantidade em estoque"
        )
        self.entry_estoque.pack(side="left", padx=10)

        self.entry_paginas = ctk.CTkEntry(
            linha2,
            width=220,
            placeholder_text="Nº de páginas"
        )
        self.entry_paginas.pack(side="left", padx=10)

        # Botões
        linha_botoes = ctk.CTkFrame(frame, fg_color="transparent")
        linha_botoes.pack(pady=35)

        btn_limpar = ctk.CTkButton(
            linha_botoes,
            text="Limpar",
            width=150,
            fg_color="#6b7280",
            hover_color="#4b5563",
            command=self.limpar_campos
        )
        btn_limpar.pack(side="left", padx=10)

        btn_salvar = ctk.CTkButton(
            linha_botoes,
            text="Salvar",
            width=150,
            fg_color="#16a34a",
            hover_color="#15803d",
            command=self.salvar_livro
        )
        btn_salvar.pack(side="left", padx=10)

    def salvar_livro(self):
        isbn = self.entry_isbn.get().strip()
        titulo = self.entry_titulo.get().strip()
        autor = self.entry_autor.get().strip()
        descricao = self.entry_descricao.get().strip()
        categoria_nome = self.combo_categoria.get()

        try:
            preco = float(self.entry_preco.get().replace(",", "."))
            estoque = int(self.entry_estoque.get())
            paginas = int(self.entry_paginas.get())
        except ValueError:
            messagebox.showerror(
                "Erro",
                "Preço, estoque e número de páginas precisam ser valores válidos."
            )
            return

        if isbn == "" or titulo == "" or autor == "":
            messagebox.showerror(
                "Erro",
                "Preencha ISBN, título e autor."
            )
            return

        if preco <= 0:
            messagebox.showerror(
                "Erro",
                "O preço precisa ser maior que zero."
            )
            return

        if estoque < 0:
            messagebox.showerror(
                "Erro",
                "O estoque não pode ser negativo."
            )
            return

        if paginas <= 0:
            messagebox.showerror(
                "Erro",
                "O número de páginas precisa ser maior que zero."
            )
            return

        id_categoria = self.categorias.get(categoria_nome)

        try:
            inserir_livro(
                codigo_isbn=isbn,
                titulo=titulo,
                descricao=descricao,
                imagem_capa=None,
                autor=autor,
                preco=preco,
                qtd_estoque=estoque,
                num_paginas=paginas,
                id_categoria=id_categoria
            )

            messagebox.showinfo(
                "Sucesso",
                "Livro cadastrado com sucesso!"
            )

            self.limpar_campos()

        except Exception as erro:
            messagebox.showerror(
                "Erro ao cadastrar",
                f"Não foi possível cadastrar o livro.\n\nDetalhe: {erro}"
            )

    def limpar_campos(self):
        self.entry_isbn.delete(0, "end")
        self.entry_titulo.delete(0, "end")
        self.entry_autor.delete(0, "end")
        self.entry_descricao.delete(0, "end")
        self.entry_preco.delete(0, "end")
        self.entry_estoque.delete(0, "end")
        self.entry_paginas.delete(0, "end")
        self.combo_categoria.set("Romance")

    def voltar_inicio(self):
        print("Voltando para a tela inicial...")
        self.destroy()