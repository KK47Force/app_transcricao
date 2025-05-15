# Aplicativo de Transcrição de Áudio (v1.0)

Este aplicativo converte arquivos de áudio em diferentes formatos para texto utilizando reconhecimento de fala via Google Speech Recognition.

## Estrutura do Projeto

```
app_transcricao/
├── app.py          # Script principal de transcrição (versão 1.0)
```

## Requisitos

- Python 3.6+
- Pacotes Python: speech_recognition, pydub
- FFmpeg

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

```
pip install SpeechRecognition pydub
```

## Por que converter para WAV?

É necessário converter arquivos de áudio para o formato WAV porque o Speech Recognition só processa diretamente arquivos neste formato. O WAV é um formato sem compressão que preserva toda a qualidade do áudio original, permitindo uma análise mais precisa dos padrões de fala pelo algoritmo de reconhecimento.

Outros formatos como MP3, OPUS, OGG ou AAC são formatos comprimidos que, embora economizem espaço, podem perder detalhes sutis necessários para um reconhecimento de fala eficiente. O FFmpeg realiza esta conversão automaticamente durante a execução do script para garantir a compatibilidade.

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
   - Exibir o texto transcrito no terminal

## Limitações

- O reconhecimento de fala via Google tem um limite aproximado de 60 segundos por arquivo
- Para áudios mais longos, é recomendado dividi-los em segmentos menores
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