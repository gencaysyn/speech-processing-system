import grpc
from concurrent import futures

from src.services.transcription.grpc import transcription_pb2_grpc, transcription_pb2
from src.services.transcription.transcription_processor import TranscriptionProcessor


class TranscriptionService(transcription_pb2_grpc.TranscriptionServiceServicer):
    def __init__(self):
        self.transcription_processor = TranscriptionProcessor()
    async def StreamTranscripts(self, request_iterator, context):
        async for request in request_iterator:
            transcript = await self.transcribe(request.audio_file_path)
            yield transcription_pb2.TranscriptResponse(transcript=transcript)

    async def transcribe(self, audio_file_path) -> str:
        sr = self.transcription_processor.read_audio(audio_file_path)
        return self.transcription_processor.audio_to_text(sr)


async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    transcription_pb2_grpc.add_TranscriptionServiceServicer_to_server(TranscriptionService(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    import asyncio

    asyncio.run(serve())
