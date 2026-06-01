import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "livraria_pdv.db"


def conectar():
    conexao = sqlite3.connect(DB_PATH)
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def registrar_venda(valor_total, itens, forma_pagamento="Não informado"):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO vendas (valor_total, status, forma_pagamento)
        VALUES (?, 'concluida', ?)
    """, (valor_total, forma_pagamento))

    id_venda = cursor.lastrowid

    for item in itens:
        cursor.execute("""
            INSERT INTO itens_venda
            (id_venda, id_livro, quantidade, preco_unitario, subtotal)
            VALUES (?, ?, ?, ?, ?)
        """, (
            id_venda,
            item["id_livro"],
            item["quantidade"],
            item["preco_unitario"],
            item["subtotal"]
        ))

        cursor.execute("""
            UPDATE livros
            SET qtd_estoque = qtd_estoque - ?
            WHERE id_livro = ?
        """, (
            item["quantidade"],
            item["id_livro"]
        ))

    conexao.commit()
    conexao.close()

    return id_venda