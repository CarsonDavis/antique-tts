# utils/chunker.py
import nltk
from typing import List


class TextChunker:
    def __init__(self, chunk_size: int = 4000):
        self.chunk_size = chunk_size
        nltk.download("punkt", quiet=True)
        self.sentence_tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")

    def process(self, text: str) -> List[str]:
        sentences = self.sentence_tokenizer.tokenize(text)
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) > self.chunk_size:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += " " + sentence

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks
