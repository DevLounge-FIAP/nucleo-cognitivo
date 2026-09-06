# 🚀 Núcleo Cognitivo da Aurora Siger (NCAS)
### Fase 5: Inteligência Artificial no Comando | FIAP

---

## 📌 Sumário
1. [Visão Geral do Projeto](#-visão-geral-do-projeto)
2. [Conexão com as Disciplinas da Fase 5](#-conexão-com-as-disciplinas-da-fase-5)
3. [Arquitetura do Sistema e Estrutura de Arquivos](#-arquitetura-do-sistema-e-estrutura-de-arquivos)
4. [Armazenamento de Dados: Justificativa Técnica (TXT vs JSON)](#-armazenamento-de-dados-justificativa-técnica-txt-vs-json)
5. [Organização Computacional: Memória, Barramentos e Fluxo de Dados](#-organização-computacional-memória-barramentos-e-fluxo-de-dados)
6. [Lógica Booleana e Teoremas de Simplificação (De Morgan)](#-lógica-booleana-e-teoremas-de-simplificação-de-morgan)
7. [Engenharia de Prompts e Simulação de IA Generativa](#-engenharia-de-prompts-e-simulação-de-ia-generativa)
8. [Conexão com Aprendizado de Máquina e Otimização](#-conexão-com-aprendizado-de-máquina-e-otimização)
9. [Ética, Diversidade e Responsabilidade Social no Uso da IA](#-ética-diversidade-e-responsabilidade-social-no-uso-da-ia)
10. [Instruções de Execução e Verificação](#-instruções-de-execução-e-verificação)
11. [Roteiro Detalhado para Gravação do Vídeo (Até 5 Minutos)](#-roteiro-detalhado-para-gravação-do-vídeo-até-5-minutos)

---

## 🌌 Visão Geral do Projeto

Na expansão da infraestrutura da colônia marciana **Aurora Siger**, os diferentes módulos (Suporte Vital, Geração de Energia, Telecomunicações e Estufa Hidropônica) passaram a produzir um volume contínuo e heterogêneo de dados operacionais.

O **Núcleo Cognitivo da Aurora Siger (NCAS)** foi concebido como um sistema de apoio computacional à decisão. Ele não substitui os especialistas humanos, mas atua como um elo central capaz de:
- Registrar eventos e logs de rotina em arquivos de texto;
- Estruturar o estado operacional e telemetrias em formato JSON;
- Aplicar validações lógicas booleanas simplificadas para triagem de anomalias em tempo real;
- Estruturar prompts para simular a assistência de modelos de linguagem natural (LLMs);
- Gerar recomendações padronizadas para a tomada de decisão do centro de controle da base.

---

## 🔗 Conexão com as Disciplinas da Fase 5

O projeto integra de forma prática as seis frentes de conhecimento da fase:

| Disciplina | Aplicação no Projeto NCAS |
| :--- | :--- |
| **Pensamento Computacional e Automação com Python** | Manipulação robusta de arquivos (`.txt` e `.json`), funções de I/O (`open`), gerenciamento de contexto (`with`), tratamento de exceções e menus interativos de terminal. |
| **Computer Science (Lógica Digital)** | Formalização de regras operacionais da base com operadores booleanos (`AND`, `OR`, `NOT`) e simplificação algébrica através do **Teorema de De Morgan**. |
| **Prompt and Artificial Intelligence** | Engenharia de prompts com técnicas de **Zero-shot**, **Few-shot** e **Structured Outputs** para suporte a decisões de alto risco. |
| **Modelagem Linear Aplicada ao ML** | Análise de erro, função de custo e regularização no processo de refinamento de prompts e consistência de respostas. |
| **Computer Organization and Architecture** | Compreensão do fluxo de I/O, hierarquia de memórias (RAM vs Disco), barramentos e persistência de dados. |
| **Formação Social e Sustentabilidade** | Análise crítica sobre vieses algorítmicos, mitigação de discriminação, impactos de decisões autônomas e responsabilidade humana (*Human-in-the-Loop*). |

---

## 📂 Arquitetura do Sistema e Estrutura de Arquivos

Conforme estipulado na **Seção 6.2 do Edital da FIAP**, os arquivos obrigatórios e complementares organizam-se da seguinte forma:

'''
nucleo-cognitivo/
│
├── codigo_fonte.py # [OBRIGATÓRIO] Arquivo principal e único ponto de entrada (inclui o menu do terminal)
├── dados_colonia.json # [OBRIGATÓRIO] Dados estruturados dos módulos e alertas da colônia
├── registros_colonia.txt # [OBRIGATÓRIO] Registros cronológicos e logs operacionais
├── regras_logicas.pdf # [OBRIGATÓRIO] Demonstração teórica das expressões e De Morgan
├── prompts_utilizados.pdf # [OBRIGATÓRIO] Documentação dos modelos de prompts estruturados
├── link_video.txt # [OBRIGATÓRIO] Arquivo contendo o link do YouTube (Não listado)
│
├── regras_logicas.py # [CÓDIGO] Módulo Python com as funções booleanas puras
├── validacao_regras.py # [CÓDIGO] Script de validação automática por tabela-verdade
├── ia_generativa.py # [CÓDIGO] Motor de simulação de prompts e respostas do assistente
├── historico_respostas.txt # [LOGS] Histórico persistente de pareceres emitidos pela IA
├── gerar_entrega_zip.py # [UTIL] Script automatizado de validação e criação do .zip
└── README.md # [DOCS] Documentação técnica e científica integral


---
'''

## 💾 Armazenamento de Dados: Justificativa Técnica (TXT vs JSON)

O sistema utiliza dois paradigmas de persistência em arquivos físicos:

### 1. Registros em Arquivo Texto (`registros_colonia.txt`)
- **Modo de Operação**: Abertura em modo append (`'a'`), escrita sequencial e leitura com `readlines()`.
- **Por que utilizar texto plano?**
  - **Eficiência de I/O em Tempo Real**: Na colônia, centenas de sensores e membros da tripulação registram ocorrências por minuto. A escrita em modo `append` opera em complexidade de tempo constante $\mathcal{O}(1)$, gravando o dado diretamente ao final do arquivo sem a necessidade de ler ou desserializar o arquivo inteiro na memória.
  - **Imutabilidade e Auditoria (Log Append-Only)**: Garante que registros históricos não sejam acidentalmente corrompidos ou apagados por novas inserções.

### 2. Dados Estruturados em JSON (`dados_colonia.json`)
- **Modo de Operação**: Serialização e desserialização com `json.dump()` e `json.load()`, utilizando dicionários e listas nativas do Python.
- **Por que utilizar JSON?**
  - **Tipagem Rica e Hierarquia**: Permite armazenar valores booleanos (`falha_critica: true`), números decimais (`temperatura: 21.8`), status de subsistemas e coleções de objetos complexos (lista de alertas).
  - **Acesso Aleatório por Chave-Valor**: Facilita consultas diretas aos módulos da colônia sem necessidade de varredura manual de texto.
  - **Interoperabilidade de Redes**: Formato padrão de comunicação entre diferentes subsistemas da base e potenciais APIs espaciais.

---

## 🖥️ Organização Computacional: Memória, Barramentos e Fluxo de Dados

A manipulação de arquivos em Python reflete diretamente a arquitetura de hardware subjacente:

'''
+-------------------------------------------------------------------------+
| CPU (Processador) |
| [Registradores] <---> [ALU / Lógica Booleana] <---> [Caches L1/L2/L3] |
+-------------------------------------------------------------------------+
▲
BARRAMENTO DO SISTEMA (BUS)
[Barramento de Dados | Barramento de Endereço | Barramento de Controle]
▼
+-------------------------------------------------------------------------+
| MEMÓRIA PRINCIPAL (RAM) |
| Variáveis Python em execução, Dicionários JSON carregados em memória |
+-------------------------------------------------------------------------+
▲
BARRAMENTO DE I/O (SATA / NVMe / Flash)
▼
+-------------------------------------------------------------------------+
| ARMAZENAMENTO SECUNDÁRIO (NÃO-VOLÁTIL) |
| registros_colonia.txt | dados_colonia.json | historico_respostas.txt |
+-------------------------------------------------------------------------+


1. **Memória Volátil (RAM)**: Quando o sistema executa `ler_dados_colonia()`, o interpretador Python aloca estruturas de dicionários e listas na memória RAM. Qualquer alteração nessas variáveis existe apenas enquanto o processo estiver ativo.
2. **Armazenamento Não-Volátil (Disco/Flash)**: Dispositivos de armazenamento secundário preservam os registros mesmo se houver queda total de energia na colônia marciana.
3. **Barramentos e Ciclo de Leitura/Escrita**:
   - Para salvar um alerta no JSON, os dados em RAM são serializados em bytes;
   - O controlador do sistema operacional emite comandos pelo **Barramento de Controle**;
   - O **Barramento de Endereço** localiza os blocos físicos livres no armazenamento;
   - O **Barramento de Dados** transporta o fluxo binário gravado via chamada `open(..., 'w')`.

---
'''

## 🧮 Lógica Booleana e Teoremas de Simplificação (De Morgan)

As operações da base utilizam 4 regras de decisão implementadas em [`regras_logicas.py`](file:///home/Aelton0/Dev/nucleo-cognitivo/regras_logicas.py):

### Cenário 1: Liberação de Consulta
$$CONSULTA\_LIBERADA = AUTORIZADO \land MODULO\_ATIVO$$

### Cenário 2: Geração de Alerta
$$GERAR\_ALERTA = FALHA\_CRITICA \lor CONSUMO\_ELEVADO$$

### Cenário 3: Priorização de Solicitações da Tripulação
$$PRIORIDADE\_MAXIMA = URGENTE \land SETOR\_ESSENCIAL$$

### Cenário 4: Bloqueio Emergencial de Operação (Aplicação de De Morgan)
- **Definição de Estado Normal**: A operação só transcorre normalmente se não houver falha de segurança **E** não houver inconsistência de dados:
  $$OPERACAO\_NORMAL = \neg(FALHA\_SEGURANCA) \land \neg(INCONSISTENCIA\_DADOS)$$
- **Condição de Bloqueio**: É o exato complemento do estado normal:
  $$BLOQUEAR\_OPERACAO = \neg(OPERACAO\_NORMAL)$$
  $$BLOQUEAR\_OPERACAO = \neg(\neg(FALHA\_SEGURANCA) \land \neg(INCONSISTENCIA\_DADOS))$$
- **Aplicação do Teorema de De Morgan** ($\neg(A \land B) = \neg A \lor \neg B$):
  $$BLOQUEAR\_OPERACAO = \neg(\neg(FALHA\_SEGURANCA)) \lor \neg(\neg(INCONSISTENCIA\_DADOS))$$
  Pela propriedade da dupla negação ($\neg(\neg X) = X$):
  $$BLOQUEAR\_OPERACAO = FALHA\_SEGURANCA \lor INCONSISTENCIA\_DADOS$$

#### Tabela-Verdade Comprobatória:
| $FALHA\_SEGURANCA$ | $INCONSISTENCIA\_DADOS$ | Expressão Não-Simplificada | Expressão Simplificada (De Morgan) | Equivalência |
| :---: | :---: | :---: | :---: | :---: |
| True | True | True | True | **✔ OK** |
| True | False | True | True | **✔ OK** |
| False | True | True | True | **✔ OK** |
| False | False | False | False | **✔ OK** |

> A simplificação reduz ciclos de clock na CPU, elimina operadores redundantes de negação e torna as condicionais de código muito mais legíveis e menos propensas a erros de software.

---

## 🤖 Engenharia de Prompts e Simulação de IA Generativa

O módulo [`ia_generativa.py`](file:///home/Aelton0/Dev/nucleo-cognitivo/ia_generativa.py) simula a integração com Modelos de Linguagem de Grande Porte (LLMs):

1. **Zero-Shot Prompting**:
   - Envia apenas a instrução e o contexto textual, sem fornecer exemplos prévios.
   - Ideal para resumos abrangentes dos registros operacionais da base.
2. **Few-Shot Prompting**:
   - Fornece pares de exemplo (*input $\rightarrow$ label*) antes da consulta real.
   - Utilizado para calibrar a classificação de prioridade (`NORMAL`, `ATENÇÃO`, `CRÍTICA`), orientando o modelo a seguir o padrão de criticidade da colônia.
3. **Structured Outputs**:
   - Força o modelo a responder estritamente dentro de uma estrutura pré-determinada com campos-chave:
     `STATUS`, `MODULO`, `PRIORIDADE`, `PROBLEMA`, `RECOMENDACAO`.
   - Evita alucinações e permite que outros softwares processem a resposta de maneira determinística.

---

## 📈 Conexão com Aprendizado de Máquina e Otimização

Embora o sistema utilize simulação determinística sem treinamento pesado de redes neurais (em total conformidade com o escopo da fase), ele incorpora conceitos fundamentais de **Modelagem Linear e Aprendizado de Máquina**:

- **Função de Custo e Minimização de Erro**: Em tarefas de linguagem natural, o erro pode ser compreendido como a divergência entre a resposta gerada e o protocolo de segurança esperado.
- **Engenharia de Prompts como Otimização**: A evolução do prompt *Zero-shot* para *Few-shot* atua analogamente ao **Gradiente Descendente**, ajustando o "espaço de busca" do modelo para minimizar o erro de classificação.
- **Regularização e Generalização**: A técnica de **Structured Outputs** opera como uma forma de *regularização*, restringindo a complexidade da saída para garantir que a IA generalize assertivamente para novos incidentes sem divagar ou alucinar.

---

## ⚖️ Ética, Diversidade e Responsabilidade Social no Uso da IA

Conforme exigido na Seção 5.7 do edital, o NCAS foi projetado considerando os riscos e responsabilidades sociais:

1. **Mitigação de Vieses Algorítmicos**: Sistemas de triagem automatizados podem priorizar chamados ou analisar relatórios com base em padrões históricos enviesados. Em uma colônia multiétnica e multidisciplinar, parâmetros de urgência devem basear-se exclusivamente em métricas objetivas de risco à vida e integridade técnica.
2. **Diversidade no Design de Sistemas**: Equipes de desenvolvimento diversas antecipam pontos cegos em interfaces e regras de negócio, assegurando que o sistema não produza linguagem discriminatória ou condescendente.
3. **Princípio Human-in-the-Loop (Decisões de Alto Risco)**: O NCAS é explicitamente um **sistema de apoio computacional à decisão**, nunca o decisor soberano em situações críticas de suporte vital. A responsabilidade moral e técnica permanece inegavelmente com a liderança humana da missão.

---

## 💻 Instruções de Execução e Verificação

### 1. Requisitos
- Python 3.10 ou superior instalado.
- Nenhuma biblioteca externa é necessária (usa exclusivamente a biblioteca padrão do Python).

### 2. Como Executar o Sistema Principal
No terminal, execute o arquivo principal:
```bash
python codigo_fonte.py
```

### 3. Como Executar a Validação das Regras Lógicas
Para testar todas as combinações da tabela-verdade:
```bash
python validacao_regras.py
```

### 4. Como Gerar o Pacote de Entrega (.zip)
Execute o script utilitário para validar todos os arquivos obrigatórios e compactar a pasta final para submissão:
```bash
python gerar_entrega_zip.py
```

---

## 🎬 Roteiro Detalhado para Gravação do Vídeo (Até 5 Minutos)

O vídeo de apresentação deve ser postado no **YouTube como "Não listado"** com duração máxima de **5 minutos**. Abaixo está o roteiro estruturado contemplando os 10 itens obrigatórios da avaliação:

### [00:00 - 00:30] 1. Abertura e Descrição do NCAS
- *Fala sugerida*: "Olá! Apresentamos o Núcleo Cognitivo da Aurora Siger (NCAS), desenvolvido para apoiar o centro de controle da nossa colônia marciana na organização, análise de dados e tomada de decisão operacional."

### [00:30 - 01:00] 2 e 4. Armazenamento (Texto vs JSON) e Demonstração dos Arquivos
- *Ação no vídeo*: Mostrar na tela o arquivo `registros_colonia.txt` e o arquivo `dados_colonia.json`.
- *Fala sugerida*: "Os dados são persistidos em dois formatos: registros em texto plano para logs sequenciais append-only em tempo real, e arquivos JSON para o estado estruturado dos módulos e alertas da base."

### [01:00 - 01:45] 3 e 10. Demonstração Prática do Sistema em Python
- *Ação no vídeo*: Executar `python codigo_fonte.py` no terminal.
- *Ação*: Mostrar a **Opção 1** (cadastrar um novo registro em TXT) e a **Opção 2** (consultar registros na tela com `readlines`).
- *Ação*: Mostrar a **Opção 7** (visualizar os módulos e telemetria do JSON).

### [01:45 - 02:30] 5. Regras Lógicas e Simplificação de De Morgan
- *Ação no vídeo*: Executar a **Opção 3** no menu (ou mostrar `python validacao_regras.py`).
- *Fala sugerida*: "Na disciplina de Computer Science, modelamos 4 regras operacionais. No Cenário 4, aplicamos o Teorema de De Morgan para simplificar a regra de bloqueio emergencial: a negação de que a operação está normal transforma um AND negado em um OR de falha de segurança ou inconsistência de dados. A tabela-verdade comprova a equivalência nas 16 combinações."

### [02:30 - 03:30] 6, 7 e Funcionalidade Integradora Mestre
- *Ação no vídeo*: Selecionar a **Opção 9 - Analisar alerta operacional (JSON + Booleana + IA)**.
- *Fala sugerida*: "Aqui temos a maior integração do projeto: o sistema lê o alerta gravado em JSON, passa pela validação booleana simplificada para atestar criticidade, injeta os dados em um prompt estruturado de IA e gera a recomendação padronizada ao centro de controle, salvando o histórico."
- *Ação*: Explicar rapidamente as técnicas Zero-shot, Few-shot e Structured Outputs mostradas no PDF `prompts_utilizados.pdf`.

### [03:30 - 04:15] 8. Otimização de Modelos e ML
- *Fala sugerida*: "Conectando com Modelagem Linear e ML, a transição para prompts Few-shot e saídas estruturadas minimiza o erro e a função de custo do modelo, atuando como regularização para impedir alucinações em relatórios operacionais críticos."

### [04:15 - 04:45] 9. Ética, Diversidade e Responsabilidade Social
- *Fala sugerida*: "Em Formação Social e Ética, garantimos que os critérios de alerta sejam baseados em segurança objetiva, sem vieses na triagem, e reforçamos o princípio de Human-in-the-Loop, onde a IA é ferramenta de suporte e os especialistas humanos mantêm a responsabilidade final."

### [04:45 - 05:00] Encerramento
- *Fala sugerida*: "Com isso, integramos programação Python, lógica computacional, arquitetura de computadores, inteligência artificial e ética em um sistema robusto e funcional para a missão Aurora Siger. Obrigado!"
