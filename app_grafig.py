import flet as ft


def main(page: ft.Page):
    # Configuração da página com scroll habilitado explicitamente
    page.title = "Transcrição de Áudio"
    page.window.width = 540
    page.window.height = 650
    page.bgcolor = "#FFFFFF"
    page.scroll = ft.ScrollMode.AUTO  # Habilitando scroll na página
    page.padding = 0

    # Centralizar a janela na tela
    page.window.center()

    # Título do aplicativo com ícone
    titulo_app = ft.Row(
        [
            ft.Icon(ft.Icons.HEADPHONES, size=28, color="#6366F1"),
            ft.Text("AudioTranscribe", size=22,
                    weight=ft.FontWeight.BOLD, color="#6366F1"),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=8,
    )

    # Subtítulo
    subtitulo = ft.Text(
        "       Faça upload de um arquivo de áudio ou grave diretamente para começar",
        size=14,
        color="#71757E",
        text_align=ft.TextAlign.CENTER,
    )

    # Área de upload de áudio - ajustada para ficar igual à imagem
    area_upload = ft.Container(
        content=ft.Column(
            [
                # Ícone de upload com arquivo - ajustado para o formato exato da imagem
                ft.Icon(ft.Icons.UPLOAD_FILE, size=48, color="#6366F1"),
                ft.Text("Upload do seu áudio",
                        weight=ft.FontWeight.W_500, size=16),
                ft.Text("Arraste e solte um arquivo de áudio ou clique para navegar",
                        size=13, color="#71757E"),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Selecionar arquivo",
                            icon=ft.Icons.FOLDER_OPEN,
                            icon_color="#FFFFFF",
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=6),
                                color="#FFFFFF",
                                bgcolor="#6366F1",
                            ),
                        ),
                        ft.ElevatedButton(
                            "Gravar áudio",
                            icon=ft.Icons.MIC,
                            icon_color="#6366F1",
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=6),
                                color="#6366F1",
                                bgcolor="#FFFFFF",
                                side=ft.BorderSide(1, "#6366F1"),
                            ),
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
        border=ft.border.all(1, "#E0E3EA"),
        border_radius=8,
        padding=15,
        margin=ft.margin.only(left=20, right=20),
        bgcolor="#FFFFFF",
    )

    # Título da área de transcrição
    titulo_transcricao = ft.Text(
        "Transcrição",
        size=16,
        weight=ft.FontWeight.BOLD,
        color="#1A1D21"
    )

    # Área de exibição da transcrição
    area_transcricao = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Nenhuma transcrição ainda",
                    italic=True,
                    color="#71757E",
                    text_align=ft.TextAlign.CENTER,
                    size=14,
                ),
                ft.Text(
                    "Faça upload de um arquivo de áudio para iniciar",
                    size=13,
                    color="#71757E",
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            scroll=ft.ScrollMode.AUTO,
        ),
        width=500,
        height=250,
        bgcolor="#FFFFFF",
        border=ft.border.all(1, "#E0E3EA"),
        border_radius=8,
        padding=20,
        margin=ft.margin.only(left=20, right=20),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

    # Adiciona um botão para limpar a transcrição
    botao_limpar = ft.ElevatedButton(
        "Limpar transcrição",
        icon=ft.Icons.CLEANING_SERVICES_OUTLINED,
        icon_color="#FF5252",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=6),
            color="#FF5252",
            bgcolor="#FFFFFF",
            side=ft.BorderSide(1, "#FF5252"),
        ),
    )

    # Container principal com scroll usando Container ao invés de Column diretamente
    # Isso garante que o scroll funcione corretamente
    conteudo_principal = ft.Container(
        content=ft.Column(
            [
                ft.Container(height=15),
                titulo_app,
                ft.Container(height=5),
                subtitulo,
                ft.Container(height=15),
                area_upload,
                ft.Container(height=15),
                ft.Container(
                    content=titulo_transcricao,
                    margin=ft.margin.only(left=20)
                ),
                ft.Container(height=8),
                area_transcricao,
                ft.Container(height=15),
                ft.Container(
                    content=ft.Row(
                        [botao_limpar],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    margin=ft.margin.only(right=20)
                ),
                ft.Container(height=15),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,  # Scroll na coluna
        ),
        expand=True,  # Importante: permite que o container se expanda conforme necessário
    )

    # Adiciona o conteúdo principal à página em um ScrollableControl
    page.add(
        ft.ListView(
            [conteudo_principal],
            expand=True,
            spacing=0,
            padding=0,
            auto_scroll=False
        )
    )

    # Garantir que a página seja atualizada
    page.update()


# Inicia o aplicativo
ft.app(target=main)
