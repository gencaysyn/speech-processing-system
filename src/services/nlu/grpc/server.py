import grpc
from concurrent import futures
import nlu_pb2
import nlu_pb2_grpc
from src.services.nlu.nlu_processor import NLUProcessor


class NLUService(nlu_pb2_grpc.NLUServiceServicer):

    def __init__(self):
        self.nlu_processor = NLUProcessor()

    async def StreamAnalysis(self, request_iterator, context):
        async for request in request_iterator:
            sentiment, intention = await self.analyze(request.transcript)
            yield nlu_pb2.NLUResponse(sentiment=sentiment, intention=intention)

    async def analyze(self, transcript: str):

        return self.nlu_processor.get_sentiment(transcript), self.nlu_processor.get_intention(transcript)


async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    nlu_pb2_grpc.add_NLUServiceServicer_to_server(NLUService(), server)
    server.add_insecure_port('[::]:50052')
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    import asyncio

    asyncio.run(serve())