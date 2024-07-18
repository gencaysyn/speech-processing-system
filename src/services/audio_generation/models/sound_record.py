import dataclasses

from numpy import ndarray


@dataclasses.dataclass
class SoundRecord:
    audio_array: ndarray
    sample_rate: int
