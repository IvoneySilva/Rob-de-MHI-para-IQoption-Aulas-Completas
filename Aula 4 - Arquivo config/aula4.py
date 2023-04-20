from iqoptionapi.stable_api import IQ_Option
import time
from configobj import ConfigObj
import json, sys


### CRIANDO ARQUIVO DE CONFIGURAÇÃO ####
config = ConfigObj('config.txt')
email = config['LOGIN']['email']
senha = config['LOGIN']['senha']
tipo = config['AJUSTES']['tipo']
valor_entrada = config['AJUSTES']['valor_entrada']



print('Iniciando Conexão com a IQOption')
API = IQ_Option(email,senha)

### Função para conectar na IQOPTION ###
check, reason = API.connect()
if check:
    print('\nConectado com sucesso')
else:
    if reason == '{"code":"invalid_credentials","message":"You entered the wrong credentials. Please ensure that your login/password is correct."}':
        print('\nEmail ou senha incorreta')
        sys.exit()
        
    else:
        print('\nHouve um problema na conexão')

        print(reason)
        sys.exit()

### Função para Selecionar demo ou real ###
while True:
    escolha = input('\nSelecione a conta em que deseja conectar: demo ou real  - ')
    if escolha == 'demo':
        conta = 'PRACTICE'
        print('Conta demo selecionada')
        break
    if escolha == 'real':
        conta = 'REAL'
        print('Conta real selecionada')
        break
    else:
        print('Escolha incorreta! Digite demo ou real')
        
API.change_balance(conta)

### Função abrir ordem e checar resultado ###
def compra(ativo,valor_entrada,direcao,exp,tipo):
    if tipo == 'digital':
        check, id = API.buy_digital_spot_v2(ativo,valor_entrada,direcao,exp)
    else:
        check, id = API.buy(valor_entrada,ativo,direcao,exp)


    if check:
        print('\n >> Ordem aberta \n>> Par:',ativo,'\n>> Timeframe:',exp,'\n>> Entrada de:',cifrao,valor_entrada)

        while True:
            time.sleep(0.1)
            status , resultado = API.check_win_digital_v2(id) if tipo == 'digital' else API.check_win_v4(id)

            if status:
                if resultado > 0:
                    print('\n >> Resultado: WIN \n >> Lucro:', round(resultado,2), '\n >> Par:', ativo)
                elif resultado == 0:
                    print('\n >> Resultado: EMPATE \n >> Lucro:', round(resultado,2), '\n >> Par:', ativo)
                else:
                    print('\n >> Resultado: LOSS \n >> Lucro:', round(resultado,2), '\n >> Par:', ativo)
                break

    else:
        print('erro na abertura da ordem,', id,ativo)
        


### DEFININCO INPUTS NO INICIO DO ROBÔ ###

ativo = input('\n >> Digite o ativo que você deseja operar: ').upper()
exp = input('\n >> Qual timeframe? ')
direcao = input('\n >> Entrada para call ou put? ')

perfil = json.loads(json.dumps(API.get_profile_ansyc()))
cifrao = str(perfil['currency_char'])
nome = str(perfil['name'])

valorconta = float(API.get_balance())

print('\n ######################################################################')
print('\n Olá, ',nome, '\nSeja bem vindo ao Robô do Canal do Lucas.')
print('\n Seu Saldo na conta ',escolha, 'é de', cifrao,valorconta)
print('\n Seu valor de entrada é de ',cifrao,valor_entrada)
print('\n ######################################################################\n\n')


### chamada da função de compra ###
compra(ativo,valor_entrada,direcao,exp,tipo)