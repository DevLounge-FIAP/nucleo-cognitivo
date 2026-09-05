"""
================================================================================
PROJETO: Núcleo Cognitivo da Aurora Siger (NCAS)
ARQUIVO: codigo_fonte.py (Arquivo Principal do Sistema)
DISCIPLINAS: Pensamento Computacional e Automação com Python | Computer Science |
             Prompt & AI | Computer Organization | Formação Social e Sustentabilidade
AUTORES: Aelton Soares de Menezes e Equipe da Colônia Aurora Siger
================================================================================
"""

import getpass
import json
import os
from datetime import datetime

# Importações dos subsistemas especializados do projeto
from regras_logicas import (
    liberar_consulta,
    gerar_alerta,
    prioridade_maxima,
    bloquear_operacao,
)
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
# Demonstração do uso de open(), gerenciador with, modos 'a', 'r', 'w' e readlines()
# ==============================================================================

def cadastrar_registro(mensagem: str) -> bool:
    """
    Grava um novo registro de log no arquivo texto utilizando o modo append ('a').
    Preserva as informações anteriores sem sobrescrever o arquivo.
    """
    try:
        with open(ARQUIVO_REGISTROS, 'a', encoding='utf-8') as arquivo:
            arquivo.write(mensagem + '\n')
        return True
    except OSError as erro:
        print(f"[ERRO DE I/O] Não foi possível gravar o registro: {erro}")
        return False


def ler_registro() -> list[str]:
    """
    Lê todas as linhas armazenadas no arquivo de registros utilizando o modo leitura ('r')
    e o método readlines(). Se o arquivo não existir, cria um vazio.
    """
    try:
        with open(ARQUIVO_REGISTROS, 'r', encoding='utf-8') as arquivo:
            return [linha.strip() for linha in arquivo.readlines() if linha.strip()]
    except FileNotFoundError:
        # Criação segura com modo 'w' caso ainda não exista
        with open(ARQUIVO_REGISTROS, 'w', encoding='utf-8') as arquivo:
            pass
        return []
    except OSError as erro:
        print(f"[ERRO DE I/O] Falha ao ler registros: {erro}")
        return []


def limpar_registros() -> bool:
    """
    Limpa o conteúdo do arquivo de registros abrindo-o no modo escrita ('w')
    sem escrever dados, truncando o arquivo de forma segura.
    """
    try:
        with open(ARQUIVO_REGISTROS, 'w', encoding='utf-8') as arquivo:
            pass
        return True
    except OSError as erro:
        print(f"[ERRO DE I/O] Falha ao limpar registros: {erro}")
        return False


# ==============================================================================
# MANIPULAÇÃO DE DADOS ESTRUTURADOS JSON (.JSON)
# Demonstração de json.load(), json.dump(), integridade de tipos e persistência
# ==============================================================================

def ler_dados_colonia() -> dict:
    """
    Carrega o arquivo JSON com os dados estruturados da colônia.
    Se o arquivo não existir ou estiver corrompido, recria com o schema base padrão.
    """
    try:
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        salvar_dados_colonia(SCHEMA_BASE_JSON)
        return SCHEMA_BASE_JSON


def salvar_dados_colonia(dados: dict) -> bool:
    """
    Serializa e persiste o dicionário Python no arquivo JSON com indentação padronizada.
    """
    try:
        with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, indent=2, ensure_ascii=False)
        return True
    except OSError as erro:
        print(f"[ERRO DE I/O] Falha ao persistir dados JSON: {erro}")
        return False


def exibir_status_colonia() -> None:
    """
    Apresenta no terminal os dados estruturados dos módulos e alertas salvos no JSON.
    """
    dados = ler_dados_colonia()
    print("\n" + "=" * 60)
    print(f"🛰️  STATUS DA COLÔNIA: {dados.get('colonia', 'Aurora Siger').upper()}")
    print(f"📍 Localização: {dados.get('localizacao', 'Marte')}")
    print("=" * 60)

    print("\n--- MÓDULOS OPERACIONAIS ---")
    modulos = dados.get("status_modulos", {})
    for nome, info in modulos.items():
        estado = info.get("estado", "desconhecido").upper()
        indicador = "🟢" if estado == "ATIVO" else "🔴"
        print(f"{indicador} {nome.replace('_', ' ').title()}:")
        for k, v in info.items():
            if k != "estado":
                print(f"     • {k.replace('_', ' ').title()}: {v}")

    print("\n--- ALERTAS ATIVOS NO SISTEMA ---")
    alertas = dados.get("alertas_ativos", [])
    if not alertas:
        print("  (Nenhum alerta ativo no momento. Todos os sistemas nominais.)")
    else:
        for alerta in alertas:
            crit = alerta.get("criticidade", "INFO")
            emoji = "🚨" if crit == "CRITICA" else "⚠️" if crit == "ATENCAO" else "ℹ️"
            print(f"  {emoji} [ID {alerta.get('id_alerta')}] {crit} | Módulo: {alerta.get('modulo')} | {alerta.get('timestamp')}")
            print(f"     Mensagem: {alerta.get('mensagem')}")
            print(f"     Flags: Falha Crítica={alerta.get('falha_critica')} | Consumo Elevado={alerta.get('consumo_elevado')} | Bloqueio={alerta.get('falha_seguranca') or alerta.get('inconsistencia_dados')}")


