# ==============================================================================
# File: test_engine.py
# Description: A comprehensive test suite for the core engine logic.
# ==============================================================================
import unittest
from engine import retrieve_relevant_context

class TestEngine(unittest.TestCase):

    def setUp(self):
        """This method is called before each test function."""
        self.mock_memories = [
            {
                "timestamp": "2025-07-18T01:00:00Z",
                "summary": "Felt a deep sense of gratitude toward family and friends who always provided support.",
            },
            {
                "timestamp": "2025-07-18T02:00:00Z",
                "summary": "Appreciation for a professor at university who was exceptionally helpful in job search.",
            },
            {
                "timestamp": "2025-07-18T03:00:00Z", # Newer memory about the same topic
                "summary": "Thinking about the art project and how to start it.",
            },
            {
                "timestamp": "2025-07-18T04:00:00Z", # Most recent memory
                "summary": "Reflecting on the new art project and the fear of failure.",
            }
        ]
        self.mock_goals = [
            {
                "name": "Become proficient in Spanish",
                "description": "Reach CEFR Level C2."
            },
            {
                "name": "Launch AI MVP prototype",
                "description": "Build the first functioning version of the assistant app."
            }
        ]

    # --- Original Tests ---

    def test_retrieve_memory_by_keyword(self):
        """Test if we can retrieve a specific memory using a keyword."""
        user_input = "I'm thinking about how much I love my family."
        relevant_memories = retrieve_relevant_context(
            user_input, self.mock_memories, "summary", max_results=1
        )
        self.assertEqual(len(relevant_memories), 1)
        self.assertEqual(relevant_memories[0]['summary'], "Felt a deep sense of gratitude toward family and friends who always provided support.")
        print("\n✅ test_retrieve_memory_by_keyword: PASSED")

    def test_retrieve_goal_by_keyword(self):
        """Test if we can retrieve a specific goal using a keyword."""
        user_input = "I need to focus on the AI prototype."
        relevant_goals = retrieve_relevant_context(
            user_input, self.mock_goals, ["name", "description"], max_results=1
        )
        self.assertEqual(len(relevant_goals), 1)
        self.assertEqual(relevant_goals[0]['name'], "Launch AI MVP prototype")
        print("✅ test_retrieve_goal_by_keyword: PASSED")

    def test_no_relevant_context_found(self):
        """Test that nothing is returned when no keywords match."""
        user_input = "I want to talk about cooking."
        relevant_memories = retrieve_relevant_context(user_input, self.mock_memories, "summary")
        relevant_goals = retrieve_relevant_context(user_input, self.mock_goals, ["name", "description"])
        self.assertEqual(len(relevant_memories), 0)
        self.assertEqual(len(relevant_goals), 0)
        print("✅ test_no_relevant_context_found: PASSED")

    # --- New, More Robust Tests ---

    def test_retrieval_order_is_chronological(self):
        """Test that the most RECENT relevant memory is returned first."""
        user_input = "Tell me about the art project."
        # Ask for only one result
        relevant_memories = retrieve_relevant_context(
            user_input, self.mock_memories, "summary", max_results=1
        )
        self.assertEqual(len(relevant_memories), 1)
        # It should return the memory from 04:00:00, not the one from 03:00:00
        self.assertEqual(relevant_memories[0]['summary'], "Reflecting on the new art project and the fear of failure.")
        print("✅ test_retrieval_order_is_chronological: PASSED")

    def test_case_and_punctuation_insensitivity(self):
        """Test that search ignores capitalization and punctuation."""
        user_input = "Reminiscing about that special professor..."
        relevant_memories = retrieve_relevant_context(
            user_input, self.mock_memories, "summary", max_results=1
        )
        self.assertEqual(len(relevant_memories), 1)
        self.assertEqual(relevant_memories[0]['summary'], "Appreciation for a professor at university who was exceptionally helpful in job search.")
        print("✅ test_case_and_punctuation_insensitivity: PASSED")

    def test_stop_word_filtering(self):
        """Test that common 'stop words' are ignored for more accurate matching."""
        # This input shares many stop words with the "professor" memory ("with", "a", "at")
        # but the meaningful keyword is "wedding".
        user_input = "I was at a wedding with my family."
        relevant_memories = retrieve_relevant_context(
            user_input, self.mock_memories, "summary", max_results=1
        )
        self.assertEqual(len(relevant_memories), 1)
        # It should correctly match the "betrayal" memory, not the "professor" memory.
        self.assertEqual(relevant_memories[0]['summary'], "Felt a deep sense of gratitude toward family and friends who always provided support.")
        print("✅ test_stop_word_filtering: PASSED")

    def test_empty_data_sources(self):
        """Test that the function handles empty data sources gracefully without crashing."""
        user_input = "This is a test."
        # Pass empty lists as the data sources
        relevant_memories = retrieve_relevant_context(user_input, [], "summary")
        relevant_goals = retrieve_relevant_context(user_input, [], ["name", "description"])
        self.assertEqual(len(relevant_memories), 0)
        self.assertEqual(len(relevant_goals), 0)
        print("✅ test_empty_data_sources: PASSED")


if __name__ == '__main__':
    unittest.main()