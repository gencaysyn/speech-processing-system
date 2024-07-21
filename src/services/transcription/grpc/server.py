from concurrent import futures

import grpc
import numpy as np

from src.services.common.models.sound_record import SoundRecord
from src.services.transcription.grpc import transcription_pb2
from src.services.transcription.grpc.transcription_pb2_grpc import TranscriptionServiceServicer, \
    add_TranscriptionServiceServicer_to_server
from src.services.transcription.transcription_processor import TranscriptionProcessor


class TranscriptionService(TranscriptionServiceServicer):

    def __init__(self):
        self.transcription_processor = TranscriptionProcessor()

    def StreamTranscription(self, request_iterator, context):
        for audio_chunk in request_iterator:
            audio_np = np.frombuffer(audio_chunk.audio_array, dtype=np.float32)

            sr = SoundRecord(audio_array=audio_np, sample_rate=audio_chunk.sample_rate)
            result = self.transcription_processor.audio_to_text(sr)

            yield transcription_pb2.TranscriptionResult(
                text=result,
                sequence_number=audio_chunk.sequence_number
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_TranscriptionServiceServicer_to_server(
        TranscriptionService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