def cadastrar_novo_alerta_json() -> bool:
    """
    Permite à equipe cadastrar um novo alerta estruturado no arquivo JSON.
    """
    dados = ler_dados_colonia()
    alertas = dados.setdefault("alertas_ativos", [])

    print("\n--- CADASTRO DE NOVO ALERTA OPERACIONAL (JSON) ---")
    modulo = input("Nome do módulo (ex: suporte_vital, energia, comunicacao): ").strip().lower()
    mensagem = input("Descrição da ocorrência técnica: ").strip()

    falha_critica_input = input("É uma falha grave/crítica? (s/n): ").strip().lower() == 's'
    consumo_elevado_input = input("Houve consumo excessivo de energia? (s/n): ").strip().lower() == 's'
    falha_seguranca_input = input("Há indício de falha de segurança? (s/n): ").strip().lower() == 's'
    inconsistencia_input = input("Há inconsistência ou corrupção de dados? (s/n): ").strip().lower() == 's'

    # Avaliação lógica preliminar
    critico = falha_critica_input or falha_seguranca_input or inconsistencia_input
    criticidade = "CRITICA" if critico else ("ATENCAO" if consumo_elevado_input else "INFO")

    novo_id = (max([a.get("id_alerta", 0) for a in alertas], default=0)) + 1
    novo_alerta = {
        "id_alerta": novo_id,
        "modulo": modulo,
        "criticidade": criticidade,
        "falha_critica": falha_critica_input,
        "consumo_elevado": consumo_elevado_input,
        "falha_seguranca": falha_seguranca_input,
        "inconsistencia_dados": inconsistencia_input,
        "mensagem": mensagem,
        "timestamp": datetime.now().isoformat()[:19]
    }

    alertas.append(novo_alerta)
    if salvar_dados_colonia(dados):
        print(f"✔ Alerta #{novo_id} salvo com sucesso no arquivo '{ARQUIVO_DADOS}'.")
        return True
    return False


# ==============================================================================
# INTEGRAÇÃO DE REGRAS LÓGICAS E PROMPT ENGINEERING (SEÇÃO 5 E 6 DO PDF)
# ==============================================================================

def validar_regras_logicas() -> None:
    """
    Executa a validação formal das regras booleanas da Aurora Siger
    e do Teorema de De Morgan (Etapa 4 do projeto).
    """
    executar_validacao_completa()


def exibir_prompt_estruturado() -> None:
    """
    Exibe os modelos de prompts da colônia: Zero-shot, Few-shot e Structured Output.
    """
    ia_generativa.exibir_prompt_estruturado()


def simulador_resposta_ia() -> None:
    """
    Simula a interação com o assistente cognitivo inteligente da Aurora Siger,
    orientado por prompts estruturados e gerando histórico persistente.
    """
    ia_generativa.simulador_resposta_ia()


def analisar_alerta_operacional() -> None:
    """
    FUNCIONALIDADE INTEGRADORA PRINCIPAL (Seção 6.1 do PDF da FIAP):
    1. Carrega os alertas operacionais do arquivo JSON;
    2. Aplica as regras lógicas booleanas (incluindo a regra de De Morgan);
    3. Constrói um prompt estruturado (Structured Output) em tempo de execução;
    4. Gera o parecer simulado da IA da Aurora Siger para apoiar o centro de controle.
    """
    dados = ler_dados_colonia()
    alertas = dados.get("alertas_ativos", [])

    print("\n" + "=" * 65)
    print("🔍 ANÁLISE INTEGRADA DE ALERTA OPERACIONAL (JSON + BOOLEANA + IA)")
    print("=" * 65)

    if not alertas:
        print("Nenhum alerta registrado no momento. Utilize a opção do menu para cadastrar.")
        return

    print("Alertas disponíveis para análise:")
    for idx, alt in enumerate(alertas, start=1):
        print(f"  [{idx}] Módulo: {alt.get('modulo')} | Ocorrência: {alt.get('mensagem')}")

    escolha = input(f"\nSelecione o alerta (1 a {len(alertas)}): ").strip()
    try:
        indice = int(escolha) - 1
        alerta_sel = alertas[indice]
    except (ValueError, IndexError):
        print("Seleção inválida. Operação cancelada.")
        return

    modulo = alerta_sel.get("modulo", "sistema")
    mensagem = alerta_sel.get("mensagem", "Sem descrição")
    falha_critica = alerta_sel.get("falha_critica", False)
    consumo_elevado = alerta_sel.get("consumo_elevado", False)
    falha_seguranca = alerta_sel.get("falha_seguranca", False)
    inconsistencia = alerta_sel.get("inconsistencia_dados", False)

    # 1. Aplicação das Regras Lógicas
    alerta_disparado = gerar_alerta(falha_critica, consumo_elevado)
    operacao_bloqueada = bloquear_operacao(falha_seguranca, inconsistencia)

    print("\n--- [ETAPA 1: AVALIAÇÃO DE LÓGICA BOOLEANA COMPUTACIONAL] ---")
    print(f"• Regra GERAR_ALERTA (falha_critica OR consumo_elevado): {alerta_disparado}")
    print(f"• Regra BLOQUEAR_OPERACAO (De Morgan: falha_seg OR inconsistência): {operacao_bloqueada}")

    e_critico = bool(falha_critica or operacao_bloqueada)
    if operacao_bloqueada:
        print("⛔ ATENÇÃO MÁXIMA: Protocolo de bloqueio ativado por segurança via Teorema de De Morgan!")
    elif alerta_disparado:
        print("⚠️ ALERTA CONFIRMADO: Risco operacional validado pela regra booleana.")
    else:
        print("ℹ️ CONDIÇÃO NOMINAL: Sem violações lógicas detectadas.")

    # 2. Geração do Prompt Estruturado e Parecer da IA
    print("\n--- [ETAPA 2: PROMPT ENGINEERING & SIMULAÇÃO DE IA] ---")
    prompt_gerado, resposta_ia = ia_generativa.processar_analise_alerta(
        modulo=modulo,
        mensagem=mensagem,
        e_critico=e_critico
    )

    print(">> Prompt Estruturado Enviado:")
    print(prompt_gerado)
    print("\n>> Parecer Padronizado Retornado pelo Núcleo Cognitivo:")
    print(resposta_ia)
    print("\n✔ Evento arquivado com sucesso no histórico ('historico_respostas.txt').")


