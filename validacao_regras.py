# validacao_regras.py
# Parte da Maria - Validacao da consistencia dos alertas logicos (Etapa 4)
# Aqui eu testo minhas proprias funcoes com TODAS as combinacoes possiveis de entrada,
# pra garantir que elas se comportam do jeito esperado em qualquer cenario, nao so nos
# casos que eu escolhi manualmente antes.

from regras_logicas import (
    liberar_consulta,
    gerar_alerta,
    prioridade_maxima,
    bloquear_operacao,
)


def validar_funcao(nome_funcao, funcao, esperado_and):
    """
    Testa uma funcao de 2 variaveis booleanas com as 4 combinacoes possiveis
    (True/True, True/False, False/True, False/False) e confere se o resultado
    bate com o que a regra deveria dar (AND ou OR).

    esperado_and = True  -> a regra e do tipo AND (so True se as duas forem True)
    esperado_and = False -> a regra e do tipo OR  (True se pelo menos uma for True)
    """
    combinacoes = [(True, True), (True, False), (False, True), (False, False)]
    print(f"\nValidando: {nome_funcao}")
    tudo_ok = True

    for a, b in combinacoes:
        resultado = funcao(a, b)

        if esperado_and:
            esperado = a and b
        else:
            esperado = a or b

        status = "OK" if resultado == esperado else "ERRO"
        if resultado != esperado:
            tudo_ok = False

        print(
            f"  entrada=({a}, {b}) -> resultado={resultado} | esperado={esperado} [{status}]"
        )

    if tudo_ok:
        print(f"  -> {nome_funcao} passou em todas as combinacoes.")
    else:
        print(f"  -> {nome_funcao} tem inconsistencia! Revisar a funcao.")

    return tudo_ok


def executar_validacao_completa() -> bool:
    print("\n=== Validação das Regras Lógicas da Aurora Siger (Tabela-Verdade) ===")

    resultados = []
    resultados.append(
        validar_funcao("liberar_consulta (AND: AUTORIZADO AND MODULO_ATIVO)", liberar_consulta, esperado_and=True)
    )
    resultados.append(
        validar_funcao("gerar_alerta (OR: FALHA_CRITICA OR CONSUMO_ELEVADO)", gerar_alerta, esperado_and=False)
    )
    resultados.append(
        validar_funcao("prioridade_maxima (AND: URGENTE AND SETOR_ESSENCIAL)", prioridade_maxima, esperado_and=True)
    )
    resultados.append(
        validar_funcao("bloquear_operacao (De Morgan: FALHA_SEGURANCA OR INCONSISTENCIA_DADOS)", bloquear_operacao, esperado_and=False)
    )

    print("\n=== Resumo da Verificação Lógica ===")
    if all(resultados):
        print("✔ Todas as regras lógicas estão consistentes em todas as 16 combinações possíveis.")
        return True
    else:
        print("✖ Alguma regra apresentou inconsistência. Ver detalhes acima.")
        return False


if __name__ == "__main__":
    executar_validacao_completa()
