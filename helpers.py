def check_win(game, turn):
    # Check for win
    winner = None
    # Check rows and columns
    for i in range(3):
        if ((game[i][0] == turn and 
            game[i][1] == turn and
            game[i][2] == turn) or 
            (game[0][i] == turn and
            game[1][i] == turn and
            game[2][i] == turn)):
            winner = turn
            break
    # Check diagonals
    if ((game[0][0] == turn and
        game[1][1] == turn and
        game[2][2] == turn) or
        (game[0][2] == turn and
        game[1][1] == turn and
        game[2][0] == turn)):
       winner = turn
    
    return winner

def minimax(game, turn, coords=None):
    if check_win(game, turn) == "X":
        return 1, coords
    elif check_win(game, turn) == "O":
        return -1, coords

    moves = []
    for i in range(3):
        for j in range(3):
            if game[i][j] is None:
                moves.append((i,j))
    # Draw
    if moves == []:
        return 0, coords
    
    if turn == "X":
        score = -100, coords
        for move in moves:
            new_game = game.copy()
            new_game[move[0]][move[1]] = "X"
            new_score = minimax(new_game, "O", move)
            if new_score[0] > score[0]:
                score = new_score
        return score
    
    if turn == "O":
        score = 100, coords
        for move in moves:
            new_game = game.copy()
            new_game[move[0]][move[1]] = "O"
            new_score = minimax(new_game, "X", move)
            if new_score[0] < score[0]:
                score = new_score
        return score
            
        