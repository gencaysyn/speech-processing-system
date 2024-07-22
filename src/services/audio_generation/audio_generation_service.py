# This service just created to generate test data
import json

from optimum.bettertransformer import BetterTransformer
from scipy.io.wavfile import write as write_wav
from transformers import AutoProcessor, BarkModel

from src.services.audio_generation.constants.voice_presets import VoicePresets
from src.services.common.models.sound_record import SoundRecord


class AudioGenerationService:
    def __init__(self):
        self.processor = AutoProcessor.from_pretrained("suno/bark")
        self.model = BetterTransformer.transform(BarkModel.from_pretrained("suno/bark"), keep_original_model=False)

    def text_to_audio(self, text: str, voice_preset: str = VoicePresets.EN_MALE_SPEAKER) -> SoundRecord:
        inputs = self.processor(text, voice_preset=voice_preset)

        audio_array = self.model.generate(**inputs).cpu().numpy().squeeze()
        sample_rate = self.model.generation_config.sample_rate
        return SoundRecord(audio_array=audio_array, sample_rate=sample_rate)

    def write_audio_to_file(self, file_name: str, sample: SoundRecord):
        if not file_name.endswith(".wav"):
            raise ValueError("File name must end with .wav")
        write_wav(file_name, sample.sample_rate, sample.audio_array)


if __name__ == "__main__":
    ags = AudioGenerationService()

    with open("../../../data/customer-employee-conversation.json") as f:
        conversation_obj = json.load(f)

    for c in conversation_obj["conversation"]:
        sr = ags.text_to_audio(c["message"],
                               VoicePresets.EN_MALE_SPEAKER
                               if c["role"] == "employee"
                               else VoicePresets.EN_FEMALE_SPEAKER)
        ags.write_audio_to_file(f"../../../data/audio/{c["sequence"]}_{c["role"]}.wav", sr)

