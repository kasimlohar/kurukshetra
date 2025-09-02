"""
Enhanced Question Answering Service for ConfluxAI Phase 3
Provides intelligent Q&A capabilities with conversational context and advanced features
"""
import logging
import asyncio
from typing import List, Dict, Any, Optional, Tuple, Callable
from datetime import datetime
import numpy as np
import time
import uuid

# AI/ML Dependencies
try:
    from transformers import pipeline, AutoTokenizer
    import torch
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False
    pipeline = None
    AutoTokenizer = None
    torch = None

from models.schemas import SearchResult, ProcessingResult
from services.search_service import SearchService
from config.settings import Settings

logger = logging.getLogger(__name__)

class QAResult:
    """Question answering result"""
    def __init__(self, question: str, answer: str, confidence: float, 
                 source_documents: List[SearchResult], context_used: str):
        self.question = question
        self.answer = answer
        self.confidence = confidence
        self.source_documents = source_documents
        self.context_used = context_used
        self.answer_span = None
        self.timestamp = datetime.now()

class ConversationResponse:
    """Conversational question answering result"""
    def __init__(self, current_answer: QAResult, conversation_context: List[Dict[str, Any]], 
                 suggested_follow_ups: List[str], session_id: str):
        self.current_answer = current_answer
        self.conversation_context = conversation_context
        self.suggested_follow_ups = suggested_follow_ups
        self.session_id = session_id
        self.timestamp = datetime.now()

class CitedResponse:
    """Answer with detailed source citations"""
    def __init__(self, answer: str, citations: List[Dict[str, Any]], 
                 confidence: float, citation_quality: str):
        self.answer = answer
        self.citations = citations
        self.confidence = confidence
        self.citation_quality = citation_quality
        self.timestamp = datetime.now()

class MultiDocQAResult:
    """Multi-document question answering result"""
    def __init__(self, question: str, aggregated_answer: str, 
                 individual_answers: List[QAResult], confidence: float):
        self.question = question
        self.aggregated_answer = aggregated_answer
        self.individual_answers = individual_answers
        self.confidence = confidence
        self.source_count = len(individual_answers)
        self.timestamp = datetime.now()

