import json

#prompts zero shot, fews shot e structured
PROMPT_ZERO_SHOT = """Você é o Assistente Cognitivo da Aurora Siger.
Analise os registros e apresente um resumo. Não invente informações.

Registros:
{REGISTROS}"""

PROMPT_FEW_SHOT = """Você é o Assistente Cognitivo da Aurora Siger.
Classifique o nível de prioridade da ocorrência.

Exemplo 1: "Pequena variação de temperatura." = ATENÇÃO
Exemplo 2: "Falha completa no sistema de oxigênio." = CRÍTICA

Ocorrência: {OCORRENCIA}"""

PROMPT_STRUCTURED = """Analise o registro e responda neste formato:
STATUS: [NORMAL/ATENÇÃO/CRÍTICA]
MODULO: [nome]
PRIORIDADE: [BAIXA/MÉDIA/ALTA]
PROBLEMA: [descrição]
RECOMENDACAO: [orientação]

Registro: {REGISTRO}"""


RESPOSTAS = {
    "oxigênio":    "CRÍTICA — Módulo SUPORTE_VITAL com nível de oxigênio reduzido.\nRecomendação: Verificar imediatamente o sistema de fornecimento.",
    "energia":     "ATENÇÃO — Módulo ENERGIA com sobrecarga detectada.\nRecomendação: Redistribuir carga entre os módulos disponíveis.",
    "temperatura": "ATENÇÃO — Módulo HABITAT com variação de temperatura acima do limite.\nRecomendação: Verificar sistema de climatização.",
    "comunicação": "ATENÇÃO — Módulo COMUNICACAO com latência elevada.\nRecomendação: Verificar canais de transmissão.",
    "padrão":      "NORMAL — Todos os sistemas da colônia operam dentro dos parâmetros.\nNenhuma ocorrência crítica registrada.",
}


def _resposta(texto):
    for chave in RESPOSTAS:
        if chave != "padrão" and chave in texto.lower():
            return RESPOSTAS[chave]
    return RESPOSTAS["padrão"]

#prompt que a pessoa deseja ver
def exibir_prompt_estruturado():
    print("\n1 - Zero-shot  |  2 - Few-shot  |  3 - Structured Output")
    escolha = input("Qual prompt exibir? ")

    if escolha == "1":
        texto = input("Digite os registros: ")
        print("\n" + PROMPT_ZERO_SHOT.replace("{REGISTROS}", texto))

    elif escolha == "2":
        texto = input("Descreva a ocorrência: ")
        print("\n" + PROMPT_FEW_SHOT.replace("{OCORRENCIA}", texto))

    elif escolha == "3":
        texto = input("Digite o registro: ")
        print("\n" + PROMPT_STRUCTURED.replace("{REGISTRO}", texto))

    else:
        print("Opção inválida.")

#Respostas simuladas pela IA
def simulador_resposta_ia():
    print("\n1 - Zero-shot  |  2 - Few-shot  |  3 - Structured Output")
    escolha = input("Qual prompt simular? ")

    if escolha == "1":
        texto = input("Digite os registros: ")
        prompt = PROMPT_ZERO_SHOT.replace("{REGISTROS}", texto)

    elif escolha == "2":
        texto = input("Descreva a ocorrência: ")
        prompt = PROMPT_FEW_SHOT.replace("{OCORRENCIA}", texto)

    elif escolha == "3":
        texto = input("Digite o registro: ")
        prompt = PROMPT_STRUCTURED.replace("{REGISTRO}", texto)

    else:
        print("Opção inválida.")
        return

    print("\n[PROMPT ENVIADO]")
    print(prompt)
    print("\n[RESPOSTA SIMULADA DA IA]")
    print(_resposta(texto))

#Salva no Histórico
    with open("historico_respostas.txt", "a", encoding="utf-8") as f:
        f.write(f"\nPROMPT:\n{prompt}\nRESPOSTA:\n{_resposta(texto)}\n")

    print("\n Salvo em historico_respostas.txt")