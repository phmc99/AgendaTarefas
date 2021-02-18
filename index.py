from funcs import cabecalho, menu, adicionar, consulta, remove, altera


with open('dadosagenda.txt', 'a'):
    while True:

            print(cabecalho('Sua agenda'))
            resposta = menu(['Adicionar compromissos', 'Alterar um ou mais compromissos', 'Apagar um ou mais compromissos', 'Carregar agenda de compromissos', 'Sair do programa'])

            if resposta == 1:
                adicionar()
                
            elif resposta == 2:
                altera()

            elif resposta == 3:
                remove()

            elif resposta == 4:
                consulta()

            elif resposta == 5:
                print(cabecalho('Saindo do programa... Até logo!'))
                break
            else:
                print('\033[31mERRO: por favor, digite uma opção existente no menu.\033[m')