"""
AI Service for ConfluxAI - Enhanced Document Summarization and Analysis
Provides intelligent document processing using transformer models with Phase 3 enhancements
"""
import logging
import asyncio
from typing import List, Dict, Any, Optional, Union, Callable, AsyncGenerator
from datetime import datetime
import numpy as np
import json
import time

# AI/ML Dependencies
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
    import torch
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False
    pipeline = None
    AutoTokenizer = None
    torch = None

from models.schemas import ProcessingResult, SearchResult
from config.settings import Settings

logger = logging.getLogger(__name__)

class DocumentSummary:
    """Document summary result"""
    def __init__(self, summary: str, key_points: List[str], confidence: float, 
                 original_length: int, summary_length: int):
        self.summary = summary
        self.key_points = key_points
        self.confidence = confidence
        self.original_length = original_length
        self.summary_length = summary_length
        self.compression_ratio = summary_length / original_length if original_length > 0 else 0

class SectionSummary:
    """Section-wise summary result"""
    def __init__(self, section_title: str, summary: str, section_index: int):
        self.section_title = section_title
        self.summary = summary
        self.section_index = section_index

class MultiDocSummary:
    """Multi-document summary result"""
    def __init__(self, document_ids: List[str], individual_summaries: List[DocumentSummary],
                 combined_summary: str, common_themes: List[str], confidence: float,
                 cross_references: List[Dict[str, Any]]):
        self.document_ids = document_ids
        self.individual_summaries = individual_summaries
        self.combined_summary = combined_summary
        self.common_themes = common_themes
        self.confidence = confidence
        self.cross_references = cross_references

class CustomSummary:
    """Custom styled summary result"""
    def __init__(self, summary: str, style: str, audience: str, key_points: List[str],
                 confidence: float, custom_elements: Dict[str, Any]):
        self.summary = summary
        self.style = style
        self.audience = audience
        self.key_points = key_points
        self.confidence = confidence
        self.custom_elements = custom_elements

class ConversationContext:
    """Context for conversational interactions"""
    def __init__(self, conversation_id: str, history: List[Dict[str, Any]], 
                 last_query: str, last_response: str):
        self.conversation_id = conversation_id
        self.history = history
        self.last_query = last_query
        self.last_response = last_response
        self.timestamp = datetime.now()

class ProgressiveUpdate:
    """Progressive summarization update"""
    def __init__(self, partial_summary: str, progress: float, stage: str, 
                 estimated_time_remaining: Optional[float] = None):
        self.partial_summary = partial_summary
        self.progress = progress
        self.stage = stage
        self.estimated_time_remaining = estimated_time_remaining
        self.timestamp = datetime.now()

class AnalyticsData:
    """AI service analytics and performance data"""
    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.average_processing_time = 0.0
        self.model_performance = {}
        self.error_count = 0
        self.last_updated = datetime.now()

