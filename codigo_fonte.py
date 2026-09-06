"""
================================================================================
PROJETO: Núcleo Cognitivo da Aurora Siger (NCAS)
ARQUIVO: codigo_fonte.py (arquivo principal - arquivos, JSON, regras e menu)
AUTORES: Aelton Soares de Menezes, Victor Mantovani, Bruno Santos, Maria Eduarda Fernandes, Michelly Santos
================================================================================
"""

import json
import getpass
from datetime import datetime

from regras_logicas import gerar_alerta, bloquear_operacao
from validacao_regras import executar_validacao_completa
import ia_generativa


# ==============================================================================
# CONFIGURAÇÕES E ARQUIVOS PERSISTENTES
# ==============================================================================
ARQUIVO_REGISTROS = 'registros_colonia.txt'
ARQUIVO_DADOS = 'dados_colonia.json'

SCHEMA_BASE_JSON = {
    "colonia": "Aurora Siger",
    "localizacao": "Planeta Marte - Cratera Gale",
    "status_modulos": {
        "suporte_vital": {
            "estado": "ativo",
            "nivel_oxigenio_percentual": 98.5,
            "pressao_kpa": 101.3,
            "temperatura_interna_celsius": 21.8
        },
        "energia": {
            "estado": "ativo",
            "reserva_bateria_percentual": 87.4,
            "consumo_kw": 465,
            "fonte_primaria": "Reator Solar-Termico"
        },
        "comunicacao": {
            "estado": "ativo",
            "latencia_ms": 45,
            "antena_deep_space": "sincronizada"
        },
        "estufa_hidroponica": {
            "estado": "ativo",
            "umidade_percentual": 68.0,
            "nivel_nutrientes": "otimo"
        }
    },
    "alertas_ativos": [
        {
            "id_alerta": 1,
            "modulo": "suporte_vital",
            "criticidade": "CRITICA",
            "falha_critica": True,
            "consumo_elevado": False,
            "falha_seguranca": False,
            "inconsistencia_dados": False,
            "mensagem": "Queda rapida no suprimento de oxigenio do setor B",
            "timestamp": "2026-09-05T08:14:22"
        }
    ]
}


# ==============================================================================
# MANIPULAÇÃO DE ARQUIVOS TEXTO (.TXT)
# ==============================================================================

def cadastrar_registro(mensagem: str) -> bool:
    """Grava um novo registro no arquivo texto, sem sobrescrever o conteúdo
    já existente (modo append: 'a')."""
    try:
        with open(ARQUIVO_REGISTROS, 'a', encoding='utf-8') as arquivo:
            arquivo.write(mensagem + '\n')
        return True
    except OSError as erro:
        print(f"[ERRO DE I/O] Não foi possível gravar o registro: {erro}")
        return False


def ler_registro() -> list[str]:
    """Lê todas as linhas do arquivo de registros. Cria o arquivo vazio se
    ele ainda não existir."""
    try:
        with open(ARQUIVO_REGISTROS, 'r', encoding='utf-8') as arquivo:
            return [linha.strip() for linha in arquivo.readlines() if linha.strip()]
    except FileNotFoundError:
        with open(ARQUIVO_REGISTROS, 'w', encoding='utf-8') as arquivo:
            pass
        return []
    except OSError as erro:
        print(f"[ERRO DE I/O] Falha ao ler registros: {erro}")
        return []


def limpar_registros() -> bool:
    """Esvazia o arquivo de registros abrindo-o em modo escrita ('w')."""
    try:
        with open(ARQUIVO_REGISTROS, 'w', encoding='utf-8') as arquivo:
            pass
        return True
    except OSError as erro:
        print(f"[ERRO DE I/O] Falha ao limpar registros: {erro}")
        return False


# ==============================================================================
# MANIPULAÇÃO DE DADOS ESTRUTURADOS JSON (.JSON)
# ==============================================================================

def ler_dados_colonia() -> dict:
    """Carrega o JSON da colônia. Se não existir ou estiver corrompido,
    recria com o schema base padrão."""
    try:
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        salvar_dados_colonia(SCHEMA_BASE_JSON)
        return SCHEMA_BASE_JSON


def salvar_dados_colonia(dados: dict) -> bool:
    """Serializa e persiste o dicionário no arquivo JSON."""
    try:
        with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, indent=2, ensure_ascii=False)
        return True
    except OSError as erro:
        print(f"[ERRO DE I/O] Falha ao persistir dados JSON: {erro}")
        return False


def exibir_status_colonia() -> None:
    """Mostra no terminal os módulos e alertas salvos no JSON."""
    dados = ler_dados_colonia()
    print("\n" + "=" * 60)
    print(f"STATUS DA COLÔNIA: {dados.get('colonia', 'Aurora Siger').upper()}")
    print(f"Localização: {dados.get('localizacao', 'Marte')}")
    print("=" * 60)

    print("\n--- MÓDULOS OPERACIONAIS ---")
    for nome, info in dados.get("status_modulos", {}).items():
        print(f"\n{nome.replace('_', ' ').title()}:")
        for chave, valor in info.items():
            if chave != "estado":
                print(f"  {chave.replace('_', ' ').title()}: {valor}")

    print("\n--- ALERTAS ATIVOS ---")
    alertas = dados.get("alertas_ativos", [])
    if not alertas:
        print("Nenhum alerta ativo no momento.")
    else:
        for alerta in alertas:
            print(f"\n[ID {alerta.get('id_alerta')}] {alerta.get('criticidade')} "
                  f"| Módulo: {alerta.get('modulo')} | {alerta.get('timestamp')}")
            print(f"  Mensagem: {alerta.get('mensagem')}")


