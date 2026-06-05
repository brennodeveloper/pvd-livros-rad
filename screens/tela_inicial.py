import customtkinter as ctk
from screens.vendas import VendaScreen
from screens.cadastro_livros import CadastroScreen
from screens.consulta_livros import ConsultaScreen

class MenuScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.pack(fill="both", expand=True)

        self.criar_layout()

    def criar_layout(self):
        # Cabeçalho
        header = ctk.CTkFrame(self, height=80)
        header.pack(fill="x", padx=15, pady=(15, 10))
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="📚 LIVRARIA PDV",
            font=("Arial", 30, "bold")
        ).pack(side="left", padx=25)

        ctk.CTkLabel(
            header,
            text="Operador: Admin\nTerminal 01",
            font=("Arial", 13),
            justify="right"
        ).pack(side="right", padx=25)

        # Área de título
        title_box = ctk.CTkFrame(self, height=60)
        title_box.pack(fill="x", padx=15, pady=10)
        title_box.pack_propagate(False)

        ctk.CTkLabel(
            title_box,
            text="Ações do Sistema",
            font=("Arial", 18, "bold")
        ).pack(side="left", padx=20)

        # Container dos botões
        content = ctk.CTkFrame(self)
        content.pack(fill="both", expand=True, padx=15, pady=10)

        # Botão principal
        btn_vender = ctk.CTkButton(
            content,
            text="🛒\nVENDER LIVRO",
            height=130,
            font=("Arial", 28, "bold"),
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.abrir_vendas
        )
        btn_vender.pack(fill="x", padx=20, pady=(25, 20))

        # Grade de botões
        grid = ctk.CTkFrame(content, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=20, pady=10)

        btn_cadastrar = ctk.CTkButton(
            grid,
            text="➕\nCADASTRAR LIVRO",
            height=110,
            font=("Arial", 18, "bold"),
            fg_color="#374151",
            hover_color="#4b5563",
            command=self.abrir_cadastro
        )
        btn_cadastrar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        btn_consultar = ctk.CTkButton(
            grid,
            text="🔍\nCONSULTAR LIVROS",
            height=110,
            font=("Arial", 18, "bold"),
            fg_color="#374151",
            hover_color="#4b5563",
            command=self.abrir_consulta
        )
        btn_consultar.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        btn_sobre = ctk.CTkButton(
            grid,
            text="ℹ\nSOBRE O PROJETO",
            height=110,
            font=("Arial", 18, "bold"),
            fg_color="#374151",
            hover_color="#4b5563",
            command=self.abrir_sobre
        )
        btn_sobre.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        btn_sair = ctk.CTkButton(
            grid,
            text="⏻\nSAIR",
            height=110,
            font=("Arial", 18, "bold"),
            fg_color="#991b1b",
            hover_color="#7f1d1d",
            command=self.parent.destroy
        )
        btn_sair.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        grid.grid_columnconfigure(0, weight=1)
        grid.grid_columnconfigure(1, weight=1)
        grid.grid_rowconfigure(0, weight=1)
        grid.grid_rowconfigure(1, weight=1)

        # Rodapé
        ctk.CTkLabel(
            self,
            text="Projeto Acadêmico RAD • Python + CustomTkinter + SQLite",
            font=("Arial", 12)
        ).pack(pady=(0, 15))

    def abrir_vendas(self):
        from screens.vendas import VendaScreen
        self.parent.mostrar_tela(VendaScreen)

    def abrir_cadastro(self):
        from screens.cadastro_livros import CadastroScreen
        self.parent.mostrar_tela(CadastroScreen)

    def abrir_consulta(self):
        from screens.consulta_livros import ConsultaScreen
        self.parent.mostrar_tela(ConsultaScreen)

    def abrir_sobre(self):
        modal = ctk.CTkToplevel(self)
        modal.title("Sobre")
        modal.geometry("350x220")
        modal.grab_set()

        ctk.CTkLabel(
            modal,
            text="Livraria PDV",
            font=("Arial", 24, "bold")
        ).pack(pady=(25, 10))

        ctk.CTkLabel(
            modal,
            text="Projeto acadêmico da disciplina de\nDesenvolvimento Rápido de Aplicações em Python.",
            font=("Arial", 14),
            justify="center"
        ).pack(pady=10)

        ctk.CTkButton(
            modal,
            text="OK",
            command=modal.destroy
        ).pack(pady=20)