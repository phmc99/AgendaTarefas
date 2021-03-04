import calendar
from datetime import date

##### Funções para a parte visual do menu. #####
def linha(tam = 42):
    return '-'*tam

def cabecalho(texto):
    print(linha())
    print(texto.center(42))
    return f'{linha()}'

def menu(texto): 
    print(cabecalho('Menu'))
    n_opcao = 1
    
    for item in texto:
        print(f'({n_opcao}) {item}')
        n_opcao += 1

    print(f'{linha()}')
    
    opcao_escolha = escolha('Digite sua opção: ')
    return opcao_escolha

##### Função para capturar a opção do usuário. #####
def escolha(mensagem):
    while True:
        try:
            numero_opcao = int(input(mensagem))
        except ValueError:
            print('ERRO: por favor, digite uma opção com o número inteiro válido.')
        else:
            return numero_opcao

###### Função para mostrar calendario. #####
def mostra_calendario(ano, mes):
    calendar.setfirstweekday(6)
    matriz_calendario = calendar.monthcalendar(ano, mes)
    
    print('\n', calendar.month(ano, mes))
        
    return matriz_calendario

##### Funções para adicionar o compromisso. #####
def consulta_mes():
    meses_adicionados = []
    dicio_meses = {
        1:'Janeiro', 2:'Fevereiro', 3:'Março', 4:'Abril', 5:'Maio', 6:'Junho', 7:'Julho', 
        8:'Agosto', 9:'Setembro', 10:'Outubro', 11:'Novembro', 12:'Dezembro'
    }

    with open('meses.txt', 'r') as arquivo:
        for mes in arquivo:
            meses_adicionados.append(int(mes.strip('\n')))
        arquivo.close()

    return sorted(meses_adicionados), dicio_meses

def adiciona_mes():
    meses = consulta_mes()
    meses_ordenados = meses[0]
    dicio_meses = meses[1]

    for mes in meses_ordenados:
        print(f'({mes}) {dicio_meses[mes]}')
    
    try:
        mes = int(input('Informe o mês que deseja adicionar um compromisso: '))
        if mes in meses_ordenados:
            print('ERRO: esse mês já foi adicionado.')
        elif mes not in meses_ordenados and mes >= 1 and mes <= 12:
            meses_ordenados.append(mes)            
            print(cabecalho(f'Mês {dicio_meses[mes]} foi adicionado com sucesso!'.center(42)))
        else:
            raise ValueError

    except (ValueError, TypeError):
        print('ERRO: por favor, digite uma opção com o número inteiro de 1 a 12.')

    with open('meses.txt', 'w') as arquivo:
        for mes in meses_ordenados:
            arquivo.write(f'{mes}\n')
        arquivo.close()

    return mes

def escolhe_mes():
    meses = consulta_mes()
    meses_ordenados = meses[0] 
    dicio_meses = meses[1]

    print(cabecalho('Meses registrados'))

    if len(meses_ordenados) == 0:
        print('ERRO: não exite nenhum mês registrado.')
    else:
        for mes in meses_ordenados:
            print(f'({mes}) {dicio_meses[mes]}')

    while True:
        mes_escolhido = int(input('Digite a opção correspondente ao mês: '))

        if mes_escolhido not in meses_ordenados:
            print('ERRO: escolha entre uma das opções.')
            break
        else: 
            return mes_escolhido
            
def remove_mes():
    meses = consulta_mes()
    meses_ordenados = meses[0]

    if len(meses_ordenados) == 0:
        print('ERRO: não exite nenhum mês registrado.')
    else:
        mes_remover = escolhe_mes()
        remove_tudo(mes_remover)
        meses_ordenados.remove(mes_remover)

        with open('meses.txt', 'w') as arquivo:
            for mes in meses_ordenados:
                arquivo.write(f'{mes}\n')
            arquivo.close()

        print(cabecalho('Mês removido com sucesso!'))

def adicionar(mes):
    print(cabecalho('Adicione seus compromissos.'))

    opcao_compromisso = ''
    ano_atual = date.today().year
    ultimo_dia = calendar.mdays
    meses = consulta_mes()
    meses_ordenados = meses[0]

    with open('dadosagenda.txt', 'a') as arquivo:
        while opcao_compromisso != 'n':

            if len(meses_ordenados) == 1:
                mes_adiciona = meses_ordenados[0]
                mostra_calendario(ano_atual, mes_adiciona)
            else:
                mes_adiciona = mes
                mostra_calendario(ano_atual, mes_adiciona)

            while True:
                try:
                    dia = int(input('Informe o dia do compromisso: '))
                    if dia >= 1 and dia <= ultimo_dia[mes_adiciona]:
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print('ERRO: por favor, digite uma opção com o número inteiro que esteja presente no calendário.')

            while True:
                try:
                    horario = input('Informe a hora desse compromisso (hh:mm): ')
                    if len(horario) == 5 and horario[2] == ':':
                        hora = int(horario[:2])
                        minuto = int(horario[3:])
                    else:
                        raise ValueError

                    if (hora >= 0 and hora <= 23) and (minuto >= 0 and minuto <= 59):  
                        break
                    else:
                        raise ValueError
    
                except ValueError:
                    print('ERRO: por favor, digite o formato de hora corretamente (hora:minuto).')

            compromisso = input('Informe o compromisso: ')

            try:
                arquivo.write(f'{mes_adiciona:02}-{dia:02}-{hora:02}{minuto:02}-{compromisso}\n')
            except UnboundLocalError:
                print('ERRO: houve algum problema na hora de salvar seu arquivo.')

            print(cabecalho('Compromisso adicionado com sucesso!'))
            

            while True:
                try:
                    opcao_compromisso = input('Deseja inserir mais um compromisso? (s/n): ')
                
                    if opcao_compromisso == 's' or opcao_compromisso == 'n':
                        break
                    else:
                        raise ValueError

                except (ValueError, TypeError):
                    print('ERRO: por favor, digite uma opção válida, "s" ou "n".')

        arquivo.close()

