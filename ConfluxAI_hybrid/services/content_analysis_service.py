"""
Content Analysis Service for ConfluxAI (Simplified Version)
Provides content classification, entity extraction, and sentiment analysis
"""
import logging
import asyncio
import re
from typing import List, Dict, Any, Optional, Tuple, Union
from datetime import datetime
from collections import Counter

from models.schemas import ProcessingResult
from config.settings import Settings

logger = logging.getLogger(__name__)

# Simple version without AI dependencies for Phase 3 foundation
class ContentClassification:
    """Content classification result"""
    def __init__(self, document_type: str, confidence: float, topics: List[Tuple[str, float]], 
                 sentiment: Dict[str, float], language: str, complexity_score: float):
        self.document_type = document_type
        self.confidence = confidence
        self.topics = topics
        self.sentiment = sentiment
        self.language = language
        self.complexity_score = complexity_score
        self.timestamp = datetime.now()

class EntityExtractionResult:
    """Entity extraction result"""
    def __init__(self, entities: List[Dict[str, Any]], relationships: List[Dict[str, Any]], 
                 entity_counts: Dict[str, int], confidence_score: float):
        self.entities = entities
        self.relationships = relationships
        self.entity_counts = entity_counts
        self.confidence_score = confidence_score
        self.timestamp = datetime.now()

