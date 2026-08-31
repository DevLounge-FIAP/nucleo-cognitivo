import json

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
        with open('registros_colonia.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(mensagem + '\n')
        return True
    except OSError:
        return False

def ler_registro() -> str:
    try:
        with open('registros_colonia.txt', 'r', encoding='utf-8') as arquivo:
            return arquivo.read()
    except FileNotFoundError:
        with open('registros_colonia.txt', 'w', encoding='utf-8') as arquivo:
            pass 
        return ""

def ler_dados_colonia() -> dict:
    try:
        with open('dados_colonia.json', 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        with open('dados_colonia.json', 'w', encoding='utf-8') as arquivo:
            json.dump(SCHEMA_BASE_JSON, arquivo, indent=4)
        return SCHEMA_BASE_JSON

def salvar_dados_colonia(dados: dict) -> bool:
    try:
        with open('dados_colonia.json', 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, indent=4)
        return True
    except OSError:
        return False

def validar_regras_logicas():
    # Maria vai implementar aqui: regra booleana simplificada
    print("Função ainda não implementada.")


def exibir_prompt_estruturado():
    # Bruno vai implementar aqui: prompt zero-shot/few-shot
    print("Função ainda não implementada.")


def simulador_resposta_ia():
    # Bruno vai implementar aqui: resposta simulada do "assistente"
    print("Função ainda não implementada.")


