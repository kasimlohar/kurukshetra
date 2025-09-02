"""
Knowledge Graph Service for ConfluxAI - Phase 3 Enhancement
Provides entity relationship mapping and graph-based search capabilities
"""
import logging
import asyncio
from typing import List, Dict, Any, Optional, Set, Tuple
from datetime import datetime
import json
import sqlite3
from pathlib import Path

# NLP Dependencies
try:
    import spacy
    from spacy import displacy
    import networkx as nx
    import numpy as np
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

from models.schemas import SearchResult
from services.search_service import SearchService
from config.settings import Settings

logger = logging.getLogger(__name__)

class Entity:
    """Entity representation in knowledge graph"""
    def __init__(self, entity_id: str, name: str, entity_type: str, 
                 confidence: float, metadata: Dict[str, Any] = None):
        self.entity_id = entity_id
        self.name = name
        self.entity_type = entity_type
        self.confidence = confidence
        self.metadata = metadata or {}
        self.mentions = []
        self.relationships = []

class Relationship:
    """Relationship between entities"""
    def __init__(self, source_entity: str, target_entity: str, 
                 relation_type: str, confidence: float, context: str = ""):
        self.source_entity = source_entity
        self.target_entity = target_entity
        self.relation_type = relation_type
        self.confidence = confidence
        self.context = context
        self.timestamp = datetime.now()

class GraphSearchResult:
    """Graph-based search result"""
    def __init__(self, entities: List[Entity], relationships: List[Relationship], 
                 subgraph: Dict[str, Any], relevance_score: float):
        self.entities = entities
        self.relationships = relationships
        self.subgraph = subgraph
        self.relevance_score = relevance_score
        self.timestamp = datetime.now()

class GraphVisualization:
    """Graph visualization data"""
    def __init__(self, nodes: List[Dict], edges: List[Dict], layout: str = "force"):
        self.nodes = nodes
        self.edges = edges
        self.layout = layout
        self.metadata = {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "generated_at": datetime.now().isoformat()
        }

