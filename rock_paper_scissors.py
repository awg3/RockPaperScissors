"""Simple Rock-Paper-Scissors CLI game.

Run the script and type one of: rock/r, paper/p, scissors/s or quit to exit.
The computer picks randomly each round. Scores for player and computer are tracked
and printed after each round.
"""
from __future__ import annotations

import random
from typing import Literal

Move = Literal["rock", "paper", "scissors"]


def normalize_move(raw: str) -> str | None:
    """Normalize user input into 'rock', 'paper', or 'scissors'.

    Returns None if the input is 'quit' or not a valid move.
    """
    if not raw:
        return None
    s = raw.strip().lower()
    if s in ("quit", "q", "exit"):
        return None
    if s in ("rock", "r"):
        return "rock"
    if s in ("paper", "p"):
        return "paper"
    if s in ("scissors", "scissor", "s"):
        return "scissors"
    return ""  # invalid marker


def determine_winner(player: Move, computer: Move) -> str:
    """Return 'player', 'computer', or 'tie' based on the moves.

    Rules:
    - Rock beats Scissors
    - Scissors beats Paper
    - Paper beats Rock
    """
    if player == computer:
        return "tie"

    wins = {
        ("rock", "scissors"),
        ("scissors", "paper"),
        ("paper", "rock"),
    }
    if (player, computer) in wins:
        return "player"
    return "computer"


def random_move() -> Move:
    return random.choice(["rock", "paper", "scissors"])


def main() -> None:
    print("Rock Paper Scissors — type 'rock', 'paper', or 'scissors' (or r/p/s). Type 'quit' to exit.")
    player_score = 0
    computer_score = 0
    round_no = 0

    while True:
        raw = input("Your move: ")
        norm = normalize_move(raw)
        if norm is None:
            print("Goodbye!")
            break
        if norm == "":
            print("Invalid input. Please type rock/paper/scissors or quit.")
            continue

        player_move: Move = norm  # type: ignore
        comp_move = random_move()
        round_no += 1

        print(f"You: {player_move}  —  Computer: {comp_move}")
        winner = determine_winner(player_move, comp_move)
        if winner == "tie":
            print("It's a tie!")
        elif winner == "player":
            player_score += 1
            print("You win this round!")
        else:
            computer_score += 1
            print("Computer wins this round!")

        print(f"Score -> You: {player_score}  Computer: {computer_score}  (Rounds: {round_no})")
        print("---")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
