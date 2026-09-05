"""
Módulo de Regras Lógicas e Álgebra Booleana - Núcleo Cognitivo da Aurora Siger (NCAS)
Disciplina: Computer Science & Lógica Computacional

Este módulo define as regras de tomada de decisão lógica utilizadas pelo NCAS
para apoiar as operações e garantir a segurança na colônia marciana Aurora Siger.
"""

def liberar_consulta(autorizado: bool, modulo_ativo: bool) -> bool:
    """
    Cenário 1: Liberação de consulta aos dados da colônia.
    
    Regra Booleana:
        CONSULTA_LIBERADA = AUTORIZADO AND MODULO_ATIVO
        
    Justificativa:
        Apenas usuários credenciados podem consultar dados de subsistemas que
        estejam ativos e operando normalmente.
    """
    return bool(autorizado and modulo_ativo)


def gerar_alerta(falha_critica: bool, consumo_elevado: bool) -> bool:
    """
    Cenário 2: Geração de alerta operacional automático.
    
    Regra Booleana:
        GERAR_ALERTA = FALHA_CRITICA OR CONSUMO_ELEVADO
        
    Justificativa:
        Se qualquer anomalia grave ocorrer (uma falha mecânica/vital crítica
        OU um pico de consumo de energia além do limite seguro), o sistema
        imediatamente gera um sinal de alerta para a equipe de controle.
    """
    return bool(falha_critica or consumo_elevado)


def prioridade_maxima(urgente: bool, setor_essencial: bool) -> bool:
    """
    Cenário 3: Priorização de solicitações e chamados da tripulação.
    
    Regra Booleana:
        PRIORIDADE_MAXIMA = URGENTE AND SETOR_ESSENCIAL
        
    Justificativa:
        Um chamado só recebe prioridade de atendimento emergencial máxima se
        for explicitamente classificado como urgente E tiver origem em um setor
        essencial à sobrevivência (ex.: Suporte Vital, Habitat ou Navegação).
    """
    return bool(urgente and setor_essencial)


def bloquear_operacao(falha_seguranca: bool, inconsistencia_dados: bool) -> bool:
    """
    Cenário 4: Bloqueio emergencial de operação por segurança.
    
    Aplicação do Teorema de De Morgan:
    ----------------------------------
    Definição de operação normal:
        A operação só continua em estado normal se NÃO houver falha de segurança
        E NÃO houver inconsistência nos dados recebidos:
        OPERACAO_NORMAL = NOT(FALHA_SEGURANCA) AND NOT(INCONSISTENCIA_DADOS)
        
    Condição de bloqueio (negação do estado normal):
        BLOQUEAR_OPERACAO = NOT(OPERACAO_NORMAL)
        BLOQUEAR_OPERACAO = NOT( NOT(FALHA_SEGURANCA) AND NOT(INCONSISTENCIA_DADOS) )
        
    Pelo Teorema de De Morgan:
        NOT(A AND B) = NOT(A) OR NOT(B)
        
    Substituindo com dupla negação (NOT(NOT(X)) = X):
        BLOQUEAR_OPERACAO = NOT(NOT(FALHA_SEGURANCA)) OR NOT(NOT(INCONSISTENCIA_DADOS))
        BLOQUEAR_OPERACAO = FALHA_SEGURANCA OR INCONSISTENCIA_DADOS
        
    Equivalência Lógica comprovada por Tabela-Verdade:
    +------------------+----------------------+--------------------+--------------------+
    | FALHA_SEGURANCA  | INCONSISTENCIA_DADOS | Expressão De Morgan| Regra Simplificada |
    +------------------+----------------------+--------------------+--------------------+
    | True             | True                 | True               | True               |
    | True             | False                | True               | True               |
    | False            | True                 | True               | True               |
    | False            | False                | False              | False              |
    +------------------+----------------------+--------------------+--------------------+
    """
    return bool(falha_seguranca or inconsistencia_dados)


if __name__ == "__main__":
    print("=== Testes de Verificação Rápida - Regras Lógicas ===")
    print("1. Consulta liberada (True, True):", liberar_consulta(True, True))
    print("2. Gerar alerta (False, True):", gerar_alerta(False, True))
    print("3. Prioridade máxima (True, True):", prioridade_maxima(True, True))
    print("4. Bloquear operação com De Morgan (True, False):", bloquear_operacao(True, False))
    print("Todos os testes individuais executados com sucesso.")
