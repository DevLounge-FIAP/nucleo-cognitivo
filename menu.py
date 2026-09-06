import getpass
from datetime import datetime

from codigo_fonte import (
    cadastrar_registro,
    ler_registro,
    limpar_registros,
    validar_regras_logicas,
    exibir_status_colonia,
    cadastrar_novo_alerta_json,
    analisar_alerta_operacional,
)
from ia_generativa import (
    exibir_prompt_estruturado,
    simulador_resposta_ia,
    listar_topicos_disponiveis,
)


def menu():
    while True:
        print("\n=== NÚCLEO COGNITIVO DA AURORA SIGER (NCAS) ===")
        print("1. Cadastrar registro da colônia")
        print("2. Consultar registros salvos")
        print("3. Executar validação lógica")
        print("4. Ver palavras-chave que a IA reconhece")
        print("5. Exibir prompt estruturado")
        print("6. Simular resposta do assistente IA")
        print("7. Visualizar status da colônia (JSON)")
        print("8. Cadastrar novo alerta (JSON)")
        print("9. Analisar alerta operacional (JSON + Booleana + IA)")
        print("10. Limpar registros")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            mensagem = input("Digite o registro: ")
            data_hora = datetime.now().strftime("%d/%m %H:%M")
            usuario = getpass.getuser()
            linha_formatada = f"[Data e Hora: {data_hora} Usuário: {usuario}]: {mensagem}"

            if cadastrar_registro(linha_formatada):
                print("Registro salvo com sucesso.")
            else:
                print("Falha ao salvar o registro. Verifique os logs do sistema.")

        elif opcao == "2":
            registros = ler_registro()
            if not registros:
                print("Nenhum registro encontrado.")
            else:
                for indice, registro in enumerate(registros, start=1):
                    print(f"Registro {indice}: {registro}")

        elif opcao == "3":
            validar_regras_logicas()

        elif opcao == "4":
            listar_topicos_disponiveis()

        elif opcao == "5":
            exibir_prompt_estruturado()

        elif opcao == "6":
            simulador_resposta_ia()

        elif opcao == "7":
            exibir_status_colonia()

        elif opcao == "8":
            cadastrar_novo_alerta_json()

        elif opcao == "9":
            analisar_alerta_operacional()

        elif opcao == "10":
            if limpar_registros():
                print("Registros limpos com sucesso.")
            else:
                print("Erro ao limpar registros. Verifique os logs do sistema.")

        elif opcao == "0":
            print("Encerrando o sistema...")
            break

        else:
            print("Opção inválida, tente novamente.")


if __name__ == "__main__":
    menu()