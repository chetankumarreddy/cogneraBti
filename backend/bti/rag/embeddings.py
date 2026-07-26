import hashlib
import math
from typing import List

class LocalEmbeddingModel:
    def __init__(self, dimensions: int = 64):
        self.dimensions = dimensions

    def embed(self, text: str) -> List[float]:
        tokens = text.lower().split()
        vec = [0.0] * self.dimensions
        for token in tokens:
            idx = int(hashlib.sha256(token.encode()).hexdigest(), 16) % self.dimensions
            vec[idx] += 1.0
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [round(v / norm, 6) for v in vec]
