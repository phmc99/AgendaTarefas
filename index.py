from funcs import cabecalho, menu, adicionar, consulta, remove, altera, adiciona_mes, escolhe_mes, remove_mes


with open('dadosagenda.txt', 'a'):
    while True:

            print(cabecalho('Sua agenda'))
            resposta = menu(['Adicionar compromissos', 'Alterar um ou mais compromissos', 'Apagar um ou mais compromissos', 'Carregar agenda de compromissos', 'Sair do programa'])

            if resposta == 1:
                with open('meses.txt', 'a'):
                    resposta_meses = menu(['Adicionar um novo mês', 'Escolher entre os meses já adicionados', 'Apagar um mês'])
                    
                    if resposta_meses == 1:
                        mes = adiciona_mes()
                        try:
                            while True:
                                opcao_adiciona = input('Deseja adicionar um compromisso nesse mês? (s/n): ')

                                if opcao_adiciona == 's':
                                    adicionar(mes)
                                    break
                                elif opcao_adiciona == 'n':
                                    break
                                else:
                                    raise ValueError
                        except ValueError:
                            print('ERRO: por favor, digite uma opção válida, "s" ou "n".')

                    elif resposta_meses == 2:
                        adicionar(escolhe_mes())

                    elif resposta_meses == 3:
                        remove_mes()

                    else:
                        print('\033[31mERRO: por favor, digite uma opção existente no menu.\033[m')
                
                
            elif resposta == 2:
                altera(escolhe_mes())

            elif resposta == 3:
                remove(escolhe_mes())

            elif resposta == 4:
                consulta(escolhe_mes())

            elif resposta == 5:
                print(cabecalho('Saindo do programa... Até logo!'))
                break
            