# ==============================================================================
# MENU PRINCIPAL DE NAVEGAÇÃO
# ==============================================================================

def menu() -> None:
    """
    Interface textual no terminal para navegação entre todas as funcionalidades
    requisitadas na avaliação da FIAP.
    """
    while True:
        print("\n" + "=" * 60)
        print("🚀 NÚCLEO COGNITIVO DA AURORA SIGER (NCAS) - SISTEMA DE APOIO")
        print("=" * 60)
        print("1. Cadastrar registro da colônia (Arquivo TXT)")
        print("2. Consultar registros salvos (Arquivo TXT)")
        print("3. Visualizar status e dados estruturados (Arquivo JSON)")
        print("4. Executar validação lógica (Tabela-Verdade & De Morgan)")
        print("5. Exibir prompts estruturados (Zero-shot, Few-shot, Structured)")
        print("6. Simular resposta do assistente inteligente IA")
        print("7. Analisar alerta operacional (Integração JSON + Booleana + IA)")
        print("8. Cadastrar novo alerta no arquivo JSON")
        print("9. Limpar registros do arquivo texto")
        print("0. Sair do sistema")
        print("=" * 60)

        opcao = input("Escolha uma opção (0-9): ").strip()

        if opcao == "1":
            mensagem = input("Digite o registro operacional: ").strip()
            if not mensagem:
                print("Registro não pode ser vazio.")
                continue
            data_hora = datetime.now().strftime("%d/%m %H:%M")
            usuario = getpass.getuser()
            linha_formatada = f"[Data e Hora: {data_hora} Usuário: {usuario}]: {mensagem}"

            if cadastrar_registro(linha_formatada):
                print(f"✔ Registro salvo com sucesso em '{ARQUIVO_REGISTROS}'.")
            else:
                print("✖ Falha ao salvar o registro. Verifique os logs.")

        elif opcao == "2":
            registros = ler_registro()
            print("\n--- REGISTROS OPERACIONAIS DA COLÔNIA ---")
            if not registros:
                print("Nenhum registro encontrado no arquivo.")
            else:
                for indice, reg in enumerate(registros, start=1):
                    print(f"[{indice:02d}] {reg}")

        elif opcao == "3":
            exibir_status_colonia()

        elif opcao == "4":
            validar_regras_logicas()

        elif opcao == "5":
            exibir_prompt_estruturado()

        elif opcao == "6":
            simulador_resposta_ia()

        elif opcao == "7":
            analisar_alerta_operacional()

        elif opcao == "8":
            cadastrar_novo_alerta_json()

        elif opcao == "9":
            confirma = input("Tem certeza que deseja apagar todos os registros em TXT? (s/n): ").strip().lower()
            if confirma == 's':
                if limpar_registros():
                    print(f"✔ Registros limpos com sucesso em '{ARQUIVO_REGISTROS}'.")
                else:
                    print("✖ Erro ao limpar registros.")
            else:
                print("Operação cancelada.")

        elif opcao == "0":
            print("\nEncerrando o Núcleo Cognitivo da Aurora Siger. Operações salvas.")
            break

        else:
            print("Opção inválida. Digite um número de 0 a 9.")


if __name__ == "__main__":
    menu()