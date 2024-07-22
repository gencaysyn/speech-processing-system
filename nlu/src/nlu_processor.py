from typing import List

from transformers import pipeline


class NLUProcessor:
    def __init__(self):
        self.zeroshot_classifier = pipeline("zero-shot-classification",
                                            model="MoritzLaurer/deberta-v3-large-zeroshot-v2.0")

    def analyze(self, text: str, hypothesis_template: str, classes_verbalized: List[str]) -> str:
        output = self.zeroshot_classifier(text, classes_verbalized, hypothesis_template=hypothesis_template,
                                          multi_label=False)

        mapped_list = list(zip(output["labels"], output["scores"]))
        return max(mapped_list, key=lambda x: x[1])[0]

    def get_sentiment(self, text: str,
                      hypothesis_template: str = "Sentiment of this text is {}.",
                      classes_verbalized: List[str] = None) -> str:
        if classes_verbalized is None:
            classes_verbalized = ["positive", "negative", "neutral"]
        return self.analyze(text, hypothesis_template, classes_verbalized)

    def get_intention(self, text: str, hypothesis_template: str = "Intention of this text is {}.",
                      classes_verbalized: List[str] = None) -> str:
        if classes_verbalized is None:
            classes_verbalized = ["change_package", "upgrade", "learn_price", "product_detail"]
        return self.analyze(text, hypothesis_template, classes_verbalized)