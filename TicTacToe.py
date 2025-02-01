import tkinter as tk
import random
from tkinter import messagebox

class TicTacToeGUI:
    def __init__(self, master):
        """Initialize the GUI for Tic Tac Toe."""
        self.master = master
        self.master.title("Tic Tac Toe")
        self.board = ["-" for _ in range(9)]
        self.current_player = "X"
        self.game_mode = None  # Player vs Player or Player vs AI
        self.buttons = []

        self.create_mode_selection()

    def create_mode_selection(self):
        """Creates a mode selection screen before starting the game."""
        self.mode_label = tk.Label(self.master, text="Choose Game Mode", font=("Arial", 16))
        self.mode_label.pack(pady=10)

        self.pvp_button = tk.Button(self.master, text="Player vs Player", font=("Arial", 14),
                                    command=lambda: self.start_game("PVP"))
        self.pvp_button.pack(pady=5)

        self.pvai_button = tk.Button(self.master, text="Player vs AI", font=("Arial", 14),
                                     command=lambda: self.start_game("PVAI"))
        self.pvai_button.pack(pady=5)

    def start_game(self, mode):
        """Initializes the game with the chosen mode."""
        self.game_mode = mode
        self.mode_label.destroy()
        self.pvp_button.destroy()
        self.pvai_button.destroy()

        self.create_board()
        self.status_label = tk.Label(self.master, text="Player X's Turn", font=("Arial", 14))
        self.status_label.pack(pady=10)

    def create_board(self):
        """Creates the game board buttons."""
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        for i in range(9):
            btn = tk.Button(self.frame, text="", font=("Arial", 20), width=5, height=2,
                            command=lambda i=i: self.handle_move(i))
            btn.grid(row=i // 3, column=i % 3)
            self.buttons.append(btn)

    def handle_move(self, index):
        """Handles a player's move when they click on a button."""
        if self.board[index] == "-" and self.winner() is None:
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player, state="disabled")

            if self.winner():
                self.show_winner()
            elif self.is_tie():
                messagebox.showinfo("Game Over", "It's a Tie! 🤝")
                self.reset_board()
            else:
                self.switch_player()

                if self.game_mode == "PVAI" and self.current_player == "O":
                    self.master.after(500, self.computer_move)

    def computer_move(self):
        """Handles the AI's move."""
        best_move = self.find_best_move()
        self.board[best_move] = "O"
        self.buttons[best_move].config(text="O", state="disabled")

        if self.winner():
            self.show_winner()
        elif self.is_tie():
            messagebox.showinfo("Game Over", "It's a Tie! 🤝")
            self.reset_board()
        else:
            self.switch_player()

    def find_best_move(self):
        """Finds the best possible move for AI."""
        for symbol in ["O", "X"]:
            for i in range(9):
                if self.board[i] == "-":
                    self.board[i] = symbol
                    if self.winner():
                        self.board[i] = "-"
                        return i
                    self.board[i] = "-"

        available_moves = [i for i in range(9) if self.board[i] == "-"]
        return random.choice(available_moves)

    def winner(self):
        """Checks for a winner and returns the winning player if found."""
        win_conditions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontals
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Verticals
            (0, 4, 8), (2, 4, 6)             # Diagonals
        ]
        for a, b, c in win_conditions:
            if self.board[a] == self.board[b] == self.board[c] != "-":
                return self.board[a]
        return None

    def is_tie(self):
        """Checks if the board is full and the game is a tie."""
        return "-" not in self.board and self.winner() is None

    def show_winner(self):
        """Displays the winner and resets the board."""
        messagebox.showinfo("Game Over", f"🏆 Player {self.current_player} Wins!")
        self.reset_board()

    def switch_player(self):
        """Switches the turn between players."""
        self.current_player = "O" if self.current_player == "X" else "X"
        self.status_label.config(text=f"Player {self.current_player}'s Turn")

    def reset_board(self):
        """Resets the board to start a new game."""
        self.board = ["-" for _ in range(9)]
        for button in self.buttons:
            button.config(text="", state="normal")
        self.current_player = "X"
        self.status_label.config(text="Player X's Turn")


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()