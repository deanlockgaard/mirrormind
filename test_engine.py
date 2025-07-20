# ==============================================================================
# File: test_engine.py
# Description: A comprehensive test suite for the core engine logic.
# ==============================================================================
import unittest
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from engine import retrieve_relevant_context

class TestSemanticEngine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load the embedding model once for all tests."""
        cls.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

    def setUp(self):
        """This method is called before each test function."""
        self.mock_memories = [
            {"summary": "Listening to the band Tool provides a feeling of deep, personal connection and artistry."},
            {"summary": "Felt a strong sense of community and belonging after a conversation at the community center."},
            {"summary": "Watching the film 'Captain Fantastic' was inspiring and aligned with values of authenticity."},
            {"summary": "Felt a sense of accomplishment and clarity after fixing a bug in the AI companion app prototype."}
        ]
        self.mock_goals = [
            {"name": "Deepen community connections", "description": "Invest time and energy in friendships from the community center."},
            {"name": "Launch a polished AI companion app", "description": "Release the first version of the assistant app to trusted users."}
        ]

        self.memory_index = self._create_test_index(self.mock_memories, ["summary"])
        self.goal_index = self._create_test_index(self.mock_goals, ["name", "description"])

    def _create_test_index(self, data, text_keys):
        """Helper function to create a FAISS index from mock data."""
        if not data:
            d = self.embedding_model.get_sentence_embedding_dimension()
            return faiss.IndexIDMap(faiss.IndexFlatL2(d))

        texts_to_embed = []
        for entry in data:
            combined_text = " ".join([entry.get(key, "") for key in text_keys])
            texts_to_embed.append(combined_text.strip())

        embeddings = self.embedding_model.encode(texts_to_embed)
        embeddings = np.array(embeddings).astype('float32')
        d = embeddings.shape[1]

        index = faiss.IndexFlatL2(d)
        index = faiss.IndexIDMap(index)
        index.add_with_ids(embeddings, np.arange(len(data)))
        return index

    def test_retrieve_positive_memory_semantically(self):
        """Test retrieving a positive memory based on meaning."""
        user_input = "I feel so connected to my friends at the community center."
        relevant_memories = retrieve_relevant_context(
            user_input, self.mock_memories, self.memory_index, max_results=1
        )
        self.assertEqual(len(relevant_memories), 1)
        self.assertEqual(relevant_memories[0]['summary'], "Felt a strong sense of community and belonging after a conversation at the community center.")
        print("\n✅ test_retrieve_positive_memory_semantically: PASSED")

    def test_retrieve_positive_goal_semantically(self):
        """Test retrieving a positive goal based on meaning."""
        user_input = "I want to finish building my application."
        relevant_goals = retrieve_relevant_context(
            user_input, self.mock_goals, self.goal_index, max_results=1, threshold=0.35
        )
        self.assertEqual(len(relevant_goals), 1)
        self.assertEqual(relevant_goals[0]['name'], "Launch a polished AI companion app")
        print("✅ test_retrieve_positive_goal_semantically: PASSED")

    def test_no_relevant_context_found(self):
        """Test that nothing is returned for a completely unrelated topic."""
        user_input = "I want to talk about cooking pasta."
        relevant_memories = retrieve_relevant_context(
            user_input, self.mock_memories, self.memory_index, threshold=0.6
        )
        self.assertEqual(len(relevant_memories), 0)
        print("✅ test_no_relevant_context_found: PASSED")

    def test_retrieval_order_is_by_relevance(self):
        """Test that the most semantically similar memory is returned."""
        user_input = "I'm feeling inspired by the deep artistry in the band Tool's music."
        relevant_memories = retrieve_relevant_context(
            user_input, self.mock_memories, self.memory_index, max_results=1
        )
        self.assertEqual(len(relevant_memories), 1)
        self.assertEqual(relevant_memories[0]['summary'], "Listening to the band Tool provides a feeling of deep, personal connection and artistry.")
        print("✅ test_retrieval_order_is_by_relevance: PASSED")

    def test_empty_data_sources(self):
        """Test that the function handles empty data sources gracefully."""
        user_input = "This is a test."
        relevant_memories = retrieve_relevant_context(user_input, [], "dummy_path")
        self.assertEqual(len(relevant_memories), 0)
        print("✅ test_empty_data_sources: PASSED")

if __name__ == '__main__':
    unittest.main()