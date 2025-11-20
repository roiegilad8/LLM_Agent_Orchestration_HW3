# ADR-002: Embedding Model Selection for Semantic Distance

**Status:** Accepted  
**Date:** November 20, 2025  
**Deciders:** Roie Gilad  
**Supersedes:** None

---

## Context

We need to quantify semantic drift across translation chains. The key challenge is measuring semantic preservation objectively. We need:

1. **Accuracy:** Correctly identify when meaning is lost
2. **Speed:** Process large datasets quickly
3. **Language Coverage:** Support English, French, Hebrew
4. **Reliability:** Consistent results across runs
5. **Low Overhead:** Can run on local hardware

## Decision

We use **Sentence-BERT (all-MiniLM-L6-v2)** as the embedding model with **Cosine Distance** as the distance metric.

### Selected Model
- **Model:** all-MiniLM-L6-v2
- **Framework:** sentence-transformers
- **Dimension:** 384-dimensional embeddings
- **Language Coverage:** 101 languages (including EN, FR, HE)
- **Size:** 22MB (fits in memory)

### Distance Metric
- **Metric:** Cosine Distance (1 - Cosine Similarity)
- **Range:** 0.0 (identical) to 1.0 (orthogonal)
- **Interpretation:** Higher distance = greater semantic drift

---

## Rationale

### Why Sentence-BERT?

**Advantages:**
- ✅ Pre-trained on semantic similarity tasks
- ✅ Works directly with sentences (no tokenization needed)
- ✅ Multilingual support (covers our 3 languages)
- ✅ Fast inference (~milliseconds per sentence)
- ✅ Mature and well-maintained library
- ✅ No GPU required (runs on CPU)
- ✅ Proven in academic research

**Performance:**
- Model size: 22MB (small, fits in memory)
- Inference time: ~5ms per sentence
- Full experiment: ~18 sentences × 3 stages = 54 embeddings

**Accuracy:**
- Tested on semantic similarity benchmarks (STSBM: 0.83 correlation)
- Outperforms basic Word2Vec approaches
- Suitable for detecting meaning changes in translations

### Why Cosine Distance?

**Advantages:**
- ✅ Normalized (0.0-1.0) - easy to interpret
- ✅ Computationally efficient
- ✅ Standard in NLP for embedding comparison
- ✅ Invariant to vector magnitude (important for embeddings)

**Interpretation:**
- 0.0 = perfect semantic match (same meaning)
- 0.3 = high semantic similarity (minor changes)
- 0.5 = moderate semantic distance (some change)
- 0.7+ = low semantic similarity (major changes)

---

## Alternatives Considered

### 1. **GPT Embeddings (OpenAI)**
- ✅ Superior quality
- ❌ Requires API key (not local)
- ❌ Higher cost
- ❌ Dependent on external service
- ❌ **Rejected:** Violates local-first requirement

### 2. **LLaMA Embeddings (Meta)**
- ✅ State-of-the-art quality
- ❌ Large model (7B parameters)
- ❌ Requires significant GPU memory
- ❌ Slow inference
- ❌ **Rejected:** Too resource-intensive

### 3. **Word2Vec/FastText**
- ✅ Fast and lightweight
- ❌ Word-level, not sentence-level
- ❌ Poor for multilingual
- ❌ Doesn't capture word order/context
- ❌ **Rejected:** Insufficient for semantic task

### 4. **Euclidean Distance**
- ✅ Simple and fast
- ❌ Not normalized
- ❌ Sensitive to embedding magnitude
- ❌ Poor for high-dimensional spaces
- ❌ **Rejected:** Cosine is superior

### 5. **Edit Distance (BLEU Score)**
- ✅ Word-level precision
- ❌ Only measures lexical overlap
- ❌ Ignores semantic meaning
- ❌ Biased toward word order
- ❌ **Rejected:** Not semantic-based

---

## Implementation

### Code

```python
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

class SimilarityCalculator:
    """Calculate semantic distance between sentences."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
    
    def get_distance(self, text1: str, text2: str) -> float:
        """Calculate cosine distance between two texts."""
        if not text1 or not text2:
            return 1.0  # Maximum distance for empty strings
        
        embedding1 = self.model.encode(text1, convert_to_tensor=False)
        embedding2 = self.model.encode(text2, convert_to_tensor=False)
        
        distance = cosine(embedding1, embedding2)
        return float(distance)
```

### Performance Metrics

**Embedding Generation:**
- Time: ~5ms per sentence (CPU)
- Memory: 22MB model + ~384 bytes per embedding
- Caching: Optional for repeated texts

**Full Experiment:**
- 18 experiment configurations
- 3 stages per config = 54 embeddings total
- Expected runtime: < 1 second for all embeddings

---

## Validation & Testing

### Unit Tests
```python
def test_identical_strings():
    calc = SimilarityCalculator()
    distance = calc.get_distance("hello world", "hello world")
    assert distance < 0.01  # Nearly identical
    
def test_different_strings():
    calc = SimilarityCalculator()
    distance = calc.get_distance("hello world", "goodbye moon")
    assert 0.3 < distance < 0.7  # Moderately different
    
def test_empty_strings():
    calc = SimilarityCalculator()
    distance = calc.get_distance("", "hello")
    assert distance == 1.0  # Maximum distance
```

### Coverage
- ✅ Edge cases tested
- ✅ Multilingual verified (EN, FR, HE)
- ✅ Consistency checked (same input = same output)

---

## Consequences

### Positive
- ✅ Semantic measurements are objective and reproducible
- ✅ Results are interpretable (0.0-1.0 range)
- ✅ No external dependencies or API calls
- ✅ Fast enough for real-time applications
- ✅ Proven in academic literature

### Negative
- ⚠️ Pre-trained model may have biases
- ⚠️ Not perfect for all semantic changes
- ⚠️ Requires first inference for embedding cache

### Mitigation
- Use multiple test sentences to verify robustness
- Document limitations in README
- Compare results with alternative metrics if needed

---

## Monitoring & Maintenance

**Metrics to Track:**
- Consistency of distance calculations
- Coverage across language pairs
- Performance over time

**Update Strategy:**
- Monitor new embedding models
- Re-evaluate if better models become available
- Stay with current model unless significant improvements appear

---

## Related Decisions

- ADR-001: Multi-Agent Orchestration Pattern
- ADR-003: Error Injection Strategy

---

## References

- Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. arXiv preprint arXiv:1908.10084
- Sentence-Transformers Documentation: https://www.sbert.net/
- Cosine Similarity in NLP: https://en.wikipedia.org/wiki/Cosine_similarity
