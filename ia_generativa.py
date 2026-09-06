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

# ---------------------------------------------------------------------------
# TABELA CENTRAL DE TÓPICOS — fonte única de verdade.
# Cada tópico é escrito UMA vez aqui. Os 3 formatos de resposta (zero-shot,
# few-shot, structured) são gerados a partir destes mesmos dados, então
# nunca ficam desalinhados entre si.
# Chaves sem acento de propósito: o texto do usuário é normalizado antes
# de comparar, então comparamos sempre "sem acento" dos dois lados.
# ---------------------------------------------------------------------------
TOPICOS = {
    "oxigenio": {
        "status": "CRÍTICA",
        "modulo": "SUPORTE_VITAL",
        "prioridade": "ALTA",
        "problema": "Redução do nível de oxigênio para 72%, indicando condição de risco.",
        "recomendacao": "Verificar imediatamente o fornecimento de oxigênio e restabelecer o nível.",
    },
    "falha": {
        "status": "CRÍTICA",
        "modulo": "SISTEMA",
        "prioridade": "ALTA",
        "problema": "Falha geral detectada em um dos sistemas da colônia.",
        "recomendacao": "Isolar o sistema afetado e acionar a equipe técnica imediatamente.",
    },
    "radiacao": {
        "status": "CRÍTICA",
        "modulo": "BLINDAGEM",
        "prioridade": "ALTA",
        "problema": "Nível de radiação acima do limite seguro detectado pelos sensores externos.",
        "recomendacao": "Ativar blindagem de emergência e restringir o acesso às áreas expostas.",
    },
    "pressao": {
        "status": "CRÍTICA",
        "modulo": "HABITAT",
        "prioridade": "ALTA",
        "problema": "Variação crítica de pressão interna detectada no habitat.",
        "recomendacao": "Verificar vedação das câmaras e acionar o protocolo de despressurização controlada.",
    },
    "seguranca": {
        "status": "CRÍTICA",
        "modulo": "SEGURANCA",
        "prioridade": "ALTA",
        "problema": "Falha de segurança detectada. Operação bloqueada por protocolo.",
        "recomendacao": "Isolar módulo afetado. Acionar equipe de segurança imediatamente.",
    },
    "inconsistencia": {
        "status": "CRÍTICA",
        "modulo": "DADOS",
        "prioridade": "ALTA",
        "problema": "Inconsistência nos dados detectada. Operação bloqueada por segurança.",
        "recomendacao": "Verificar integridade dos dados. Restaurar backup se necessário.",
    },
    "temperatura": {
        "status": "ATENÇÃO",
        "modulo": "HABITAT",
        "prioridade": "MÉDIA",
        "problema": "Variação de temperatura acima do limite permitido (+4 °C).",
        "recomendacao": "Verificar climatização. Monitorar a cada 30 minutos.",
    },
    "energia": {
        "status": "ATENÇÃO",
        "modulo": "ENERGIA",
        "prioridade": "MÉDIA",
        "problema": "Consumo acima do limite de 500 kW. Consumo atual: 520 kW.",
        "recomendacao": "Redistribuir carga entre os módulos. Acionar equipe técnica.",
    },
    "agua": {
        "status": "ATENÇÃO",
        "modulo": "SUPORTE_VITAL",
        "prioridade": "MÉDIA",
        "problema": "Nível de reserva de água abaixo do recomendado para operação segura.",
        "recomendacao": "Acionar sistema de reciclagem hídrica e monitorar o consumo.",
    },
    "comunicacao": {
        "status": "ATENÇÃO",
        "modulo": "COMUNICACAO",
        "prioridade": "MÉDIA",
        "problema": "Latência elevada detectada no módulo de comunicação.",
        "recomendacao": "Verificar canais de transmissão. Reiniciar roteadores de backup.",
    },
    "padrao": {
        "status": "NORMAL",
        "modulo": "CENTRAL",
        "prioridade": "BAIXA",
        "problema": "Nenhum problema identificado no registro analisado.",
        "recomendacao": "Manter monitoramento de rotina conforme protocolo.",
    },
}

# Palavras que o usuário pode digitar e que na verdade se referem a um
# tópico que já existe acima — sem precisar duplicar os dados de novo.
SINONIMOS = {
    "latencia": "comunicacao",
    "rotina": "padrao",
    "manutencao": "padrao",
}


_TABELA_SEM_ACENTO = str.maketrans(
    "áàãâäéèêëíìîïóòõôöúùûüç",
    "aaaaaeeeeiiiiooooouuuuc",
)


def _normalizar(texto: str) -> str:
    """Remove acentos e caixa alta/baixa, pra comparação ficar tolerante
    a 'Oxigênio', 'oxigenio' e 'OXIGÊNIO' significarem a mesma coisa.
    Usa apenas string e dicionário (str.maketrans/translate), sem depender
    de bibliotecas fora do conteúdo estudado no curso."""
    return texto.lower().translate(_TABELA_SEM_ACENTO)


