import customtkinter as ctk
from db.database import create_db
from screens.tela_inicial import MenuScreen


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PDV Livraria")
        self.geometry("1000x650")

        self.historico = []
        self.tela_atual = None

        create_db()

        self.mostrar_tela(MenuScreen, salvar_historico=False)

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

    def mostrar_tela(self, tela_classe, salvar_historico=True, **kwargs):
        if salvar_historico and self.tela_atual is not None:
            self.historico.append(self.tela_atual)

        self.limpar_tela()

        self.tela_atual = {
            "classe": tela_classe,
            "kwargs": kwargs
        }

        tela_classe(self, **kwargs)

    def voltar_tela(self):
        if len(self.historico) == 0:
            self.mostrar_tela(MenuScreen, salvar_historico=False)
            return

        tela_anterior = self.historico.pop()

        self.limpar_tela()

        self.tela_atual = tela_anterior

        tela_anterior["classe"](
            self,
            **tela_anterior["kwargs"]
        )


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()