##### Função para fazer a consulta dos compromissos. #####
def consulta(mes):
    print(cabecalho('Seus compromissos'))

    todos_compromissos = []
    compromissos_mes = []
    lista_indice = []
    hora = ''
    indice = 1

    
    with open('dadosagenda.txt', 'r') as arquivo:
        for compromissos in arquivo:
            todos_compromissos.append(compromissos.split('-'))

    for x in range(len(todos_compromissos)):
        if f'{mes:02}' == todos_compromissos[x][0]:
            compromissos_mes.append(todos_compromissos[x])

    
    lista_ordenada = sorted(compromissos_mes)

    if len(compromissos_mes) == 0:
        print('ERRO: não existe nenhum compromisso.')

    else:       
        for i in range(len(compromissos_mes)):
            lista_indice.append(indice)
            hora = lista_ordenada[i][2]
            print(f'({indice}) {lista_ordenada[i][1]}/{lista_ordenada[i][0]} - {hora[:2]}:{hora[2:]} - {lista_ordenada[i][3]}')
            indice += 1

    return lista_indice, lista_ordenada

##### Funçao para apagar um ou mais compromissos. #####
def remove(mes):
    print(cabecalho('Apagando seus compromissos'))
    listas = consulta(mes)
    compromissos = listas[1]
    indices = listas[0]
    opcao = ''

    with open('dadosagenda.txt', 'r') as arquivao:
        todos_compromissos = [x.split('-') for x in arquivao]
        arquivao.close()    

    while opcao != 'n':
        if len(compromissos) == 0:
            break
        else:
            while True:
                try:
                    resposta = int(input('Digite a opção do compromisso que deseja apagar: '))
                        
                    if resposta in indices:
                        indices.pop((len(indices)-1))
                        
                        break
                    else:
                        raise ValueError
                
                except (ValueError, TypeError):
                    print('ERRO: por favor, digite uma das opções que foram apresentadas.')

            with open('dadosagenda.txt', 'w') as arquivo:
                for i in range(len(todos_compromissos)):
                    if compromissos[resposta-1] != todos_compromissos[i]:
                        arquivo.write(f'{todos_compromissos[i][0]}-{todos_compromissos[i][1]}-{todos_compromissos[i][2]}-{todos_compromissos[i][3]}')    
                compromissos.pop((resposta-1))
                arquivo.close()

            print(cabecalho('Compromisso removido com sucesso!'))

            while True:
                try:
                    opcao = input('Deseja apagar mais um compromisso? (s/n): ')
                
                    if opcao == 's':
                        consulta(mes)
                        break
                    elif opcao == 'n':
                        break
                    else:
                        raise ValueError

                except (ValueError, TypeError):
                    print('ERRO: por favor, digite uma opção válida, "s" ou "n".')
      
    return compromissos

def remove_tudo(mes):
    # Função para remover todos os compromissos de um mês.
    lista_compromisso = []

    with open('dadosagenda.txt', 'r') as arquivo:
        for compromissos in arquivo:
            lista_compromisso.append(compromissos.split('-'))
        arquivo.close()

    for i in range(len(lista_compromisso)-(len(lista_compromisso)//2)):
        if f'{mes:02}' == lista_compromisso[i][0]:
            lista_compromisso.remove(lista_compromisso[i])

    with open('dadosagenda.txt', 'w') as arquivo:
        for i in range(len(lista_compromisso)):
            arquivo.write(f'{lista_compromisso[i][0]}-{lista_compromisso[i][1]}-{lista_compromisso[i][2]}-{lista_compromisso[i][3]}')
        arquivo.close()

    return lista_compromisso

##### Função para alterar um compromisso #####
def altera(mes):
    print(cabecalho('Alterando seus compromissos'))
    listas = consulta(mes)
    compromissos = listas[1]
    indices = listas[0]
    opcao = ''
    ultimo_dia = calendar.mdays

    while opcao != 'n':
        if len(compromissos) == 0:
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
                    print('ERRO: por favor, digite uma das opções que foram apresentadas.')

            resposta = menu(['Alterar hora', 'Alterar data', 'Alterar compromisso', 'Cancelar'])

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

                    except ValueError:
                        print('ERRO: por favor, digite o formato de hora corretamente (hora:minuto).')
                    
            
                
            elif resposta == 2: # Alterando só a data
                while True:
                    try:
                        nova_data = input('Informe a nova data (dia/mês): ')
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
                    except ValueError:
                        print('ERRO: data inválida.')

        
            elif resposta == 3: # Alterando só o compromisso
                novo_compromisso = input('Digite o novo compromisso: ')
                compromissos[alteracao-1].pop(3)
                compromissos[alteracao-1].insert(3, f'{novo_compromisso}\n')
                    

            elif resposta == 4: # Sair do menu
                break

        with open('dadosagenda.txt', 'w') as arquivo:
            for i in range(len(compromissos)):
                arquivo.write(f'{compromissos[i][0]}-{compromissos[i][1]}-{compromissos[i][2]}-{compromissos[i][3]}')
        arquivo.close()

        print(cabecalho('Alteração feita com sucesso!'))

        while True:
            try:
                opcao = input('Deseja alterar mais um compromisso? (s/n): ')
            
                if opcao == 's':
                    consulta(escolhe_mes())
                    break
                elif opcao == 'n':
                    break
                else:
                    raise ValueError

            except (ValueError, TypeError):
                print('ERRO: por favor, digite uma opção válida, "s" ou "n".')
      
    return compromissos
