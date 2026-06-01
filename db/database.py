import sqlite3

def create_db():
    conexao = sqlite3.connect("db/livraria_pdv.db") 
    cursor = conexao.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_categoria TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            id_livro INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_isbn TEXT NOT NULL UNIQUE,
            titulo TEXT NOT NULL,
            descricao TEXT,
            imagem_capa TEXT,
            autor TEXT NOT NULL,
            preco REAL NOT NULL CHECK(preco > 0),
            qtd_estoque INTEGER NOT NULL DEFAULT 0 CHECK(qtd_estoque >= 0),
            num_paginas INTEGER NOT NULL CHECK(num_paginas > 0),
            id_categoria INTEGER,
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(id_categoria)
            REFERENCES categorias(id_categoria)
            ON DELETE SET NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
            data_venda DATETIME DEFAULT CURRENT_TIMESTAMP,
            valor_total REAL NOT NULL CHECK(valor_total >= 0),
            status TEXT NOT NULL DEFAULT 'concluida'
                CHECK(status IN ('pendente', 'concluida', 'cancelada')),
            forma_pagamento TEXT DEFAULT 'Não informado'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_venda (
            id_item INTEGER PRIMARY KEY AUTOINCREMENT,
            id_venda INTEGER NOT NULL,
            id_livro INTEGER NOT NULL,
            quantidade INTEGER NOT NULL CHECK(quantidade > 0),
            preco_unitario REAL NOT NULL CHECK(preco_unitario > 0),
            subtotal REAL NOT NULL CHECK(subtotal >= 0),

            FOREIGN KEY(id_venda)
            REFERENCES vendas(id_venda)
            ON DELETE CASCADE,

            FOREIGN KEY(id_livro)
            REFERENCES livros(id_livro)
        )
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO categorias (id_categoria, nome_categoria)
    VALUES
    (1, 'Romance'),
    (2, 'Aventura'),
    (3, 'Tecnologia'),
    (4, 'Terror')
    """)
    
    cursor.execute("""
        INSERT OR IGNORE INTO livros
        (codigo_isbn, titulo, descricao, imagem_capa, autor, preco, qtd_estoque, num_paginas, id_categoria)
        VALUES
        ('123456789', 'Dom Casmurro', 'Clássico da literatura brasileira.', NULL, 'Machado de Assis', 39.90, 10, 256, 1),
        ('978741852', '1984', 'Distopia política e social.', NULL, 'George Orwell', 45.50, 8, 300, 4),
        ('978963852', 'O Hobbit', 'Aventura fantástica na Terra Média.', NULL, 'J.R.R. Tolkien', 59.90, 5, 320, 2),
        ('978111222', 'Clean Code', 'Livro sobre boas práticas de programação.', NULL, 'Robert C. Martin', 89.90, 6, 464, 3)
    """)
    conexao.commit()
    conexao.close()


if __name__ == "__main__":
    create_db()