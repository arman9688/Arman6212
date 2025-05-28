import tkinter as tk
from tkinter import messagebox, ttk
import random
import copy

class SudokuGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sudoku Game")
        self.root.geometry("600x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize the game board (9x9 grid)
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self.original_board = [[0 for _ in range(9)] for _ in range(9)]
        
        # Create GUI elements
        self.create_widgets()
        self.generate_puzzle()
        self.update_display()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="SUDOKU", font=("Arial", 24, "bold"), 
                              bg='#f0f0f0', fg='#333')
        title_label.pack(pady=10)
        
        # Game board frame
        self.board_frame = tk.Frame(self.root, bg='#333', bd=2)
        self.board_frame.pack(pady=10)
        
        # Create 9x9 grid of entry widgets
        self.entries = []
        for i in range(9):
            row = []
            for j in range(9):
                # Create frame for each 3x3 box with different background
                box_row, box_col = i // 3, j // 3
                bg_color = '#fff' if (box_row + box_col) % 2 == 0 else '#f8f8f8'
                
                entry = tk.Entry(self.board_frame, width=2, font=("Arial", 16, "bold"),
                               justify='center', bd=1, relief='solid',
                               bg=bg_color, fg='#333')
                entry.grid(row=i, column=j, padx=1, pady=1, ipady=5)
                entry.bind('<KeyPress>', lambda e, r=i, c=j: self.on_key_press(e, r, c))
                entry.bind('<FocusOut>', lambda e, r=i, c=j: self.validate_entry(r, c))
                row.append(entry)
            self.entries.append(row)
        
        # Buttons frame
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        # Control buttons
        tk.Button(button_frame, text="New Game", command=self.new_game,
                 font=("Arial", 12), bg='#4CAF50', fg='white', padx=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Check Solution", command=self.check_solution,
                 font=("Arial", 12), bg='#2196F3', fg='white', padx=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Get Hint", command=self.get_hint,
                 font=("Arial", 12), bg='#FF9800', fg='white', padx=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Solve", command=self.show_solution,
                 font=("Arial", 12), bg='#9C27B0', fg='white', padx=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Reset", command=self.reset_game,
                 font=("Arial", 12), bg='#F44336', fg='white', padx=20).pack(side=tk.LEFT, padx=5)
        
        # Difficulty selection
        difficulty_frame = tk.Frame(self.root, bg='#f0f0f0')
        difficulty_frame.pack(pady=10)
        
        tk.Label(difficulty_frame, text="Difficulty:", font=("Arial", 12), 
                bg='#f0f0f0').pack(side=tk.LEFT, padx=5)
        
        self.difficulty_var = tk.StringVar(value="Medium")
        difficulty_combo = ttk.Combobox(difficulty_frame, textvariable=self.difficulty_var,
                                       values=["Easy", "Medium", "Hard"], state="readonly")
        difficulty_combo.pack(side=tk.LEFT, padx=5)
        
    def on_key_press(self, event, row, col):
        # Only allow digits 1-9 and backspace/delete
        if event.char.isdigit() and '1' <= event.char <= '9':
            return True
        elif event.keysym in ['BackSpace', 'Delete']:
            return True
        else:
            return "break"
    
    def validate_entry(self, row, col):
        try:
            value = self.entries[row][col].get()
            if value == '':
                self.board[row][col] = 0
            elif value.isdigit() and 1 <= int(value) <= 9:
                self.board[row][col] = int(value)
                # Check if the move is valid
                if not self.is_valid_move(row, col, int(value)):
                    self.entries[row][col].configure(fg='red')
                else:
                    self.entries[row][col].configure(fg='#333')
            else:
                self.entries[row][col].delete(0, tk.END)
                self.board[row][col] = 0
        except:
            self.entries[row][col].delete(0, tk.END)
            self.board[row][col] = 0
    
    def is_valid_move(self, row, col, num):
        # Check row
        for j in range(9):
            if j != col and self.board[row][j] == num:
                return False
        
        # Check column
        for i in range(9):
            if i != row and self.board[i][col] == num:
                return False
        
        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if (i != row or j != col) and self.board[i][j] == num:
                    return False
        
        return True
    
    def solve_sudoku(self, board):
        """Solve Sudoku using backtracking algorithm"""
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid_placement(board, i, j, num):
                            board[i][j] = num
                            if self.solve_sudoku(board):
                                return True
                            board[i][j] = 0
                    return False
        return True
    
    def is_valid_placement(self, board, row, col, num):
        # Check row
        for j in range(9):
            if board[row][j] == num:
                return False
        
        # Check column
        for i in range(9):
            if board[i][col] == num:
                return False
        
        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False
        
        return True
    
    def generate_puzzle(self):
        """Generate a new Sudoku puzzle"""
        # Start with empty board
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        
        # Fill diagonal 3x3 boxes first (they don't affect each other)
        for box in range(0, 9, 3):
            self.fill_box(box, box)
        
        # Solve the rest
        self.solve_sudoku(self.board)
        
        # Store the complete solution
        self.solution = [row[:] for row in self.board]
        
        # Remove numbers based on difficulty
        difficulty = self.difficulty_var.get()
        if difficulty == "Easy":
            cells_to_remove = 40
        elif difficulty == "Medium":
            cells_to_remove = 50
        else:  # Hard
            cells_to_remove = 60
        
        # Randomly remove numbers
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        
        for i in range(cells_to_remove):
            row, col = cells[i]
            self.board[row][col] = 0
        
        # Store the original puzzle
        self.original_board = [row[:] for row in self.board]
    
    def fill_box(self, row, col):
        """Fill a 3x3 box with random valid numbers"""
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        
        for i in range(3):
            for j in range(3):
                self.board[row + i][col + j] = numbers[i * 3 + j]
    
    def update_display(self):
        """Update the GUI display with current board state"""
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                if self.board[i][j] != 0:
                    self.entries[i][j].insert(0, str(self.board[i][j]))
                
                # Color original numbers differently
                if self.original_board[i][j] != 0:
                    self.entries[i][j].configure(fg='black', font=("Arial", 16, "bold"))
                    self.entries[i][j].configure(state='readonly')
                else:
                    self.entries[i][j].configure(fg='blue', font=("Arial", 16, "normal"))
                    self.entries[i][j].configure(state='normal')
    
    def new_game(self):
        """Start a new game"""
        self.generate_puzzle()
        self.update_display()
    
    def check_solution(self):
        """Check if the current solution is correct"""
        # First check if board is complete
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    messagebox.showinfo("Incomplete", "Please fill in all cells first!")
                    return
        
        # Check if solution is valid
        if self.is_solution_valid():
            messagebox.showinfo("Congratulations!", "You solved the puzzle correctly!")
        else:
            messagebox.showerror("Incorrect", "The solution is not correct. Keep trying!")
    
    def is_solution_valid(self):
        """Check if the current board state is a valid Sudoku solution"""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return False
                if not self.is_valid_move(i, j, self.board[i][j]):
                    return False
        return True
    
    def get_hint(self):
        """Provide a hint by filling one empty cell"""
        empty_cells = [(i, j) for i in range(9) for j in range(9) 
                      if self.board[i][j] == 0]
        
        if not empty_cells:
            messagebox.showinfo("No Hints", "The puzzle is already complete!")
            return
        
        # Choose a random empty cell
        row, col = random.choice(empty_cells)
        self.board[row][col] = self.solution[row][col]
        self.entries[row][col].delete(0, tk.END)
        self.entries[row][col].insert(0, str(self.solution[row][col]))
        self.entries[row][col].configure(fg='green')
    
    def show_solution(self):
        """Show the complete solution"""
        self.board = [row[:] for row in self.solution]
        self.update_display()
        messagebox.showinfo("Solution", "Here's the complete solution!")
    
    def reset_game(self):
        """Reset to the original puzzle"""
        self.board = [row[:] for row in self.original_board]
        self.update_display()
    
    def run(self):
        """Start the game"""
        self.root.mainloop()

# Create and run the game
if __name__ == "__main__":
    print("Starting Sudoku Game...")
    print("Features:")
    print("- Generate new puzzles with different difficulty levels")
    print("- Validate moves in real-time")
    print("- Get hints when stuck")
    print("- Check your solution")
    print("- View complete solution")
    print("- Reset to original puzzle")
    print("\nGame window should open shortly...")
    
    game = SudokuGame()
    game.run()