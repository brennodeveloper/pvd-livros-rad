import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "livraria_pdv.db"


def conectar():
    conexao = sqlite3.connect(DB_PATH)
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


# CREATE
def inserir_livro(
    codigo_isbn,
    titulo,
    descricao,
    imagem_capa,
    autor,
    preco,
    qtd_estoque,
    num_paginas,
    id_categoria
):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO livros
        (
            codigo_isbn,
            titulo,
            descricao,
            imagem_capa,
            autor,
            preco,
            qtd_estoque,
            num_paginas,
            id_categoria
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        codigo_isbn,
        titulo,
        descricao,
        imagem_capa,
        autor,
        preco,
        qtd_estoque,
        num_paginas,
        id_categoria
    ))

    conexao.commit()
    conexao.close()


# READ - listar todos
def listar_livros():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            livros.id_livro,
            livros.codigo_isbn,
            livros.titulo,
            livros.descricao,
            livros.imagem_capa,
            livros.autor,
            livros.preco,
            livros.qtd_estoque,
            livros.num_paginas,
            livros.id_categoria,
            categorias.nome_categoria
        FROM livros
        LEFT JOIN categorias
        ON livros.id_categoria = categorias.id_categoria
        ORDER BY livros.titulo
    """)

    livros = cursor.fetchall()

    conexao.close()

    return livros


# READ - buscar por ISBN
def buscar_livro_por_isbn(codigo_isbn):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            id_livro,
            codigo_isbn,
            titulo,
            autor,
            preco,
            qtd_estoque
        FROM livros
        WHERE codigo_isbn = ?
    """, (codigo_isbn,))

    livro = cursor.fetchone()

    conexao.close()

    return livro


# READ - buscar por ID
def buscar_livro_por_id(id_livro):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            livros.id_livro,
            livros.codigo_isbn,
            livros.titulo,
            livros.descricao,
            livros.imagem_capa,
            livros.autor,
            livros.preco,
            livros.qtd_estoque,
            livros.num_paginas,
            livros.id_categoria,
            categorias.nome_categoria
        FROM livros
        LEFT JOIN categorias
        ON livros.id_categoria = categorias.id_categoria
        WHERE livros.id_livro = ?
    """, (id_livro,))

    livro = cursor.fetchone()

    conexao.close()

    return livro


# READ - pesquisar por título, autor ou ISBN
def pesquisar_livros(termo):
    conexao = conectar()
    cursor = conexao.cursor()

    termo_busca = f"%{termo}%"

    cursor.execute("""
        SELECT
            livros.id_livro,
            livros.codigo_isbn,
            livros.titulo,
            livros.descricao,
            livros.imagem_capa,
            livros.autor,
            livros.preco,
            livros.qtd_estoque,
            livros.num_paginas,
            livros.id_categoria,
            categorias.nome_categoria
        FROM livros
        LEFT JOIN categorias
        ON livros.id_categoria = categorias.id_categoria
        WHERE
            livros.titulo LIKE ?
            OR livros.autor LIKE ?
            OR livros.codigo_isbn LIKE ?
        ORDER BY livros.titulo
    """, (
        termo_busca,
        termo_busca,
        termo_busca
    ))

    livros = cursor.fetchall()

    conexao.close()

    return livros


# UPDATE
def atualizar_livro(
    id_livro,
    codigo_isbn,
    titulo,
    descricao,
    imagem_capa,
    autor,
    preco,
    qtd_estoque,
    num_paginas,
    id_categoria
):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE livros
        SET
            codigo_isbn = ?,
            titulo = ?,
            descricao = ?,
            imagem_capa = ?,
            autor = ?,
            preco = ?,
            qtd_estoque = ?,
            num_paginas = ?,
            id_categoria = ?
        WHERE id_livro = ?
    """, (
        codigo_isbn,
        titulo,
        descricao,
        imagem_capa,
        autor,
        preco,
        qtd_estoque,
        num_paginas,
        id_categoria,
        id_livro
    ))

    conexao.commit()

    linhas_afetadas = cursor.rowcount

    conexao.close()

    return linhas_afetadas > 0


# DELETE
def deletar_livro(id_livro):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM livros
        WHERE id_livro = ?
    """, (id_livro,))

    conexao.commit()

    linhas_afetadas = cursor.rowcount

    conexao.close()

    return linhas_afetadas > 0


# UPDATE específico para venda
def baixar_estoque(id_livro, quantidade):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE livros
        SET qtd_estoque = qtd_estoque - ?
        WHERE id_livro = ?
    """, (
        quantidade,
        id_livro
    ))

    conexao.commit()

    linhas_afetadas = cursor.rowcount

    conexao.close()

    return linhas_afetadas > 0