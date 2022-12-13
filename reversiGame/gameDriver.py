from reversiGame import *

if __name__ == '__main__': # Driver logic
    os.system('clear')
    size = int(input("Enter game board size (EVEN): "))
    if(size % 2 == 0 and size > 0):
        print(f""" \n\x1b[1;37;47m ------- REVERSI GAME {size} X {size} ------- {RESET_COLOR} """)
    else:
        print("INVALID SIZE- Please enter even number.")
        os._exit(0)    
    print()
    game = ReversiGame(size)
    players = [BLACK, WHITE]
    playerScore, aiScore = 2, 2
    while True:
        for player in players:
            game.printBoard()
            print()
            playerScore = game.evalBoard(game.board, BLACK)
            aiScore = game.evalBoard(game.board, WHITE)
            print(f""" {SCORESP_COLOR} {BLACK}Player Score: {playerScore} {RESET_COLOR}{SCORESA_COLOR} {WHITE}AI Score: {aiScore} {RESET_COLOR}""")
            if(player == BLACK):
                print('\n PLAYER TURN: ' + player, end = ' ')
            else:
                print('\n AI TURN: ' + player, end = ' ')
            if game.isTerminalNode(game.board, player):
                print('Player cannot play! Game ended!')
                if(playerScore > aiScore):
                    print('\n Player' + BLACK + '\n')
                elif(aiScore > playerScore):
                    print('\n AI WINS' + WHITE + '\n')
                else:
                    print('\n DRAW \n')
                os._exit(0)            
            if player == BLACK: # user's turn
                while True:
                    xy = input(' X Y: ')
                    if xy == '': os._exit(0)
                    (x, y) = xy.split()
                    x = int(x); y = int(y)
                    if game.validMove(game.board, x, y, player):
                        (board, totctr) = game.makeMove(game.board, x, y, player)
                        print(' # of pieces taken: ' + str(totctr) + '\n')
                        break
                    else:
                        print('\n  Invalid move! Try again! \n')
            else: # AI's turn
                (x, y) = game.bestMove(game.board, player)
                if not (x == -1 and y == -1):
                    (board, totctr) = game.makeMove(game.board, x, y, player)
                    print('AI played (X Y): ' + str(x) + ' ' + str(y))
                    print('\n # of pieces taken: ' + str(totctr) + '\n')