class AIService:
    """Enhanced AI-powered document analysis and processing service with Phase 3 features"""
    
    def __init__(self, search_service=None):
        self.settings = Settings()
        self.search_service = search_service
        self.summarizer = None
        self.long_summarizer = None
        self.tokenizer = None
        self.initialized = False
        
        # Model configurations
        self.summarization_model = "facebook/bart-large-cnn"
        self.long_summarization_model = "pszemraj/long-t5-tglobal-base-16384-book-summary"
        self.max_chunk_length = 1024
        self.max_summary_length = 150
        self.min_summary_length = 30
        
        # Phase 3 enhancements
        self.analytics = AnalyticsData()
        self.conversation_contexts = {}  # Store conversation contexts
        self.model_cache = {}  # Cache for model outputs
        self.performance_metrics = {}
        
        # Advanced configuration
        self.domain_specific_models = {
            "technical": "allenai/led-base-16384",
            "medical": "emilyalsentzer/Bio_ClinicalBERT", 
            "legal": "nlpaueb/legal-bert-base-uncased",
            "financial": "ProsusAI/finbert"
        }
        
        # Real-time features
        self.active_tasks = {}
        self.task_callbacks = {}
    
    async def initialize(self):
        """Initialize AI models"""
        try:
            if not HF_AVAILABLE:
                logger.warning("Transformers library not available. AI features will be disabled.")
                return
            
            logger.info("Initializing AI service...")
            
            # Check for GPU availability
            device = 0 if HF_AVAILABLE and torch and torch.cuda.is_available() else -1
            logger.info(f"Using device: {'GPU' if device == 0 else 'CPU'}")
            
            # Initialize standard summarizer
            logger.info(f"Loading summarization model: {self.summarization_model}")
            if pipeline:
                self.summarizer = pipeline(
                    "summarization",
                    model=self.summarization_model,
                    device=device,
                    model_kwargs={"torch_dtype": torch.float16} if device == 0 and torch else {}
                )
            
            # Initialize tokenizer for text chunking
            if AutoTokenizer:
                self.tokenizer = AutoTokenizer.from_pretrained(self.summarization_model)
            
            self.initialized = True
            logger.info("AI service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize AI service: {str(e)}")
            self.initialized = False
    
    async def summarize_document(self, text: str, max_length: Optional[int] = None) -> DocumentSummary:
        """
        Summarize a document with intelligent chunking for long texts
        
        Args:
            text: Input text to summarize
            max_length: Maximum summary length (optional)
            
        Returns:
            DocumentSummary object with summary and metadata
        """
        if not self.initialized or not self.summarizer:
            raise Exception("AI service not initialized or summarizer not available")
        
        try:
            start_time = datetime.now()
            max_length = max_length or self.max_summary_length
            
            # Clean and prepare text
            cleaned_text = self._preprocess_text(text)
            original_length = len(cleaned_text.split())
            
            # Handle very short texts
            if original_length < 50:
                return DocumentSummary(
                    summary=cleaned_text,
                    key_points=[cleaned_text],
                    confidence=1.0,
                    original_length=original_length,
                    summary_length=original_length
                )
            
            # Chunk text if too long
            chunks = self._chunk_text(cleaned_text)
            
            if len(chunks) == 1:
                # Single chunk summarization
                summary_result = await self._summarize_chunk(chunks[0], max_length)
                key_points = self._extract_key_points(summary_result)
                
                return DocumentSummary(
                    summary=summary_result,
                    key_points=key_points,
                    confidence=0.85,  # Base confidence for single chunk
                    original_length=original_length,
                    summary_length=len(summary_result.split())
                )
            else:
                # Multi-chunk hierarchical summarization
                return await self._hierarchical_summarization(chunks, max_length, original_length)
                
        except Exception as e:
            logger.error(f"Document summarization failed: {str(e)}")
            raise
    
    async def summarize_by_sections(self, document_chunks: List[Dict[str, str]]) -> List[SectionSummary]:
        """
        Summarize document sections individually
        
        Args:
            document_chunks: List of sections with 'title' and 'content'
            
        Returns:
            List of SectionSummary objects
        """
        if not self.initialized:
            raise Exception("AI service not initialized")
        
        try:
            section_summaries = []
            
            for i, chunk in enumerate(document_chunks):
                title = chunk.get('title', f'Section {i+1}')
                content = chunk.get('content', '')
                
                if len(content.split()) < 20:
                    # Skip very short sections
                    continue
                
                summary = await self._summarize_chunk(content, max_length=100)
                section_summaries.append(SectionSummary(
                    section_title=title,
                    summary=summary,
                    section_index=i
                ))
            
            return section_summaries
            
        except Exception as e:
            logger.error(f"Section summarization failed: {str(e)}")
            raise
    
    async def multi_document_summarization(self, document_ids: List[str]) -> "MultiDocSummary":
        """
        Enhanced cross-document summarization for document collections with theme detection
        
        Args:
            document_ids: List of document IDs to summarize together
            
        Returns:
            MultiDocSummary with aggregated insights and cross-references
        """
        if not self.initialized:
            raise Exception("AI service not initialized")
        
        start_time = time.time()
        
        try:
            if not self.search_service:
                raise Exception("Search service not available for multi-document summarization")
            
            # Retrieve documents
            documents = []
            document_summaries = []
            
            for doc_id in document_ids:
                try:
                    doc = await self.search_service.get_document(doc_id)
                    if doc:
                        documents.append(doc)
                        
                        # Generate individual summary
                        individual_summary = await self.summarize_document(
                            doc.get('content', ''), 
                            max_length=100
                        )
                        document_summaries.append(individual_summary)
                        
                except Exception as e:
                    logger.warning(f"Failed to process document {doc_id}: {str(e)}")
                    continue
            
            if not documents:
                raise Exception("No valid documents found for summarization")
            
            # Extract common themes and cross-references
            common_themes = self._extract_common_themes(document_summaries)
            cross_references = self._identify_cross_references(documents)
            
            # Generate combined summary
            combined_text = " ".join([doc.get('content', '') for doc in documents])
            combined_summary_result = await self.summarize_document(
                combined_text, 
                max_length=200
            )
            
            # Enhanced combined summary with themes
            enhanced_summary = self._enhance_with_themes(
                combined_summary_result.summary, 
                common_themes
            )
            
            processing_time = time.time() - start_time
            self._update_analytics("multi_document_summarization", processing_time, True)
            
            return MultiDocSummary(
                document_ids=document_ids,
                individual_summaries=document_summaries,
                combined_summary=enhanced_summary,
                common_themes=common_themes,
                confidence=0.8,
                cross_references=cross_references
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            self._update_analytics("multi_document_summarization", processing_time, False)
            logger.error(f"Multi-document summarization failed: {str(e)}")
            raise
    
    async def progressive_summarization(self, text: str, callback: Optional[Callable] = None) -> AsyncGenerator[ProgressiveUpdate, None]:
        """
        Enhanced real-time progressive summarization with detailed progress tracking
        
        Args:
            text: Input text to summarize
            callback: Optional callback for real-time updates
            
        Yields:
            ProgressiveUpdate objects with partial summaries and progress
        """
        if not self.initialized:
            raise Exception("AI service not initialized")
        
        start_time = time.time()
        
        try:
            # Split text into progressive chunks
            chunks = self._chunk_text(text)
            total_chunks = len(chunks)
            
            progressive_summary = ""
            estimated_time_per_chunk = 2.0  # Initial estimate
            
            for i, chunk in enumerate(chunks):
                chunk_start_time = time.time()
                
                # Calculate progress and ETA
                progress = (i + 1) / total_chunks * 100
                remaining_chunks = total_chunks - (i + 1)
                estimated_time_remaining = remaining_chunks * estimated_time_per_chunk
                
                stage = f"Processing chunk {i+1}/{total_chunks}"
                
                # Update callback if provided
                if callback:
                    await callback({
                        "progress": progress, 
                        "stage": stage,
                        "estimated_time_remaining": estimated_time_remaining
                    })
                
                # Summarize chunk with enhanced processing
                chunk_summary = await self._summarize_chunk_with_context(chunk, progressive_summary)
                
                # Accumulate progressive summary with intelligent merging
                if progressive_summary:
                    progressive_summary = await self._merge_summaries(progressive_summary, chunk_summary)
                else:
                    progressive_summary = chunk_summary
                
                # Update time estimate based on actual processing time
                chunk_processing_time = time.time() - chunk_start_time
                estimated_time_per_chunk = (estimated_time_per_chunk + chunk_processing_time) / 2
                
                # Yield progressive result
                update = ProgressiveUpdate(
                    partial_summary=progressive_summary,
                    progress=progress,
                    stage=stage,
                    estimated_time_remaining=estimated_time_remaining
                )
                
                yield update
                
                # Small delay for real-time effect
                await asyncio.sleep(0.1)
            
            # Final callback
            if callback:
                total_time = time.time() - start_time
                await callback({
                    "progress": 100, 
                    "stage": "Summarization complete",
                    "total_time": total_time
                })
            
            self._update_analytics("progressive_summarization", time.time() - start_time, True)
                
        except Exception as e:
            self._update_analytics("progressive_summarization", time.time() - start_time, False)
            logger.error(f"Progressive summarization failed: {str(e)}")
            raise
    
    async def custom_summarization(self, text: str, style: str, audience: str, custom_length: Optional[int] = None) -> "CustomSummary":
        """
        Generate custom summaries based on style and target audience
        
        Args:
            text: Input text to summarize
            style: Summary style (executive, technical, bullet_points, narrative)
            audience: Target audience (expert, general, student, executive)
            custom_length: Custom length override
            
        Returns:
            CustomSummary with style-specific formatting
        """
        if not self.initialized:
            raise Exception("AI service not initialized")
        
        try:
            # Adjust parameters based on style and audience
            max_length = custom_length or self._get_length_for_style(style)
            
            # Generate base summary
            base_summary = await self.summarize_document(text, max_length)
            
            # Apply style-specific formatting
            formatted_summary = await self._apply_style_formatting(base_summary.summary, style, audience)
            
            return CustomSummary(
                summary=formatted_summary,
                style=style,
                audience=audience,
                key_points=base_summary.key_points,
                confidence=base_summary.confidence,
                custom_elements=self._get_custom_elements(style)
            )
            
        except Exception as e:
            logger.error(f"Custom summarization failed: {str(e)}")
            raise
    
    def _get_length_for_style(self, style: str) -> int:
        """Get appropriate length for summary style"""
        length_map = {
            "executive": 100,
            "technical": 200,
            "bullet_points": 150,
            "narrative": 250,
            "brief": 75,
            "detailed": 300
        }
        return length_map.get(style, self.max_summary_length)
    
    async def _apply_style_formatting(self, summary: str, style: str, audience: str) -> str:
        """Apply style-specific formatting to summary"""
        try:
            if style == "bullet_points":
                # Convert to bullet points
                sentences = summary.split('. ')
                return '\n'.join([f"• {sentence.strip()}" for sentence in sentences if sentence.strip()])
            
            elif style == "executive":
                # Executive summary format
                return f"Executive Summary: {summary}\n\nKey Takeaway: {summary.split('.')[0]}."
            
            elif style == "technical":
                # Technical format with more detail
                return f"Technical Overview:\n\n{summary}\n\nImplications: This analysis provides insights into the technical aspects of the subject matter."
            
            elif style == "narrative":
                # Narrative format
                return f"Overview:\n\n{summary}\n\nThis comprehensive analysis covers the essential aspects of the topic."
            
            else:
                return summary
                
        except Exception as e:
            logger.warning(f"Style formatting failed: {str(e)}")
            return summary
    
    def _get_custom_elements(self, style: str) -> Dict[str, Any]:
        """Get custom elements for different summary styles"""
        elements = {
            "executive": {"include_metrics": True, "highlight_decisions": True},
            "technical": {"include_methods": True, "highlight_data": True},
            "bullet_points": {"structured_format": True, "concise_points": True},
            "narrative": {"contextual_flow": True, "comprehensive_coverage": True}
        }
        return elements.get(style, {})
    
    async def _summarize_chunk(self, text: str, max_length: Optional[int] = None) -> str:
        """Summarize a single text chunk"""
        if not self.summarizer:
            # Fallback when summarizer is not available
            sentences = text.split('.')[:3]
            return '. '.join(sentences) + '.'
        
        max_length = max_length or self.max_summary_length
        min_length = min(self.min_summary_length, max_length // 2)
        
        try:
            # Run summarization in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.summarizer(
                    text,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False
                )
            )
            
            if isinstance(result, list) and len(result) > 0 and 'summary_text' in result[0]:
                return result[0]['summary_text'].strip()
            else:
                # Fallback
                sentences = text.split('.')[:3]
                return '. '.join(sentences) + '.'
            
        except Exception as e:
            logger.error(f"Chunk summarization failed: {str(e)}")
            # Fallback to first few sentences
            sentences = text.split('.')[:3]
            return '. '.join(sentences) + '.'
    
    async def _hierarchical_summarization(self, chunks: List[str], max_length: int, original_length: int) -> DocumentSummary:
        """Perform hierarchical summarization for long documents"""
        try:
            # Summarize each chunk
            chunk_summaries = []
            for chunk in chunks:
                summary = await self._summarize_chunk(chunk, max_length=100)
                chunk_summaries.append(summary)
            
            # Combine chunk summaries
            combined_summary = ' '.join(chunk_summaries)
            
            # Final summarization if combined is still too long
            if len(combined_summary.split()) > max_length:
                final_summary = await self._summarize_chunk(combined_summary, max_length)
            else:
                final_summary = combined_summary
            
            # Extract key points from chunk summaries
            key_points = self._extract_key_points_from_chunks(chunk_summaries)
            
            return DocumentSummary(
                summary=final_summary,
                key_points=key_points,
                confidence=0.75,  # Lower confidence for hierarchical
                original_length=original_length,
                summary_length=len(final_summary.split())
            )
            
        except Exception as e:
            logger.error(f"Hierarchical summarization failed: {str(e)}")
            raise
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and preprocess text for summarization"""
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Remove very short lines (likely artifacts)
        lines = text.split('\n')
        meaningful_lines = [line for line in lines if len(line.strip()) > 10]
        
        return ' '.join(meaningful_lines)
    
    def _chunk_text(self, text: str) -> List[str]:
        """Intelligently chunk text for processing"""
        if not self.tokenizer:
            # Fallback chunking by character count
            chunk_size = self.max_chunk_length * 4  # Approximate
            chunks = []
            for i in range(0, len(text), chunk_size):
                chunks.append(text[i:i + chunk_size])
            return chunks
        
        # Tokenize and chunk by token count
        tokens = self.tokenizer.encode(text)
        chunks = []
        
        for i in range(0, len(tokens), self.max_chunk_length):
            chunk_tokens = tokens[i:i + self.max_chunk_length]
            chunk_text = self.tokenizer.decode(chunk_tokens, skip_special_tokens=True)
            chunks.append(chunk_text)
        
        return chunks
    
    def _extract_key_points(self, summary: str) -> List[str]:
        """Extract key points from summary"""
        # Simple extraction by sentences
        sentences = [s.strip() for s in summary.split('.') if len(s.strip()) > 10]
        return sentences[:5]  # Return top 5 key points
    
    def _extract_key_points_from_chunks(self, chunk_summaries: List[str]) -> List[str]:
        """Extract key points from multiple chunk summaries"""
        all_points = []
        for summary in chunk_summaries:
            points = self._extract_key_points(summary)
            all_points.extend(points)
        
        # Return unique points, up to 7
        unique_points = list(dict.fromkeys(all_points))  # Remove duplicates while preserving order
        return unique_points[:7]
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get enhanced AI service status with Phase 3 metrics"""
        return {
            "initialized": self.initialized,
            "summarizer_available": self.summarizer is not None,
            "models": {
                "summarization": self.summarization_model if self.initialized else None,
                "device": "GPU" if torch and torch.cuda.is_available() else "CPU" if HF_AVAILABLE else "Not Available"
            },
            "capabilities": {
                "document_summarization": self.initialized,
                "section_summarization": self.initialized,
                "hierarchical_summarization": self.initialized,
                "multi_document_summarization": self.initialized and self.search_service is not None,
                "progressive_summarization": self.initialized,
                "custom_summarization": self.initialized,
                "real_time_progress": True,
                "conversation_context": True
            },
            "analytics": {
                "total_requests": self.analytics.total_requests,
                "success_rate": (self.analytics.successful_requests / max(self.analytics.total_requests, 1)) * 100,
                "average_processing_time": self.analytics.average_processing_time,
                "error_count": self.analytics.error_count
            },
            "performance": self.performance_metrics,
            "active_tasks": len(self.active_tasks)
        }
    
    # Phase 3 Enhanced Helper Methods
    
    def _extract_common_themes(self, document_summaries: List[DocumentSummary]) -> List[str]:
        """Extract common themes from multiple document summaries"""
        try:
            # Simple keyword-based theme extraction
            all_words = []
            for summary in document_summaries:
                words = summary.summary.lower().split()
                all_words.extend([word.strip('.,!?;') for word in words if len(word) > 4])
            
            # Count word frequency
            word_freq = {}
            for word in all_words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            # Extract most common themes (words appearing in multiple summaries)
            min_frequency = max(2, len(document_summaries) // 2)
            themes = [word for word, freq in word_freq.items() if freq >= min_frequency]
            
            return sorted(themes, key=lambda x: word_freq[x], reverse=True)[:5]
            
        except Exception as e:
            logger.warning(f"Theme extraction failed: {str(e)}")
            return ["analysis", "content", "information", "data", "results"]
    
    def _identify_cross_references(self, documents: List[Dict]) -> List[Dict[str, Any]]:
        """Identify cross-references between documents"""
        try:
            cross_refs = []
            
            for i, doc1 in enumerate(documents):
                for j, doc2 in enumerate(documents[i+1:], i+1):
                    # Simple overlap detection based on keywords
                    content1 = doc1.get('content', '').lower()
                    content2 = doc2.get('content', '').lower()
                    
                    # Extract key terms (simplified)
                    words1 = set([w.strip('.,!?;') for w in content1.split() if len(w) > 5])
                    words2 = set([w.strip('.,!?;') for w in content2.split() if len(w) > 5])
                    
                    overlap = words1.intersection(words2)
                    if len(overlap) > 3:  # Significant overlap
                        cross_refs.append({
                            "document1": doc1.get('id', i),
                            "document2": doc2.get('id', j),
                            "common_terms": list(overlap)[:5],
                            "overlap_score": len(overlap) / len(words1.union(words2))
                        })
            
            return cross_refs
            
        except Exception as e:
            logger.warning(f"Cross-reference identification failed: {str(e)}")
            return []
    
    def _enhance_with_themes(self, summary: str, themes: List[str]) -> str:
        """Enhance summary with identified themes"""
        try:
            if not themes:
                return summary
                
            theme_text = ", ".join(themes[:3])
            enhanced_summary = f"{summary}\n\nKey themes identified: {theme_text}."
            
            return enhanced_summary
            
        except Exception as e:
            logger.warning(f"Theme enhancement failed: {str(e)}")
            return summary
    
    async def _summarize_chunk_with_context(self, chunk: str, context: str) -> str:
        """Summarize chunk with awareness of previous context"""
        try:
            if context and len(context.split()) > 10:
                # Add context awareness
                enhanced_input = f"Context: {context[-200:]}...\n\nNew content: {chunk}"
                return await self._summarize_chunk(enhanced_input, max_length=80)
            else:
                return await self._summarize_chunk(chunk, max_length=80)
                
        except Exception as e:
            logger.warning(f"Context-aware summarization failed: {str(e)}")
            return await self._summarize_chunk(chunk, max_length=80)
    
    async def _merge_summaries(self, summary1: str, summary2: str) -> str:
        """Intelligently merge two summaries"""
        try:
            combined_text = f"{summary1} {summary2}"
            
            if len(combined_text.split()) > self.max_summary_length:
                # Re-summarize if too long
                return await self._summarize_chunk(combined_text, self.max_summary_length)
            else:
                return combined_text
                
        except Exception as e:
            logger.warning(f"Summary merging failed: {str(e)}")
            return f"{summary1} {summary2}"
    
    def _update_analytics(self, operation: str, processing_time: float, success: bool):
        """Update analytics and performance metrics"""
        try:
            self.analytics.total_requests += 1
            
            if success:
                self.analytics.successful_requests += 1
            else:
                self.analytics.error_count += 1
            
            # Update average processing time
            if self.analytics.total_requests == 1:
                self.analytics.average_processing_time = processing_time
            else:
                self.analytics.average_processing_time = (
                    (self.analytics.average_processing_time * (self.analytics.total_requests - 1) + processing_time) 
                    / self.analytics.total_requests
                )
            
            # Update operation-specific metrics
            if operation not in self.performance_metrics:
                self.performance_metrics[operation] = {
                    "count": 0,
                    "avg_time": 0.0,
                    "success_rate": 0.0
                }
            
            op_metrics = self.performance_metrics[operation]
            op_metrics["count"] += 1
            op_metrics["avg_time"] = (
                (op_metrics["avg_time"] * (op_metrics["count"] - 1) + processing_time) 
                / op_metrics["count"]
            )
            op_metrics["success_rate"] = (
                (op_metrics["success_rate"] * (op_metrics["count"] - 1) + (1.0 if success else 0.0)) 
                / op_metrics["count"]
            ) * 100
            
            self.analytics.last_updated = datetime.now()
            
        except Exception as e:
            logger.warning(f"Analytics update failed: {str(e)}")
    
    async def get_conversation_context(self, conversation_id: str) -> Optional[ConversationContext]:
        """Retrieve conversation context for multi-turn interactions"""
        return self.conversation_contexts.get(conversation_id)
    
    async def update_conversation_context(self, conversation_id: str, query: str, response: str):
        """Update conversation context with new interaction"""
        try:
            if conversation_id not in self.conversation_contexts:
                self.conversation_contexts[conversation_id] = ConversationContext(
                    conversation_id=conversation_id,
                    history=[],
                    last_query=query,
                    last_response=response
                )
            
            context = self.conversation_contexts[conversation_id]
            context.history.append({
                "query": query,
                "response": response,
                "timestamp": datetime.now()
            })
            context.last_query = query
            context.last_response = response
            context.timestamp = datetime.now()
            
            # Limit history size
            if len(context.history) > 10:
                context.history = context.history[-10:]
                
        except Exception as e:
            logger.warning(f"Failed to update conversation context: {str(e)}")
    
    async def clear_conversation_context(self, conversation_id: str):
        """Clear conversation context"""
        if conversation_id in self.conversation_contexts:
            del self.conversation_contexts[conversation_id]
    
    def get_analytics_summary(self) -> Dict[str, Any]:
        """Get comprehensive analytics summary"""
        return {
            "overview": {
                "total_requests": self.analytics.total_requests,
                "successful_requests": self.analytics.successful_requests,
                "error_count": self.analytics.error_count,
                "success_rate": (self.analytics.successful_requests / max(self.analytics.total_requests, 1)) * 100,
                "average_processing_time": self.analytics.average_processing_time
            },
            "performance_by_operation": self.performance_metrics,
            "active_conversations": len(self.conversation_contexts),
            "model_status": {
                "summarizer_loaded": self.summarizer is not None,
                "device": "GPU" if torch and torch.cuda.is_available() else "CPU" if HF_AVAILABLE else "Not Available"
            },
            "last_updated": self.analytics.last_updated.isoformat() if self.analytics.last_updated else None
        }
