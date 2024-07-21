import librosa
from transformers import WhisperProcessor, WhisperForConditionalGeneration

from src.services.common.models.sound_record import SoundRecord


class TranscriptionProcessor:
    def __init__(self):
        self.processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
        self.model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")
        self.model.config.forced_decoder_ids = None

    def audio_to_text(self, sound_record: SoundRecord) -> str:
        if sound_record.sample_rate != 16000:
            raise ValueError("sample_rate must be 16000, provided {}.".format(sound_record.sample_rate))

        input_features = self.processor(sound_record.audio_array, sampling_rate=sound_record.sample_rate,
                                        return_tensors="pt").input_features

        predicted_ids = self.model.generate(input_features)
        return self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0].strip()

    def read_audio(self, file_name: str) -> SoundRecord:
        audio_array, sample_rate = librosa.load(file_name, sr=16000)
        return SoundRecord(audio_array=audio_array, sample_rate=sample_rate)

