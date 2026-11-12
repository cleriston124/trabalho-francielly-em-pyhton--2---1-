from conexao_banco import conexao
from getpass import getpass
AdminEmail = "arroz@gmail.com"
senha = 1234

def MenuGeral():
    opcao = 0
    while opcao != 3:
        print("\n MENU GERAL \n")
        print("1- você é admnistrador")
        print("2- você é cliente")
        print("3- sair ")

        try:
            opcao = int(input("qual a sua opção? "))
        except ValueError:
            print("opção inválida!!")
            continue

        if opcao == 1:
            cursor = conexao.cursor()
            validacaoemail = input("digite o seu email: ")
            
            try:
                validacaosenha = int(input("qual a sua senha? "))
            except ValueError:
                print("A senha deve ser numérica!")
                continue

            if validacaoemail == AdminEmail and validacaosenha == senha:
                print("login aceito")

                
                opcaoAdmin = 0
                while opcaoAdmin != 4:
                    print("\n MENU ADMIN \n")
                    print("1- cadastrar cliente")
                    print("2- alterar cliente")
                    print("3- excluir cliente ")
                    print("4- sair ")

                    try:
                        opcaoAdmin = int(input("qual a sua opção? "))
                    except ValueError:
                        print("opção inválida")
                        continue

                    if opcaoAdmin == 1:
                        emailcli = input("digite o email do cliente: ")
                        senhacli = input("digite a senha do cliente: ")
                        cpf = input("digite o cpf do cliente: ")
                        nome = input("digite o nome completo do cliente: ")
                        
                        try:
                            cnh = int(input("digite a cnh do cliente: "))
                        except ValueError:
                            print("CNH inválida!")
                            continue

                        
                        comando_sql = """INSERT INTO dadoscliente(cpf,nome,email,senha,cnh)
                        VALUES(%s,%s,%s,%s,%s)"""

                        valores = (cpf, nome, emailcli, senhacli, cnh)

                        try:
                            cursor.execute(comando_sql, valores)
                            conexao.commit()
                            print(f"\n usuário {nome} cadastrado com sucesso")
                        except Exception as erro:
                            print(f"deu erro: {erro}")

                    elif opcaoAdmin == 2:
                        cpf_alvo = input("qual o cpf do ciente que vocêQUER ALTERAR? ")
                        cursor.execute("SELECT nome,email,senha  FROM dados clientes WHERE cpf", (cpf_alvo))
                        cliente=cursor.fetchone()
                        
                        if not cliente:
                            print("cpf não encontrado")
                        else:
                            nome_a, emaila ,senhaa, = cliente
                            print("\n oque voce n quiser mudar deixe em brancon\n")
                        
                            novo_nome=input("qual o novo nome ")
                            email_novo=input("digite o novo email do cliente")
                            senha_novo=input("digite a nova senha do cliente")
                        
                        
                                                        
                            if novo_nome.strip()=="": 
                                novo_nome = nome_a
                            else :
                                nome_final=novo_nome
                                                        
                            if email_novo.strip()=="": 
                                email_novo = emaila
                            else:
                                email_final=email_novo
                                                        
                            if senha_novo.strip()=="": 
                                senha_novo = senhaa
                            else:
                                senha_final=senha_novo
                        
                        
                        
                                                   
                            comando_sql="""UPDATE dadosclientes SET nome=%S,email=%S,senha=%S,cnh=%S WHERE = cpf=%S"""
                            valores(nome_final,email_final,senha_final,cpf_alvo)
                        
                            try:
                                cursor.execute(comando_sql,valores)
                                conexao.commit()
                                if cursor.rowcount > 0:
                                    print(f"\nDados do usuário {nome} alterados com sucesso!")
                                else:
                                    print("\nNenhum cliente foi encontrado com esse CPF.")
                            except Exception as erro:
                                print("deu bosta")
                        
                        

                    elif opcaoAdmin == 3:
                        cpf_excluido=input("qual o cpf do cliente que voce que excluir ")
                        
                        cursor.execute("""SELECT FROM dadoscliente WHERE cpf=%S"""(cpf_excluido))
                        cliente=cursor.fetchone()
                        
                        if not cliente:
                            print("cliente não encontrado")
                        else:
                            nome_cliente=cliente[0]
                            confirma=input("dejesa continuar a operação, digite (sim)")
                        
                            if confirma=="sim":
                                comando_sql="""SELECT FROM dadoscliente WHERE cpf=%S"""
                            try:
                                cursor.execute(comando_sql,cpf_excluido)
                                conexao.commit()
                                if cursor.rowcount > 0:
                                    print(f"\nDados do usuário {nome} excluido com sucesso!")
                                else:
                                    print("\nNenhum cliente foi encontrado com esse CPF.")
                            except Exception as erro:
                                    print("deu bosta {erro}")
                       
                        
                
                
                cursor.close()
                print("Sessão de administrador encerrada.")
            else:
                print("Email ou senha incorretos!")

MenuGeral()
