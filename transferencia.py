import mysql.connector
from mysql.connector import Error

def buscar_saldo(conta):
    try:
        # Conecta ao banco de dados
        conexao = mysql.connector.connect(host='localhost',
                                          database='transf_atomica',
                                          user='root',
                                          password='')

        if conexao.is_connected():

            cursor = conexao.cursor()

            # Busca o saldo da conta
            cursor.execute(f"SELECT saldo FROM contas WHERE id = {conta}")
            saldo = cursor.fetchone()[0]

            # Imprime o saldo da conta
            print(f'O saldo da conta no Banco de Dados é: {saldo}')

            # Pergunta ao usuário se ele deseja fazer uma transação
            transacao = input('\nDeseja fazer uma transação? (Y/N) ')
            if transacao.lower() == 'y':
                destino = int(input("\n\nDigite o ID da conta de destino: "))
                valor = float(input("Digite o valor a ser transferido: "))
                transferencia_atomica(conta, destino, valor, conexao, cursor)

    except Error as e:
        print("ABORTANDO - Erro ao conectar ao MySQL", e)

    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()
            print('OK - Conexão ao MySQL fechada')

def transferencia_atomica(origem, destino, valor, conexao, cursor):
    try:
        # Verifica se há saldo suficiente para a transferência
        cursor.execute(f"SELECT saldo FROM contas WHERE id = {origem}")
        saldo_origem = cursor.fetchone()[0]
        if saldo_origem < valor:
            print('ABORTANDO - Saldo insuficiente')
            return

        # Remove o valor da conta de origem
        cursor.execute(f"UPDATE contas SET saldo = saldo - {valor} WHERE id = {origem}")
        if cursor.rowcount != 1:
            print('ABORTANDO - Erro ao remover o valor da conta de origem')
            conexao.rollback()
            return

        # Adiciona o valor à conta de destino
        cursor.execute(f"UPDATE contas SET saldo = saldo + {valor} WHERE id = {destino}")
        if cursor.rowcount != 1:
            print('ABORTANDO - Erro ao adicionar o valor à conta de destino')
            conexao.rollback()
            return

        # Confirma a transação
        conexao.commit()

        print('\n\nOK - Transferência realizada com sucesso!')
        
        # Busca o saldo da conta
        cursor.execute(f"SELECT saldo FROM contas WHERE id = {origem}")
        saldo_final = cursor.fetchone()[0]

        # Imprime o saldo da conta
        print(f'\n-> Seu saldo ficou: {saldo_final}\n')

    except Error as e:
        print("ABORTANDO - Erro ao conectar ao MySQL", e)
        # Desfaz a transação em caso de erro
        conexao.rollback()
    
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()
            print('OK - Conexão ao Banco de Dados fechada!')
            
# Pede ao usuário que insira o ID da conta
conta = int(input('Digite o ID da conta: '))
buscar_saldo(conta)