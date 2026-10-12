numero_chamado = 1  # Exemplo de número de chamado, você pode implementar uma lógica para gerar números únicos
chamados = []

print()
print("==============================")
print("       CONTROLE DE ACESSO")
print("==============================")
print("1 - Usuário")
print("2 - Suporte")

perfil = input("Escolha seu perfil: ")




while True:
        print()
        print("========================================")
        print("       SISTEMA DE CHAMADOS DE TI")
        print("========================================")

        print()
        print("1 - Abrir chamado")
        print("2 - Listar chamados")
        print("3 - Consultar chamado")
        if perfil == "2":
           print("4 - Alterar status")
           print("5 - Encerrar chamado")

        print("0 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            print("Encerrando o sistema...")
            break


        elif opcao == "1":
            print()
            print("--- NOVO CHAMADO ---")
            print("Abrindo formulário de chamado...")

            nome = input("Digite seu nome: ")
            problema = input("Descreva o problema: ")

            print()
            print("Categoria do chamado:")
            print("1 - Hardware")
            print("2 - Software")
            print("3 - Rede/Internet")
            print("4 - Acesso/Conta")

            categoria = input("Escolha uma categoria: ")

            if categoria == "1":
                categoria = "Hardware"
            elif categoria == "2":
                categoria = "Software"
            elif categoria == "3":
                categoria = "Rede/Internet"
            elif categoria == "4":
                categoria = "Acesso/Conta"

            print()
            print("Prioridade do chamado:")
            print("1 - Baixa")
            print("2 - Média")
            print("3 - Alta")

            prioridade = input("Escolha a prioridade: ")

            if prioridade == "1":
                prioridade = "Baixa"
            elif prioridade == "2":
                prioridade = "Média"
            elif prioridade == "3":
                prioridade = "Alta"

            print()
            print("==============================")
            print("       CHAMADO ABERTO")
            print("==============================")
            print("Número do chamado:", numero_chamado)
            print("Solicitante:", nome)
            print("Problema:", problema)
            print("Categoria:", categoria)
            print("Prioridade:", prioridade)
            print("Status: Aberto")
            print("==============================")

            chamado = {
                "numero": numero_chamado,
                "nome": nome,
                "problema": problema,
                "categoria": categoria,
                "prioridade": prioridade,
                "status": "Aberto"
            }

            chamados.append(chamado)
            numero_chamado += 1

        elif opcao == "2":
            print()
            print("====== LISTA DE CHAMADOS ======")

            if len(chamados) == 0:
                print("Nenhum chamado cadastrado.")
            else:
                for chamado in chamados:
                    print()
                    print("Número:", chamado["numero"])
                    print("Solicitante:", chamado["nome"])
                    print("Problema:", chamado["problema"])
                    print("Categoria:", chamado["categoria"])
                    print("Prioridade:", chamado["prioridade"])
                    print("Status:", chamado["status"])
                    print("------------------------------")

        elif opcao == "3":
            numero_consulta = int(input("Digite o número do chamado: "))
            encontrado = False

            for chamado in chamados:
                if chamado["numero"] == numero_consulta:
                    print()
                    print("===== CHAMADO ENCONTRADO =====")
                    print("Número:", chamado["numero"])
                    print("Solicitante:", chamado["nome"])
                    print("Problema:", chamado["problema"])
                    print("Categoria:", chamado["categoria"])
                    print("Prioridade:", chamado["prioridade"])
                    print("Status:", chamado["status"])
                    print("------------------------------")
                    encontrado = True

            if not encontrado:
                    print("Chamado não encontrado.")

        elif opcao == "4":
            print("ENTREI NA OPÇÃO 4")
            numero_alteracao = int(input("Digite o número do chamado: "))
            encontrado = False

            for chamado in chamados:
                if chamado["numero"] == numero_alteracao:
                    encontrado = True
                    print("1 - Em andamento")
                    print("2 - Aguardando")
                    print("3 - Resolvido")
                    print("4 - Encerrado")
                    novo_status = int(input("Escolha o novo status: "))

                    if novo_status == 1:
                        chamado["status"] = "Em Andamento"
                    elif novo_status == 2:
                        chamado["status"] = "Aguardando"
                    elif novo_status == 3:
                        chamado["status"] = "Resolvido"
                    elif novo_status == 4:
                        chamado["status"] = "Encerrado"
                    else:
                        print("Status inválido.")
                        continue

                    print("Status do chamado alterado com sucesso!")
                    break

            if not encontrado:
                print("Chamado não encontrado.")

        elif opcao == "5":
            numero_encerramento = int(input(
                "Digite o número do chamado para encerrar: "
            ))
            encontrado = False

            for chamado in chamados:
                if chamado["numero"] == numero_encerramento:
                    encontrado = True

                    if chamado["status"] == "Encerrado":
                        print("Chamado já está encerrado.")
                    else:
                        chamado["status"] = "Encerrado"
                        print("Chamado encerrado com sucesso!")

                    break

            if not encontrado:
                print("Chamado não encontrado.")

        else:
            print("Opção inválida. Tente novamente.")