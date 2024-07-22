import os
import logging

import grpc
import librosa

from nlu.src.proto import nlu_pb2_grpc
from transcription.src.proto import transcription_pb2_grpc
from transcription.src.proto import transcription_pb2


def run():
    channel = grpc.insecure_channel('localhost:50051')
    transcription_stub = transcription_pb2_grpc.TranscriptionServiceStub(channel)

    nlu_channel = grpc.insecure_channel('localhost:50052')
    nlu_stub = nlu_pb2_grpc.NLUServiceStub(nlu_channel)

    def audio_chunks():
        files = os.listdir("../data/audio")
        for f in files:
            if f.endswith(".wav"):
                sequence = f.split("_")[0]
                audio_data, _ = librosa.load(f"../data/audio/{f}", sr=16000)

                yield transcription_pb2.AudioChunk(
                    audio_array=audio_data.tobytes(),
                    sample_rate=16000,
                    sequence_number=int(sequence)
                )

    transcription_stream = transcription_stub.StreamTranscription(audio_chunks())

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