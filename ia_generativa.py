import json

PROMPT_ZERO_SHOT = """Você é o Assistente Cognitivo da Aurora Siger.
Analise os registros e apresente um resumo. Não invente informações.

Registros:
{REGISTROS}"""

PROMPT_FEW_SHOT = """Você é o Assistente Cognitivo da Aurora Siger.
Classifique o nível de prioridade da ocorrência.

Exemplo 1: "Pequena variação de temperatura." → ATENÇÃO
Exemplo 2: "Falha completa no sistema de oxigênio." → CRÍTICA

Ocorrência: {OCORRENCIA}"""

PROMPT_STRUCTURED = """Analise o registro e responda neste formato:
STATUS: [NORMAL/ATENÇÃO/CRÍTICA]
MODULO: [nome]
PRIORIDADE: [BAIXA/MÉDIA/ALTA]
PROBLEMA: [descrição]
RECOMENDACAO: [orientação]

Registro: {REGISTRO}"""

RESPOSTAS_ZERO_SHOT = {
    "oxigênio": (
        "O Núcleo Cognitivo da Aurora Siger possui registros relacionados\n"
        "ao funcionamento dos principais módulos da colônia.\n\n"
        "O módulo de Suporte Vital encontra-se com nível de oxigênio reduzido.\n"
        "Situação requer atenção imediata da equipe técnica.\n\n"
        "Os registros indicam uma condição de risco no sistema de suporte vital."
    ),
    "energia": (
        "O Núcleo Cognitivo da Aurora Siger possui registros relacionados\n"
        "ao funcionamento dos principais módulos da colônia.\n\n"
        "O módulo de Energia encontra-se ativo, com bateria em 100%\n"
        "e consumo registrado de 450 kW.\n\n"
        "Os registros indicam que os sistemas monitorados estão operacionais."
    ),
    "temperatura": (
        "O Núcleo Cognitivo da Aurora Siger possui registros relacionados\n"
        "ao funcionamento dos principais módulos da colônia.\n\n"
        "O módulo de Habitat registra variação de temperatura acima do limite.\n"
        "Temperatura interna: 22,5 °C.\n\n"
        "Os registros indicam necessidade de verificação do sistema de climatização."
    ),
    "comunicação": (
        "O Núcleo Cognitivo da Aurora Siger possui registros relacionados\n"
        "ao funcionamento dos principais módulos da colônia.\n\n"
        "O módulo de Comunicação está ativo, apresentando latência de 45 ms.\n\n"
        "Os registros indicam operação dentro dos parâmetros normais."
    ),
    "padrão": (
        "O Núcleo Cognitivo da Aurora Siger possui registros relacionados\n"
        "ao funcionamento dos principais módulos da colônia.\n\n"
        "O módulo de Suporte Vital encontra-se ativo, com nível de oxigênio\n"
        "em 100% e temperatura interna registrada em 22,5 °C.\n\n"
        "O módulo de Energia encontra-se ativo, com bateria em 100%\n"
        "e consumo registrado de 450 kW.\n\n"
        "O módulo de Comunicação também está ativo, apresentando latência de 45 ms.\n\n"
        "Os registros indicam que os sistemas monitorados estão operacionais\n"
        "e que não há, nos dados consultados, uma ocorrência crítica registrada."
    ),
}

RESPOSTAS_FEW_SHOT = {
    "oxigênio":    "CRÍTICA",
    "falha":       "CRÍTICA",
    "radiação":    "CRÍTICA",
    "pressão":     "CRÍTICA",
    "temperatura": "ATENÇÃO",
    "energia":     "ATENÇÃO",
    "água":        "ATENÇÃO",
    "comunicação": "ATENÇÃO",
    "latência":    "ATENÇÃO",
    "rotina":      "NORMAL",
    "manutenção":  "NORMAL",
    "padrão":      "NORMAL",
}

RESPOSTAS_STRUCTURED = {
    "oxigênio": (
        "STATUS:       CRÍTICA\n"
        "MODULO:       SUPORTE_VITAL\n"
        "PRIORIDADE:   ALTA\n"
        "PROBLEMA:     Redução do nível de oxigênio para 72%, indicando condição de risco.\n"
        "RECOMENDACAO: Verificar imediatamente o fornecimento de oxigênio e restabelecer o nível."
    ),
    "energia": (
        "STATUS:       ATENÇÃO\n"
        "MODULO:       ENERGIA\n"
        "PRIORIDADE:   MÉDIA\n"
        "PROBLEMA:     Sobrecarga detectada no módulo de distribuição de energia.\n"
        "RECOMENDACAO: Redistribuir carga. Acionar equipe técnica para inspeção."
    ),
    "temperatura": (
        "STATUS:       ATENÇÃO\n"
        "MODULO:       HABITAT\n"
        "PRIORIDADE:   MÉDIA\n"
        "PROBLEMA:     Variação de temperatura acima do limite permitido (+4 °C).\n"
        "RECOMENDACAO: Verificar climatização. Monitorar a cada 30 minutos."
    ),
    "comunicação": (
        "STATUS:       ATENÇÃO\n"
        "MODULO:       COMUNICACAO\n"
        "PRIORIDADE:   MÉDIA\n"
        "PROBLEMA:     Latência elevada detectada no módulo de comunicação.\n"
        "RECOMENDACAO: Verificar canais de transmissão. Reiniciar roteadores de backup."
    ),
    "padrão": (
        "STATUS:       NORMAL\n"
        "MODULO:       CENTRAL\n"
        "PRIORIDADE:   BAIXA\n"
        "PROBLEMA:     Nenhum problema identificado no registro analisado.\n"
        "RECOMENDACAO: Manter monitoramento de rotina conforme protocolo."
    ),
}

def _resposta(texto, dicionario):
    for chave in dicionario:
        if chave != "padrão" and chave in texto.lower():
            return dicionario[chave]
    return dicionario["padrão"]

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

def simulador_resposta_ia():
    print("\n1 - Zero-shot  |  2 - Few-shot  |  3 - Structured Output")
    escolha = input("Qual prompt simular? ")

    if escolha == "1":
        texto = input("Digite os registros: ")
        prompt = PROMPT_ZERO_SHOT.replace("{REGISTROS}", texto)
        resposta = _resposta(texto, RESPOSTAS_ZERO_SHOT)

    elif escolha == "2":
        texto = input("Descreva a ocorrência: ")
        prompt = PROMPT_FEW_SHOT.replace("{OCORRENCIA}", texto)
        resposta = _resposta(texto, RESPOSTAS_FEW_SHOT)

    elif escolha == "3":
        texto = input("Digite o registro: ")
        prompt = PROMPT_STRUCTURED.replace("{REGISTRO}", texto)
        resposta = _resposta(texto, RESPOSTAS_STRUCTURED)

    else:
        print("Opção inválida.")
        return

    print("\n[PROMPT ENVIADO]")
    print(prompt)
    print("\n[RESPOSTA SIMULADA DA IA]")
    print(resposta)

    with open("historico_respostas.txt", "a", encoding="utf-8") as f:
        f.write(f"\nPROMPT:\n{prompt}\nRESPOSTA:\n{resposta}\n")

    print("\nSalvo em historico_respostas.txt")# atualizado