class QuestionAnsweringService:
    """Enhanced intelligent question answering over document collections with Phase 3 features"""
    
    def __init__(self, search_service: SearchService):
        self.settings = Settings()
        self.search_service = search_service
        self.qa_pipeline = None
        self.long_qa_pipeline = None
        self.tokenizer = None
        self.initialized = False
        
        # Model configurations
        self.qa_model = "deepset/roberta-base-squad2"
        self.long_qa_model = "allenai/longformer-large-4096-finetuned-triviaqa"
        self.max_context_length = 4096
        self.max_answer_length = 150
        self.confidence_threshold = 0.3
        self.top_k_documents = 5
        
        # Phase 3 enhancements
        self.conversation_sessions = {}  # Store conversation contexts
        self.qa_analytics = {
            "total_questions": 0,
            "successful_answers": 0,
            "average_confidence": 0.0,
            "conversation_sessions": 0,
            "popular_topics": {},
            "last_updated": None
        }
        
        # Advanced features
        self.citation_extractors = []
        self.follow_up_generators = []
        self.context_memory_limit = 10  # Number of previous Q&A pairs to remember
    
    async def initialize(self):
        """Initialize Q&A models"""
        try:
            if not HF_AVAILABLE:
                logger.warning("Transformers library not available. Q&A features will be disabled.")
                return
            
            logger.info("Initializing Question Answering service...")
            
            # Check for GPU availability
            device = 0 if torch.cuda.is_available() else -1
            logger.info(f"Using device: {'GPU' if device == 0 else 'CPU'}")
            
            # Initialize standard Q&A pipeline
            logger.info(f"Loading Q&A model: {self.qa_model}")
            self.qa_pipeline = pipeline(
                "question-answering",
                model=self.qa_model,
                device=device,
                model_kwargs={"torch_dtype": torch.float16} if device == 0 else {}
            )
            
            # Initialize tokenizer
            from transformers import AutoTokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.qa_model)
            
            self.initialized = True
            logger.info("Question Answering service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Q&A service: {str(e)}")
            self.initialized = False
    
    async def answer_question(self, question: str, context_limit: int = 5, 
                            file_filters: Optional[List[str]] = None) -> QAResult:
        """
        Answer a question using relevant documents from the search index
        
        Args:
            question: Natural language question
            context_limit: Maximum number of documents to consider
            file_filters: Optional list of file types to filter by
            
        Returns:
            QAResult with answer and supporting information
        """
        if not self.initialized or not self.qa_pipeline:
            raise Exception("Q&A service not initialized")
        
        try:
            start_time = datetime.now()
            
            # Search for relevant documents
            logger.info(f"Searching for context documents for question: {question[:100]}...")
            search_results = await self.search_service.search(
                query=question,
                limit=context_limit * 2,  # Get more results to filter
                threshold=0.6  # Lower threshold for Q&A context
            )
            
            if not search_results:
                return QAResult(
                    question=question,
                    answer="I couldn't find any relevant documents to answer this question.",
                    confidence=0.0,
                    source_documents=[],
                    context_used=""
                )
            
            # Filter by file types if specified
            if file_filters:
                search_results = [
                    result for result in search_results 
                    if any(result.filename.lower().endswith(f".{ft.lower()}") for ft in file_filters)
                ]
            
            # Take top results for context
            top_results = search_results[:context_limit]
            
            # Build context from search results
            context = self._build_context(top_results)
            
            # Generate answer
            qa_input = {
                "question": question,
                "context": context
            }
            
            # Run Q&A in thread pool
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: self.qa_pipeline(qa_input)
            )
            
            answer = result['answer'].strip()
            confidence = result['score']
            
            # Enhance answer if confidence is low
            if confidence < self.confidence_threshold:
                answer = f"Based on the available documents, {answer.lower()}. However, I'm not very confident about this answer."
            
            processing_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"Q&A completed in {processing_time:.3f}s with confidence {confidence:.3f}")
            
            return QAResult(
                question=question,
                answer=answer,
                confidence=confidence,
                source_documents=top_results,
                context_used=context
            )
            
        except Exception as e:
            logger.error(f"Question answering failed: {str(e)}")
            return QAResult(
                question=question,
                answer=f"I encountered an error while trying to answer this question: {str(e)}",
                confidence=0.0,
                source_documents=[],
                context_used=""
            )
    
    async def multi_document_qa(self, question: str, file_filters: List[str] = None) -> MultiDocQAResult:
        """
        Answer questions across multiple documents with answer aggregation
        
        Args:
            question: Natural language question
            file_filters: Optional list of file types to filter by
            
        Returns:
            MultiDocQAResult with aggregated answer
        """
        if not self.initialized:
            raise Exception("Q&A service not initialized")
        
        try:
            # Get more documents for multi-doc analysis
            search_results = await self.search_service.search(
                query=question,
                limit=10,
                threshold=0.5
            )
            
            if not search_results:
                return MultiDocQAResult(
                    question=question,
                    aggregated_answer="No relevant documents found to answer this question.",
                    individual_answers=[],
                    confidence=0.0
                )
            
            # Filter by file types if specified
            if file_filters:
                search_results = [
                    result for result in search_results 
                    if any(result.filename.lower().endswith(f".{ft.lower()}") for ft in file_filters)
                ]
            
            # Get individual answers from different documents
            individual_answers = []
            for result in search_results[:6]:  # Limit to avoid too many calls
                try:
                    # Create context from single document
                    single_context = result.content[:self.max_context_length]
                    
                    qa_input = {
                        "question": question,
                        "context": single_context
                    }
                    
                    # Run Q&A
                    loop = asyncio.get_event_loop()
                    qa_result = await loop.run_in_executor(
                        None,
                        lambda: self.qa_pipeline(qa_input)
                    )
                    
                    if qa_result['score'] > 0.2:  # Only include reasonable answers
                        individual_answers.append(QAResult(
                            question=question,
                            answer=qa_result['answer'],
                            confidence=qa_result['score'],
                            source_documents=[result],
                            context_used=single_context
                        ))
                        
                except Exception as e:
                    logger.warning(f"Error processing document {result.filename}: {str(e)}")
                    continue
            
            if not individual_answers:
                return MultiDocQAResult(
                    question=question,
                    aggregated_answer="I couldn't find sufficient information to answer this question.",
                    individual_answers=[],
                    confidence=0.0
                )
            
            # Aggregate answers
            aggregated_answer = self._aggregate_answers(individual_answers)
            overall_confidence = sum(ans.confidence for ans in individual_answers) / len(individual_answers)
            
            return MultiDocQAResult(
                question=question,
                aggregated_answer=aggregated_answer,
                individual_answers=individual_answers,
                confidence=overall_confidence
            )
            
        except Exception as e:
            logger.error(f"Multi-document Q&A failed: {str(e)}")
            raise
    
    def _build_context(self, search_results: List[SearchResult]) -> str:
        """Build context string from search results"""
        context_parts = []
        total_length = 0
        
        for result in search_results:
            # Add document content with source information
            content = result.content
            source_info = f"[Source: {result.filename}]"
            
            # Ensure we don't exceed context length
            remaining_length = self.max_context_length - total_length - len(source_info) - 10
            if remaining_length <= 0:
                break
            
            if len(content) > remaining_length:
                content = content[:remaining_length] + "..."
            
            context_part = f"{source_info} {content}"
            context_parts.append(context_part)
            total_length += len(context_part)
        
        return " ".join(context_parts)
    
    def _aggregate_answers(self, individual_answers: List[QAResult]) -> str:
        """Aggregate individual answers into a comprehensive response"""
        if not individual_answers:
            return "No answers available."
        
        if len(individual_answers) == 1:
            return individual_answers[0].answer
        
        # Sort by confidence
        sorted_answers = sorted(individual_answers, key=lambda x: x.confidence, reverse=True)
        
        # Take the highest confidence answer as primary
        primary_answer = sorted_answers[0].answer
        
        # Check for consensus or conflicting information
        unique_answers = []
        for ans in sorted_answers:
            if ans.answer.lower() not in [ua.lower() for ua in unique_answers]:
                unique_answers.append(ans.answer)
        
        if len(unique_answers) == 1:
            # Consensus - strengthen the answer
            source_count = len(individual_answers)
            return f"{primary_answer} This information is consistent across {source_count} source documents."
        else:
            # Multiple perspectives - present them
            aggregated = f"Primary answer: {primary_answer}"
            
            if len(unique_answers) > 1:
                additional_info = [ans for ans in unique_answers[1:3]]  # Up to 2 additional perspectives
                if additional_info:
                    aggregated += f" Additional perspectives from other documents: {' | '.join(additional_info)}"
            
            return aggregated
    
    async def suggest_follow_up_questions(self, question: str, answer: str) -> List[str]:
        """Generate follow-up question suggestions based on the answered question"""
        try:
            # Simple rule-based follow-up generation
            follow_ups = []
            
            # Extract key terms from the question and answer
            question_words = question.lower().split()
            answer_words = answer.lower().split()
            
            # Question templates based on question type
            if any(word in question_words for word in ['what', 'define', 'explain']):
                follow_ups.extend([
                    f"How does {self._extract_subject(question)} work?",
                    f"What are examples of {self._extract_subject(question)}?",
                    f"Why is {self._extract_subject(question)} important?"
                ])
            
            elif any(word in question_words for word in ['how', 'process', 'method']):
                follow_ups.extend([
                    f"What are the benefits of {self._extract_subject(question)}?",
                    f"What challenges are associated with {self._extract_subject(question)}?",
                    f"When should {self._extract_subject(question)} be used?"
                ])
            
            elif any(word in question_words for word in ['why', 'reason', 'cause']):
                follow_ups.extend([
                    f"What are the implications of {self._extract_subject(question)}?",
                    f"How can {self._extract_subject(question)} be addressed?",
                    f"What alternatives exist for {self._extract_subject(question)}?"
                ])
            
            # Generic follow-ups
            follow_ups.extend([
                "Can you provide more details about this topic?",
                "What are the key points I should remember?",
                "Are there any related concepts I should know about?"
            ])
            
            return follow_ups[:5]  # Return top 5 suggestions
            
        except Exception as e:
            logger.warning(f"Failed to generate follow-up questions: {str(e)}")
            return ["Can you provide more information about this topic?"]
    
    def _extract_subject(self, question: str) -> str:
        """Extract the main subject from a question"""
        # Simple extraction - remove question words and get key terms
        stop_words = {'what', 'how', 'why', 'when', 'where', 'who', 'which', 'is', 'are', 'was', 'were', 'the', 'a', 'an'}
        words = [word.lower() for word in question.split() if word.lower() not in stop_words and len(word) > 2]
        
        if words:
            return ' '.join(words[:3])  # Return first few meaningful words
        return "this topic"
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get enhanced Q&A service status with Phase 3 metrics"""
        return {
            "initialized": self.initialized,
            "qa_pipeline_available": self.qa_pipeline is not None,
            "models": {
                "qa_model": self.qa_model if self.initialized else None,
                "device": "GPU" if torch and torch.cuda.is_available() else "CPU" if HF_AVAILABLE else "Not Available"
            },
            "capabilities": {
                "single_document_qa": self.initialized,
                "multi_document_qa": self.initialized,
                "conversational_qa": self.initialized,
                "follow_up_questions": True,
                "context_length": self.max_context_length,
                "citation_support": True
            },
            "configuration": {
                "confidence_threshold": self.confidence_threshold,
                "max_context_length": self.max_context_length,
                "top_k_documents": self.top_k_documents,
                "context_memory_limit": self.context_memory_limit
            },
            "analytics": self.qa_analytics,
            "active_sessions": len(self.conversation_sessions)
        }
    
    # Phase 3 Enhanced Methods
    
    async def conversational_qa(self, question: str, session_id: Optional[str] = None, 
                               context_limit: int = 5) -> ConversationResponse:
        """
        Enhanced conversational Q&A with session context and follow-up suggestions
        
        Args:
            question: Current question
            session_id: Optional session ID for conversation continuity
            context_limit: Number of documents to consider for context
            
        Returns:
            ConversationResponse with answer, context, and suggestions
        """
        if not self.initialized:
            raise Exception("Q&A service not initialized")
        
        start_time = time.time()
        
        try:
            # Generate session ID if not provided
            if not session_id:
                session_id = str(uuid.uuid4())
            
            # Get or create conversation context
            conversation_context = self.conversation_sessions.get(session_id, [])
            
            # Enhance question with conversation context
            enhanced_question = self._enhance_question_with_context(question, conversation_context)
            
            # Get answer using enhanced question
            qa_result = await self.answer_question(enhanced_question, context_limit)
            
            # Generate follow-up suggestions
            follow_ups = await self.suggest_follow_up_questions(question, qa_result.answer)
            
            # Update conversation context
            conversation_entry = {
                "question": question,
                "answer": qa_result.answer,
                "confidence": qa_result.confidence,
                "timestamp": datetime.now().isoformat(),
                "documents_used": len(qa_result.source_documents)
            }
            
            conversation_context.append(conversation_entry)
            
            # Limit conversation history
            if len(conversation_context) > self.context_memory_limit:
                conversation_context = conversation_context[-self.context_memory_limit:]
            
            self.conversation_sessions[session_id] = conversation_context
            
            # Update analytics
            self._update_qa_analytics(question, qa_result.confidence, time.time() - start_time)
            
            return ConversationResponse(
                current_answer=qa_result,
                conversation_context=conversation_context,
                suggested_follow_ups=follow_ups,
                session_id=session_id
            )
            
        except Exception as e:
            logger.error(f"Conversational Q&A failed: {str(e)}")
            raise
    
    async def cite_sources(self, answer: str, sources: List[SearchResult]) -> CitedResponse:
        """
        Generate detailed citations for answer sources
        
        Args:
            answer: The generated answer
            sources: Source documents used
            
        Returns:
            CitedResponse with detailed citations
        """
        try:
            citations = []
            citation_quality = "high"
            
            for i, source in enumerate(sources[:5]):  # Limit to top 5 sources
                # Extract relevant passages that contributed to the answer
                relevant_passages = self._extract_relevant_passages(answer, source.content)
                
                citation = {
                    "source_id": i + 1,
                    "filename": source.filename,
                    "relevance_score": source.score,
                    "relevant_passages": relevant_passages,
                    "document_type": self._get_document_type(source.filename),
                    "context": source.content[:200] + "...",
                    "citation_strength": "strong" if source.score > 0.8 else "moderate" if source.score > 0.5 else "weak"
                }
                citations.append(citation)
            
            # Assess overall citation quality
            if len(citations) < 2:
                citation_quality = "low"
            elif all(c["citation_strength"] == "weak" for c in citations):
                citation_quality = "moderate"
            
            # Format answer with inline citations
            cited_answer = self._format_answer_with_citations(answer, citations)
            
            return CitedResponse(
                answer=cited_answer,
                citations=citations,
                confidence=0.8,  # Base confidence for cited response
                citation_quality=citation_quality
            )
            
        except Exception as e:
            logger.error(f"Citation generation failed: {str(e)}")
            return CitedResponse(answer, [], 0.5, "error")
    
    async def suggest_related_questions(self, question: str, context: str) -> List[str]:
        """
        Generate related questions based on the current question and context
        
        Args:
            question: Current question
            context: Context from documents
            
        Returns:
            List of related question suggestions
        """
        try:
            related_questions = []
            
            # Extract key topics from question and context
            key_topics = self._extract_key_topics(question + " " + context)
            
            # Generate questions based on question patterns
            question_templates = [
                "What are the benefits of {topic}?",
                "How does {topic} work?",
                "What are the challenges with {topic}?",
                "Who is involved in {topic}?",
                "When should {topic} be used?",
                "What are alternatives to {topic}?",
                "What is the impact of {topic}?",
                "How can {topic} be improved?"
            ]
            
            # Generate questions for each key topic
            for topic in key_topics[:3]:  # Limit to top 3 topics
                for template in question_templates[:3]:  # Use first 3 templates
                    related_question = template.format(topic=topic)
                    if related_question not in related_questions:
                        related_questions.append(related_question)
            
            # Add generic follow-ups
            generic_questions = [
                "Can you provide more details about this topic?",
                "What are the key points I should remember?",
                "Are there any examples or case studies?"
            ]
            
            related_questions.extend(generic_questions)
            
            return related_questions[:8]  # Return top 8 suggestions
            
        except Exception as e:
            logger.warning(f"Related question generation failed: {str(e)}")
            return [
                "Can you tell me more about this?",
                "What are the main points?",
                "Are there any examples?"
            ]
    
    async def get_conversation_summary(self, session_id: str) -> Dict[str, Any]:
        """Get summary of conversation session"""
        try:
            if session_id not in self.conversation_sessions:
                return {"error": "Session not found"}
            
            conversation = self.conversation_sessions[session_id]
            
            # Calculate session statistics
            total_questions = len(conversation)
            avg_confidence = sum(entry["confidence"] for entry in conversation) / total_questions if total_questions > 0 else 0
            topics_discussed = list(set(self._extract_key_topics(entry["question"]) for entry in conversation))
            
            return {
                "session_id": session_id,
                "total_questions": total_questions,
                "average_confidence": avg_confidence,
                "duration_minutes": self._calculate_session_duration(conversation),
                "topics_discussed": [topic for sublist in topics_discussed for topic in sublist][:10],
                "conversation_quality": "high" if avg_confidence > 0.7 else "moderate" if avg_confidence > 0.4 else "low",
                "last_activity": conversation[-1]["timestamp"] if conversation else None
            }
            
        except Exception as e:
            logger.error(f"Conversation summary generation failed: {str(e)}")
            return {"error": str(e)}
    
    async def clear_conversation_session(self, session_id: str) -> bool:
        """Clear conversation session"""
        try:
            if session_id in self.conversation_sessions:
                del self.conversation_sessions[session_id]
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to clear conversation session: {str(e)}")
            return False
    
    def get_analytics_summary(self) -> Dict[str, Any]:
        """Get comprehensive Q&A analytics"""
        try:
            # Calculate success rate
            success_rate = (self.qa_analytics["successful_answers"] / 
                          max(self.qa_analytics["total_questions"], 1)) * 100
            
            # Get popular topics
            popular_topics = sorted(
                self.qa_analytics["popular_topics"].items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:10]
            
            return {
                "overview": {
                    "total_questions": self.qa_analytics["total_questions"],
                    "successful_answers": self.qa_analytics["successful_answers"],
                    "success_rate": success_rate,
                    "average_confidence": self.qa_analytics["average_confidence"],
                    "active_conversations": len(self.conversation_sessions)
                },
                "popular_topics": [{"topic": topic, "count": count} for topic, count in popular_topics],
                "conversation_stats": {
                    "total_sessions": self.qa_analytics["conversation_sessions"],
                    "active_sessions": len(self.conversation_sessions),
                    "average_session_length": self._calculate_average_session_length()
                },
                "last_updated": self.qa_analytics["last_updated"]
            }
            
        except Exception as e:
            logger.error(f"Analytics summary generation failed: {str(e)}")
            return {"error": str(e)}
    
    # Helper Methods for Phase 3 Features
    
    def _enhance_question_with_context(self, question: str, conversation_context: List[Dict]) -> str:
        """Enhance question with conversation context"""
        try:
            if not conversation_context:
                return question
            
            # Get recent context (last 3 exchanges)
            recent_context = conversation_context[-3:]
            context_text = " ".join([
                f"Previous Q: {entry['question']} A: {entry['answer'][:100]}"
                for entry in recent_context
            ])
            
            # Simple context enhancement
            enhanced = f"Context: {context_text[:200]}... Current question: {question}"
            return enhanced if len(enhanced) < 500 else question
            
        except Exception as e:
            logger.warning(f"Question context enhancement failed: {str(e)}")
            return question
    
    def _extract_relevant_passages(self, answer: str, content: str) -> List[str]:
        """Extract passages from content that are relevant to the answer"""
        try:
            # Simple overlap-based extraction
            answer_words = set(answer.lower().split())
            sentences = content.split('.')
            
            relevant_passages = []
            for sentence in sentences:
                sentence_words = set(sentence.lower().split())
                overlap = len(answer_words.intersection(sentence_words))
                
                if overlap > 2 and len(sentence.strip()) > 20:
                    relevant_passages.append(sentence.strip())
            
            return relevant_passages[:3]  # Return top 3 passages
            
        except Exception as e:
            logger.warning(f"Passage extraction failed: {str(e)}")
            return []
    
    def _get_document_type(self, filename: str) -> str:
        """Get document type from filename"""
        extension = filename.split('.')[-1].lower() if '.' in filename else 'unknown'
        type_mapping = {
            'pdf': 'PDF Document',
            'txt': 'Text File',
            'docx': 'Word Document',
            'md': 'Markdown File',
            'html': 'Web Page',
            'json': 'JSON Data'
        }
        return type_mapping.get(extension, 'Unknown Document')
    
    def _format_answer_with_citations(self, answer: str, citations: List[Dict]) -> str:
        """Format answer with inline citations"""
        try:
            # Simple citation formatting
            cited_answer = answer
            for i, citation in enumerate(citations):
                source_ref = f" [{i+1}]"
                # Add citation at the end for simplicity
                if i == 0:
                    cited_answer += source_ref
            
            # Add citations list
            citation_list = "\n\nSources:\n"
            for i, citation in enumerate(citations):
                citation_list += f"[{i+1}] {citation['filename']} (Relevance: {citation['citation_strength']})\n"
            
            return cited_answer + citation_list
            
        except Exception as e:
            logger.warning(f"Citation formatting failed: {str(e)}")
            return answer
    
    def _extract_key_topics(self, text: str) -> List[str]:
        """Extract key topics from text"""
        try:
            # Simple keyword extraction
            words = text.lower().split()
            
            # Filter out common words
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'what', 'how', 'why', 'when', 'where', 'who'}
            keywords = [word.strip('.,!?;') for word in words if len(word) > 3 and word not in stop_words]
            
            # Count frequency and return most common
            word_freq = {}
            for word in keywords:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            topics = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            return [topic[0] for topic in topics[:5]]
            
        except Exception as e:
            logger.warning(f"Topic extraction failed: {str(e)}")
            return []
    
    def _calculate_session_duration(self, conversation: List[Dict]) -> float:
        """Calculate session duration in minutes"""
        try:
            if len(conversation) < 2:
                return 0.0
            
            start_time = datetime.fromisoformat(conversation[0]["timestamp"])
            end_time = datetime.fromisoformat(conversation[-1]["timestamp"])
            duration = (end_time - start_time).total_seconds() / 60
            
            return round(duration, 2)
            
        except Exception as e:
            logger.warning(f"Session duration calculation failed: {str(e)}")
            return 0.0
    
    def _calculate_average_session_length(self) -> float:
        """Calculate average session length across all sessions"""
        try:
            if not self.conversation_sessions:
                return 0.0
            
            total_questions = sum(len(session) for session in self.conversation_sessions.values())
            total_sessions = len(self.conversation_sessions)
            
            return round(total_questions / total_sessions, 2) if total_sessions > 0 else 0.0
            
        except Exception as e:
            logger.warning(f"Average session length calculation failed: {str(e)}")
            return 0.0
    
    def _update_qa_analytics(self, question: str, confidence: float, processing_time: float):
        """Update Q&A analytics"""
        try:
            self.qa_analytics["total_questions"] += 1
            
            if confidence > self.confidence_threshold:
                self.qa_analytics["successful_answers"] += 1
            
            # Update average confidence
            total = self.qa_analytics["total_questions"]
            current_avg = self.qa_analytics["average_confidence"]
            self.qa_analytics["average_confidence"] = (current_avg * (total - 1) + confidence) / total
            
            # Update popular topics
            topics = self._extract_key_topics(question)
            for topic in topics:
                self.qa_analytics["popular_topics"][topic] = self.qa_analytics["popular_topics"].get(topic, 0) + 1
            
            self.qa_analytics["last_updated"] = datetime.now().isoformat()
            
        except Exception as e:
            logger.warning(f"Analytics update failed: {str(e)}")
