import csv
import pandas as pd
from datetime import date


def cadastrar_paciente():
    """Realiza o cadastro do paciente caso não haja duplicidade de telefone, salvando em um arquivo .csv."""
    print("Informe o nome e o telefone do paciente.")
    nome = input("Nome: ")
    telefone = input("Telefone: ")

    with open("pacientes.csv", "a", newline="") as arquivo1:
        escritor = csv.writer(arquivo1)

        with open("pacientes.csv") as arquivo2:
            leitor = csv.DictReader(arquivo2, fieldnames=['nome', 'telefone'])
            verificador = True
            primeiro_acesso = False

            try:
                leitor.__next__()

                for linha in leitor:
                    if linha["telefone"] == telefone:
                        verificador = False
            except:
                # Exceção lançada quando o arquivo está vazio.
                escritor.writerow(["nome", "telefone"])
                escritor.writerow([nome, telefone])
                primeiro_acesso = True
                print("Primeiro acesso. Paciente cadastrado com sucesso.")

            if verificador and not primeiro_acesso:
                escritor.writerow([nome, telefone])
                print("Paciente cadastrado com sucesso.")
            if not verificador:
                print("Telefone já cadastrado.")


def verifica_dia_mes():
    """Verifica a validade do mês e do dia informados, retornando uma data formatada."""
    data_atual = date.today()
    try:
        mes = int(input("""Informe o número do mês:
1 - Janeiro
2 - Fevereiro
3 - Março
4 - Abril
5 - Maio
6 - Junho
7 - Julho
8 - Agosto
9 - Setembro
10 - Outubro
11 - Novembro
12 - Dezembro
Mês: """))
        if 0 < mes <= 12 and mes >= data_atual.month:
            dia = int(input("Dia: "))
            if mes != data_atual.month or (mes == data_atual.month and dia > data_atual.day):
                if mes in [1, 3, 5, 7, 8, 10, 12]:
                    if 0 < dia <= 31:
                        data = f"{dia}/{mes}/{data_atual.year}"
                elif mes in [4, 6, 9, 11]:
                    if 0 < dia <= 30:
                        data = f"{dia}/{mes}/{data_atual.year}"
                elif mes == 2:
                    if 0 < dia <= 29:
                        data = f"{dia}/{mes}/{data_atual.year}"
    except:
        print("Entrada inválida.")
    return data


def verifica_hora():
    """Verifica a validade da hora informada, retornando uma hora formatada."""
    try:
        hora = int(input("Hora: "))
        if 7 <= hora <= 17:
            hora_consulta = f"{hora}:00"
    except:
        print("Entrada inválida.")
    return hora_consulta


def verifica_disponibilidade(data, hora, numero, df, especialidade):
    """Verifica se a consulta está disponível, retornando true ou false conforme o caso."""
    with open("lista_de_agendamentos.csv", "a", newline="") as arquivo1:
        escritor = csv.writer(arquivo1)

        with open("lista_de_agendamentos.csv") as arquivo2:
            leitor = csv.DictReader(arquivo2, fieldnames=['nome', 'telefone', 'data', 'hora'])
            verificador = True
            primeiro_acesso = False
            agendamento = True

            try:
                leitor.__next__()

                for linha in leitor:
                    if linha["data"] == data and linha["hora"] == hora:
                        verificador = False
                        agendamento = False
            except:
                # Exceção lançada quando o arquivo está vazio.
                escritor.writerow(["nome", "telefone", "data", "hora", "especialidade"])
                escritor.writerow([df.iloc[numero-1]["nome"], df.iloc[numero-1]["telefone"], data, hora, especialidade])
                primeiro_acesso = True

            if verificador and not primeiro_acesso:
                escritor.writerow([df.iloc[numero-1]["nome"], df.iloc[numero-1]["telefone"], data, hora, especialidade])
    return agendamento


def exibe_dataframe(arquivo):
    """Retorna um dataframe a partir do arquivo .csv fornecido."""
    return pd.read_csv(arquivo, sep=",", encoding='latin-1').rename(index=lambda x: x + 1)