class ContentAnalysisService:
    """Advanced content analysis with classification and entity extraction"""
    
    def __init__(self):
        self.settings = Settings()
        self.initialized = False
        
        # Document type classification keywords
        self.document_types = {
            'technical': ['algorithm', 'system', 'architecture', 'implementation', 'code', 'technical', 'software', 'hardware'],
            'legal': ['contract', 'agreement', 'law', 'legal', 'regulation', 'compliance', 'policy', 'terms'],
            'academic': ['research', 'study', 'analysis', 'paper', 'journal', 'academic', 'university', 'education'],
            'business': ['business', 'strategy', 'market', 'financial', 'revenue', 'customer', 'company', 'corporate'],
            'medical': ['medical', 'health', 'patient', 'treatment', 'diagnosis', 'clinical', 'healthcare'],
            'news': ['news', 'report', 'article', 'journalist', 'media', 'press', 'breaking'],
            'manual': ['manual', 'guide', 'instructions', 'how-to', 'tutorial', 'steps', 'procedure']
        }
        
        # Sentiment keywords
        self.positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'like', 'happy', 'joy']
        self.negative_words = ['bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike', 'sad', 'angry', 'disappointed', 'frustrated']
    
    
    async def initialize(self):
        """Initialize content analysis service"""
        try:
            logger.info("Initializing Content Analysis service (rule-based version)...")
            self.initialized = True
            logger.info("Content Analysis service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Content Analysis service: {str(e)}")
            self.initialized = False
    
    async def classify_content(self, text: str) -> ContentClassification:
        """
        Classify content into document types with topic modeling and sentiment analysis
        
        Args:
            text: Input text to classify
            
        Returns:
            ContentClassification with document type, topics, sentiment, etc.
        """
        try:
            start_time = datetime.now()
            
            # Detect language (simple heuristic)
            language = self._detect_language_simple(text)
            
            # Classify document type
            doc_type, doc_confidence = self._classify_document_type(text)
            
            # Extract topics
            topics = self._extract_topics(text)
            
            # Analyze sentiment
            sentiment = self._analyze_sentiment_simple(text)
            
            # Calculate complexity score
            complexity = self._calculate_complexity(text)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"Content classification completed in {processing_time:.3f}s")
            
            return ContentClassification(
                document_type=doc_type,
                confidence=doc_confidence,
                topics=topics,
                sentiment=sentiment,
                language=language,
                complexity_score=complexity
            )
            
        except Exception as e:
            logger.error(f"Content classification failed: {str(e)}")
            raise
    
    async def extract_entities(self, text: str) -> EntityExtractionResult:
        """
        Extract named entities and relationships from text using rule-based approach
        
        Args:
            text: Input text for entity extraction
            
        Returns:
            EntityExtractionResult with entities, relationships, and statistics
        """
        try:
            start_time = datetime.now()
            
            # Extract entities using regex patterns
            entities = self._extract_entities_regex(text)
            
            # Find entity relationships
            relationships = self._extract_relationships_simple(entities, text)
            
            # Count entity types
            entity_counts = Counter([entity['label'] for entity in entities])
            
            # Calculate confidence score
            confidence_score = 0.8 if entities else 0.0
            
            processing_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"Entity extraction completed in {processing_time:.3f}s - found {len(entities)} entities")
            
            return EntityExtractionResult(
                entities=entities,
                relationships=relationships,
                entity_counts=dict(entity_counts),
                confidence_score=confidence_score
            )
            
        except Exception as e:
            logger.error(f"Entity extraction failed: {str(e)}")
            raise
    
    def _detect_language_simple(self, text: str) -> str:
        """Simple language detection based on character patterns"""
        # Count English characters
        english_chars = sum(1 for c in text if c.isascii() and c.isalpha())
        total_chars = sum(1 for c in text if c.isalpha())
        
        if total_chars == 0:
            return "unknown"
        
        english_ratio = english_chars / total_chars
        if english_ratio > 0.8:
            return "en"
        else:
            return "other"
    
    def _classify_document_type(self, text: str) -> Tuple[str, float]:
        """Classify document type based on keyword analysis"""
        text_lower = text.lower()
        word_counts = Counter(text_lower.split())
        
        type_scores = {}
        
        for doc_type, keywords in self.document_types.items():
            score = 0
            for keyword in keywords:
                # Count exact matches and partial matches
                exact_count = word_counts.get(keyword, 0)
                partial_count = sum(1 for word in word_counts if keyword in word)
                score += exact_count * 2 + partial_count
            
            # Normalize by text length
            type_scores[doc_type] = score / len(text_lower.split()) * 1000
        
        if not type_scores or max(type_scores.values()) == 0:
            return "general", 0.5
        
        best_type = max(type_scores.keys(), key=lambda k: type_scores[k])
        confidence = min(type_scores[best_type] / 10, 1.0)  # Normalize to 0-1
        
        return best_type, confidence
    
    def _extract_topics(self, text: str) -> List[Tuple[str, float]]:
        """Extract topics using keyword frequency analysis"""
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'}
        
        # Extract words and their frequencies
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        word_counts = Counter([word for word in words if word not in stop_words])
        
        # Get top topics
        total_words = sum(word_counts.values())
        topics = []
        
        for word, count in word_counts.most_common(10):
            relevance = count / total_words
            if relevance > 0.01:  # At least 1% frequency
                topics.append((word, relevance))
        
        return topics
    
    def _analyze_sentiment_simple(self, text: str) -> Dict[str, float]:
        """Simple sentiment analysis using keyword matching"""
        text_lower = text.lower()
        words = text_lower.split()
        
        positive_count = sum(1 for word in words if any(pos_word in word for pos_word in self.positive_words))
        negative_count = sum(1 for word in words if any(neg_word in word for neg_word in self.negative_words))
        
        total_sentiment = positive_count + negative_count
        if total_sentiment == 0:
            return {"positive": 0.33, "neutral": 0.34, "negative": 0.33}
        
        positive_score = positive_count / total_sentiment
        negative_score = negative_count / total_sentiment
        neutral_score = 1.0 - positive_score - negative_score
        
        return {
            "positive": positive_score,
            "neutral": max(neutral_score, 0.1),  # Ensure some neutral score
            "negative": negative_score
        }
    
    def _calculate_complexity(self, text: str) -> float:
        """Calculate text complexity score"""
        try:
            words = text.split()
            sentences = [s for s in text.split('.') if s.strip()]
            
            if not words or not sentences:
                return 0.0
            
            # Average word length
            avg_word_length = sum(len(word) for word in words) / len(words)
            
            # Average sentence length
            avg_sentence_length = len(words) / len(sentences)
            
            # Vocabulary diversity (unique words / total words)
            unique_words = len(set(word.lower() for word in words))
            vocabulary_diversity = unique_words / len(words)
            
            # Combine metrics (normalized to 0-1)
            complexity = (
                min(avg_word_length / 10, 1.0) * 0.3 +
                min(avg_sentence_length / 20, 1.0) * 0.4 +
                vocabulary_diversity * 0.3
            )
            
            return complexity
            
        except Exception:
            return 0.5
    
    def _extract_entities_regex(self, text: str) -> List[Dict[str, Any]]:
        """Extract entities using regex patterns"""
        entities = []
        
        # Email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        for match in re.finditer(email_pattern, text):
            entities.append({
                'text': match.group(),
                'label': 'EMAIL',
                'score': 0.95,
                'start': match.start(),
                'end': match.end(),
                'type': 'contact'
            })
        
        # Phone numbers
        phone_pattern = r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b'
        for match in re.finditer(phone_pattern, text):
            entities.append({
                'text': match.group(),
                'label': 'PHONE',
                'score': 0.9,
                'start': match.start(),
                'end': match.end(),
                'type': 'contact'
            })
        
        # Dates
        date_patterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # MM/DD/YYYY
            r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',    # YYYY/MM/DD
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b'  # Month DD, YYYY
        ]
        
        for pattern in date_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities.append({
                    'text': match.group(),
                    'label': 'DATE',
                    'score': 0.9,
                    'start': match.start(),
                    'end': match.end(),
                    'type': 'temporal'
                })
        
        # Monetary amounts
        money_pattern = r'\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\b\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s*(?:dollars?|USD|EUR|GBP)\b'
        for match in re.finditer(money_pattern, text, re.IGNORECASE):
            entities.append({
                'text': match.group(),
                'label': 'MONEY',
                'score': 0.85,
                'start': match.start(),
                'end': match.end(),
                'type': 'financial'
            })
        
        # URLs
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        for match in re.finditer(url_pattern, text):
            entities.append({
                'text': match.group(),
                'label': 'URL',
                'score': 0.95,
                'start': match.start(),
                'end': match.end(),
                'type': 'web'
            })
        
        # Simple person names (capitalized words)
        name_pattern = r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'
        for match in re.finditer(name_pattern, text):
            # Skip if it's a common pattern that's not a name
            name_text = match.group()
            if not any(word.lower() in ['the', 'and', 'for', 'but', 'not'] for word in name_text.split()):
                entities.append({
                    'text': name_text,
                    'label': 'PERSON',
                    'score': 0.7,  # Lower confidence for simple pattern
                    'start': match.start(),
                    'end': match.end(),
                    'type': 'person'
                })
        
        return entities
    
    def _extract_relationships_simple(self, entities: List[Dict], text: str) -> List[Dict[str, Any]]:
        """Extract simple relationships between entities"""
        relationships = []
        
        # Simple co-occurrence based relationships
        for i, entity1 in enumerate(entities):
            for entity2 in entities[i+1:]:
                # Check if entities are close to each other in text
                distance = abs(entity1.get('start', 0) - entity2.get('start', 0))
                
                if distance < 100:  # Within 100 characters
                    relationship = {
                        'entity1': entity1['text'],
                        'entity1_label': entity1['label'],
                        'entity2': entity2['text'],
                        'entity2_label': entity2['label'],
                        'relationship_type': 'co_occurrence',
                        'confidence': 0.6,
                        'distance': distance
                    }
                    relationships.append(relationship)
        
        return relationships[:20]  # Limit to top 20 relationships
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get content analysis service status"""
        return {
            "initialized": self.initialized,
            "type": "rule_based",
            "capabilities": {
                "content_classification": True,
                "entity_extraction": True,
                "custom_entities": True,
                "relationship_extraction": True,
                "sentiment_analysis": True,
                "language_detection": True,
                "complexity_analysis": True
            },
            "supported_document_types": list(self.document_types.keys()),
            "supported_entities": ["EMAIL", "PHONE", "DATE", "MONEY", "URL", "PERSON"],
            "performance": "fast_rule_based"
        }
