"""Sentence embedding and similarity calculation."""
import logging
from typing import List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


class SimilarityCalculator:
    """Calculates semantic similarity using sentence embeddings."""
    
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """Initialize the similarity calculator."""
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self._cache = {}
        logger.info(f"Model loaded. Embedding dimension: {self.model.get_sentence_embedding_dimension()}")
        
    def get_embedding(self, text: str) -> np.ndarray:
        """Get embedding for text (with caching)."""
        if text in self._cache:
            logger.debug(f"Cache hit for text (length: {len(text)})")
            return self._cache[text]
        
        logger.debug(f"Computing embedding for text (length: {len(text)})")
        embedding = self.model.encode(text, convert_to_numpy=True)
        self._cache[text] = embedding
        return embedding
    
    def calculate_distance(self, text1: str, text2: str) -> float:
        """Calculate cosine distance between two texts."""
        emb1 = self.get_embedding(text1).reshape(1, -1)
        emb2 = self.get_embedding(text2).reshape(1, -1)
        
        similarity = cosine_similarity(emb1, emb2)[0][0]
        distance = 2 - 2 * similarity
        
        logger.debug(f"Distance: {distance:.4f} | Similarity: {similarity:.4f}")
        return float(distance)
    
    def batch_calculate(self, text_pairs: List[Tuple[str, str]]) -> List[float]:
        """Calculate distances for multiple text pairs."""
        distances = []
        for i, (text1, text2) in enumerate(text_pairs, 1):
            logger.info(f"Processing pair {i}/{len(text_pairs)}")
            distances.append(self.calculate_distance(text1, text2))
        return distances