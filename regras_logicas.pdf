# regras_logicas.py
# Parte da Maria - Engenharia de Lógica e Arquitetura
# Aqui eu transformo as regras que defini nas etapas anteriores em condicionais de Python.

# ---------------------------------------------------
# Cenário 1 - Liberação de consulta ao sistema
# Regra: CONSULTA_LIBERADA = AUTORIZADO AND MODULO_ATIVO
# ---------------------------------------------------
def liberar_consulta(autorizado, modulo_ativo):
    if autorizado and modulo_ativo:
        return True
    else:
        return False


# ---------------------------------------------------
# Cenário 2 - Geração de alerta operacional
# Regra: GERAR_ALERTA = FALHA_CRITICA OR CONSUMO_ELEVADO
# ---------------------------------------------------
def gerar_alerta(falha_critica, consumo_elevado):
    if falha_critica or consumo_elevado:
        return True
    else:
        return False


# ---------------------------------------------------
# Cenário 3 - Priorização de solicitações da tripulação
# Regra: PRIORIDADE_MAXIMA = URGENTE AND SETOR_ESSENCIAL
# ---------------------------------------------------
def prioridade_maxima(urgente, setor_essencial):
    if urgente and setor_essencial:
        return True
    else:
        return False


# ---------------------------------------------------
# Cenário 4 - Bloqueio de operação por segurança
# Regra simplificada com De Morgan: BLOQUEAR_OPERACAO = FALHA_SEGURANCA OR INCONSISTENCIA_DADOS
# (o processo de simplificação está no arquivo regras_logicas.pdf)
# ---------------------------------------------------
def bloquear_operacao(falha_seguranca, inconsistencia_dados):
    if falha_seguranca or inconsistencia_dados:
        return True
    else:
        return False