class KnowledgeGraphService:
    """Advanced knowledge graph service for entity relationship mapping"""
    
    def __init__(self, search_service: SearchService):
        self.settings = Settings()
        self.search_service = search_service
        self.nlp = None
        self.graph = None
        self.entity_index = {}
        self.initialized = False
        
        # Database for persistent storage
        self.db_path = Path(self.settings.INDEX_DIR) / "knowledge_graph.db"
        
        # Configuration
        self.entity_types = [
            "PERSON", "ORG", "GPE", "PRODUCT", "EVENT", 
            "WORK_OF_ART", "LAW", "LANGUAGE", "DATE", "TIME"
        ]
        self.relation_types = [
            "WORKS_FOR", "LOCATED_IN", "PART_OF", "RELATED_TO",
            "CREATED_BY", "MENTIONS", "REFERS_TO", "SIMILAR_TO"
        ]
    
    async def initialize(self):
        """Initialize knowledge graph service"""
        try:
            logger.info("Initializing Knowledge Graph service...")
            
            if not SPACY_AVAILABLE:
                logger.warning("spaCy not available. Knowledge graph features will be limited.")
                self.initialized = False
                return
            
            # Initialize spaCy model
            try:
                self.nlp = spacy.load("en_core_web_sm")
                logger.info("Loaded spaCy English model")
            except OSError:
                logger.warning("spaCy English model not found. Install with: python -m spacy download en_core_web_sm")
                self.initialized = False
                return
            
            # Initialize NetworkX graph
            self.graph = nx.DiGraph()
            
            # Initialize database
            await self._init_database()
            
            # Load existing graph data
            await self._load_graph_from_db()
            
            self.initialized = True
            logger.info("Knowledge Graph service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Knowledge Graph service: {str(e)}")
            self.initialized = False
    
    async def extract_entities(self, text: str, document_id: str = None) -> List[Entity]:
        """Extract entities from text using NLP"""
        if not self.initialized or not self.nlp:
            return []
        
        try:
            # Process text with spaCy
            doc = self.nlp(text)
            
            entities = []
            for ent in doc.ents:
                if ent.label_ in self.entity_types and len(ent.text.strip()) > 1:
                    entity_id = self._generate_entity_id(ent.text, ent.label_)
                    
                    entity = Entity(
                        entity_id=entity_id,
                        name=ent.text.strip(),
                        entity_type=ent.label_,
                        confidence=0.8,  # Base confidence from spaCy
                        metadata={
                            "start_char": ent.start_char,
                            "end_char": ent.end_char,
                            "document_id": document_id,
                            "context": text[max(0, ent.start_char-50):ent.end_char+50]
                        }
                    )
                    entities.append(entity)
            
            # Store entities in database
            if entities:
                await self._store_entities(entities)
            
            return entities
            
        except Exception as e:
            logger.error(f"Entity extraction failed: {str(e)}")
            return []
    
    async def build_relationships(self, entities: List[Entity], context: str = "") -> List[Relationship]:
        """Build relationships between entities"""
        if not self.initialized:
            return []
        
        try:
            relationships = []
            
            # Extract co-occurrence relationships
            for i, entity1 in enumerate(entities):
                for entity2 in entities[i+1:]:
                    # Check if entities co-occur in the same context
                    relation = await self._infer_relationship(entity1, entity2, context)
                    if relation:
                        relationships.append(relation)
            
            # Store relationships in database
            if relationships:
                await self._store_relationships(relationships)
            
            return relationships
            
        except Exception as e:
            logger.error(f"Relationship building failed: {str(e)}")
            return []
    
    async def graph_search(self, query: str, max_depth: int = 2, max_results: int = 10) -> GraphSearchResult:
        """Perform graph-based search for related entities and concepts"""
        if not self.initialized:
            return GraphSearchResult([], [], {}, 0.0)
        
        try:
            # Extract entities from query
            query_entities = await self.extract_entities(query)
            
            if not query_entities:
                # Fallback to keyword matching
                query_entities = await self._find_entities_by_keywords(query)
            
            if not query_entities:
                return GraphSearchResult([], [], {}, 0.0)
            
            # Find related entities through graph traversal
            related_entities = set()
            relationships = []
            
            for entity in query_entities:
                # Get direct neighbors
                if entity.entity_id in self.graph:
                    neighbors = list(self.graph.neighbors(entity.entity_id))
                    related_entities.update(neighbors[:max_results//2])
                    
                    # Get relationships
                    for neighbor in neighbors[:max_results//2]:
                        edge_data = self.graph.get_edge_data(entity.entity_id, neighbor)
                        if edge_data:
                            relationships.append(Relationship(
                                source_entity=entity.entity_id,
                                target_entity=neighbor,
                                relation_type=edge_data.get('type', 'RELATED_TO'),
                                confidence=edge_data.get('confidence', 0.5),
                                context=edge_data.get('context', '')
                            ))
            
            # Create subgraph
            subgraph_nodes = [e.entity_id for e in query_entities] + list(related_entities)
            subgraph = self.graph.subgraph(subgraph_nodes)
            
            # Convert to dict for serialization
            subgraph_dict = {
                "nodes": [{"id": node, "data": self.graph.nodes[node]} for node in subgraph.nodes()],
                "edges": [{"source": edge[0], "target": edge[1], "data": self.graph.edges[edge]} 
                         for edge in subgraph.edges()]
            }
            
            # Calculate relevance score based on graph connectivity
            relevance_score = min(1.0, len(related_entities) / max_results)
            
            return GraphSearchResult(
                entities=query_entities + [self._get_entity_by_id(eid) for eid in related_entities],
                relationships=relationships,
                subgraph=subgraph_dict,
                relevance_score=relevance_score
            )
            
        except Exception as e:
            logger.error(f"Graph search failed: {str(e)}")
            return GraphSearchResult([], [], {}, 0.0)
    
    async def visualize_connections(self, entity_name: str, max_connections: int = 20) -> GraphVisualization:
        """Create visualization data for entity connections"""
        if not self.initialized:
            return GraphVisualization([], [])
        
        try:
            # Find entity
            entity = await self._find_entity_by_name(entity_name)
            if not entity:
                return GraphVisualization([], [])
            
            # Get connected entities
            if entity.entity_id in self.graph:
                neighbors = list(self.graph.neighbors(entity.entity_id))[:max_connections]
                all_nodes = [entity.entity_id] + neighbors
                
                # Create visualization nodes
                nodes = []
                for node_id in all_nodes:
                    node_data = self.graph.nodes.get(node_id, {})
                    nodes.append({
                        "id": node_id,
                        "label": node_data.get("name", node_id),
                        "type": node_data.get("type", "UNKNOWN"),
                        "size": 20 if node_id == entity.entity_id else 10,
                        "color": self._get_node_color(node_data.get("type", "UNKNOWN"))
                    })
                
                # Create visualization edges
                edges = []
                for neighbor in neighbors:
                    edge_data = self.graph.get_edge_data(entity.entity_id, neighbor, {})
                    edges.append({
                        "source": entity.entity_id,
                        "target": neighbor,
                        "label": edge_data.get("type", "RELATED_TO"),
                        "weight": edge_data.get("confidence", 0.5),
                        "color": self._get_edge_color(edge_data.get("type", "RELATED_TO"))
                    })
                
                return GraphVisualization(nodes, edges, "force")
            
            return GraphVisualization([], [])
            
        except Exception as e:
            logger.error(f"Visualization creation failed: {str(e)}")
            return GraphVisualization([], [])
    
    async def get_entity_clusters(self, min_cluster_size: int = 3) -> Dict[str, List[Entity]]:
        """Get clusters of related entities"""
        if not self.initialized:
            return {}
        
        try:
            # Use community detection for clustering
            if len(self.graph.nodes()) < min_cluster_size:
                return {}
            
            # Convert to undirected graph for community detection
            undirected_graph = self.graph.to_undirected()
            
            # Simple clustering based on connected components
            clusters = {}
            for i, component in enumerate(nx.connected_components(undirected_graph)):
                if len(component) >= min_cluster_size:
                    cluster_name = f"cluster_{i}"
                    clusters[cluster_name] = [
                        self._get_entity_by_id(entity_id) for entity_id in component
                    ]
            
            return clusters
            
        except Exception as e:
            logger.error(f"Entity clustering failed: {str(e)}")
            return {}
    
    # Private helper methods
    
    async def _init_database(self):
        """Initialize SQLite database for knowledge graph storage"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create entities table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS entities (
                    entity_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    entity_type TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create relationships table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS relationships (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_entity TEXT NOT NULL,
                    target_entity TEXT NOT NULL,
                    relation_type TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    context TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (source_entity) REFERENCES entities (entity_id),
                    FOREIGN KEY (target_entity) REFERENCES entities (entity_id)
                )
            ''')
            
            # Create indexes
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_entity_name ON entities (name)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_entity_type ON entities (entity_type)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_relationship_source ON relationships (source_entity)')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Database initialization failed: {str(e)}")
            raise
    
    async def _load_graph_from_db(self):
        """Load existing graph data from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Load entities
            cursor.execute("SELECT * FROM entities")
            for row in cursor.fetchall():
                entity_id, name, entity_type, confidence, metadata_str, created_at = row
                metadata = json.loads(metadata_str) if metadata_str else {}
                
                self.graph.add_node(entity_id, 
                                  name=name, 
                                  type=entity_type, 
                                  confidence=confidence,
                                  metadata=metadata)
                
                self.entity_index[entity_id] = Entity(entity_id, name, entity_type, confidence, metadata)
            
            # Load relationships
            cursor.execute("SELECT * FROM relationships")
            for row in cursor.fetchall():
                _, source, target, rel_type, confidence, context, created_at = row
                self.graph.add_edge(source, target, 
                                  type=rel_type, 
                                  confidence=confidence,
                                  context=context)
            
            conn.close()
            logger.info(f"Loaded knowledge graph: {len(self.graph.nodes())} entities, {len(self.graph.edges())} relationships")
            
        except Exception as e:
            logger.error(f"Failed to load graph from database: {str(e)}")
    
    async def _store_entities(self, entities: List[Entity]):
        """Store entities in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for entity in entities:
                cursor.execute('''
                    INSERT OR REPLACE INTO entities 
                    (entity_id, name, entity_type, confidence, metadata)
                    VALUES (?, ?, ?, ?, ?)
                ''', (entity.entity_id, entity.name, entity.entity_type, 
                     entity.confidence, json.dumps(entity.metadata)))
                
                # Add to graph
                self.graph.add_node(entity.entity_id,
                                  name=entity.name,
                                  type=entity.entity_type,
                                  confidence=entity.confidence,
                                  metadata=entity.metadata)
                
                # Add to entity index
                self.entity_index[entity.entity_id] = entity
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to store entities: {str(e)}")
    
    async def _store_relationships(self, relationships: List[Relationship]):
        """Store relationships in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for rel in relationships:
                cursor.execute('''
                    INSERT INTO relationships 
                    (source_entity, target_entity, relation_type, confidence, context)
                    VALUES (?, ?, ?, ?, ?)
                ''', (rel.source_entity, rel.target_entity, rel.relation_type,
                     rel.confidence, rel.context))
                
                # Add to graph
                self.graph.add_edge(rel.source_entity, rel.target_entity,
                                  type=rel.relation_type,
                                  confidence=rel.confidence,
                                  context=rel.context)
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to store relationships: {str(e)}")
    
    def _generate_entity_id(self, name: str, entity_type: str) -> str:
        """Generate unique entity ID"""
        import hashlib
        content = f"{name.lower().strip()}:{entity_type}"
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    async def _infer_relationship(self, entity1: Entity, entity2: Entity, context: str) -> Optional[Relationship]:
        """Infer relationship between two entities"""
        try:
            # Simple co-occurrence based relationship inference
            confidence = 0.6  # Base confidence for co-occurrence
            
            # Determine relationship type based on entity types
            rel_type = "RELATED_TO"  # Default
            
            if entity1.entity_type == "PERSON" and entity2.entity_type == "ORG":
                rel_type = "WORKS_FOR"
                confidence = 0.7
            elif entity1.entity_type == "PERSON" and entity2.entity_type == "GPE":
                rel_type = "LOCATED_IN"
                confidence = 0.6
            elif entity1.entity_type == "ORG" and entity2.entity_type == "GPE":
                rel_type = "LOCATED_IN"
                confidence = 0.6
            elif entity1.entity_type == entity2.entity_type:
                rel_type = "SIMILAR_TO"
                confidence = 0.5
            
            return Relationship(
                source_entity=entity1.entity_id,
                target_entity=entity2.entity_id,
                relation_type=rel_type,
                confidence=confidence,
                context=context[:200]  # Truncate context
            )
            
        except Exception as e:
            logger.warning(f"Relationship inference failed: {str(e)}")
            return None
    
    async def _find_entities_by_keywords(self, query: str) -> List[Entity]:
        """Find entities matching query keywords"""
        try:
            keywords = query.lower().split()
            matching_entities = []
            
            for entity in self.entity_index.values():
                for keyword in keywords:
                    if keyword in entity.name.lower():
                        matching_entities.append(entity)
                        break
            
            return matching_entities[:10]  # Limit results
            
        except Exception as e:
            logger.error(f"Keyword entity search failed: {str(e)}")
            return []
    
    async def _find_entity_by_name(self, name: str) -> Optional[Entity]:
        """Find entity by name"""
        name_lower = name.lower()
        for entity in self.entity_index.values():
            if entity.name.lower() == name_lower:
                return entity
        return None
    
    def _get_entity_by_id(self, entity_id: str) -> Optional[Entity]:
        """Get entity by ID"""
        return self.entity_index.get(entity_id)
    
    def _get_node_color(self, entity_type: str) -> str:
        """Get color for entity type in visualization"""
        colors = {
            "PERSON": "#FF6B6B",
            "ORG": "#4ECDC4", 
            "GPE": "#45B7D1",
            "PRODUCT": "#96CEB4",
            "EVENT": "#FECA57",
            "WORK_OF_ART": "#FF9FF3",
            "LAW": "#54A0FF",
            "LANGUAGE": "#5F27CD",
            "DATE": "#00D2D3",
            "TIME": "#FF9F43"
        }
        return colors.get(entity_type, "#95A5A6")
    
    def _get_edge_color(self, relation_type: str) -> str:
        """Get color for relationship type in visualization"""
        colors = {
            "WORKS_FOR": "#2C3E50",
            "LOCATED_IN": "#27AE60",
            "PART_OF": "#8E44AD",
            "RELATED_TO": "#95A5A6",
            "CREATED_BY": "#E74C3C",
            "MENTIONS": "#F39C12",
            "REFERS_TO": "#3498DB",
            "SIMILAR_TO": "#16A085"
        }
        return colors.get(relation_type, "#BDC3C7")
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for knowledge graph service"""
        return {
            "status": "healthy" if self.initialized else "unhealthy",
            "initialized": self.initialized,
            "entities_count": len(self.graph.nodes()) if self.graph else 0,
            "relationships_count": len(self.graph.edges()) if self.graph else 0,
            "spacy_available": SPACY_AVAILABLE,
            "sklearn_available": SKLEARN_AVAILABLE,
            "database_path": str(self.db_path),
            "last_check": datetime.now().isoformat()
        }
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get comprehensive service status"""
        return {
            "initialized": self.initialized,
            "graph_available": self.graph is not None,
            "entity_count": len(self.entity_index),
            "capabilities": {
                "entity_extraction": self.initialized and SPACY_AVAILABLE,
                "relationship_building": self.initialized,
                "graph_search": self.initialized,
                "visualization": self.initialized,
                "clustering": self.initialized
            },
            "models": {
                "spacy_model": "en_core_web_sm" if self.nlp else None,
                "graph_library": "NetworkX" if nx else None
            },
            "database": {
                "path": str(self.db_path),
                "exists": self.db_path.exists()
            }
        }
