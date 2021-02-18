import calendar
from datetime import date

##### Funções para a parte visual do menu. #####
def linha(tam = 42):
    return '-'*tam

def cabecalho(texto):
    print(linha())
    print(texto.center(42))
    return linha()

def menu(texto): 
    print(cabecalho('Menu'))
    n_opcao = 1
    
    for item in texto:
        print(f'(\033[33m{n_opcao}\033[m) \033[34m{item}\033[m')
        n_opcao += 1

    print(f'\n{linha()}')
    
    opcao_escolha = escolha('\033[32mDigite sua opção: \033[m')
    return opcao_escolha

##### Função para capturar a opção do usuário. #####
def escolha(mensagem):
    while True:
        try:
            numero_opcao = int(input(mensagem))
        except (ValueError, TabError):
            print('\033[31mERRO: por favor, digite uma opção com o número inteiro válido.\033[m')
            continue
        except (KeyboardInterrupt):
            print('\033[31m Erro: o usuário preferiu não informar uma opção.\033[m')
        else:
            return numero_opcao

###### Função para mostrar calendario. #####
def mostra_calendario(ano, mes):
    calendar.setfirstweekday(6)
    matriz_calendario = calendar.monthcalendar(ano, mes)
    
    print('\n', calendar.month(ano, mes))
        
    return matriz_calendario

##### Funções para adicionar o compromisso. #####
def adicionar():
    print(cabecalho('Adicione seus compromissos.'))

    opcao_calendario = 0
    opcao_compromisso = ''
    ano_atual = date.today().year
    ultimo_dia = calendar.mdays
    meses = []
    contador = 1
    
    # Escolhendo os meses para adicionar compromisso
    while opcao_calendario != 'n':
        opcao_calendario = ''
        try:
            mes = int(input('\033[32mInforme o mês que deseja adicionar um compromisso: \033[m'))
            if mes in meses:
                print('\033[31mERRO: esse mês já foi informado.\033[m')
            elif mes not in meses and mes >= 1 and mes <= 12:
                meses.append(mes)            
            else:
                raise ValueError

        except (ValueError, TypeError):
            print('\033[31mERRO: por favor, digite uma opção com o número inteiro de 1 a 12.\033[m')

        except (KeyboardInterrupt):
            print('\033[31m Erro: o usuário preferiu não informar uma opção.\033[m')
        
        while opcao_calendario != 's' and opcao_calendario != 'n':
            try:
                opcao_calendario = input('Deseja informar mais um mês? (s/n): ')
                
                if opcao_calendario == 's' or opcao_calendario == 'n':
                    if opcao_calendario == 's':
                        contador += len(meses)
                    else:
                        pass
                else:
                    raise ValueError

            except (ValueError, TypeError):
                print('\033[31mERRO: por favor, digite uma opção válida, "s" ou "n".\033[m')
            
            except (KeyboardInterrupt):
                print('\033[31m Erro: o usuário preferiu não informar uma opção.\033[m')

    # Mostrando os meses selecionados
    if len(meses) > 0:
        for i in range(len(meses)):
            mostra_calendario(ano_atual, meses[i])
        
    # Adicionando compromissos no arquivo
    with open('dadosagenda.txt', 'a') as arquivo:
        while opcao_compromisso != 'n':
            while True:
                if len(meses) == 1:
                    mes_adiciona = meses[0]
                    break
                else:
                    try:
                        mes_adiciona = int(input(f'\033[32mEscolha um dos meses para adicionar o compromisso:\033[m \033[33m{str(meses).strip("[]")}: \033[m'))
                        if mes_adiciona not in meses:
                            raise ValueError
                        else:
                            break
                    except KeyboardInterrupt:
                        print('\033[31m Erro: o usuário preferiu não informar um compromisso.\033[m')
                    except ValueError:
                        print('\033[31mERRO: por favor, digite uma das opções que foram apresentadas.\033[m')

            while True:
                try:
                    dia = int(input('\033[32mInforme o dia do compromisso: \033[m'))

                    if dia >= 1 and dia <= ultimo_dia[mes_adiciona]:
                        break
                    else:
                        raise ValueError
                            
                except KeyboardInterrupt:
                    print('\033[31m Erro: o usuário preferiu não informar um compromisso.\033[m')
                except ValueError:
                    print('\033[31mERRO: por favor, digite uma opção com o número inteiro que esteja presente no calendário.\033[m')

            while True:
                try:
                    horario = input('\033[32mInforme a hora desse compromisso \033[33m(hh:mm)\033[m: \033[m')
                    if len(horario) == 5 and horario[2] == ':':
                        hora = int(horario[:2])
                        minuto = int(horario[3:])
                    else:
                        raise ValueError

                    if (hora >= 0 and hora <= 23) and (minuto >= 0 and minuto <= 59):  
                        break
                    else:
                        raise ValueError

                except KeyboardInterrupt:
                    print('\033[31m Erro: o usuário preferiu não informar um compromisso.\033[m')        
                except ValueError:
                    print('\033[31mERRO: por favor, digite o formato de hora corretamente (hora:minuto).\033[m')
                        

            try:
                compromisso = input('\033[32mInforme o compromisso: \033[m')

            except KeyboardInterrupt:
                print('\033[31m Erro: o usuário preferiu não informar um compromisso.\033[m')

            try:
                arquivo.write(f'{mes_adiciona:02}-{dia:02}-{hora:02}{minuto:02}-{compromisso}\n')

            except (KeyboardInterrupt, UnboundLocalError):
                print('\033[31m Erro: houve algum problema na hora de salvar seu arquivo.\033[m')

            while True:
                try:
                    opcao_compromisso = input('Deseja inserir mais um compromisso? (s/n): ')
                
                    if opcao_compromisso == 's' or opcao_compromisso == 'n':
                        break
                    else:
                        raise ValueError

                except (ValueError, TypeError):
                    print('\033[31mERRO: por favor, digite uma opção válida, "s" ou "n".\033[m')
                
                except (KeyboardInterrupt):
                    print('\033[31m Erro: o usuário preferiu não informar uma opção.\033[m')

