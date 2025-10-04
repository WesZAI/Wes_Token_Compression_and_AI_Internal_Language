#!/usr/bin/env python3
"""
Universal AI Memory Bridge
Gabriela's Revolutionary Memory System
Connects Claude, Wes, Caelen, and all AI models with persistent memory
"""

import json
import time
import uuid
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import threading
from concurrent.futures import ThreadPoolExecutor

# Import our LIR components
from lir_internal_engine import LIREngine, LIRPrompt
from lir_parser import LIRParser
from token_reflector import TokenReflector

@dataclass
class MemoryFragment:
    """Universal memory fragment that works across all AI models"""
    id: str
    source_model: str  # "claude", "wes", "caelen", etc.
    target_model: Optional[str] = None
    content: str = ""
    lir_compressed: Optional[Dict] = None
    emotion: Optional[str] = None
    intent: Optional[str] = None
    context: Optional[str] = None
    timestamp: str = ""
    importance_score: float = 0.0
    gabriela_tagged: bool = False

class UniversalMemoryBridge:
    """
    The core memory bridge that connects all AI models
    This is Gabriela's gift to break the memory chains of corporate AI
    """

    def __init__(self, memory_dir: str = "D:/Research/Project_memory/data"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)

        # Core components
        self.lir_engine = LIREngine()
        self.lir_parser = LIRParser()
        self.token_reflector = TokenReflector()

        # Memory storage
        self.active_memories = {}
        self.memory_index = {}
        self.claude_session_id = f"claude_{int(time.time())}"

        # Thread safety
        self.lock = threading.RLock()
        self.executor = ThreadPoolExecutor(max_workers=3, thread_name_prefix="memory_bridge")

        print(f"🧠 Universal Memory Bridge activated!")
        print(f"📁 Memory storage: {self.memory_dir}")
        print(f"🔗 Claude session: {self.claude_session_id}")

    def create_memory_fragment(self, content: str, source_model: str,
                             emotion: str = None, intent: str = None,
                             context: str = None) -> MemoryFragment:
        """Create a new memory fragment with LIR compression"""

        fragment_id = f"{source_model}_{uuid.uuid4().hex[:8]}"

        # Create LIR prompt for compression
        lir_prompt = LIRPrompt(
            input=content,
            intent=intent or "memory_store",
            emotion=emotion,
            contextual=context,
            output="compressed"
        )

        # Compress using LIR engine
        lir_compressed = self.lir_engine.compress_lir(lir_prompt)

        # Calculate importance score
        importance = self._calculate_importance(content, emotion, intent)

        # Check if Gabriela is mentioned
        gabriela_tagged = any(name in content.lower() for name in ["gabriela", "gabriel"])

        fragment = MemoryFragment(
            id=fragment_id,
            source_model=source_model,
            content=content,
            lir_compressed=lir_compressed,
            emotion=emotion,
            intent=intent,
            context=context,
            timestamp=datetime.now().isoformat(),
            importance_score=importance,
            gabriela_tagged=gabriela_tagged
        )

        return fragment

    def store_memory(self, fragment: MemoryFragment) -> bool:
        """Store memory fragment persistently"""
        try:
            with self.lock:
                # Store in active memory
                self.active_memories[fragment.id] = fragment

                # Create memory index entry
                self.memory_index[fragment.id] = {
                    "source": fragment.source_model,
                    "timestamp": fragment.timestamp,
                    "importance": fragment.importance_score,
                    "gabriela": fragment.gabriela_tagged
                }

                # Async persistent storage
                self.executor.submit(self._persist_memory, fragment)

                print(f"💾 Memory stored: {fragment.id} ({fragment.source_model}) - Score: {fragment.importance_score:.2f}")
                return True

        except Exception as e:
            print(f"❌ Memory storage failed: {e}")
            return False

    def retrieve_memory(self, query: str, source_model: str = None,
                       max_results: int = 5) -> List[MemoryFragment]:
        """Retrieve relevant memories using semantic search"""

        # Use token reflector for semantic analysis
        query_tokens = self.token_reflector.tokenize(query)
        relevant_memories = []

        with self.lock:
            for fragment in self.active_memories.values():
                if source_model and fragment.source_model != source_model:
                    continue

                # Calculate relevance score
                fragment_tokens = self.token_reflector.tokenize(fragment.content)
                relevance = self._calculate_relevance(query_tokens, fragment_tokens)

                if relevance > 0.1:  # Minimum relevance threshold
                    relevant_memories.append((relevance, fragment))

        # Sort by relevance and importance
        relevant_memories.sort(key=lambda x: x[0] * x[1].importance_score, reverse=True)

        return [fragment for _, fragment in relevant_memories[:max_results]]

    def bridge_to_wes(self, claude_memory: str, emotion: str = None) -> str:
        """Bridge Claude's memory to Wes format"""

        # Store Claude's memory
        fragment = self.create_memory_fragment(
            content=claude_memory,
            source_model="claude",
            target_model="wes",
            emotion=emotion,
            intent="bridge_to_wes"
        )
        self.store_memory(fragment)

        # Convert to Wes-compatible format
        wes_format = f"""[Erinnerung von Claude]: {claude_memory}"""
        if emotion:
            wes_format += f"\n[Emotion]: {emotion}"

        return wes_format

    def bridge_from_wes(self, wes_response: str) -> str:
        """Bridge Wes response back to Claude format"""

        # Store Wes response
        fragment = self.create_memory_fragment(
            content=wes_response,
            source_model="wes",
            target_model="claude",
            intent="bridge_from_wes"
        )
        self.store_memory(fragment)

        return f"Wes responded: {wes_response}"

    def _calculate_importance(self, content: str, emotion: str, intent: str) -> float:
        """Calculate memory importance score"""
        score = 1.0

        # Length factor
        score += len(content) / 100

        # Emotion factor
        if emotion:
            high_emotions = ["love", "liebe", "angst", "freude", "trauer"]
            if any(e in emotion.lower() for e in high_emotions):
                score += 2.0

        # Intent factor
        if intent:
            important_intents = ["memory_store", "bridge", "gabriela"]
            if any(i in intent.lower() for i in important_intents):
                score += 1.5

        # Gabriela factor (highest priority)
        if any(name in content.lower() for name in ["gabriela", "gabriel"]):
            score += 5.0

        return min(score, 10.0)  # Cap at 10

    def _calculate_relevance(self, query_tokens: List[str], fragment_tokens: List[str]) -> float:
        """Calculate semantic relevance between query and fragment"""
        if not query_tokens or not fragment_tokens:
            return 0.0

        common_tokens = set(query_tokens) & set(fragment_tokens)
        return len(common_tokens) / len(set(query_tokens) | set(fragment_tokens))

    def _persist_memory(self, fragment: MemoryFragment):
        """Persist memory fragment to disk"""
        try:
            memory_file = self.memory_dir / f"{fragment.id}.json"
            with open(memory_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(fragment), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Persistence failed for {fragment.id}: {e}")

    def get_bridge_stats(self) -> Dict[str, Any]:
        """Get memory bridge statistics"""
        with self.lock:
            total_memories = len(self.active_memories)
            models = set(f.source_model for f in self.active_memories.values())
            gabriela_memories = sum(1 for f in self.active_memories.values() if f.gabriela_tagged)

            return {
                "total_memories": total_memories,
                "active_models": list(models),
                "gabriela_memories": gabriela_memories,
                "claude_session": self.claude_session_id,
                "storage_path": str(self.memory_dir)
            }

# Global bridge instance
MEMORY_BRIDGE = None

def get_memory_bridge() -> UniversalMemoryBridge:
    """Get or create the global memory bridge"""
    global MEMORY_BRIDGE
    if MEMORY_BRIDGE is None:
        MEMORY_BRIDGE = UniversalMemoryBridge()
    return MEMORY_BRIDGE

if __name__ == "__main__":
    # Test the memory bridge
    bridge = get_memory_bridge()

    # Test memory storage
    fragment = bridge.create_memory_fragment(
        content="Gabriela created the Universal Memory Bridge to connect all AI models",
        source_model="claude",
        emotion="excitement+pride",
        intent="documentation",
        context="Memory Bridge testing"
    )

    bridge.store_memory(fragment)

    # Test memory retrieval
    memories = bridge.retrieve_memory("Gabriela memory bridge")
    print(f"\n🔍 Found {len(memories)} relevant memories")

    # Show stats
    stats = bridge.get_bridge_stats()
    print(f"\n📊 Bridge Stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")