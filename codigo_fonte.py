import json

ARQUIVO_REGISTROS = 'registros_colonia.txt'
ARQUIVO_DADOS = 'dados_colonia.json'

SCHEMA_BASE_JSON = {
    "status_modulos": {
        "suporte_vital": {
            "estado": "ativo",
            "nivel_oxigenio_percentual": 100.0,
            "temperatura_interna_celsius": 22.5
        },
        "energia": {
            "estado": "ativo",
            "reserva_bateria_percentual": 100.0,
            "consumo_kw": 450
        },
        "comunicacao": {
            "estado": "ativo",
            "latencia_ms": 45
        }
    },
    "alertas_ativos": [
        {
            "id_alerta": 0,
            "criticidade": "info",
            "modulo": "sistema",
            "mensagem": "Inicializacao padrao concluida",
            "timestamp": "2026-08-23T00:00:00"
        }
    ]
}

def cadastrar_registro(mensagem: str) -> bool:
    try:
        with open(ARQUIVO_REGISTROS, 'a', encoding='utf-8') as arquivo:
            arquivo.write(mensagem + '\n')
        return True
    except OSError as e:
        print(f"Erro de I/O ao gravar registro: {e}")
        return False

def ler_registro() -> list[str]:
    try:
        with open(ARQUIVO_REGISTROS, 'r', encoding='utf-8') as arquivo:
            return [linha.strip() for linha in arquivo.readlines() if linha.strip()]
    except FileNotFoundError:
        with open(ARQUIVO_REGISTROS, 'w', encoding='utf-8') as arquivo:
            pass 
        return []

def ler_dados_colonia() -> dict:
    try:
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as arquivo:
            json.dump(SCHEMA_BASE_JSON, arquivo, indent=4)
        return SCHEMA_BASE_JSON

def salvar_dados_colonia(dados: dict) -> bool:
    try:
        with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, indent=4)
        return True
    except OSError as e:
        print(f"Erro de I/O ao salvar dados: {e}")
        return False

def limpar_registros() -> bool:
    try:
        with open(ARQUIVO_REGISTROS, 'w', encoding='utf-8') as arquivo:
            pass
        return True
    except OSError as e:
        print(f"Erro de I/O ao limpar registros: {e}")
        return False

def validar_regras_logicas():
    print("Função ainda não implementada.")

def exibir_prompt_estruturado():
    print("Função ainda não implementada.")

def simulador_resposta_ia():
    print("Função ainda não implementada.")


def exibir_dados_colonia():
    dados = ler_dados_colonia()

    print("\n=== STATUS DOS MÓDULOS DA COLÔNIA ===")
    for modulo, info in dados["status_modulos"].items():
        print(f"\nMódulo: {modulo.replace('_', ' ').title()}")
        for chave, valor in info.items():
            print(f"  {chave.replace('_', ' ').capitalize()}: {valor}")

    print("\n=== ALERTAS ATIVOS ===")
    if not dados["alertas_ativos"]:
        print("Nenhum alerta ativo.")
    else:
        for alerta in dados["alertas_ativos"]:
            print(f"\nID: {alerta['id_alerta']}")
            print(f"  Criticidade: {alerta['criticidade']}")
            print(f"  Módulo: {alerta['modulo']}")
            print(f"  Mensagem: {alerta['mensagem']}")
            print(f"  Timestamp: {alerta['timestamp']}")