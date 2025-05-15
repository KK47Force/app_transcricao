import flet as ft

# Definindo constantes para cores e estilos reutilizáveis
COR_PRINCIPAL = "#6366F1"
COR_TEXTO_SECUNDARIO = "#71757E"
COR_BORDA = "#E0E3EA"
COR_FUNDO = "#FFFFFF"
COR_ALERTA = "#FF5252"
COR_TEXTO_PRINCIPAL = "#1A1D21"


def main(page: ft.Page):
    # Configuração da página
    page.title = "Transcrição de Áudio"
    page.window.width = 540
    page.window.height = 650
    page.bgcolor = COR_FUNDO
    page.padding = 0
    page.window.center()

    # Função para criar botões com estilo padronizado
    def criar_botao(texto, icone, cor_icone, cor_bg, cor_texto, borda=None):
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
        )

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

    # Área de upload de áudio
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
                        criar_botao(
                            "Selecionar arquivo",
                            ft.Icons.FOLDER_OPEN,
                            COR_FUNDO,
                            COR_PRINCIPAL,
                            COR_FUNDO
                        ),
                        criar_botao(
                            "Gravar áudio",
                            ft.Icons.MIC,
                            COR_PRINCIPAL,
                            COR_FUNDO,
                            COR_PRINCIPAL,
                            ft.BorderSide(1, COR_PRINCIPAL)
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        width=500,
        height=190,
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
                    "Faça upload de um arquivo de áudio para iniciar",
                    size=13,
                    color=COR_TEXTO_SECUNDARIO,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
        ),
        width=500,
        height=250,
        bgcolor=COR_FUNDO,
        border=ft.border.all(1, COR_BORDA),
        border_radius=8,
        padding=20,
        margin=ft.margin.symmetric(horizontal=20),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

    # Botão para limpar a transcrição
    botao_limpar = criar_botao(
        "Limpar transcrição",
        ft.Icons.CLEANING_SERVICES_OUTLINED,
        COR_ALERTA,
        COR_FUNDO,
        COR_ALERTA,
        ft.BorderSide(1, COR_ALERTA)
    )

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
            area_transcricao,
            ft.Container(padding=15),  # Espaçamento médio
            ft.Container(
                content=ft.Row(
                    [botao_limpar],
                    alignment=ft.MainAxisAlignment.END,
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
ft.app(target=main)