def marcar_consulta():
    """Exibe uma lista dos pacientes cadastrados. Chama os métodos para agendamento de consulta."""
    print("Pacientes cadastrados:")
    try:
        df = exibe_dataframe("pacientes.csv")
        print(df)
        try:
            numero = int(input("\nInforme o número do paciente: "))
            if 0 < numero <= len(df):
                print("Informe a data (2024), a hora (das 7h às 17h) e a especialidade desejados.")
                data = verifica_dia_mes()
                if data is not None:
                    hora = verifica_hora()
                    if hora is not None:
                        especialidade = input("Especialidade: ")
                        if verifica_disponibilidade(data, hora, numero, df, especialidade):
                            print(f"""
Paciente: {df.iloc[numero-1]["nome"]}
Telefone: {df.iloc[numero-1]["telefone"]}
Especialidade: {especialidade}
Data: {data}
Hora: {hora}

Consulta marcada com sucesso.
""")
                        else:
                            print("Data e hora indisponíveis para agendamento.")
            else:
                print("Paciente não encontrado.")
        except:
            print("Entrada inválida.")
    except:
        print("Nenhum paciente cadastrado até o momento.")


def le_linha(numero, arquivo):
    """Retorna uma string com linha do arquivo que se busca."""
    with open(arquivo, mode="r", encoding="latin-1") as novo_arquivo:
        for i, linha in enumerate(novo_arquivo, start=1):
            if i == numero:
                return linha


def realizar_cancelamento(numero, arquivo):
    """Realiza o cancelamento da consulta através de modificação no arquivo fornecido."""
    linha_a_excluir = le_linha(numero+1, arquivo)
    with open(arquivo, "r") as arquivo1:
        linhas = arquivo1.readlines()

        with open(arquivo, "w") as arquivo2:
            for linha in linhas:
                if linha != linha_a_excluir:
                    arquivo2.write(linha)
            print("Agendamento cancelado com sucesso.")
            

def cancelar_consulta():
    """"Exibe uma lista dos agendamentos existentes. Chama os métodos para cancelamento de consulta."""
    print("Agendamentos existentes:")
    try:
        df = exibe_dataframe("lista_de_agendamentos.csv")
        if len(df.index) > 0:
            print(df)
            try:
                numero = int(input("\nInforme o número do agendamento: "))
                if 0 < numero <= len(df):
                    print(f"""Agendamento encontrado:
Paciente: {df.iloc[numero-1]["nome"]}
Telefone: {df.iloc[numero-1]["telefone"]}
Especialidade: {df.iloc[numero-1]["especialidade"]}
Data: {df.iloc[numero-1]["data"]}
Hora: {df.iloc[numero-1]["hora"]}
""")
                    cancelamento = input("Deseja cancelar o agendamento? (s/n): ").lower()
                    if cancelamento == "s":
                        realizar_cancelamento(numero, "lista_de_agendamentos.csv")
                    else:
                        print("Cancelamento não realizado.")
                else:
                    print("Agendamento não encontrado.")
            except:
                print("Entrada inválida.")
        else:
            print("Nenhum agendamento realizado até o momento.")
    except:
        print("Nenhum agendamento realizado até o momento.")


def menu():
    """Apresenta o menu de opções disponíveis."""

    while True:
        print("--------------------------------\nMenu:")
        print("1. Cadastrar um paciente")
        print("2. Marcações de consultas")
        print("3. Cancelamento de consultas")
        print("4. SAIR")

        opcao = input("Opção desejada: ")
        print("--------------------------------\n")

        if opcao == "1":
            print("1. Cadastrar um paciente\n")
            cadastrar_paciente()

        elif opcao == "2":
            print("2. Marcações de consultas\n")
            marcar_consulta()

        elif opcao == "3":
            print("3. Cancelamento de consultas\n")
            cancelar_consulta()

        elif opcao == "4":
            print("4. Saindo do sistema...\n")
            break

        else:
            print("Opção inválida...\n")


print("Bem vindo ao sistema de consultas!\nEscolha uma das opções abaixo.")
menu()
