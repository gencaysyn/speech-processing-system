import logging
import os

import grpc
import librosa

from nlu.src.proto import nlu_pb2_grpc
from transcription.src.proto import transcription_pb2
from transcription.src.proto import transcription_pb2_grpc


def run():
    with open('../ssl/ca.cert', 'rb') as f:
        ca_cert = f.read()
    with open('../ssl/client.key', 'rb') as f:
        client_key = f.read()
    with open('../ssl/client.cert', 'rb') as f:
        client_cert = f.read()

    credentials = grpc.ssl_channel_credentials(
        root_certificates=ca_cert,
        private_key=client_key,
        certificate_chain=client_cert
    )

    channel = grpc.secure_channel('localhost:50051', credentials)
    transcription_stub = transcription_pb2_grpc.TranscriptionServiceStub(channel)

    nlu_channel = grpc.secure_channel('localhost:50052', credentials)
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
