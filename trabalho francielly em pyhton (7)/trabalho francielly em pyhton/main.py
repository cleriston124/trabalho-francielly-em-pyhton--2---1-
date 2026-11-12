from conexao_banco import conexao
import re
from dotenv import load_dotenv
import os
import bcrypt


load_dotenv()
Emailad=os.getenv("EmailAdmin")
senhaAd=os.getenv("SenhaAdmin")

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
            
            
            validacaosenha = input("qual a sua senha? ")

            if Emailad is None or senhaAd is None:
                print(" Não foi possível ler as credenciais do arquivo .env!")
                continue
            
                
                
            if validacaoemail == Emailad:
                #transforma em bytes
                senha_digitada_bytes = validacaosenha.encode('utf-8')
                hash_salvo_bytes = senhaAd.encode('utf-8')

                #calculo para comparaç]ão da senha digitada com o hash
                if bcrypt.checkpw(senha_digitada_bytes, hash_salvo_bytes):
                    print("login aceito")
                else:
                    print("Email ou senha incorretos")

                

                
                opcaoAdmin = 0
                while opcaoAdmin != 6:
                    print("\n MENU ADMIN \n")
                    print("1- cadastrar cliente")
                    print("2- alterar cliente")
                    print("3- excluir cliente ")
                    print("4- adicionar carro ao cliente ")
                    print("5- status do estacionamneto  ")
                    print("6- sair  ")

                    try:
                        opcaoAdmin = int(input("qual a sua opção? "))
                    except ValueError:
                        print("opção inválida")
                        continue

                    if opcaoAdmin == 1:
                        emailcli = input("digite o email do cliente: ").strip()
                        if not emailcli:
                            print(" Erro: O e-mail não pode ficar vazio!")
                            continue
                        #validação do formato do email, para garantir que tenha um nome antes do arroba depois venha o arroba e depois do arroba tenha outro texto e finalize com .com
                        if not re.match(r"[^@]+@[^@]+\.[^@]+", emailcli):
                            print(" Formato de e-mail inválido! Deve conter '@' e um domínio (ex: .com).")
                            continue
                        
                        cursor.execute("SELECT email FROM dadoscliente WHERE email = %s", [emailcli])
                        email_existente = cursor.fetchone()
                        
                        if email_existente:
                            print(" Erro: Este email já está cadastrado no sistema!")
                            continue  # Bloqueia o cadastro e volta para o menu


                        senhacli = input("digite a senha do cliente: ").strip()
                        if not senhacli:
                            print(" Erro: A senha não pode ficar vazia ou conter apenas espaços!")
                            continue
            
                        cpf = input("digite o cpf do cliente: ").strip()
                        if not cpf:
                            print(" Erro: O CPF não pode ficar vazio!")
                            continue
                        
                        #limpa todas letras ou simbolos por vazio no cpf e se n estiver 11 numeros da erro

                        cpf_limpo = re.sub(r"\D", "", cpf)
                        if len(cpf_limpo) != 11:
                            print(" Erro: O CPF deve conter exatamente 11 números!")
                            continue
                        
                        cursor.execute("SELECT cpf FROM dadoscliente WHERE cpf = %s", [cpf_limpo])
                        cpf_existente = cursor.fetchone()

                        if cpf_existente:
                            print(" Erro: Este CPF já está cadastrado no sistema!")
                            continue  



                        nome = input("digite o nome completo do cliente: ").strip()
                        if not nome:
                            print(" Erro: O nome não pode ficar vazio!")
                            continue
                        #limpa o nome junta ele e ver se n tem numero ou caracatres especiais se tiver ele para o codigo
                        if not nome.replace(" ", "").isalpha():
                            print(" Erro: O nome não pode conter números ou caracteres especiais!")
                            continue


                        cnh = input("Digite a CNH do cliente: ").strip()
                        if not cnh:
                            print(" Erro: A CNH não pode ficar vazia!")
                            continue

                        #mesma coisa do cpf
                        cnh_limpa = re.sub(r"\D", "", cnh)
                        if len(cnh_limpa) != 11:
                            print(" Erro: A CNH deve conter exatamente 11 dígitos numéricos!")
                            continue
                        cursor.execute("SELECT cnh FROM dadoscliente WHERE cnh = %s", [cnh_limpa])
                        cnh_existente = cursor.fetchone()

                        if cnh_existente:
                            print(" Erro: Esta CNH já está cadastrada no sistema!")
                            continue
                       
                        #se algum safadinho tentar colocar o cpf a mesma coisa da cnh
                        if cnh_limpa == cpf_limpo:
                            print("erro detectado")
                            continue

                        senha_bytes = senhacli.encode('utf-8')
                        senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())

                        #para o banco de dados entender
                        senhaCripto= senha_hash.decode('utf-8')
                                            
                       

                        
                        comando_sql = """INSERT INTO dadoscliente(cpf,nome,email,senha,cnh)
                        VALUES(%s,%s,%s,%s,%s)"""

                        valores = (cpf_limpo, nome, emailcli, senhaCripto, cnh_limpa)

                        try:
                            cursor.execute(comando_sql, valores)
                            conexao.commit()
                            print(f"\n usuário {nome} cadastrado com sucesso")
                        except Exception as erro:
                            print(f"deu erro: {erro}")

                    elif opcaoAdmin == 2:
                        cpf_alvo = input("qual o cpf do ciente que vocêQUER ALTERAR? ")
                        cursor.execute("SELECT nome,email,senha  FROM dadoscliente WHERE cpf=%s", [cpf_alvo])
                        cliente=cursor.fetchone()

                        
                        
                        if not cliente:
                            print("cpf não encontrado")
                        else:
                            nome_a, emaila ,senhaa, = cliente
                            print("\n oque voce n quiser mudar deixe em brancon\n")
                        
                            novo_nome=input("qual o novo nome ").strip()
                            if novo_nome and not novo_nome.replace(" ", "").isalpha():
                                print(" Erro: O nome não pode conter números ou caracteres especiais!")
                                continue
                            email_novo=input("digite o novo email do cliente").strip()
                            if email_novo and not re.match(r"[^@]+@[^@]+\.[^@]+", email_novo):
                                print(" Formato de e-mail inválido! Deve conter '@' e um domínio (ex: .com).")
                                continue
                            
                            senha_novo=input("digite a nova senha do cliente").strip()
                        
                        
                                                        
                            nome_final  = novo_nome  if novo_nome  != "" else nome_a
                            email_final = email_novo if email_novo != "" else emaila
                            if senha_novo != "":
                            # hash da senha nova
                                senha_bytes = senha_novo.encode('utf-8')
                                senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
                                senha_final = senha_hash.decode('utf-8')
                            else:
                            # Se ele deixou em branco, mantemos o hash antigo ('senhaa') que veio do banco
                                senha_final = senhaa


                        
                        
                                                   
                            comando_sql="""UPDATE dadoscliente SET nome=%s,email=%s,senha=%s WHERE  cpf=%s"""
                            valores=(nome_final,email_final,senha_final,cpf_alvo)
                        
                            try:
                                cursor.execute(comando_sql,valores)
                                conexao.commit()
                                if cursor.rowcount > 0:
                                    print(f"\nDados do usuário {nome_final} alterados com sucesso!")
                                else:
                                    print("\nvocê não mudou nada.")
                            except Exception as erro:
                                print(f"deu bosta{erro}")
                        
                        

                    elif opcaoAdmin == 3:
                        cpf_excluido=input("qual o cpf do cliente que voce que excluir ")
                        
                        cursor.execute("SELECT nome FROM dadoscliente WHERE cpf=%s",[cpf_excluido])
                        cliente=cursor.fetchone()
                        
                        if not cliente:
                            print("cliente não encontrado")
                        else:
                            nome_cliente=cliente[0]
                            confirma=input(f"dejesa continuar a operação {nome_cliente}, digite (sim)")
                        
                            if confirma=="sim":
                                comando_sql="""DELETE  FROM dadoscliente WHERE cpf=%s"""
                            try:
                                cursor.execute(comando_sql,[cpf_excluido])
                                conexao.commit()
                                if cursor.rowcount > 0:
                                    print(f"\nDados do usuário {nome_cliente} excluido com sucesso!")
                                else:
                                    print("\nNenhum cliente foi encontrado com esse CPF.")
                            except Exception as erro:
                                    print(f"deu ruim {erro}")

                    elif opcaoAdmin == 4:
                        cursor.execute("SELECT SUM(tamanho) FROM carros")
                        vagas_ocupadas = cursor.fetchone()[0]
                        if vagas_ocupadas is None:
                            vagas_ocupadas = 0
                
                        vagas_livres = 20 - vagas_ocupadas
                
                        if vagas_livres <= 0:
                            print(" Erro: O estacionamento está totalmente LOTADO (20/20 vagas)!")
                            continue
                        
                        cpf_cliente_carro = input("Digite o CPF do cliente dono do carro: ").strip()
                
              
                        cursor.execute("SELECT nome FROM dadoscliente WHERE cpf=%s", [cpf_cliente_carro])
                        cliente = cursor.fetchone()
                
                        if not cliente:
                            print(" Erro: Cliente não encontrado com esse CPF! Cadastre o cliente primeiro.")
                        else:
                            nome_cliente = cliente[0]
                            print(f"Cliente encontrado: {nome_cliente}")
                            print("\nTamanho do veículo:")
                            print("1 - Carro Normal (Ocupa 1 vaga)")
                            print("2 - Carro Maior  (Ocupa 2 vagas)")
                    
                            try:
                                tamanho = int(input("Escolha o tamanho (1 ou 2): "))
                                if tamanho not in[1,2]:
                                    print(" Opção inválida! Operação cancelada.")
                                    continue
                            except ValueError:
                                print(" Entrada inválida! Operação cancelada.")
                                continue
                        
                    
                            if tamanho > vagas_livres:
                                print(f"  Não há espaço! Este carro precisa de {tamanho} vagas, mas restam apenas {vagas_livres}.")
                                continue
                    
                            modelo = input("Digite o modelo do carro : ").strip()
                            if not modelo:
                                print(" Erro: o modelo não pode ficar vazia!")
                                continue

                            marca = input("Digite a marca do carro : ").strip()
                            if not marca:
                                print(" Erro: A marca não pode ficar vazia!")
                                continue
                            while True:
                                placa = input("Digite a placa do carro (ex: ABC123): ").strip().upper()
                                if not placa:
                                    print(" Erro: A placa não pode ficar vazia!")
                                    continue
                                cursor.execute("SELECT placa FROM carros WHERE placa = %s", [placa])
                                placaIgual = cursor.fetchone()
                                                        
                                if placaIgual:
                                    print(" Erro: Esta placa  já está cadastrado no sistema!")
                                    continue
                        
                        
                                if re.match(r"^[A-Z]{3}[0-9]{3}$", placa):
                                    break 
                                else:
                                    print(" Erro: A placa deve ter exatamente 3 letras seguidas de 3 números! (Ex: ABC123)")
                  
                            cor = input("Digite a cor do carro: ").strip()
                            if not cor:
                                print(" Erro: A cor não pode ficar vazia!")
                                continue
                                
                            
                            if cor.replace(" ", "").isalpha():
                                break 
                                
                            print(" Erro: A cor deve conter apenas letras! Números e símbolos não são permitidos.")
                    
                    
                            comando_sql = """INSERT INTO carros(modelo, marca, placa, cor, cpf_cliente,tamanho) 
                                     VALUES (%s, %s, %s, %s, %s,%s)"""
                            valores = (modelo, marca, placa, cor, cpf_cliente_carro,tamanho)
                    
                            try:
                                cursor.execute(comando_sql, valores)
                                conexao.commit()
                                print(f"\n Carro {marca} {modelo} associado com sucesso ao cliente {nome_cliente}!")
                            except Exception as erro:
                                print(f"Erro ao adicionar carro: {erro}")


                       
                        
                
                
                    elif opcaoAdmin == 5 :
                        cursor.execute("SELECT SUM(tamanho) FROM carros")
                        resultado_vagas = cursor.fetchone()
                
                
                        vagas_ocupadas = resultado_vagas[0] if resultado_vagas and resultado_vagas[0] is not None else 0
                
                        vagas_disponiveis = 20 - vagas_ocupadas
                
                        
                        print("   PAINEL DO ESTACIONAMENTO")
                       
                        print(f" Vagas Ocupadas: {vagas_ocupadas} / 20")
                        print(f" Vagas Livres:   {vagas_disponiveis} / 20")
                        
                    elif opcaoAdmin==6:
                        cursor.close()
                        print("Sessão de administrador encerrada.")

                        
                            
            else:
                print("Email ou senha incorretos!")

        if opcao==2:
            cursor=conexao.cursor()
            LoginCliente=input("qual o seu email: ").strip()
            senhacliente=input("qual a sua senha: ").strip()

            comando_login = "SELECT cpf, nome,senha  FROM dadoscliente WHERE email=%s "
            valores_login = [LoginCliente]

            cursor.execute(comando_login, valores_login)
            cliente_autenticado = cursor.fetchone()

            if cliente_autenticado:
                cpf_cliente, nome_cliente,hashBanco = cliente_autenticado
                senha_digitada_bytes = senhacliente.encode('utf-8')
                hash_salvo_bytes = hashBanco.encode('utf-8')
                if bcrypt.checkpw(senha_digitada_bytes, hash_salvo_bytes):
                                print(f" Bem-vindo de volta, {nome_cliente}! Login realizado com sucesso.")
                else:
                    print(f"{erro}")

            
            

                opcaocliente = 0
                while opcaocliente != 4:
                    print("\n MENU CLIENTE \n")
                    print("1- alterar a senha")
                    print("2- consultar carros")
                    print("3-ver dados")
                    print("4- sair ")
                            
                    try:
                        opcaocliente = int(input("qual a sua opção? "))
                    except ValueError:
                        print("opção inválida")
                        continue
                
                    if opcaocliente == 1:
                        cpf_alvo = input("qual o seu cpf ? ")
                        cursor.execute("SELECT nome, email, senha FROM dadoscliente WHERE cpf=%s", (cpf_alvo,))
                        cliente = cursor.fetchone()
                                            
                        if not cliente:
                            print("cpf não encontrado")
                        else:
                    
                            nome_atual, email_atual, senha_atual = cliente
                                                
                            senha_novo = input("digite a nova senha do cliente: ").strip()
                           
                            if senha_novo == "":
                                print("você não digitou nd")
                               
                                senha_final = senha_atual 
                            else:
                                                        
                                senha_bytes = senha_novo.encode('utf-8')
                                senha_hash = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
                                senha_final = senha_hash.decode('utf-8')
                                     
                                            
                            comando_sql = """UPDATE dadoscliente SET nome=%s, email=%s, senha=%s WHERE cpf=%s"""
                    
                    
                            valores = (nome_atual, email_atual, senha_final, cpf_alvo)
                                                    
                            try:
                                cursor.execute(comando_sql, valores)
                                conexao.commit()
                                if cursor.rowcount > 0:
                                    print(f"\nsenha do usuário {nome_atual} alterada com sucesso!")
                                else:
                                    print("\nvocê não mudou nada.")
                            except Exception as erro:
                                print(f"deu bosta: {erro}")

                    elif opcaocliente == 2:
                         # Busca todos os carros que pertencem ao CPF do cliente logado
                        comando_sql = "SELECT marca, modelo, placa, cor, tamanho FROM carros WHERE cpf_cliente = %s"
                        cursor.execute(comando_sql, [cpf_cliente])
                        meus_carros = cursor.fetchall()

                        if not meus_carros:
                            print("\n Você não possui nenhum carro cadastrado no nosso estacionamento.")
                        else:
                            print(f"\n--- SEUS VEÍCULOS CADASTRADOS ({nome_cliente}) ---")
                            total_vagas_cliente = 0
                    
                            # Lista cada carro encontrado
                            for carro in meus_carros:
                                marca, modelo, placa, cor, tamanho = carro
                                total_vagas_cliente += tamanho
                        
                                vaga_texto = "1 vaga (Normal)" if tamanho == 1 else "2 vagas (grande)"
                                print(f" {marca} {modelo} | Placa: {placa} | Cor: {cor} | Espaço ocupado: {vaga_texto}")
                    
                            print("-" * 50)
                            print(f" Total de vagas que seus veículos estão ocupando: {total_vagas_cliente} vaga(s).")
                            print("-" * 50)

                    elif opcaocliente==3:
                        comando_sql = "SELECT nome, email, cnh FROM dadoscliente WHERE cpf = %s"
                        cursor.execute(comando_sql, [cpf_cliente])
                        dados = cursor.fetchone()

                        if dados:
                            nome, email, cnh = dados
    
    
                            cpf_str = str(cpf_cliente).strip()
                            cpf_protegido = f"{cpf_str[:3]}.*.*-{cpf_str[-2:]}"
    
    
                            cnh_str = str(cnh).strip()
                            cnh_protegida = f"{cnh_str[:3]}**{cnh_str[-2:]}" 

    
                            if "@" in email:
                                usuario, dominio = email.split("@")
                                usuario_protegido = usuario[0] + "***" 
                                email_protegido = f"{usuario_protegido}@{dominio}" 
                            else:
                                email_protegido = "***"

    
                            print("\n--- SEUS DADOS CADASTRAIS ---")
                            print(f" Nome:   {nome}")
                            print(f" CPF:    {cpf_protegido}")  
                            print(f" E-mail: {email_protegido}") 
                            print(f" CNH:    {cnh_protegida}")  
                            print("-----------------------------")
            else:
                 print(" E-mail ou senha incorretos! Verifique os dados e tente novamente.")

           



            


MenuGeral()
