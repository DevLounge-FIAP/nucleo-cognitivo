"""
================================================================================
PROJETO: Núcleo Cognitivo da Aurora Siger (NCAS)
ARQUIVO: menu.py
FINALIDADE: Ponto de entrada amigável para navegação no terminal,
            garantindo sincronia total com o arquivo principal 'codigo_fonte.py'.
================================================================================
"""

from codigo_fonte import (
    cadastrar_registro,
    ler_registro,
    limpar_registros,
    ler_dados_colonia,
    salvar_dados_colonia,
    exibir_status_colonia,
    validar_regras_logicas,
    exibir_prompt_estruturado,
    simulador_resposta_ia,
    analisar_alerta_operacional,
    cadastrar_novo_alerta_json,
    menu,
)

if __name__ == "__main__":
    menu()