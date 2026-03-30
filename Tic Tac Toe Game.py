import random
import os
import sys
import time
from typing import List, Optional, Tuple, Dict

class TicTacToe:
    """Ultimate Tic Tac Toe game with AI opponents and statistics tracking."""
    
    def __init__(self):
        self.board: List[Optional[str]] = [None] * 9
        self.current_player: str = 'X'
        self.game_active: bool = True
        self.mode: str = 'vsComputer'  # 'vsComputer' or 'twoPlayer'
        self.difficulty: str = 'medium'  # 'easy', 'medium', 'hard', 'impossible'
        self.scores: Dict[str, int] = {
            'player': 0,
            'computer': 0,
            'draws': 0
        }
        self.win_streak: int = 0
        self.best_streak: int = 0
        self.move_history: List[str] = []
        self.winning_combination: Optional[List[int]] = None
        
        # Winning patterns
        self.win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]               # Diagonals
        ]
        
        # Corner and center positions for AI
        self.corners = [0, 2, 6, 8]
        self.center = 4
        
    def display_board(self) -> None:
        """Display the current game board with nice formatting."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\n" + "=" * 50)
        print("         🎮 TIC TAC TOE - ULTIMATE EDITION 🎮")
        print("=" * 50)
        
        # Display current mode and difficulty
        mode_text = "🤖 VS COMPUTER" if self.mode == 'vsComputer' else "👥 TWO PLAYER"
        difficulty_text = f" [{self.difficulty.upper()}]" if self.mode == 'vsComputer' else ""
        print(f"\n   Mode: {mode_text}{difficulty_text}")
        
        # Display scores
        print("\n   " + "─" * 40)
        if self.mode == 'vsComputer':
            print(f"   🧑 YOU (X): {self.scores['player']}    |    🤖 COMPUTER (O): {self.scores['computer']}    |    🤝 DRAWS: {self.scores['draws']}")
        else:
            print(f"   🧑 PLAYER X: {self.scores['player']}    |    🧑 PLAYER O: {self.scores['computer']}    |    🤝 DRAWS: {self.scores['draws']}")
        print("   " + "─" * 40)
        
        # Display win streak
        if self.win_streak > 0:
            print(f"\n   🔥 WIN STREAK: {self.win_streak} (Best: {self.best_streak})")
        
        # Display the board
        print("\n       1   2   3")
        print("     ┌───┬───┬───┐")
        for i in range(3):
            row = i * 3
            symbols = []
            for j in range(3):
                val = self.board[row + j]
                symbols.append(val if val else ' ')
            print(f"   {i+1} │ {symbols[0]} │ {symbols[1]} │ {symbols[2]} │")
            if i < 2:
                print("     ├───┼───┼───┤")
        print("     └───┴───┴───┘")
        
        # Display move history
        self.display_move_history()
        
    def display_move_history(self) -> None:
        """Display recent moves."""
        if self.move_history:
            print("\n   📝 Recent moves:")
            print("   " + "-" * 30)
            for move in self.move_history[:8]:  # Show last 8 moves
                print(f"   {move}")
        else:
            print("\n   📝 No moves yet")
    
    def get_empty_cells(self) -> List[int]:
        """Return list of empty cell indices."""
        return [i for i, cell in enumerate(self.board) if cell is None]
    
    def make_move(self, position: int, player: str, is_computer: bool = False) -> bool:
        """
        Make a move on the board.
        
        Args:
            position: Index of the cell (0-8)
            player: 'X' or 'O'
            is_computer: Whether this move is made by computer
            
        Returns:
            True if move was successful, False otherwise
        """
        if not self.game_active:
            return False
            
        if position < 0 or position > 8 or self.board[position] is not None:
            return False
            
        # Validate turn
        if self.mode == 'vsComputer':
            if not is_computer and player != 'X':
                return False
            if is_computer and player != 'O':
                return False
        else:
            if player != self.current_player:
                return False
        
        self.board[position] = player
        move_text = f"   {player} → ({position//3 + 1}, {position%3 + 1})"
        self.move_history.insert(0, move_text)
        if len(self.move_history) > 10:
            self.move_history.pop()
        
        return True
    
    def check_winner(self) -> Tuple[bool, Optional[List[int]]]:
        """
        Check if there's a winner.
        
        Returns:
            Tuple of (has_winner, winning_combination)
        """
        for pattern in self.win_patterns:
            if (self.board[pattern[0]] and 
                self.board[pattern[0]] == self.board[pattern[1]] == 
                self.board[pattern[2]]):
                return True, pattern
        return False, None
    
    def is_board_full(self) -> bool:
        """Check if the board is completely filled."""
        return all(cell is not None for cell in self.board)
    
    def check_draw(self) -> bool:
        """Check if the game is a draw."""
        return self.is_board_full() and not self.check_winner()[0]
    
    def handle_win(self, combination: List[int], winner: str) -> None:
        """
        Handle win event.
        
        Args:
            combination: Winning cell combination
            winner: 'X' or 'O'
        """
        self.game_active = False
        self.winning_combination = combination
        
        # Determine if player won (X) or computer/O won
        is_player_win = (self.mode == 'vsComputer' and winner == 'X') or \
                        (self.mode == 'twoPlayer' and winner == 'X')
        
        if self.mode == 'vsComputer':
            if is_player_win:
                self.scores['player'] += 1
                self.win_streak += 1
                self.best_streak = max(self.best_streak, self.win_streak)
            else:
                self.scores['computer'] += 1
                self.win_streak = 0
        else:
            self.scores['player' if winner == 'X' else 'computer'] += 1
        
        self.display_board()
        self.highlight_winning_cells(combination)
        
        # Display win message
        print("\n" + "=" * 50)
        if self.mode == 'vsComputer':
            if is_player_win:
                print("         🎉🎉🎉 YOU WIN! 🎉🎉🎉")
                print("        ✨✨✨ AMAZING! ✨✨✨")
            else:
                print("         🤖🤖🤖 COMPUTER WINS! 🤖🤖🤖")
                print("        💀💀💀 BETTER LUCK NEXT TIME! 💀💀💀")
        else:
            print(f"         🎉🎉🎉 PLAYER {winner} WINS! 🎉🎉🎉")
        print("=" * 50)
    
    def handle_draw(self) -> None:
        """Handle draw event."""
        self.game_active = False
        self.scores['draws'] += 1
        self.win_streak = 0
        
        self.display_board()
        print("\n" + "=" * 50)
        print("         🤝🤝🤝 IT'S A DRAW! 🤝🤝🤝")
        print("        💪💪💪 GOOD GAME! 💪💪💪")
        print("=" * 50)
    
    def highlight_winning_cells(self, combination: List[int]) -> None:
        """Display winning cells with highlighting."""
        print("\n   🏆 WINNING COMBINATION:")
        board_copy = [cell if cell else ' ' for cell in self.board]
        for i in range(3):
            row = i * 3
            print(f"   {i+1} │ ", end='')
            for j in range(3):
                idx = row + j
                if idx in combination:
                    print(f"\033[92m{board_copy[idx]}\033[0m", end='')
                else:
                    print(f"{board_copy[idx]}", end='')
                if j < 2:
                    print(" │ ", end='')
            print(" │")
            if i < 2:
                print("     ├───┼───┼───┤")
    
    def update_status(self) -> None:
        """Display current game status."""
        if not self.game_active:
            return
            
        print("\n" + "=" * 50)
        if self.mode == 'vsComputer':
            if self.current_player == 'X':
                print("   🎯 YOUR TURN (X)")
                print("   Enter position (1-9) or 'quit' to exit")
            else:
                print("   🤖 COMPUTER IS THINKING...")
                time.sleep(0.5)
        else:
            print(f"   👤 PLAYER {self.current_player}'s TURN")
            print("   Enter position (1-9) or 'quit' to exit")
        print("=" * 50)
    
    def get_player_move(self) -> Optional[int]:
        """
        Get and validate player move input.
        
        Returns:
            Position index (0-8) or None if quit
        """
        while True:
            try:
                move = input("\n   ➤ Enter your move (1-9): ").strip().lower()
                
                if move == 'quit':
                    return None
                
                # Handle special commands
                if move == 'stats':
                    self.show_stats()
                    continue
                if move == 'help':
                    self.show_help()
                    continue
                    
                position = int(move) - 1
                
                if 0 <= position <= 8:
                    if self.board[position] is None:
                        return position
                    else:
                        print("   ⚠️  That spot is already taken! Try again.")
                else:
                    print("   ⚠️  Invalid position! Use numbers 1-9.")
                    
            except ValueError:
                print("   ⚠️  Invalid input! Enter a number (1-9) or 'quit'.")
    
    def computer_move(self) -> None:
        """Execute computer's move based on difficulty."""
        if not self.game_active or self.current_player != 'O':
            return
        
        empty_cells = self.get_empty_cells()
        if not empty_cells:
            return
        
        if self.difficulty == 'easy':
            move = self.get_easy_move()
        elif self.difficulty == 'medium':
            move = self.get_medium_move()
        elif self.difficulty == 'hard':
            move = self.get_hard_move()
        else:  # impossible
            move = self.get_impossible_move()
        
        if move is not None:
            self.make_move(move, 'O', is_computer=True)
    
    def get_easy_move(self) -> Optional[int]:
        """Easy difficulty: random move."""
        empty_cells = self.get_empty_cells()
        return random.choice(empty_cells) if empty_cells else None
    
    def get_medium_move(self) -> Optional[int]:
        """Medium difficulty: 50% smart, 50% random."""
        if random.random() < 0.5:
            return self.get_smart_move()
        return self.get_easy_move()
    
    def get_hard_move(self) -> Optional[int]:
        """Hard difficulty: 80% smart, 20% random."""
        if random.random() < 0.8:
            return self.get_smart_move()
        return self.get_easy_move()
    
    def get_impossible_move(self) -> Optional[int]:
        """Impossible difficulty: always optimal move."""
        return self.get_smart_move()
    
    def get_smart_move(self) -> Optional[int]:
        """
        Smart AI move: try to win, block opponent, or take strategic positions.
        
        Returns:
            Best move index or None if no move available
        """
        empty_cells = self.get_empty_cells()
        if not empty_cells:
            return None
        
        # Try to win
        for cell in empty_cells:
            self.board[cell] = 'O'
            if self.check_winner()[0]:
                self.board[cell] = None
                return cell
            self.board[cell] = None
        
        # Try to block opponent
        for cell in empty_cells:
            self.board[cell] = 'X'
            if self.check_winner()[0]:
                self.board[cell] = None
                return cell
            self.board[cell] = None
        
        # Take center if available
        if self.center in empty_cells:
            return self.center
        
        # Take corners
        available_corners = [c for c in self.corners if c in empty_cells]
        if available_corners:
            return random.choice(available_corners)
        
        # Any empty cell
        return random.choice(empty_cells)
    
    def switch_player(self) -> None:
        """Switch the current player."""
        self.current_player = 'O' if self.current_player == 'X' else 'X'
    
    def reset_game(self) -> None:
        """Reset the game board and state."""
        self.board = [None] * 9
        self.current_player = 'X'
        self.game_active = True
        self.winning_combination = None
        # Keep scores and streaks
    
    def clear_stats(self) -> None:
        """Clear all statistics."""
        self.scores = {'player': 0, 'computer': 0, 'draws': 0}
        self.win_streak = 0
        self.best_streak = 0
        self.move_history = []
        print("\n   📊 Statistics cleared!")
        time.sleep(1)
    
    def show_stats(self) -> None:
        """Display detailed statistics."""
        total_games = sum(self.scores.values())
        win_rate = (self.scores['player'] / total_games * 100) if total_games > 0 else 0
        
        print("\n" + "=" * 50)
        print("         📊 GAME STATISTICS")
        print("=" * 50)
        print(f"\n   🏆 Total Games: {total_games}")
        print(f"   🧑 Player Wins: {self.scores['player']}")
        if self.mode == 'vsComputer':
            print(f"   🤖 Computer Wins: {self.scores['computer']}")
        else:
            print(f"   🧑 Player O Wins: {self.scores['computer']}")
        print(f"   🤝 Draws: {self.scores['draws']}")
        print(f"\n   🔥 Current Win Streak: {self.win_streak}")
        print(f"   🌟 Best Win Streak: {self.best_streak}")
        print(f"   📈 Win Rate: {win_rate:.1f}%")
        print("\n" + "=" * 50)
        input("\n   Press Enter to continue...")
    
    def show_help(self) -> None:
        """Display help information."""
        print("\n" + "=" * 50)
        print("         📖 HELP & CONTROLS")
        print("=" * 50)
        print("\n   🎮 Commands:")
        print("   • Enter numbers 1-9 to place your mark")
        print("   • 1 2 3 → Top row")
        print("   • 4 5 6 → Middle row")
        print("   • 7 8 9 → Bottom row")
        print("\n   🎯 Special Commands:")
        print("   • 'stats' - View game statistics")
        print("   • 'help'  - Show this help menu")
        print("   • 'quit'  - Exit the game")
        print("\n   🎲 Game Modes:")
        print("   • Vs Computer: Play against AI")
        print("   • Two Player: Play with a friend")
        print("\n   🤖 AI Difficulties:")
        print("   • Easy: Random moves")
        print("   • Medium: 50% strategic")
        print("   • Hard: 80% strategic")
        print("   • Impossible: Always optimal")
        print("\n" + "=" * 50)
        input("\n   Press Enter to continue...")
    
    def set_mode(self, mode: str) -> None:
        """Set game mode."""
        self.mode = mode
        self.reset_game()
        print(f"\n   🎮 Mode changed to: {'🤖 VS COMPUTER' if mode == 'vsComputer' else '👥 TWO PLAYER'}")
        time.sleep(1)
    
    def set_difficulty(self, difficulty: str) -> None:
        """Set AI difficulty."""
        self.difficulty = difficulty
        self.reset_game()
        print(f"\n   🤖 Difficulty set to: {difficulty.upper()}")
        time.sleep(1)
    
    def play(self) -> None:
        """Main game loop."""
        while True:
            self.display_board()
            
            if not self.game_active:
                print("\n   🎮 Options:")
                print("   • Press 'y' to play again")
                print("   • Press 'n' to quit")
                print("   • Press 'c' to clear stats")
                print("   • Press 'm' to change mode")
                print("   • Press 'd' to change difficulty")
                
                choice = input("\n   ➤ What would you like to do? ").strip().lower()
                
                if choice == 'y':
                    self.reset_game()
                    continue
                elif choice == 'n':
                    self.show_final_stats()
                    break
                elif choice == 'c':
                    self.clear_stats()
                    self.reset_game()
                    continue
                elif choice == 'm':
                    self.show_mode_menu()
                    continue
                elif choice == 'd':
                    if self.mode == 'vsComputer':
                        self.show_difficulty_menu()
                    else:
                        print("   ⚠️  Difficulty only available in vs Computer mode!")
                        time.sleep(1)
                    self.reset_game()
                    continue
                else:
                    print("   ⚠️  Invalid choice!")
                    time.sleep(1)
                    continue
            
            self.update_status()
            
            if self.mode == 'vsComputer' and self.current_player == 'O':
                self.computer_move()
            else:
                move = self.get_player_move()
                if move is None:
                    self.show_final_stats()
                    break
                
                if not self.make_move(move, self.current_player):
                    print("   ⚠️  Invalid move! Try again.")
                    time.sleep(1)
                    continue
            
            # Check win/draw after move
            has_winner, combination = self.check_winner()
            if has_winner:
                self.handle_win(combination, self.current_player)
                continue
            
            if self.check_draw():
                self.handle_draw()
                continue
            
            self.switch_player()
    
    def show_mode_menu(self) -> None:
        """Display mode selection menu."""
        print("\n" + "=" * 50)
        print("         🎮 SELECT GAME MODE")
        print("=" * 50)
        print("\n   1. 🤖 vs Computer")
        print("   2. 👥 Two Player")
        print("\n   Enter 1 or 2:")
        
        choice = input("   ➤ ").strip()
        if choice == '1':
            self.set_mode('vsComputer')
        elif choice == '2':
            self.set_mode('twoPlayer')
        else:
            print("   ⚠️  Invalid choice! Keeping current mode.")
            time.sleep(1)
    
    def show_difficulty_menu(self) -> None:
        """Display difficulty selection menu."""
        print("\n" + "=" * 50)
        print("         🤖 SELECT DIFFICULTY")
        print("=" * 50)
        print("\n   1. 😊 Easy")
        print("   2. 😐 Medium")
        print("   3. 🤯 Hard")
        print("   4. 💀 Impossible")
        print("\n   Enter 1-4:")
        
        choice = input("   ➤ ").strip()
        difficulties = {'1': 'easy', '2': 'medium', '3': 'hard', '4': 'impossible'}
        
        if choice in difficulties:
            self.set_difficulty(difficulties[choice])
        else:
            print("   ⚠️  Invalid choice! Keeping current difficulty.")
            time.sleep(1)
    
    def show_final_stats(self) -> None:
        """Display final statistics when quitting."""
        total_games = sum(self.scores.values())
        win_rate = (self.scores['player'] / total_games * 100) if total_games > 0 else 0
        
        print("\n" + "=" * 50)
        print("         📊 FINAL STATISTICS")
        print("=" * 50)
        print(f"\n   🏆 Total Games: {total_games}")
        print(f"   🧑 Player Wins: {self.scores['player']}")
        if self.mode == 'vsComputer':
            print(f"   🤖 Computer Wins: {self.scores['computer']}")
        else:
            print(f"   🧑 Player O Wins: {self.scores['computer']}")
        print(f"   🤝 Draws: {self.scores['draws']}")
        print(f"\n   🌟 Best Win Streak: {self.best_streak}")
        print(f"   📈 Overall Win Rate: {win_rate:.1f}%")
        print("\n" + "=" * 50)
        print("\n   Thanks for playing! 👋")
        print("   Goodbye!\n")


