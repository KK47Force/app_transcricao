import flet as ft
import os
import sys
import traceback
# Importando as funções do app.py
from app import convert_to_wav, transcribe_audio

# Definindo constantes para cores e estilos reutilizáveis
COR_PRINCIPAL = "#6366F1"
COR_TEXTO_SECUNDARIO = "#71757E"
COR_BORDA = "#E0E3EA"
COR_FUNDO = "#FFFFFF"
COR_ALERTA = "#FF5252"
COR_TEXTO_PRINCIPAL = "#1A1D21"
COR_SUCESSO = "#4CAF50"  # Cor verde para o botão de copiar


def main(page: ft.Page):
    # Configuração da página
    page.title = "Transcrição de Áudio"
    page.window.width = 540
    page.window.height = 650
    page.bgcolor = COR_FUNDO
    page.padding = 0
    page.window.center()

    # Variável para armazenar o caminho do arquivo selecionado
    arquivo_selecionado = ft.Text("", size=0)  # Tamanho 0 para não ser visível

    # Função para criar botões com estilo padronizado
    def criar_botao(texto, icone, cor_icone, cor_bg, cor_texto, borda=None, desativado=False):
        return ft.ElevatedButton(
            texto,
            icon=icone,
            icon_color=cor_icone,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=6),
                color=cor_texto,
                bgcolor=cor_bg,
                side=borda,
            ),
            disabled=desativado,
        )    
    
    # Função para mostrar mensagens de status
    def mostrar_status(mensagem, cor=COR_TEXTO_SECUNDARIO):
        mensagem_status.value = mensagem
        mensagem_status.color = cor
        # Garante que a mensagem seja exibida imediatamente
        page.update()

    # Função para copiar o texto da transcrição
    def copiar_transcricao(e):
        # Verificamos se há texto para copiar
        if len(area_transcricao.content.controls) == 1 and isinstance(area_transcricao.content.controls[0], ft.Text):
            texto = area_transcricao.content.controls[0].value
            page.set_clipboard(texto)
            mostrar_status(
                "Texto copiado para a área de transferência!", COR_SUCESSO)
        else:
            mostrar_status("Não há texto para copiar.", COR_ALERTA)

    # Função para selecionar arquivo de áudio
    def selecionar_arquivo_audio(e):
        escolher_arquivo = ft.FilePicker(
            on_result=processar_arquivo_selecionado)
        page.overlay.append(escolher_arquivo)
        page.update()
        escolher_arquivo.pick_files(
            allowed_extensions=["mp3", "wav", "opus", "ogg", "flac", "aac"],
            dialog_title="Selecionar arquivo de áudio",
        )

    # Função para processar o arquivo selecionado
    def processar_arquivo_selecionado(e):
        if e.files and len(e.files) > 0:
            arquivo_selecionado.value = e.files[0].path
            nome_arquivo = os.path.basename(arquivo_selecionado.value)
            mostrar_status(f"Arquivo selecionado: {nome_arquivo}")

            # Habilitando o botão de transcrever
            botao_transcrever.disabled = False
            page.update()

    # Função para transcrever o áudio
    def iniciar_transcricao(e):
        try:
            if not arquivo_selecionado.value:
                mostrar_status("Nenhum arquivo selecionado.", COR_ALERTA)
                return

            mostrar_status(
                "Iniciando processo de transcrição...", COR_PRINCIPAL)

            # Indicador de progresso
            page.splash = ft.ProgressBar()
            botao_transcrever.disabled = True
            botao_selecionar_arquivo.disabled = True
            page.update()

            # Print para debug
            print(f"Arquivo selecionado: {arquivo_selecionado.value}")

            # Mostrar status de conversão
            mostrar_status("Convertendo o arquivo para WAV...")

            # Converter o arquivo para WAV
            try:
                arquivo_wav = convert_to_wav(arquivo_selecionado.value)
                print(f"Arquivo convertido: {arquivo_wav}")
            except Exception as conv_error:
                print(f"Erro na conversão: {str(conv_error)}")
                mostrar_status(
                    f"Erro na conversão: {str(conv_error)}", COR_ALERTA)
                raise

            # Mostrar status de transcrição
            mostrar_status(
                "Transcrevendo o áudio... Isso pode levar alguns instantes.")

            # Transcrever o áudio
            try:
                texto_transcrito = transcribe_audio(arquivo_wav)
                print(f"Transcrição concluída: {texto_transcrito[:50]}...")
            except Exception as trans_error:
                print(f"Erro na transcrição: {str(trans_error)}")
                mostrar_status(
                    f"Erro na transcrição: {str(trans_error)}", COR_ALERTA)
                raise            # Atualizar a área de transcrição com o texto transcrito
            area_transcricao.content.controls = [
                ft.Text(
                    texto_transcrito,
                    size=14,
                    color=COR_TEXTO_PRINCIPAL,
                    selectable=True,
                )
            ]
            mostrar_status("Transcrição concluída com sucesso!", COR_PRINCIPAL)

            # Habilitar os botões de limpar e copiar
            botao_limpar.disabled = False
            botao_copiar.disabled = False
        except Exception as e:
            print(f"ERRO: {str(e)}")
            print("Detalhes do erro:")
            traceback.print_exc()
            mostrar_status(f"Erro: {str(e)}", COR_ALERTA)
        finally:
            # Remover o indicador de progresso
            page.splash = None
            botao_transcrever.disabled = False
            botao_selecionar_arquivo.disabled = False
            page.update()

    # Função para limpar a transcrição
    def limpar_transcricao(e):
        # Restaurar o conteúdo padrão da área de transcrição
        area_transcricao.content.controls = [
            ft.Text(
                "Nenhuma transcrição ainda",
                italic=True,
                color=COR_TEXTO_SECUNDARIO,
                text_align=ft.TextAlign.CENTER,
                size=14,
            ),
            ft.Text(
                "       Faça upload de um arquivo de áudio para iniciar",
                size=13,
                color=COR_TEXTO_SECUNDARIO,
                text_align=ft.TextAlign.CENTER,
            ),
        ]        # Limpar o arquivo selecionado
        arquivo_selecionado.value = ""
        # Desabilitar os botões de limpar e copiar
        botao_limpar.disabled = True
        botao_copiar.disabled = True
        # Mostrar mensagem de limpeza
        mostrar_status("Transcrição limpa.")
        page.update()

    # Título do aplicativo com ícone
    titulo_app = ft.Row(
        [
            ft.Icon(ft.Icons.HEADPHONES, size=28, color=COR_PRINCIPAL),
            ft.Text("AudioTranscribe", size=22,
                    weight=ft.FontWeight.BOLD, color=COR_PRINCIPAL),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=8,
    )

    # Subtítulo
    subtitulo = ft.Text(
        "       Faça upload de um arquivo de áudio ou grave diretamente para começar",
        size=14,
        color=COR_TEXTO_SECUNDARIO,
        text_align=ft.TextAlign.CENTER,
    )
    # Mensagem de status para informar o usuário sobre o processo
    mensagem_status = ft.Text(
        "",
        size=13,
        color=COR_TEXTO_SECUNDARIO,
        text_align=ft.TextAlign.CENTER,
        selectable=True,  # Permitir selecionar o texto para facilitar a cópia do nome do arquivo
    )

    # Botões para as ações
    botao_selecionar_arquivo = criar_botao(
        "Selecionar arquivo",
        ft.Icons.FOLDER_OPEN,
        COR_FUNDO,
        COR_PRINCIPAL,
        COR_FUNDO
    )
    botao_selecionar_arquivo.on_click = selecionar_arquivo_audio

    botao_gravar_audio = criar_botao(
        "Gravar áudio",
        ft.Icons.MIC,
        COR_PRINCIPAL,
        COR_FUNDO,
        COR_PRINCIPAL,
        ft.BorderSide(1, COR_PRINCIPAL),
        desativado=True  # Mantendo o botão de gravação desativado
    )
    # Botão para iniciar a transcrição
    botao_transcrever = criar_botao(
        "Transcrever",
        ft.Icons.TEXT_SNIPPET,
        COR_FUNDO,
        COR_PRINCIPAL,
        COR_FUNDO,
        desativado=True  # Começa desativado até que um arquivo seja selecionado
    )
    # Ajustando tamanho do botão para facilitar o clique
    botao_transcrever.width = 200
    botao_transcrever.height = 40
    # Definindo o manipulador de evento para o botão de transcrição de forma explícita
    botao_transcrever.on_click = iniciar_transcricao    # Área de upload de áudio
    area_upload = ft.Container(
        content=ft.Column(
            [
                ft.Icon(ft.Icons.UPLOAD_FILE, size=48, color=COR_PRINCIPAL),
                ft.Text("Upload do seu áudio",
                        weight=ft.FontWeight.W_500, size=16),
                ft.Text("Arraste e solte um arquivo de áudio ou clique para navegar",
                        size=13, color=COR_TEXTO_SECUNDARIO),
                ft.Row(
                    [
                        botao_selecionar_arquivo,
                        botao_gravar_audio,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
                ft.Container(
                    content=botao_transcrever,
                    margin=ft.margin.only(top=5),
                    alignment=ft.alignment.center,
                ),
                mensagem_status,  # Mensagem de status abaixo do botão
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        width=500,
        height=260,  # Aumentei a altura para acomodar melhor a mensagem de status
        border=ft.border.all(1, COR_BORDA),
        border_radius=8,
        padding=15,
        margin=ft.margin.symmetric(horizontal=20),
        bgcolor=COR_FUNDO,
    )

    # Título da área de transcrição
    titulo_transcricao = ft.Text(
        "Transcrição",
        size=16,
        weight=ft.FontWeight.BOLD,
        color=COR_TEXTO_PRINCIPAL
    )

    # Área de exibição da transcrição
    area_transcricao = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Nenhuma transcrição ainda",
                    italic=True,
                    color=COR_TEXTO_SECUNDARIO,
                    text_align=ft.TextAlign.CENTER,
                    size=14,
                ),
                ft.Text(
                    "       Faça upload de um arquivo de áudio para iniciar",
                    size=13,
                    color=COR_TEXTO_SECUNDARIO,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            scroll=ft.ScrollMode.AUTO,  # Adicionando scroll para textos longos
        ),
        width=500,
        height=250,
        bgcolor=COR_FUNDO,
        border=ft.border.all(1, COR_BORDA),
        border_radius=8,
        padding=20,
        margin=ft.margin.symmetric(horizontal=20),
        clip_behavior=ft.ClipBehavior.HARD_EDGE
    )    # Botão para limpar a transcrição
    botao_limpar = criar_botao(
        "Limpar transcrição",
        ft.Icons.CLEANING_SERVICES_OUTLINED,
        COR_ALERTA,
        COR_FUNDO,
        COR_ALERTA,
        ft.BorderSide(1, COR_ALERTA),
        desativado=True  # Começa desativado até ter uma transcrição
    )
    botao_limpar.on_click = limpar_transcricao

    # Botão para copiar a transcrição
    botao_copiar = criar_botao(
        "Copiar texto",
        ft.Icons.CONTENT_COPY,
        COR_FUNDO,
        COR_SUCESSO,
        COR_FUNDO,
        None,
        desativado=True  # Começa desativado até ter uma transcrição
    )
    botao_copiar.on_click = copiar_transcricao

    # Conteúdo principal com layout simplificado
    conteudo_principal = ft.Column(
        [
            ft.Container(padding=15),  # Espaçamento superior
            titulo_app,
            ft.Container(padding=5),  # Espaçamento pequeno
            subtitulo,
            ft.Container(padding=15),  # Espaçamento médio
            area_upload,
            ft.Container(padding=15),  # Espaçamento médio
            ft.Container(
                content=titulo_transcricao,
                margin=ft.margin.only(left=20)
            ),
            ft.Container(padding=8),   # Espaçamento pequeno
            area_transcricao,            ft.Container(
                padding=15),  # Espaçamento médio
            ft.Container(
                content=ft.Row(
                    [botao_limpar, botao_copiar],
                    alignment=ft.MainAxisAlignment.END,
                    spacing=10,
                ),
                margin=ft.margin.only(right=20)
            ),
            ft.Container(padding=15),  # Espaçamento inferior
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,  # Scroll apenas na coluna principal
        expand=True,
    )

    # Adiciona o conteúdo à página
    page.add(conteudo_principal)
    page.update()


# Inicia o aplicativo
ft.app(target=main, view=ft.AppView.FLET_APP)
