# Aplicativo de Transcrição de Áudio (v1.0)

Este aplicativo converte arquivos de áudio em diferentes formatos para texto utilizando reconhecimento de fala via Google Speech Recognition.

## Estrutura do Projeto

```
app_transcricao/
├── app.py          # Script principal de transcrição (versão 1.0)
├── app_grafig.py   # Interface gráfica para transcrição de áudio
├── app_grafig_ia.py # Interface gráfica com melhoria de texto via IA
```

## Como Usar o Aplicativo

1. Coloque seus arquivos de áudio na mesma pasta do script `app.py`

2. Execute o script:
   ```
   python app.py
   ```

3. Quando solicitado, digite o nome do arquivo de áudio que deseja transcrever (ex: `audio.opus`)

4. O aplicativo irá:
   - Verificar se o arquivo precisa ser convertido para WAV
   - Converter o arquivo se necessário (usando FFmpeg)
   - Carregar e transcrever o áudio
   - Melhorar automaticamente a transcrição de áudio usando IA generativa
   - Exibir o texto transcrito e o texto melhorado no terminal

## Interface Gráfica (app_grafig.py)

O arquivo `app_grafig.py` é uma extensão do `app.py` que fornece uma interface gráfica amigável para o processo de transcrição de áudio. Ele utiliza a biblioteca Flet (baseada em Flutter) para criar uma aplicação desktop moderna e responsiva.

### Características do app_grafig.py:

- Interface gráfica intuitiva para selecionar e transcrever arquivos de áudio
- Suporte para os mesmos formatos de áudio que o script em linha de comando
- Exibição visual do texto transcrito com opções para copiar e limpar
- Indicadores visuais do progresso durante o processamento
- Layout moderno e responsivo compatível com Windows, macOS e Linux

### Como executar a interface gráfica:

```
python app_grafig.py
```

## Interface Gráfica com IA (app_grafig_ia.py)

O arquivo `app_grafig_ia.py` é uma versão avançada da interface gráfica que adiciona o recurso de melhoria de texto usando a API do Google Gemini. Além de todas as funcionalidades do `app_grafig.py`, ele:

- Melhora automaticamente a transcrição de áudio usando IA generativa
- Apresenta o texto original e o texto melhorado lado a lado
- Permite copiar ou limpar ambas as versões do texto independentemente
- Corrige automaticamente erros de pontuação, gramática e coerência

### Configuração da API do Gemini

Para usar a versão com IA, é necessário:

1. Obter uma chave de API do Google Gemini em: https://aistudio.google.com/app/apikey
2. Criar um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
   ```
   GEMINI_KEY=sua_chave_api_aqui
   ```

### Como executar a versão com IA:

```
python app_grafig_ia.py
```

## Requisitos

- Python 3.6+
- Pacotes Python: speech_recognition, pydub, flet, python-dotenv, google-generativeai
- FFmpeg
- Chave de API do Google Gemini (para a versão com IA)

## Instalação do FFmpeg

O FFmpeg é necessário para converter arquivos de áudio de diversos formatos para o formato WAV, que é o formato aceito pelo reconhecedor de fala.

### Windows

1. Baixe o FFmpeg do site oficial: https://ffmpeg.org/download.html
   - Recomendamos baixar o build estático de https://www.gyan.dev/ffmpeg/builds/ (versão "ffmpeg-release-full")

2. Extraia o arquivo zip para uma pasta de sua escolha (ex: `C:\ffmpeg`)

3. Adicione a pasta bin do FFmpeg ao PATH do sistema:
   - Clique com o botão direito em "Este Computador" e selecione "Propriedades"
   - Clique em "Configurações avançadas do sistema"
   - Clique no botão "Variáveis de Ambiente"
   - Na seção "Variáveis do Sistema", selecione a variável "Path" e clique em "Editar"
   - Clique em "Novo" e adicione o caminho para a pasta bin (ex: `C:\ffmpeg\bin`)
   - Clique em "OK" para fechar todas as janelas

4. Verifique a instalação abrindo o Prompt de Comando e digitando:
   ```
   ffmpeg -version
   ```

### Instalação dos pacotes Python

Para a versão básica em linha de comando:
```
pip install SpeechRecognition pydub
```

Para a versão com interface gráfica:
```
pip install -r requirements.txt
```

## Por que converter para WAV?

É necessário converter arquivos de áudio para o formato WAV porque o Speech Recognition só processa diretamente arquivos neste formato. O WAV é um formato sem compressão que preserva toda a qualidade do áudio original, permitindo uma análise mais precisa dos padrões de fala pelo algoritmo de reconhecimento.

Outros formatos como MP3, OPUS, OGG ou AAC são formatos comprimidos que, embora economizem espaço, podem perder detalhes sutis necessários para um reconhecimento de fala eficiente. O FFmpeg realiza esta conversão automaticamente durante a execução do script para garantir a compatibilidade.

## Limitações

- A qualidade da transcrição depende da clareza do áudio e pode variar

## Formatos Suportados

- WAV (formato nativo)
- MP3
- OGG
- FLAC
- AAC
- OPUS

## Resolução de Problemas

Se você encontrar erros relacionados ao FFmpeg, verifique se:
1. O FFmpeg está corretamente instalado
2. O diretório do FFmpeg está adicionado ao PATH do sistema
3. O comando `ffmpeg -version` funciona no terminal/prompt de comando