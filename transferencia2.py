import mysql.connector
from mysql.connector import Error

def transferencia_atomica(origem, destino, valor):
    try:
        # Conecta ao banco de dados
        conexao = mysql.connector.connect(host='localhost',
                                          database='transf_atomica',
                                          user='root',
                                          password='')

        if conexao.is_connected():
            print('OK - Conectado ao banco de dados MySQL [1/6]')

            cursor = conexao.cursor()

            # Inicia a transação
            conexao.start_transaction()

            # Busca o saldo da conta de origem
            cursor.execute(f"SELECT saldo FROM contas WHERE id = {origem}")
            print('OK - Conta origem encontrada! [2/6]')
            saldo_origem = cursor.fetchone()[0]

            # Verifica se há saldo suficiente para a transferência
            if saldo_origem < valor:
                print('ABORTAR - Saldo insuficiente')
                return

            # Remove o valor da conta de origem
            cursor.execute(f"UPDATE contas SET saldo = saldo - {valor} WHERE id = {origem}")
            print('OK - Conta origem debitada! [3/6]')

            # Adiciona o valor à conta de destino
            cursor.execute(f"UPDATE contas SET saldo = saldo + {valor} WHERE id = {destino}")
            print('OK - Conta destino transferida! [4/6]')

            # Confirma a transação
            conexao.commit()

            print('OK - Transferência realizada com sucesso! [5/6]')

    except Error as e:
        print("ABORTAR - Erro ao conectar ao MySQL", e)
        # Desfaz a transação em caso de erro
        conexao.rollback()

    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()
            print('OK - Conexão ao MySQL fechada [6/6]')

origem = input("Digite o ID da conta de origem: ")
destino = input("Digite o ID da conta de destino: ")
valor = input("Digite o valor a ser transferido: ")

# Converte as entradas para os tipos de dados corretos
origem = int(origem)
destino = int(destino)
valor = float(valor)

transferencia_atomica(origem, destino, valor)