def main():
    """Entry point for the game."""
    game = TicTacToe()
    
    # Welcome screen
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "=" * 50)
    print("         🎮 TIC TAC TOE - ULTIMATE EDITION 🎮")
    print("=" * 50)
    print("\n   Welcome to the ultimate Tic Tac Toe experience!")
    print("\n   Features:")
    print("   • 🤖 Play against AI with 4 difficulty levels")
    print("   • 👥 Two-player mode for playing with friends")
    print("   • 📊 Track your statistics and win streaks")
    print("   • 📝 View move history")
    print("   • 🎯 Type 'help' anytime for commands")
    print("\n" + "=" * 50)
    
    # Mode selection
    print("\n   Select Game Mode:")
    print("   1. 🤖 vs Computer")
    print("   2. 👥 Two Player")
    
    choice = input("\n   ➤ Enter 1 or 2: ").strip()
    if choice == '1':
        game.set_mode('vsComputer')
        # Difficulty selection
        print("\n   Select Difficulty:")
        print("   1. 😊 Easy")
        print("   2. 😐 Medium")
        print("   3. 🤯 Hard")
        print("   4. 💀 Impossible")
        
        diff_choice = input("\n   ➤ Enter 1-4: ").strip()
        difficulties = {'1': 'easy', '2': 'medium', '3': 'hard', '4': 'impossible'}
        if diff_choice in difficulties:
            game.set_difficulty(difficulties[diff_choice])
    else:
        game.set_mode('twoPlayer')
    
    input("\n   Press Enter to start the game...")
    
    try:
        game.play()
    except KeyboardInterrupt:
        print("\n\n   Game interrupted. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
