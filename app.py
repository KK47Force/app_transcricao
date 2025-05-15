import os
import speech_recognition as sr
from pydub import AudioSegment
import subprocess
import sys


def check_ffmpeg():
    """Verifica se o FFmpeg está instalado no sistema."""
    try:
        # Tentando executar o comando ffmpeg para verificar se está instalado
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def convert_to_wav(file_path):
    """Converte um arquivo de áudio para o formato WAV e salva na mesma pasta."""
    base, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == ".wav":
        return file_path  # Já está no formato correto

    if ext in [".mp3", ".ogg", ".flac", ".aac", ".opus"]:
        # Verificar se o FFmpeg está instalado
        if not check_ffmpeg():
            print(
                "ERRO: FFmpeg não encontrado! Necessário para converter arquivos de áudio.")
            print("Por favor, instale o FFmpeg (https://ffmpeg.org/download.html) e adicione-o ao PATH do sistema.")
            sys.exit(1)

        # Criando o caminho completo para o arquivo convertido
        dir_path = os.path.dirname(file_path)
        file_name = os.path.basename(base)
        converted_file = os.path.join(dir_path, f"{file_name}.wav")

        try:
            # Usando FFmpeg diretamente via subprocess para maior compatibilidade
            if ext == ".opus":
                subprocess.run(
                    ["ffmpeg", "-i", file_path, "-y", converted_file],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True
                )
            else:
                # Para outros formatos, continue usando o pydub
                audio = AudioSegment.from_file(file_path, format=ext[1:])
                audio.export(converted_file, format="wav")

            print(f"Arquivo convertido para: {converted_file}")
            return converted_file
        except subprocess.SubprocessError as e:
            raise ValueError(f"Erro ao converter o arquivo: {e}")

    raise ValueError(f"Formato de arquivo {ext} não suportado para conversão.")


def transcribe_audio(file_path):
    """Transcreve o áudio de um arquivo WAV. Se o áudio for maior que 1 minuto,
    divide em partes, transcreve cada parte e une os resultados."""
    recognizer = sr.Recognizer()

    try:
        # Carregando o arquivo de áudio com pydub para verificar sua duração
        audio = AudioSegment.from_file(file_path)
        duration_seconds = len(audio) / 1000  # Duração em segundos

        # Se o áudio for maior que 1 minuto, vamos dividi-lo
        if duration_seconds > 60:
            print(
                f"Áudio com duração de {duration_seconds/60:.2f} minutos. Dividindo em partes...")

            # Calcular quantos segmentos de 1 minuto teremos
            segment_length_ms = 60 * 1000  # 1 minuto em milissegundos
            total_segments = int(duration_seconds / 60) + \
                (1 if duration_seconds % 60 > 0 else 0)

            complete_transcription = ""
            for i in range(total_segments):
                print(f"Processando parte {i+1} de {total_segments}...")

                # Extrair o segmento atual
                start_ms = i * segment_length_ms
                end_ms = min((i + 1) * segment_length_ms, len(audio))
                segment = audio[start_ms:end_ms]

                # Salvar o segmento em um arquivo temporário
                temp_segment_path = file_path + f"_segment_{i}.wav"
                segment.export(temp_segment_path, format="wav")

                # Transcrever o segmento
                with sr.AudioFile(temp_segment_path) as source:
                    audio_data = recognizer.record(source)
                    segment_text = recognizer.recognize_google(
                        audio_data, language="pt-BR")

                # Adicionar à transcrição completa com um espaço entre cada segmento
                if complete_transcription:
                    complete_transcription += " " + segment_text
                else:
                    complete_transcription = segment_text

                # Remover o arquivo temporário
                os.remove(temp_segment_path)

            print("Todas as partes foram transcritas e unidas.")
            return complete_transcription
        else:
            # Áudio curto, transcrição normal
            with sr.AudioFile(file_path) as source:
                print("Carregando o áudio para transcrição...")
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(
                    audio_data, language="pt-BR")
                return text
    except sr.UnknownValueError:
        return "Não foi possível entender o áudio."
    except sr.RequestError as e:
        return f"Erro no serviço de reconhecimento de fala: {e}"
    except Exception as e:
        return f"Erro ao processar o áudio: {e}"


def main():
    # Obtém o diretório base onde o script está sendo executado
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Solicitar apenas o nome do arquivo ao usuário
    file_name = input(
        "Digite o nome do arquivo de áudio (ex: audio.opus): ").strip()

    # Combina o diretório base com o nome do arquivo para formar o caminho completo
    file_path = os.path.join(base_dir, file_name)

    if not os.path.exists(file_path):
        print(
            f"Arquivo '{file_name}' não encontrado na pasta do aplicativo. Verifique o nome e tente novamente.")
        return

    try:
        print("Verificando formato do arquivo...")
        # Convertendo o arquivo para formato WAV se necessário
        compatible_file = convert_to_wav(file_path)

        print("Transcrevendo o áudio...")
        transcription = transcribe_audio(compatible_file)
        print("Transcrição concluída:")
        print(transcription)
    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()
