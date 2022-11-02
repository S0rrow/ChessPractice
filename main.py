# simple chess program to let a player play against stockfish
import chess
import chess.engine

def main():
    # ask if player wants to play against stockfish
    option = input("Do you want to play against stockfish? (y/n): ")
    if option == "y":
        bot()
    else:
        player()

# 2 player game
def player():
    board = chess.Board()
    while not board.is_game_over():
        print_seperator()
        print(board)
        print_seperator()
        move = input("Enter your move: ")
        board.push_san(move)
    print("Game over")
    print(board.result())

# 1 player game against stockfish
def bot():
    board = chess.Board()
    engine = chess.engine.SimpleEngine.popen_uci(r"D:\repository\SimpleChess\stockfish_15_win_x64_avx2\stockfish_15_x64_avx2.exe")
    limit = chess.engine.Limit(time=0.1)
    engine.play(board, limit)
    
    while not board.is_game_over():
        print_seperator()
        print(board)
        print_seperator()
        move = input("Enter your move: ")
        board.push_san(move)
        print_seperator()
        print(board)
        print_seperator()
        result = engine.play(board, limit)
        board.push(result.move)

    print("Game over")
    print(board.result())
  

def print_seperator():
    print("================================")

if __name__ == "__main__":
    main()