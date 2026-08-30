import getpass
from datetime import datetime

from codigo_fonte import (
    cadastrar_registro,
    exibir_prompt_estruturado,
    ler_registro,
    simulador_resposta_ia,
    validar_regras_logicas,
)


def menu():
    while True:
        print("\n=== NÚCLEO COGNITIVO DA AURORA SIGER (NCAS) ===")
        print("1. Cadastrar registro da colônia")
        print("2. Consultar registros salvos")
        print("3. Executar validação lógica")
        print("4. Exibir prompt estruturado")
        print("5. Simular resposta do assistente IA")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
           mensagem = input("Digite o registro: ")
           data_hora = datetime.now().strftime("%d/%m %H:%M")
           usuario = getpass.getuser()
           linha_formatada = f"[Data e Hora: {data_hora} Usuário: {usuario}]: {mensagem}"
           cadastrar_registro(linha_formatada)

        elif opcao == "2":
            conteudo = ler_registro()
            if conteudo.strip() == "":
                 print("Nenhum registro encontrado.")
            else:
                registros = conteudo.strip().split("\n")
                for indice, registro in enumerate(registros, start=1):
                    print(f"Registro {indice} {registro}")

        elif opcao == "3":
            validar_regras_logicas()

        elif opcao == "4":
            exibir_prompt_estruturado()

        elif opcao == "5":
            simulador_resposta_ia()

        
        #elif opcao == "6":
        #    limpar_registro()
            

        elif opcao == "0":
            print("Encerrando o sistema...")
            break

        else:
            print("Opção inválida, tente novamente.")


if __name__ == "__main__":
    menu()