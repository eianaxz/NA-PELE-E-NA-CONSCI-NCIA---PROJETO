# Arquivo: Database.py
import sqlite3
from typing import Optional, Tuple, Dict, Any

class Database:
    def __init__(self, db_name: str = "usuarios.db") -> None:
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self) -> None:
        """Cria a tabela de usuários se não existir"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                apelido TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def get_user_data(self, user_id: int) -> Optional[Tuple]:
        """Obtém os dados do usuário pelo ID"""
        self.cursor.execute(
            "SELECT nome, apelido, email, senha FROM usuarios WHERE id = ?", 
            (user_id,)
        )
        return self.cursor.fetchone()

    def get_user_id_by_email(self, email: str) -> Optional[int]:
        """Obtém o ID do usuário pelo email"""
        self.cursor.execute(
            "SELECT id FROM usuarios WHERE email = ?", 
            (email,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else None

    def insert_user(self, user_data: Dict[str, Any]) -> bool:
        """Insere um novo usuário no banco de dados"""
        try:
            self.cursor.execute('''
                INSERT INTO usuarios (nome, apelido, email, senha)
                VALUES (?, ?, ?, ?)
            ''', (
                user_data["nome"],
                user_data["apelido"],
                user_data["email"],
                user_data["senha"]
            ))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Erro de integridade: {e}")
            return False
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return False

    # ... (outros métodos mantidos conforme original)

    def update_user_data(self, user_id, column, new_value):
        try:
            self.cursor.execute(f"UPDATE usuarios SET {column} = ? WHERE id = ?", (new_value, user_id))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                return "unique_constraint"
            return False
        except Exception as e:
            print(f"Erro ao atualizar: {e}")
            return False

    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
        self.conn.commit()

    def check_apelido_exists(self, apelido, current_user_id=None):
        if current_user_id:
            self.cursor.execute("SELECT 1 FROM usuarios WHERE apelido = ? AND id != ?", (apelido, current_user_id))
        else:
            self.cursor.execute("SELECT 1 FROM usuarios WHERE apelido = ?", (apelido,))
        return self.cursor.fetchone() is not None

    def check_email_exists(self, email, current_user_id=None):
        if current_user_id:
            self.cursor.execute("SELECT 1 FROM usuarios WHERE email = ? AND id != ?", (email, current_user_id))
        else:
            self.cursor.execute("SELECT 1 FROM usuarios WHERE email = ?", (email,))
        return self.cursor.fetchone() is not None

    
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
    def close(self):
        self.conn.close()

if __name__ == '__main__':
    db = Database()
    # Exemplo de uso (apenas para teste)
    # db.cursor.execute("INSERT INTO usuarios (nome, apelido, email, senha) VALUES (?, ?, ?, ?)",
    #                   ("Teste User", "testeuser", "teste@gmail.com", "123456"))
    # db.conn.commit()
    # print(db.get_user_data(1))
    # db.close()