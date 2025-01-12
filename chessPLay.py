import chess
import chess.engine
from all_imports import *
import tkinter as tk


class MessageDisplay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chess Game")
        self.root.geometry("400x200")
        self.root.configure(bg="#222")
        self.label = tk.Label(
            self.root,
            font=("Helvetica", 24),
            width=30,
            height=5,
            anchor="center",
            bg="#222",
            fg="gold",
            wraplength=400,
        )
        self.label.pack(expand=True, padx=20, pady=20)

    def update_msg(self, msg):
        self.label.config(text=msg)
        self.root.update_idletasks()

    def run(self):
        self.root.mainloop()


STOCKFISH_PATH = "D:\Software\Modulo 8\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"
driver = setup_driver()
print(driver.title)
board = chess.Board()
Move = 0
previous_move = ""
display = MessageDisplay()


is_stockfish_turn = False


def game_loop():
    global Move, previous_move, is_stockfish_turn

    if board.is_game_over():
        display.root.quit()
        return

    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        if is_stockfish_turn:
            display.update_msg("Stockfish is thinking...")
            result = engine.play(board, chess.engine.Limit(time=2))
            board.push(result.move)
            print("best_move", ":=", result.move)
            print(board, "\nBest Move (Stockfish as White):", result.move)
            display.update_msg(f"Best Move: {result.move}")

            is_stockfish_turn = False

        else:
            latest_move = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        ".node-highlight-content.offset-for-annotation-icon.selected",
                    )
                )
            )
            try:
                piece = latest_move.find_element(
                    By.CLASS_NAME, "icon-font-chess"
                ).get_attribute("data-figurine")
                latest_move_key = piece.replace(" ", "") + latest_move.get_attribute(
                    "innerText"
                ).replace(" ", "")
            except Exception:
                latest_move_key = latest_move.get_attribute("innerText").replace(
                    " ", ""
                )

            current_move = latest_move_key
            if Move == 0 or current_move != previous_move:
                previous_move = current_move.replace("+", "")

                try:

                    board.push_san(current_move)
                    display.update_msg("Stockfish is thinking...")
                    result = engine.play(board, chess.engine.Limit(time=2))
                    board.push(result.move)
                    best_move = result.move
                    display.update_msg(f"Best Move: {best_move}")

                except ValueError:
                    print("\nInvalid move format:", current_move)

            Move += 1

    display.root.after(1000, game_loop)


game_loop()


display.run()