def _localizar_topico(texto: str):
    """Procura no texto digitado alguma palavra-chave conhecida (tópico
    ou sinônimo) e devolve os dados desse tópico. Devolve None se nada
    bater — ou seja, texto fora do escopo da IA."""
    texto_normalizado = _normalizar(texto)

    for chave, topico_id in SINONIMOS.items():
        if chave in texto_normalizado:
            return TOPICOS[topico_id]

    for chave, dados in TOPICOS.items():
        if chave != "padrao" and chave in texto_normalizado:
            return dados

    return None


def _resumo_zero_shot(topico: dict) -> str:
    modulo_legivel = topico["modulo"].replace("_", " ").title()
    return (
        "O Núcleo Cognitivo da Aurora Siger possui registros relacionados\n"
        "ao funcionamento dos principais módulos da colônia.\n\n"
        f"O módulo de {modulo_legivel} apresenta a seguinte ocorrência:\n"
        f"{topico['problema']}\n\n"
        f"Recomendação: {topico['recomendacao']}"
    )


def _resposta_structured(topico: dict) -> str:
    return (
        f"STATUS:       {topico['status']}\n"
        f"MODULO:       {topico['modulo']}\n"
        f"PRIORIDADE:   {topico['prioridade']}\n"
        f"PROBLEMA:     {topico['problema']}\n"
        f"RECOMENDACAO: {topico['recomendacao']}"
    )


def exibir_prompt_estruturado():
    print("\n1 - Zero-shot  |  2 - Few-shot  |  3 - Structured Output")
    escolha = input("Qual prompt exibir? ")

    if escolha == "1":
        texto = input("Digite os registros: ")
        if _localizar_topico(texto) is None:
            print("\nIsso foge do escopo de análise da IA da colônia.")
            return
        print("\n" + PROMPT_ZERO_SHOT.replace("{REGISTROS}", texto))

    elif escolha == "2":
        texto = input("Descreva a ocorrência: ")
        if _localizar_topico(texto) is None:
            print("\nIsso foge do escopo de análise da IA da colônia.")
            return
        print("\n" + PROMPT_FEW_SHOT.replace("{OCORRENCIA}", texto))

    elif escolha == "3":
        texto = input("Digite o registro: ")
        if _localizar_topico(texto) is None:
            print("\nIsso foge do escopo de análise da IA da colônia.")
            return
        print("\n" + PROMPT_STRUCTURED.replace("{REGISTRO}", texto))

    else:
        print("Opção inválida.")


def simulador_resposta_ia():
    print("\n1 - Zero-shot  |  2 - Few-shot  |  3 - Structured Output")
    escolha = input("Qual prompt simular? ")

    if escolha == "1":
        texto = input("Digite os registros: ")
        topico = _localizar_topico(texto)
        if topico is None:
            print("\nIsso foge do escopo de análise da IA da colônia.")
            return
        prompt = PROMPT_ZERO_SHOT.replace("{REGISTROS}", texto)
        resposta = _resumo_zero_shot(topico)

    elif escolha == "2":
        texto = input("Descreva a ocorrência: ")
        topico = _localizar_topico(texto)
        if topico is None:
            print("\nIsso foge do escopo de análise da IA da colônia.")
            return
        prompt = PROMPT_FEW_SHOT.replace("{OCORRENCIA}", texto)
        resposta = topico["status"]

    elif escolha == "3":
        texto = input("Digite o registro: ")
        topico = _localizar_topico(texto)
        if topico is None:
            print("\nIsso foge do escopo de análise da IA da colônia.")
            return
        prompt = PROMPT_STRUCTURED.replace("{REGISTRO}", texto)
        resposta = _resposta_structured(topico)

    else:
        print("Opção inválida.")
        return

    print("\n[PROMPT ENVIADO]")
    print(prompt)
    print("\n[RESPOSTA SIMULADA DA IA]")
    print(resposta)

    with open("historico_respostas.txt", "a", encoding="utf-8") as f:
        f.write(f"\nPROMPT:\n{prompt}\nRESPOSTA:\n{resposta}\n")

    print("\nSalvo em historico_respostas.txt")

def listar_topicos_disponiveis():
    print("\n=== PALAVRAS-CHAVE QUE A IA RECONHECE ===")
    print("Digite algo relacionado a um destes temas nas opções 4 e 5:\n")

    for chave in TOPICOS:
        if chave != "padrao":
            print(f"  - {chave}")

    if SINONIMOS:
        print("\nTambém funcionam (equivalentes aos de cima):")
        for sinonimo, alvo in SINONIMOS.items():
            print(f"  - {sinonimo} (mesmo caso de '{alvo}')")