##### Função para fazer a consulta dos compromissos. #####
def consulta():
    print(cabecalho('Seus compromissos'))

    lista_compromisso = []
    lista_indice = []
    hora = ''
    indice = 1

    
    with open('dadosagenda.txt', 'r') as arquivo:
        for compromissos in arquivo:
            lista_compromisso.append(compromissos.split('-'))

    
    lista_ordenada = sorted(lista_compromisso)

    if len(lista_compromisso) == 0:
            print('\033[31mERRO: não exite nenhum compromisso na sua agenda.\033[m')

    else:       
        for i in range(len(lista_compromisso)):
            lista_indice.append(indice)
            hora = lista_ordenada[i][2]
            print(f'({indice}) {lista_ordenada[i][1]}/{lista_ordenada[i][0]} - {hora[:2]}:{hora[2:]} - {lista_ordenada[i][3]}')
            indice += 1
  
    return lista_indice, lista_ordenada

##### Funçao para apagar um ou mais compromissos. #####
def remove():
    print(cabecalho('Apaguando seus compromissos'))
    listas = consulta()
    compromissos = listas[1]
    indices = listas[0]
    opcao = ''
    
    while opcao != 'n':
        if len(compromissos) == 0:
            print('\033[31mERRO: não exite nenhum compromisso na sua agenda.\033[m')
            break
        else:
            while True:
                try:
                    resposta = int(input('Digite a opção do compromisso que deseja apagar: '))
                    if resposta in indices:
                        compromissos.pop((resposta-1))
                        indices.pop((len(indices)-1))
                        break
                    else:
                        raise ValueError
                
                except (ValueError, TypeError):
                    print('\033[31mERRO: por favor, digite uma das opções que foram apresentadas.\033[m')
                except KeyboardInterrupt:
                    print('\033[31m Erro: o usuário preferiu não informar uma opção.\033[m')

            with open('dadosagenda.txt', 'w') as arquivo:
                for i in range(len(compromissos)):
                        arquivo.write(f'{compromissos[i][0]}-{compromissos[i][1]}-{compromissos[i][2]}-{compromissos[i][3]}')
                    
            arquivo.close() 

            while True:
                try:
                    opcao = input('Deseja apagar mais um compromisso? (s/n): ')
                
                    if opcao == 's':
                        consulta()
                        break
                    elif opcao == 'n':
                        break
                    else:
                        raise ValueError

                except (ValueError, TypeError):
                    print('\033[31mERRO: por favor, digite uma opção válida, "s" ou "n".\033[m')
                
                except (KeyboardInterrupt):
                    print('\033[31m Erro: o usuário preferiu não informar uma opção.\033[m')
      
    return compromissos

