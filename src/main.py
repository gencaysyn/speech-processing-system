from src.services.audio_generation.audio_generation_service import AudioGenerationService

audio_generation_service = AudioGenerationService()
sf = audio_generation_service.text_to_audio("New york city can be a terrified place.")
audio_generation_service.write_audio_to_file("test.wav", sf)
