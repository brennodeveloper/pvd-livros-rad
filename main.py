import customtkinter as ctk
from db.database import create_db
from screens.cadastro_livros import CadastroScreen
from screens.vendas import VendaScreen

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

create_db()

app = ctk.CTk()
app.title("PDV Livraria")
app.geometry("1000x650")

CadastroScreen(app)
VendaScreen(app)

app.mainloop()