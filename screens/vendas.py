import customtkinter as ctk
from components.navbar import NavBar
from components.footer import Footer

from db.livros_repository import buscar_livro_por_isbn
from db.vendas_repository import registrar_venda


class VendaScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.pack(fill="both", expand=True)

        self.carrinho = []
        self.total = 0

        self.criar_layout()

    def criar_layout(self):
        NavBar(
            self,
            title="Livraria PDV — Vendas",
            operator="OP: ADMIN",
            back_command=self.voltar_inicio
        )

        Footer(
            self,
            shortcuts=("F1 Ajuda", "F2 Item", "F4 Adicionar", "F8 Finalizar"),
            status_text="SCANNER PRONTO"
        )

        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=15, pady=5)

        left_frame = ctk.CTkFrame(container)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right_frame = ctk.CTkFrame(container, width=320)
        right_frame.pack(side="right", fill="y")
        right_frame.pack_propagate(False)

        ctk.CTkLabel(
            left_frame,
            text="Itens da Venda",
            font=("Arial", 26, "bold")
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            left_frame,
            text="Livros adicionados ao carrinho",
            font=("Arial", 14)
        ).pack(pady=(0, 20))

        header = ctk.CTkFrame(left_frame)
        header.pack(fill="x", padx=15, pady=(0, 5))

        ctk.CTkLabel(header, text="ITEM", width=80).pack(side="left", padx=5)
        ctk.CTkLabel(header, text="DESCRIÇÃO", width=250).pack(side="left", padx=5)
        ctk.CTkLabel(header, text="QTD", width=80).pack(side="left", padx=5)
        ctk.CTkLabel(header, text="TOTAL", width=100).pack(side="left", padx=5)

        self.lista_frame = ctk.CTkScrollableFrame(left_frame)
        self.lista_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.label_vazio = ctk.CTkLabel(
            self.lista_frame,
            text="🛒 Nenhum item adicionado",
            font=("Arial", 16)
        )
        self.label_vazio.pack(pady=80)

        qtd_box = ctk.CTkFrame(left_frame)
        qtd_box.pack(fill="x", padx=15, pady=15)

        self.label_qtd_itens = ctk.CTkLabel(
            qtd_box,
            text="Itens: 0",
            font=("Arial", 14, "bold")
        )
        self.label_qtd_itens.pack(side="left", padx=10, pady=10)

        ctk.CTkLabel(
            right_frame,
            text="Operação",
            font=("Arial", 22, "bold")
        ).pack(pady=(25, 20))

        ctk.CTkLabel(
            right_frame,
            text="Código / ISBN do livro"
        ).pack(anchor="w", padx=20)

        self.entry_isbn = ctk.CTkEntry(
            right_frame,
            placeholder_text="Ex: 978123456",
            height=40
        )
        self.entry_isbn.pack(fill="x", padx=20, pady=(5, 15))

        ctk.CTkLabel(
            right_frame,
            text="Quantidade"
        ).pack(anchor="w", padx=20)

        self.entry_qtd = ctk.CTkEntry(
            right_frame,
            height=40
        )
        self.entry_qtd.insert(0, "1")
        self.entry_qtd.pack(fill="x", padx=20, pady=(5, 20))

        self.btn_adicionar = ctk.CTkButton(
            right_frame,
            text="➕ ADICIONAR ITEM",
            height=50,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.adicionar_item
        )
        self.btn_adicionar.pack(fill="x", padx=20, pady=(0, 25))

        total_box = ctk.CTkFrame(right_frame)
        total_box.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            total_box,
            text="TOTAL DA COMPRA",
            font=("Arial", 13, "bold")
        ).pack(pady=(15, 5))

        self.label_total = ctk.CTkLabel(
            total_box,
            text="R$ 0,00",
            font=("Arial", 32, "bold")
        )
        self.label_total.pack(pady=(0, 15))

        self.btn_finalizar = ctk.CTkButton(
            right_frame,
            text="FECHAMENTO",
            height=65,
            font=("Arial", 18, "bold"),
            fg_color="#16a34a",
            hover_color="#15803d",
            command=self.abrir_modal_finalizar
        )
        self.btn_finalizar.pack(fill="x", padx=20, pady=20)

        self.btn_cancelar = ctk.CTkButton(
            right_frame,
            text="Cancelar Pedido",
            height=40,
            fg_color="#991b1b",
            hover_color="#7f1d1d",
            command=self.cancelar_pedido
        )
        self.btn_cancelar.pack(fill="x", padx=20, pady=(5, 20))

    def voltar_inicio(self):
        self.parent.voltar_tela()

    def adicionar_item(self):
        isbn = self.entry_isbn.get().strip()

        try:
            quantidade = int(self.entry_qtd.get())
        except ValueError:
            print("Quantidade inválida")
            return

        if quantidade <= 0:
            print("Quantidade precisa ser maior que zero")
            return

        livro = buscar_livro_por_isbn(isbn)

        if livro is None:
            print("Livro não encontrado")
            return

        id_livro, codigo_isbn, titulo, autor, preco, estoque = livro

        if quantidade > estoque:
            print("Estoque insuficiente")
            return

        subtotal = preco * quantidade

        item = {
            "id_livro": id_livro,
            "titulo": titulo,
            "quantidade": quantidade,
            "preco_unitario": preco,
            "subtotal": subtotal
        }

        self.carrinho.append(item)
        self.total += subtotal

        self.atualizar_carrinho()

        self.entry_isbn.delete(0, "end")
        self.entry_qtd.delete(0, "end")
        self.entry_qtd.insert(0, "1")

    def atualizar_carrinho(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()

        if len(self.carrinho) == 0:
            self.label_vazio = ctk.CTkLabel(
                self.lista_frame,
                text="🛒 Nenhum item adicionado",
                font=("Arial", 16)
            )
            self.label_vazio.pack(pady=80)

            self.label_total.configure(text="R$ 0,00")
            self.label_qtd_itens.configure(text="Itens: 0")
            return

        for index, item in enumerate(self.carrinho, start=1):
            linha = ctk.CTkFrame(self.lista_frame)
            linha.pack(fill="x", padx=5, pady=5)

            ctk.CTkLabel(
                linha,
                text=str(index),
                width=60
            ).pack(side="left", padx=5)

            ctk.CTkLabel(
                linha,
                text=item["titulo"],
                width=230
            ).pack(side="left", padx=5)

            ctk.CTkLabel(
                linha,
                text=str(item["quantidade"]),
                width=60
            ).pack(side="left", padx=5)

            ctk.CTkLabel(
                linha,
                text=f"R$ {item['subtotal']:.2f}",
                width=100
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                linha,
                text="Remover",
                width=80,
                height=28,
                fg_color="#991b1b",
                hover_color="#7f1d1d",
                command=lambda i=index - 1: self.remover_item(i)
            ).pack(side="left", padx=5)

        self.label_total.configure(text=f"R$ {self.total:.2f}")
        self.label_qtd_itens.configure(text=f"Itens: {len(self.carrinho)}")

    def remover_item(self, index):
        item = self.carrinho.pop(index)

        self.total -= item["subtotal"]

        if self.total < 0:
            self.total = 0

        self.atualizar_carrinho()

    def abrir_modal_finalizar(self):
        if len(self.carrinho) == 0:
            print("Carrinho vazio")
            return

        modal = ctk.CTkToplevel(self)
        modal.title("Finalizar Pedido")
        modal.geometry("350x250")
        modal.grab_set()

        ctk.CTkLabel(
            modal,
            text="Finalizar Pedido",
            font=("Arial", 22, "bold")
        ).pack(pady=(25, 10))

        ctk.CTkLabel(
            modal,
            text="Deseja concluir esta venda?",
            font=("Arial", 15)
        ).pack(pady=10)

        ctk.CTkLabel(
            modal,
            text=f"Total: R$ {self.total:.2f}",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        botoes = ctk.CTkFrame(modal, fg_color="transparent")
        botoes.pack(pady=20)

        ctk.CTkButton(
            botoes,
            text="Cancelar",
            fg_color="#6b7280",
            command=modal.destroy
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            botoes,
            text="Confirmar",
            fg_color="#16a34a",
            command=lambda: self.confirmar_venda(modal)
        ).pack(side="left", padx=10)

    def confirmar_venda(self, modal_anterior):
        modal_anterior.destroy()

        registrar_venda(self.total, self.carrinho)

        modal = ctk.CTkToplevel(self)
        modal.title("Venda Concluída")
        modal.geometry("350x220")
        modal.grab_set()

        ctk.CTkLabel(
            modal,
            text="✅",
            font=("Arial", 40)
        ).pack(pady=(25, 5))

        ctk.CTkLabel(
            modal,
            text="Venda concluída!",
            font=("Arial", 22, "bold")
        ).pack(pady=5)

        ctk.CTkLabel(
            modal,
            text="Pagamento aprovado com sucesso.",
            font=("Arial", 14)
        ).pack(pady=5)

        ctk.CTkButton(
            modal,
            text="OK",
            command=lambda: self.finalizar_fluxo(modal)
        ).pack(pady=20)

    def finalizar_fluxo(self, modal):
        modal.destroy()
        self.limpar_carrinho()

    def cancelar_pedido(self):
        if len(self.carrinho) == 0:
            print("Carrinho já está vazio")
            return

        modal = ctk.CTkToplevel(self)
        modal.title("Cancelar Pedido")
        modal.geometry("350x220")
        modal.grab_set()

        ctk.CTkLabel(
            modal,
            text="Cancelar Pedido",
            font=("Arial", 22, "bold")
        ).pack(pady=(25, 10))

        ctk.CTkLabel(
            modal,
            text="Deseja remover todos os itens do carrinho?",
            font=("Arial", 14)
        ).pack(pady=10)

        botoes = ctk.CTkFrame(modal, fg_color="transparent")
        botoes.pack(pady=20)

        ctk.CTkButton(
            botoes,
            text="Não",
            fg_color="#6b7280",
            command=modal.destroy
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            botoes,
            text="Sim, cancelar",
            fg_color="#991b1b",
            hover_color="#7f1d1d",
            command=lambda: self.confirmar_cancelamento(modal)).pack(side="left", padx=10)
    
    def confirmar_cancelamento(self, modal):
        modal.destroy()
        self.limpar_carrinho()

    def limpar_carrinho(self):
        self.carrinho = []
        self.total = 0

        for widget in self.lista_frame.winfo_children():
            widget.destroy()

        self.label_vazio = ctk.CTkLabel(
            self.lista_frame,
            text="🛒 Nenhum item adicionado",
            font=("Arial", 16)
        )
        self.label_vazio.pack(pady=80)

        self.label_total.configure(text="R$ 0,00")
        self.label_qtd_itens.configure(text="Itens: 0")