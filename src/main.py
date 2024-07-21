import logging

import grpc
import librosa

from src.services.nlu.grpc import nlu_pb2_grpc
from src.services.transcription.grpc import transcription_pb2_grpc, transcription_pb2


def run():
    # Transcription Service'e bağlan
    channel = grpc.insecure_channel('localhost:50051')
    transcription_stub = transcription_pb2_grpc.TranscriptionServiceStub(channel)

    # NLU Service'e bağlan
    nlu_channel = grpc.insecure_channel('localhost:50052')
    nlu_stub = nlu_pb2_grpc.NLUServiceStub(nlu_channel)

    def audio_chunks():
        # Audio dosyalarını oku ve gönder
        for i in range(20):  # 20 adım için
            audio_file = f'test.wav'
            audio_data, _ = librosa.load(audio_file, sr=16000)

            yield transcription_pb2.AudioChunk(
                audio_array=audio_data.tobytes(),
                sample_rate=16000,
                sequence_number=i
            )

    # Transcription stream'ini başlat
    transcription_stream = transcription_stub.StreamTranscription(audio_chunks())

    # NLU analizi yap ve sonuçları al
    nlu_results = nlu_stub.AnalyzeText(transcription_stream)

    for result in nlu_results:
        print(f"Sequence: {result.sequence_number}, "
              f"Sentiment: {result.sentiment}, "
              f"Intention: {result.intention}")


if __name__ == '__main__':
    try:
        run()
    except grpc.RpcError as rpc_error:
        logging.error(f"RPC failed: {rpc_error.code()} - {rpc_error.details()}")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")