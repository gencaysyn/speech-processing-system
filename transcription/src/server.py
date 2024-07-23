import logging
import os
from concurrent import futures

import grpc
import numpy as np

import grpc_ssl_config
from models.sound_record import SoundRecord
from proto import transcription_pb2
from proto.transcription_pb2_grpc import TranscriptionServiceServicer, \
    add_TranscriptionServiceServicer_to_server
from transcription_processor import TranscriptionProcessor

log_level = os.getenv('LOG_LEVEL', 'ERROR').upper()
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)


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
    logger.info("Starting transcription server.")
    server_credentials = grpc_ssl_config.get_ssl_server_credentials()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_TranscriptionServiceServicer_to_server(
        TranscriptionService(), server)
    server.add_secure_port('[::]:50051', server_credentials)
    server.start()
    logger.info("Transcription server started.")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