##### Função para alterar um compromisso #####
def altera():
    print(cabecalho('Alterando seus compromissos'))
    listas = consulta()
    compromissos = listas[1]
    indices = listas[0]
    opcao = ''
    ultimo_dia = calendar.mdays

    while opcao != 'n':
        if len(compromissos) == 0:
            print('\033[31mERRO: não exite nenhum compromisso na sua agenda.\033[m')
            break
        else:
            while True:
                try:
                    alteracao = int(input('Informe a opção que corresponde com o compromisso que deseja alterar: '))
                    if alteracao in indices:
                        break
                    else:
                        raise ValueError

                except (ValueError, TypeError):
                    print('\033[31mERRO: por favor, digite uma das opções que foram apresentadas.\033[m')
                except KeyboardInterrupt:
                    print('\033[31m Erro: o usuário preferiu não informar uma opção.\033[m')


            resposta = menu(['Alterar hora', 'Alterar data', 'Alterar compromisso'])

            if resposta == 1: # Alterando só a hora
                while True:
                    try:
                        nova_hora = input('Informe o novo horário (hh:mm): ')
                        if len(nova_hora) == 5 and nova_hora[2] == ':':
                            hora = int(nova_hora[:2])
                            minuto = int(nova_hora[3:])
                        else:
                            raise ValueError

                        if (hora >= 0 and hora <= 23) and (minuto >= 0 or minuto <= 59):
                            compromissos[alteracao-1].pop(2)
                            compromissos[alteracao-1].insert(2, f'{hora:02}{minuto:02}') 

                            break
                        else:
                            raise ValueError

                    except KeyboardInterrupt:
                        print('\033[31m Erro: o usuário preferiu não informar um compromisso.\033[m')        
                    except ValueError:
                        print('\033[31mERRO: por favor, digite o formato de hora corretamente (hora:minuto).\033[m')
                    
            
                
            if resposta == 2: # Alterando só a data
                while True:
                    try:
                        nova_data = input('Informe a nova data: ')
                        if len(nova_data) == 5 and nova_data[2] == '/':
                            dia = int(nova_data[:2])
                            mes = int(nova_data[3:])
                        
                        else:
                            raise ValueError

                        if (dia >= 1 and dia <= ultimo_dia[mes]) and (mes >= 1 and mes <= 12):
                            compromissos[alteracao-1].pop(0)
                            compromissos[alteracao-1].insert(0, f'{mes:02}')
                            compromissos[alteracao-1].pop(1)
                            compromissos[alteracao-1].insert(1, f'{dia:02}')

                            break
                        else:
                            raise ValueError
                    except KeyboardInterrupt:
                        print('\033[31m Erro: o usuário preferiu não informar um compromisso.\033[m')
                    except ValueError:
                        print('\033[31mERRO: data inválida.\033[m')

        
            if resposta == 3: # Alterando só o compromisso
                try:
                    novo_compromisso = input('Digite o novo compromisso: ')
                    compromissos[alteracao-1].pop(3)
                    compromissos[alteracao-1].insert(3, f'{novo_compromisso}\n')
        
                except KeyboardInterrupt:
                    print('\033[31m Erro: o usuário preferiu não informar um compromisso.\033[m')

        with open('dadosagenda.txt', 'w') as arquivo:
            for i in range(len(compromissos)):
                arquivo.write(f'{compromissos[i][0]}-{compromissos[i][1]}-{compromissos[i][2]}-{compromissos[i][3]}')
        arquivo.close()

        while True:
            try:
                opcao = input('Deseja alterar mais um compromisso? (s/n): ')
            
                if opcao == 's':
                    consulta()
                    break
                elif opcao == 'n':
                    break
                else:
                    raise ValueError

            except (ValueError, TypeError):
                print('\033[31mERRO: por favor, digite uma opção válida, "s" ou "n".\033[m')
            
            except (KeyboardInterrupt):
                print('\033[31m Erro: o usuário preferiu não informar uma opção.\033[m')
      
    return compromissos