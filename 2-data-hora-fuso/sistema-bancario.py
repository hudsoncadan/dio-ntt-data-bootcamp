from datetime import datetime, timezone
import functools

historico_conta = []
saldo_conta = 0

OPERACAO_DEPOSITO = 'Depósito'
OPERACAO_SAQUE = 'Saque'

ACAO_DEPOSITAR = 'd'
ACAO_SACAR = 's'
ACAO_EXTRATO = 'e'
ACAO_SAIR = 'q'

MENU = f"""
Escolha uma opção para prosseguir:

{ACAO_DEPOSITAR} - Depositar
{ACAO_SACAR} - Sacar
{ACAO_EXTRATO} - Extrato
{ACAO_SAIR} - Sair

=> """


def criar_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f'{datetime.now(timezone.utc)}: {func.__name__.upper()}')
        resultado = func(*args, **kwargs)
        return resultado
    
    return wrapper


def limitar_transacao(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global historico_conta
        data_atual = datetime.now()
        qtd_operacoes_diario = sum(1 for historico in historico_conta if historico['data_operacao'].strftime("%d/%m/%Y") == data_atual.strftime("%d/%m/%Y"))

        LIMITE_QTD_OPERACAO_DIARIO = 10
        MSG_LIMITE_QTD_OEPRACAO_DIARIO  = f'Limite de {LIMITE_QTD_OPERACAO_DIARIO} operações excedido. Por gentileza, volte amanhã!'
   
        if (qtd_operacoes_diario >= LIMITE_QTD_OPERACAO_DIARIO):
            print(MSG_LIMITE_QTD_OEPRACAO_DIARIO)
            pular_linha()
            return
        else:
            func(*args, **kwargs)

    return wrapper


@criar_log
@limitar_transacao
def depositar():
    global saldo_conta 
    
    MSG_VALOR_INVALIDO = 'Informe um valor superior a R$ 0,00.'

    valor_deposito = input('Qual valor deseja depositar? ')
    pular_linha()

    if (valor_deposito.isnumeric() == False):
        print(MSG_VALOR_INVALIDO)
        pular_linha()
        return

    valor_deposito = int(valor_deposito)

    if (valor_deposito <= 0):
        print(MSG_VALOR_INVALIDO)
        pular_linha()
        return
    
    historico_conta.append({'tipo_operacao': OPERACAO_DEPOSITO, 'valor': valor_deposito, 'data_operacao': datetime.now()})
    saldo_conta += valor_deposito

    print('Depósito realizado com sucesso!')
    pular_linha()


@criar_log
@limitar_transacao
def sacar():
    global saldo_conta 
    
    MSG_VALOR_INVALIDO = 'Informe um valor superior a R$ 0,00.'

    LIMITE_VALOR_POR_SAQUE = 500
    MSG_LIMITE_VALOR_POR_SAQUE  = f'Limite de R$ {LIMITE_VALOR_POR_SAQUE:.2f} permitido por saque. Por gentileza, informe um valor abaixo do limite!'
   
    LIMITE_QTD_DIARIA_SAQUE = 3
    MSG_LIMITE_QTD_DIARIA_SAQUE  = f'Limite diário de {LIMITE_QTD_DIARIA_SAQUE} saques atingidos. Por gentileza, volte amanhã!'
    
    MSG_SALDO_INSUFICIENTE  = 'Saldo insuficiente. Por gentileza, informe um valor menor!'

    valor_saque = input('Qual valor deseja sacar? ')
    pular_linha()

    if (valor_saque.isnumeric() == False):
        print(MSG_VALOR_INVALIDO)
        pular_linha()
        return

    valor_saque = int(valor_saque)

    if (valor_saque > LIMITE_VALOR_POR_SAQUE):
        print(MSG_LIMITE_VALOR_POR_SAQUE)
        pular_linha()
        return
    
    data_atual = datetime.now()
    qtd_saques_realizados_diario = sum(1 for historico in historico_conta if historico['tipo_operacao'] == OPERACAO_SAQUE and historico['data_operacao'].strftime("%d/%m/%Y") == data_atual.strftime("%d/%m/%Y"))

    if (qtd_saques_realizados_diario >= LIMITE_QTD_DIARIA_SAQUE):
        print(MSG_LIMITE_QTD_DIARIA_SAQUE)
        pular_linha()
        return
    
    if (valor_saque > saldo_conta):
        print(MSG_SALDO_INSUFICIENTE)
        pular_linha()
        return
    
    historico_conta.append({'tipo_operacao': OPERACAO_SAQUE, 'valor': valor_saque, 'data_operacao': datetime.now()})
    saldo_conta -= valor_saque
   
    print('Saque realizado com sucesso!')
    pular_linha()


@criar_log
def exibir_extrato():
    print('Extrato:')
    pular_linha()

    for historico in historico_conta:
        print(f'Operação: {historico['tipo_operacao']}')
        print(f'Data: {historico['data_operacao'].strftime('%d/%m/%Y %H:%M:%S')}')
        print(f'Valor: R$ {historico['valor']:.2f}')
        pular_linha()

    print(f'Saldo atual da conta: {saldo_conta:.2f}')
    

def pular_linha():
    print('', end='\n')
    

while (True):
    acao_cliente = input(MENU).lower()
    pular_linha()

    if (acao_cliente == ACAO_DEPOSITAR):
        depositar()

    elif (acao_cliente == ACAO_SACAR):
        sacar()

    elif (acao_cliente == ACAO_EXTRATO):
        exibir_extrato()

    elif (acao_cliente == ACAO_SAIR):
        break

    else:
        print('Opção inválida. Por gentileza, tente novamente!')