def cadastrar_novo_alerta_json() -> bool:
    """Permite cadastrar um novo alerta estruturado no arquivo JSON,
    coletando as flags booleanas usadas depois pelas regras lógicas."""
    dados = ler_dados_colonia()
    alertas = dados.setdefault("alertas_ativos", [])

    print("\n--- CADASTRO DE NOVO ALERTA OPERACIONAL (JSON) ---")
    modulo = input("Nome do módulo (ex: suporte_vital, energia, comunicacao): ").strip().lower()
    mensagem = input("Descrição da ocorrência técnica: ").strip()
    falha_critica = input("É uma falha grave/crítica? (s/n): ").strip().lower() == 's'
    consumo_elevado = input("Houve consumo excessivo de energia? (s/n): ").strip().lower() == 's'
    falha_seguranca = input("Há indício de falha de segurança? (s/n): ").strip().lower() == 's'
    inconsistencia = input("Há inconsistência ou corrupção de dados? (s/n): ").strip().lower() == 's'

    critico = falha_critica or falha_seguranca or inconsistencia
    criticidade = "CRITICA" if critico else ("ATENCAO" if consumo_elevado else "INFO")

    novo_id = max([a.get("id_alerta", 0) for a in alertas], default=0) + 1
    alertas.append({
        "id_alerta": novo_id,
        "modulo": modulo,
        "criticidade": criticidade,
        "falha_critica": falha_critica,
        "consumo_elevado": consumo_elevado,
        "falha_seguranca": falha_seguranca,
        "inconsistencia_dados": inconsistencia,
        "mensagem": mensagem,
        "timestamp": datetime.now().isoformat()[:19]
    })

    if salvar_dados_colonia(dados):
        print(f"Alerta #{novo_id} salvo com sucesso em '{ARQUIVO_DADOS}'.")
        return True
    return False


# ==============================================================================
# VALIDAÇÃO DE REGRAS LÓGICAS (Etapa 4 — Maria Eduarda)
# ==============================================================================

def validar_regras_logicas() -> None:
    """Executa a validação formal das regras booleanas, incluindo a
    simplificação por Teorema de De Morgan (regras_logicas.py /
    validacao_regras.py)."""
    executar_validacao_completa()


# ==============================================================================
# FUNCIONALIDADE INTEGRADORA: JSON + REGRA BOOLEANA + IA GENERATIVA
# ==============================================================================

def analisar_alerta_operacional() -> None:
    """
    Funcionalidade integradora principal do NCAS:
    1. Carrega os alertas do arquivo JSON;
    2. Aplica as regras lógicas booleanas (De Morgan incluído);
    3. Gera um prompt estruturado e a resposta simulada da IA;
    4. Arquiva o resultado em historico_respostas.txt.
    """
    dados = ler_dados_colonia()
    alertas = dados.get("alertas_ativos", [])

    print("\n" + "=" * 60)
    print("ANÁLISE INTEGRADA DE ALERTA OPERACIONAL (JSON + BOOLEANA + IA)")
    print("=" * 60)

    if not alertas:
        print("Nenhum alerta registrado. Cadastre um alerta antes de analisar.")
        return

    print("Alertas disponíveis:")
    for indice, alerta in enumerate(alertas, start=1):
        print(f"  [{indice}] Módulo: {alerta.get('modulo')} | Ocorrência: {alerta.get('mensagem')}")

    escolha = input(f"\nSelecione o alerta (1 a {len(alertas)}): ").strip()
    try:
        alerta_selecionado = alertas[int(escolha) - 1]
    except (ValueError, IndexError):
        print("Seleção inválida. Operação cancelada.")
        return

    modulo = alerta_selecionado.get("modulo", "sistema")
    mensagem = alerta_selecionado.get("mensagem", "Sem descrição")
    falha_critica = alerta_selecionado.get("falha_critica", False)
    consumo_elevado = alerta_selecionado.get("consumo_elevado", False)
    falha_seguranca = alerta_selecionado.get("falha_seguranca", False)
    inconsistencia = alerta_selecionado.get("inconsistencia_dados", False)

    alerta_disparado = gerar_alerta(falha_critica, consumo_elevado)
    operacao_bloqueada = bloquear_operacao(falha_seguranca, inconsistencia)
    e_critico = bool(falha_critica or operacao_bloqueada)

    print("\n--- AVALIAÇÃO DE LÓGICA BOOLEANA ---")
    print(f"gerar_alerta (falha_critica OR consumo_elevado): {alerta_disparado}")
    print(f"bloquear_operacao (De Morgan: falha_seguranca OR inconsistencia): {operacao_bloqueada}")

    if operacao_bloqueada:
        print("Operação bloqueada por segurança (Teorema de De Morgan).")
    elif alerta_disparado:
        print("Alerta confirmado pela regra booleana.")
    else:
        print("Condição nominal — sem violações lógicas detectadas.")

    print("\n--- PROMPT ENGINEERING & SIMULAÇÃO DE IA ---")
    prompt_gerado, resposta_ia = ia_generativa.processar_analise_alerta(
        modulo=modulo,
        mensagem=mensagem,
        e_critico=e_critico,
    )
    print(prompt_gerado)
    print("\n[RESPOSTA SIMULADA DA IA]")
    print(resposta_ia)
    print("\nEvento arquivado em 'historico_respostas.txt'.")


# ==============================================================================
# MENU DE NAVEGAÇÃO NO TERMINAL (antes em menu.py)
# ==============================================================================

def menu() -> None:
    """Ponto único de interação do usuário com o NCAS."""
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
            ia_generativa.listar_topicos_disponiveis()

        elif opcao == "5":
            ia_generativa.exibir_prompt_estruturado()

        elif opcao == "6":
            ia_generativa.simulador_resposta_ia()

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