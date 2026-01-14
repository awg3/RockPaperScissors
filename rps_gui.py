"""Simple Tkinter GUI for Rock-Paper-Scissors.

This GUI imports the game logic from `rock_paper_scissors.py` so the rules
and tests stay in one place.
"""
from __future__ import annotations

import random
import platform
import tkinter as tk
from tkinter import ttk
from typing import Literal, cast

try:
    # local import when running from this folder
    from rock_paper_scissors import determine_winner
except Exception:  # pragma: no cover - allow running from different cwd
    # fallback for package-style imports
    from .rock_paper_scissors import determine_winner  # type: ignore

Move = Literal["rock", "paper", "scissors"]


ICON_SIZE = 64


def draw_icon_on(canvas: tk.Canvas, move: Move) -> None:
    """Draw a simple representative icon for a move on the given canvas."""
    canvas.delete("all")
    w = ICON_SIZE
    h = ICON_SIZE
    if move == "rock":
        # gray circle
        canvas.create_oval(6, 6, w - 6, h - 6, fill="#7f8c8d", outline="#2c3e50", width=2)
        # emoji overlay
        canvas.create_text(w // 2, h // 2, text="✊", font=("Segoe UI Emoji", 28))
    elif move == "paper":
        # white rectangle with shadow
        canvas.create_rectangle(8, 8, w - 8, h - 8, fill="#ecf0f1", outline="#7f8c8d", width=2)
        canvas.create_line(12, 18, w - 12, 18, fill="#bdc3c7")
        canvas.create_line(12, 28, w - 12, 28, fill="#bdc3c7")
        canvas.create_text(w // 2, h // 2, text="✋", font=("Segoe UI Emoji", 28))
    else:  # scissors
        # two crossing blades
        canvas.create_line(12, 16, w - 12, h - 16, fill="#f1c40f", width=6, capstyle="round")
        canvas.create_line(12, h - 16, w - 12, 16, fill="#e67e22", width=6, capstyle="round")
        canvas.create_oval(w // 2 - 6, h // 2 - 6, w // 2 + 6, h // 2 + 6, fill="#ecf0f1", outline="#bdc3c7")
        canvas.create_text(w // 2, h // 2, text="✌️", font=("Segoe UI Emoji", 26))


class RPSApp(tk.Tk):
    """
    Refactored RPSApp with small efficiency improvements and a High Scores feature.
    - Uses StringVar for text updates to avoid repeated .config calls.
    - Avoids redrawing icons when the move hasn't changed.
    - Persists top N high scores (player-only) in a JSON file in the user's home dir.
    - Adds a High Scores label and a button to clear saved high scores.
    """
    HIGH_SCORES_FILE = ".rps_high_scores.json"
    MAX_HIGH_SCORES = 5

    def __init__(self) -> None:
        super().__init__()
        self.title("Rock Paper Scissors")
        self.configure(bg="#2c3e50")
        self.resizable(False, False)

        self.player_score = 0
        self.computer_score = 0

        # cached last moves to avoid unnecessary redraws
        self._last_player_move: Move | None = None
        self._last_comp_move: Move | None = None

        # optional sound backend (Windows winsound)
        self._winsound = None
        try:
            if platform.system() == "Windows":
                import winsound as _wins
                self._winsound = _wins
        except Exception:
            self._winsound = None

        # UI text variables for efficient updates
        self.status_var = tk.StringVar(value="Choose rock, paper or scissors")
        self._last_score_text = self._score_text()
        self.score_var = tk.StringVar(value=self._last_score_text)
        self.high_var = tk.StringVar(value="High Scores: —")

        # high scores persistence path (home dir)
        try:
            from pathlib import Path
            self._hs_path = Path.home() / self.HIGH_SCORES_FILE
        except Exception:
            self._hs_path = None

        # load persisted high scores
        self._high_scores: list[int] = []
        self._load_high_scores()
        self._update_high_var()

        self._build_ui()

    def _build_ui(self) -> None:
        from functools import partial

        pad = 12
        frm = ttk.Frame(self, padding=pad)
        frm.grid(row=0, column=0)

        # style
        style = ttk.Style(self)
        style.configure("TLabel", font=("Segoe UI", 11))
        style.configure("Header.TLabel", font=("Segoe UI", 13, "bold"))
        style.configure("TButton", font=("Segoe UI", 10))

        header = ttk.Label(frm, text="Rock · Paper · Scissors", style="Header.TLabel")
        header.grid(row=0, column=0, columnspan=3, pady=(0, pad))

        # player / vs / computer icons
        self.player_canvas = tk.Canvas(frm, width=ICON_SIZE, height=ICON_SIZE, bg="#ffffff", bd=0, highlightthickness=0)
        self.vs_label = ttk.Label(frm, text="vs")
        self.computer_canvas = tk.Canvas(frm, width=ICON_SIZE, height=ICON_SIZE, bg="#ffffff", bd=0, highlightthickness=0)

        self.player_canvas.grid(row=1, column=0, padx=8)
        self.vs_label.grid(row=1, column=1)
        self.computer_canvas.grid(row=1, column=2, padx=8)

        # status and score (use StringVar)
        self.status = ttk.Label(frm, textvariable=self.status_var, anchor="center")
        self.status.grid(row=2, column=0, columnspan=3, pady=(pad // 2, pad))

        self.score_label = ttk.Label(frm, textvariable=self.score_var)
        self.score_label.grid(row=3, column=0, columnspan=3, pady=(0, pad))

        # high scores row
        high_frame = ttk.Frame(frm)
        high_frame.grid(row=4, column=0, columnspan=3, pady=(0, pad))
        self.high_label = ttk.Label(high_frame, textvariable=self.high_var)
        self.high_label.grid(row=0, column=0, padx=(0, 8))
        btn_clear_hs = ttk.Button(high_frame, text="Clear High Scores", command=self._clear_high_scores)
        btn_clear_hs.grid(row=0, column=1)

        # controls row
        btn_frame = ttk.Frame(frm)
        btn_frame.grid(row=5, column=0, columnspan=3)

        # use partial to avoid repeated lambdas
        btn_rock = ttk.Button(btn_frame, text="Rock", command=partial(self.play, "rock"))
        btn_paper = ttk.Button(btn_frame, text="Paper", command=partial(self.play, "paper"))
        btn_scissors = ttk.Button(btn_frame, text="Scissors", command=partial(self.play, "scissors"))
        btn_reset = ttk.Button(btn_frame, text="Reset Scores", command=self.reset_scores)
        btn_quit = ttk.Button(btn_frame, text="Quit", command=self._on_quit)

        btn_rock.grid(row=0, column=0, padx=6)
        btn_paper.grid(row=0, column=1, padx=6)
        btn_scissors.grid(row=0, column=2, padx=6)
        btn_reset.grid(row=0, column=3, padx=6)
        btn_quit.grid(row=0, column=4, padx=6)

        # keyboard shortcuts: handle both lower/upper case via single key handler
        self.bind_all("<Key>", self._on_key)

        # initialize default icons
        self._draw_player_if_changed("rock")
        self._draw_comp_if_changed("rock")

    def _on_key(self, event: tk.Event) -> None:
        c = (event.char or "").lower()
        if c == "r":
            self.play("rock")
        elif c == "p":
            self.play("paper")
        elif c == "s":
            self.play("scissors")

    def _score_text(self) -> str:
        return f"You: {self.player_score}  Computer: {self.computer_score}"

    def play(self, player_move: Move) -> None:
        # ensure the chosen move is typed as Move for static checkers
        comp_move = cast(Move, random.choice(["rock", "paper", "scissors"]))
        winner = determine_winner(player_move, comp_move)

        # update icon canvases (methods handle change detection)
        self._draw_player_if_changed(player_move)
        self._draw_comp_if_changed(comp_move)

        if winner == "tie":
            text = f"Tie — both chose {player_move}"
            self._play_sound("tie")
        elif winner == "player":
            self.player_score += 1
            text = f"You win — {player_move} beats {comp_move}"
            self._play_sound("win")
            # high scores are updated only on reset or quit
        else:
            self.computer_score += 1
            text = f"Computer wins — {comp_move} beats {player_move}"
            self._play_sound("lose")

        self.status_var.set(text)
        # Trigger a brief status label flash to indicate result
        self._flash_status()
        new_score = self._score_text()
        if new_score != self._last_score_text:
            self.score_var.set(new_score)
            self._last_score_text = new_score

    def reset_scores(self) -> None:
        # persist current player score into high scores before resetting
        self._maybe_update_high_scores(force_save=True)
        self.player_score = 0
        self.computer_score = 0
        self.score_var.set(self._score_text())

    def _on_quit(self) -> None:
        # persist before exit
        self._maybe_update_high_scores(force_save=True)
        self.destroy()

    def _draw_player_if_changed(self, move: Move) -> None:
        if move != self._last_player_move:
            draw_icon_on(self.player_canvas, move)
            self._last_player_move = move

    def _draw_comp_if_changed(self, move: Move) -> None:
        if move != self._last_comp_move:
            draw_icon_on(self.computer_canvas, move)
            self._last_comp_move = move

    def _play_sound(self, result: str) -> None:
        """Play a short sound for win/lose/tie when available (Windows only)."""
        if not self._winsound:
            return
        try:
            if result == "win":
                # two ascending beeps
                self._winsound.Beep(880, 120)
                self._winsound.Beep(988, 120)
            elif result == "lose":
                # low descending beep
                self._winsound.Beep(440, 220)
            else:
                # tie: short medium beep
                self._winsound.Beep(660, 120)
        except Exception:
            # ignore sound errors
            pass

    def _flash_status(self, flashes: int = 3) -> None:
        """Flash the status label background a few times to show result."""
        original_bg = None
        try:
            original_bg = self.status.cget("background")
        except Exception:
            original_bg = ""
        highlight = "#f1c40f"

        def _do_flash(n: int) -> None:
            if n <= 0:
                try:
                    self.status.configure(background=original_bg)
                except Exception:
                    pass
                return
            try:
                self.status.configure(background=highlight if n % 2 == 1 else original_bg)
            except Exception:
                pass
            self.after(150, _do_flash, n - 1)

        _do_flash(flashes * 2)

    # ---------------- High Scores persistence ----------------
    def _load_high_scores(self) -> None:
        """Load high scores from JSON file; keep a descending list of ints."""
        if not self._hs_path:
            return
        try:
            import json
            if self._hs_path.exists():
                data = json.loads(self._hs_path.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    # sanitize to ints
                    self._high_scores = sorted([int(x) for x in data if isinstance(x, (int, float))], reverse=True)[: self.MAX_HIGH_SCORES]
        except Exception:
            self._high_scores = []

    def _save_high_scores(self) -> None:
        if not self._hs_path:
            return
        try:
            import json
            self._hs_path.write_text(json.dumps(self._high_scores), encoding="utf-8")
        except Exception:
            pass

    def _update_high_var(self) -> None:
        if not self._high_scores:
            self.high_var.set("High Scores: —")
        else:
            self.high_var.set("High Scores: " + ", ".join(str(x) for x in self._high_scores))

    def _maybe_update_high_scores(self, force_save: bool = False) -> None:
        """
        Add current player_score to high scores if it qualifies.
        If force_save is True, will write file even if no change (used on reset/quit).
        """
        changed = False
        ps = int(self.player_score)
        if ps > 0:
            if not self._high_scores or ps > min(self._high_scores) or len(self._high_scores) < self.MAX_HIGH_SCORES:
                # insert and keep top N unique values
                self._high_scores.append(ps)
                self._high_scores = sorted(set(self._high_scores), reverse=True)[: self.MAX_HIGH_SCORES]
                changed = True
        if changed or force_save:
            self._save_high_scores()
        if changed:
            self._update_high_var()

    def _clear_high_scores(self) -> None:
        self._high_scores = []
        self._save_high_scores()
        self._update_high_var()


def main() -> None:
    app = RPSApp()
    app.mainloop()


if __name__ == "__main__":
    main()
