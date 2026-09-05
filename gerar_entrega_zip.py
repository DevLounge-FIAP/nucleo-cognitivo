"""
================================================================================
SCRIPT UTILITÁRIO: gerar_entrega_zip.py
FINALIDADE: Valida os requisitos do edital da FIAP (Seção 6.2) e gera
            o arquivo .zip pronto para submissão contendo os arquivos obrigatórios.
================================================================================
"""

import os
import zipfile

ARQUIVOS_OBRIGATORIOS = [
    'codigo_fonte.py',
    'dados_colonia.json',
    'registros_colonia.txt',
    'regras_logicas.pdf',
    'prompts_utilizados.pdf',
    'link_video.txt',
]

ARQUIVOS_COMPLEMENTARES = [
    'regras_logicas.py',
    'ia_generativa.py',
    'validacao_regras.py',
    'menu.py',
    'README.md',
    'historico_respostas.txt',
]

NOME_ZIP = 'entrega_nucleo_cognitivo.zip'

def validar_e_gerar_zip():
    print("=" * 60)
    print("📦 VERIFICADOR E GERADOR DE PACOTE DE ENTREGA (.ZIP) - FIAP")
    print("=" * 60)

    # 1. Checagem dos arquivos obrigatórios
    faltantes = []
    for arquivo in ARQUIVOS_OBRIGATORIOS:
        if os.path.exists(arquivo):
            tamanho_kb = os.path.getsize(arquivo) / 1024
            print(f"  ✔ [OBRIGATÓRIO] {arquivo:<25} ({tamanho_kb:.1f} KB)")
        else:
            print(f"  ✖ [FALTANDO]    {arquivo:<25}")
            faltantes.append(arquivo)

    if faltantes:
        print("\n❌ ERRO CRÍTICO: Os seguintes arquivos obrigatórios estão ausentes:")
        for f in faltantes:
            print(f"   - {f}")
        print("Corrija a pendência antes de submeter.")
        return False

    # 2. Checagem dos arquivos complementares de suporte
    print("\nArquivos complementares do projeto:")
    incluir_complementares = []
    for arquivo in ARQUIVOS_COMPLEMENTARES:
        if os.path.exists(arquivo):
            tamanho_kb = os.path.getsize(arquivo) / 1024
            print(f"  ✔ [SUPORTE]     {arquivo:<25} ({tamanho_kb:.1f} KB)")
            incluir_complementares.append(arquivo)

    # 3. Compactação no arquivo .zip
    print(f"\nCompactando em '{NOME_ZIP}'...")
    with zipfile.ZipFile(NOME_ZIP, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for arq in ARQUIVOS_OBRIGATORIOS + incluir_complementares:
            zipf.write(arq, arcname=arq)
            print(f"  + Adicionado ao zip: {arq}")

    tamanho_final_mb = os.path.getsize(NOME_ZIP) / (1024 * 1024)
    print(f"\n🎉 Pacote '{NOME_ZIP}' gerado com sucesso! Tamanho: {tamanho_final_mb:.2f} MB")
    print("Pronto para envio na plataforma da FIAP!")
    return True

if __name__ == "__main__":
    validar_e_gerar_zip()
