import logging
import os
from concurrent import futures

import grpc

from nlu_processor import NLUProcessor
from proto import nlu_pb2
from proto import nlu_pb2_grpc
from proto.nlu_pb2_grpc import NLUServiceServicer
import grpc_ssl_config

log_level = os.getenv('LOG_LEVEL', 'ERROR').upper()
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)

class NLUService(NLUServiceServicer):
    def __init__(self):
        self.nlu_processor = NLUProcessor()

    def AnalyzeText(self, request_iterator, context):
        for transcription_result in request_iterator:
            sentiment_result = self.nlu_processor.get_sentiment(transcription_result.text)
            intention_result = self.nlu_processor.get_intention(transcription_result.text)

            yield nlu_pb2.NLUResponse(
                sentiment=sentiment_result,
                intention=intention_result,
                sequence_number=transcription_result.sequence_number
            )


def serve():
    logger.info("Starting NLU server.")
    server_credentials = grpc_ssl_config.get_ssl_server_credentials()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    nlu_pb2_grpc.add_NLUServiceServicer_to_server(
        NLUService(), server)
    server.add_secure_port('[::]:50052', server_credentials)
    logger.info("NLU server started.")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
