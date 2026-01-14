"""Unit tests for rock_paper_scissors.determine_winner and normalize_move."""
import unittest

from rock_paper_scissors import determine_winner, normalize_move


class TestRPS(unittest.TestCase):
    def test_determine_winner_all_pairs(self):
        # ties
        self.assertEqual(determine_winner("rock", "rock"), "tie")
        self.assertEqual(determine_winner("paper", "paper"), "tie")
        self.assertEqual(determine_winner("scissors", "scissors"), "tie")

        # player wins
        self.assertEqual(determine_winner("rock", "scissors"), "player")
        self.assertEqual(determine_winner("scissors", "paper"), "player")
        self.assertEqual(determine_winner("paper", "rock"), "player")

        # computer wins
        self.assertEqual(determine_winner("scissors", "rock"), "computer")
        self.assertEqual(determine_winner("paper", "scissors"), "computer")
        self.assertEqual(determine_winner("rock", "paper"), "computer")

    def test_normalize_move_variants(self):
        self.assertEqual(normalize_move("rock"), "rock")
        self.assertEqual(normalize_move("R"), "rock")
        self.assertEqual(normalize_move(" PAPER "), "paper")
        self.assertEqual(normalize_move("s"), "scissors")
        self.assertEqual(normalize_move("scissor"), "scissors")
        self.assertIsNone(normalize_move("quit"))
        self.assertEqual(normalize_move("unknown"), "")


if __name__ == "__main__":
    unittest.main()
