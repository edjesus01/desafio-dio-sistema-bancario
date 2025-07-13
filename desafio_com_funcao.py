# Função para mostrar o menu e ler a opção do usuário
def menu_principal():
    menu = """
  --- MENU ---
[d] Depositar
[s] Sacar
[e] Extrato
[u] Criar Usuário
[c] Criar Conta
[l] Listar Contas
[q] Sair
=> """
    return input(menu).lower()

# Função para realizar depósitos
def depositar(saldo, extrato, /):
    valor = float(input("Informe o valor do depósito: "))

    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("Depósito realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato

# Função para realizar saques
def sacar(*, saldo, extrato, limite_saque, numero_saques, LIMITE_SAQUES_DIA):
    valor = float(input("Informe o valor do saque: "))

    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite_saque
    excedeu_saques = numero_saques >= LIMITE_SAQUES_DIA

    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
    elif excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print(f"Operação falhou! O valor do saque excede o limite por saque de R$ {limite_saque:.2f}.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    else:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso!")

    return saldo, extrato, numero_saques

# Função para exibir o extrato da conta
def exibir_extrato(saldo, / , *, extrato):
    print("\n================ EXTRATO ================")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        print(extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

# Função para buscar um usuário pelo CPF
def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

# Função para criar um novo usuário
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")

    if filtrar_usuario(cpf, usuarios):
        print("Já existe um usuário com esse CPF.")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, número - bairro - cidade/sigla estado): ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })
    print("Usuário criado com sucesso!")

# Função para criar uma nova conta associada a um usuário
def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input("Informe o CPF do titular da conta: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("Usuário não encontrado. Crie o usuário primeiro.")
        return

    conta = {
        "agencia": agencia,
        "numero": numero_conta,
        "usuario": usuario
    }
    contas.append(conta)
    print(f"Conta criada com sucesso! Agência: {agencia} | Conta: {numero_conta}")

# Função para listar todas as contas criadas
def listar_contas(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
        return

    print("\n========= CONTAS CADASTRADAS =========")
    for conta in contas:
        usuario = conta["usuario"]
        print(f"Agência: {conta['agencia']}, Conta: {conta['numero']}, Titular: {usuario['nome']}")
    print("=======================================")

# Função principal que controla o fluxo do programa
def main():
    saldo = 0
    extrato = ""
    limite_operacao = 300         # Limite por saque
    numero_saques = 0
    LIMITE_SAQUES_DIA = 3         # Limite de saques por dia

    usuarios = []                 # Lista de usuários (cada um é um dicionário)
    contas = []                   # Lista de contas
    AGENCIA = "0001"
    numero_conta = 1

    while True:
        opcao = menu_principal()

        if opcao == "d":
            saldo, extrato = depositar(saldo, extrato)

        elif opcao == "s":
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                extrato=extrato,
                limite_saque=limite_operacao,
                numero_saques=numero_saques,
                LIMITE_SAQUES_DIA=LIMITE_SAQUES_DIA
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "u":
            criar_usuario(usuarios)

        elif opcao == "c":
            criar_conta(AGENCIA, numero_conta, usuarios, contas)
            numero_conta += 1

        elif opcao == "l":
            listar_contas(contas)

        elif opcao == "q":
            print("Obrigado por usar o sistema bancário. Até logo!")
            break

        else:
            print("Operação inválida, por favor selecione novamente.")

# Ponto de entrada
if __name__ == "__main__":
    main()
