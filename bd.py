import mysql.connector

def create_tables():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="transf_atomica"
    )
    cursor = db.cursor()

    cursor.execute('''CREATE TABLE contas(id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), saldo DECIMAL(10, 2))''')

    cursor.execute('''INSERT INTO contas(nome, saldo) VALUES(%s, %s)''', ('Conta1', 1000))
    cursor.execute('''INSERT INTO contas(nome, saldo) VALUES(%s, %s)''', ('Conta2', 1000))

    db.commit()
    db.close()

if __name__ == '__main__':
    create_tables()