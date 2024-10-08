import random
import numpy as np

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]
    
    def succ(self, state, mypiece):
        piece = mypiece
        successor = []
        myPiece = 0
        oppPiece = 0
        for i in range(5):
            for j in range(5):
                if state[i][j] == self.my_piece:
                    myPiece += 1
                if state[i][j] == self.opp:
                    oppPiece += 1
        if oppPiece >= 4 and myPiece >= 4:
            drop_phase = False
        else:
            drop_phase = True

        if drop_phase == True:
            for i in range(len(state)):
                for j in range(len(state[i])):
                    if state[i][j] == ' ':
                        copy = [row[:] for row in state]
                        copy[i][j] = piece
                        successor.append(copy)
        else:
            for i in range(len(state)):
                for j in range(len(state[i])):
                    if state[i][j] == piece:
                        up = i - 1
                        down = i + 1
                        left = j - 1
                        right = j + 1
                        #check for up
                        if up != -1 and state[up][j] == ' ':
                            copy = [row[:] for row in state]
                            copy[up][j] = piece
                            copy[i][j] = ' '
                            successor.append(copy)
                        #check for down
                        if down != 5 and state[down][j] == ' ':
                            copy = [row[:] for row in state]
                            copy[down][j] = piece
                            copy[i][j] = ' '
                            successor.append(copy)
                        #check for left
                        if left != -1 and state[i][left] == ' ':
                            copy = [row[:] for row in state]
                            copy[i][left] = piece
                            copy[i][j] = ' '
                            successor.append(copy)
                        #check for right
                        if right != 5 and state[i][right] == ' ':
                            copy = [row[:] for row in state]
                            copy[i][right] = piece
                            copy[i][j] = ' '
                            successor.append(copy)
                        #check for up left
                        if up != -1 and left != -1 and state[up][left] == ' ':
                            copy = [row[:] for row in state]
                            copy[up][left] = piece
                            copy[i][j] = ' '
                            successor.append(copy)
                        #check for up right
                        if up != -1 and right != 5 and state[up][right] == ' ':
                            copy = [row[:] for row in state]
                            copy[up][right] = piece
                            copy[i][j] = ' '
                            successor.append(copy)
                        #check for down left
                        if down != 5 and left != -1 and state[down][left] == ' ':
                            copy = [row[:] for row in state]
                            copy[down][left] = piece
                            copy[i][j] = ' '
                            successor.append(copy)
                        #check for down right
                        if down != 5 and right != 5 and state[down][right] == ' ':
                            copy = [row[:] for row in state]
                            copy[down][right] = piece
                            copy[i][j] = ' '
                            successor.append(copy)
        return successor
    
    def heuristic_game_value(self, state):

        #check horizontal
        my_row = 0
        opp_row = 0
        my_max_row = 0
        opp_max_row = 0
        for i in range(5):
            for j in range(5):
                if state[i][j] == self.my_piece:
                    my_row += 1
                elif state[i][j] == self.opp:
                    opp_row += 1
            if my_row > my_max_row:
                my_max_row = my_row
            if opp_row > opp_max_row:
                opp_max_row = opp_row
            my_row = 0
            opp_row = 0
        
        #check vertical
        my_col = 0
        opp_col = 0
        my_max_col = 0
        opp_max_col = 0
        for i in range(5):
            for j in range(5):
                if state[j][i] == self.my_piece:
                    my_col += 1
                elif state[j][i] == self.opp:
                    opp_col += 1
            if my_col > my_max_col:
                my_max_col = my_col
            if opp_col > opp_max_col:
                opp_max_col = opp_col
            my_col = 0
            opp_col = 0
        
        #check diagonal
        my_left_diag = 0
        opp_left_diag = 0
        my_max_left_diag = 0
        opp_max_left_diag = 0
        for i in range(2):
            for j in range(2):
                if state[i][j] == self.my_piece:
                    my_left_diag += 1
                elif state[i][j] == self.opp:
                    opp_left_diag += 1
                if state[i+1][j+1] == self.my_piece:
                    my_left_diag += 1
                elif state[i+1][j+1] == self.opp:
                    opp_left_diag += 1
                if state[i+2][j+2] == self.my_piece:
                    my_left_diag += 1
                elif state[i+2][j+2] == self.opp:
                    opp_left_diag += 1
                if state[i+3][j+3] == self.my_piece:
                    my_left_diag += 1
                elif state[i+3][j+3] == self.opp:
                    opp_left_diag += 1
                if my_left_diag > my_max_left_diag:
                    my_max_left_diag = my_left_diag
                if opp_left_diag > opp_max_left_diag:
                    opp_max_left_diag = opp_left_diag
                my_left_diag = 0
                opp_left_diag = 0
        
        my_right_diag = 0
        opp_right_diag = 0
        my_max_right_diag = 0
        opp_max_right_diag = 0
        for i in range(2):
            for j in range(3,5):
                if state[i][j] == self.my_piece:
                    my_right_diag += 1
                elif state[i][j] == self.opp:
                    opp_right_diag += 1
                if state[i+1][j-1] == self.my_piece:
                    my_right_diag += 1
                elif state[i+1][j-1] == self.opp:
                    opp_right_diag += 1
                if state[i+2][j-2] == self.my_piece:
                    my_right_diag += 1
                elif state[i+2][j-2] == self.opp:
                    opp_right_diag += 1
                if state[i+3][j-3] == self.my_piece:
                    my_right_diag += 1
                elif state[i+3][j-3] == self.opp:
                    opp_right_diag += 1
                if my_right_diag > my_max_right_diag:
                    my_max_right_diag = my_right_diag
                if opp_right_diag > opp_max_right_diag:
                    opp_max_right_diag = opp_right_diag
                my_right_diag = 0
                opp_right_diag = 0
        
        #check box
        my_box = 0
        opp_box = 0
        my_max_box = 0
        opp_max_box = 0
        for i in range(4):
            for j in range(4):
                if state[i][j] == self.my_piece:
                     my_box += 1
                elif state[i][j] == self.opp:
                    opp_box += 1
                if state[i+1][j] == self.my_piece:
                     my_box += 1
                elif state[i+1][j] == self.opp:
                    opp_box += 1
                if state[i][j+1] == self.my_piece:
                     my_box += 1
                elif state[i][j+1] == self.opp:
                    opp_box += 1
                if state[i+1][j+1] == self.my_piece:
                     my_box += 1
                elif state[i+1][j+1] == self.opp:
                    opp_box += 1
                if my_box > my_max_box:
                    my_max_box = my_box
                if opp_box > opp_max_box:
                    opp_max_box = opp_box
                my_box = 0
                opp_box = 0
        
        my_score = max(my_max_row, my_max_col, my_max_left_diag, my_max_right_diag, my_max_box)
        opp_score = max(opp_max_row, opp_max_col, opp_max_left_diag, opp_max_right_diag, opp_max_box)
        
        if my_score > opp_score:
            #print(my_score/4)
            return my_score/4
        elif my_score < opp_score:
            #print((-1)*opp_score/4)
            return (-1)*opp_score/4
        else:
            #print(0)
            return 0
    
    def max_value(self, state, depth):
        if self.game_value(state) == 1 or self.game_value(state) == -1:
            #print(self.game_value(state))
            return self.game_value(state), state
        elif depth >= 3:
            return self.heuristic_game_value(state), state
        else:
            alpha = -float('inf')
            final = state
            piece = self.my_piece
            for successor in self.succ(state,piece):
                value, _ = self.min_value(successor, depth+1)
                if value > alpha:
                    alpha = value
                    final = successor
                #alpha = max(alpha, self.min_value(self, successor, depth+1))
            return (alpha, final)
    
    def min_value(self, state, depth):
        if self.game_value(state) == 1 or self.game_value(state) == -1:
            #print(self.game_value(state))
            return self.game_value(state), state
        elif depth >= 3:
            return self.heuristic_game_value(state), state
        else:
            alpha = float('inf')
            final = state
            piece = self.my_piece
            for successor in self.succ(state, piece):
                value, _ = self.max_value(successor, depth+1)
                if value < alpha:
                    alpha = value
                    final = successor
                #alpha = max(alpha, self.max_value(self, successor, depth+1))
            return alpha, final





    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        # TODO: detect drop phase
        myPiece = 0
        oppPiece = 0
        for i in range(5):
            for j in range(5):
                if state[i][j] == self.my_piece:
                    myPiece += 1
                if state[i][j] == self.opp:
                    oppPiece += 1
        if oppPiece >= 4 and myPiece >= 4:
            drop_phase = False
        else:
            drop_phase = True

        if not drop_phase:
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            move = []
            _, outstate = self.max_value(state, 0)
            for i in range(5):
                for j in range(5):
                    if state[i][j] == ' ' and outstate[i][j] != ' ':
                        (row, col) = (i, j)
                    elif state[i][j] != ' ' and outstate[i][j] == ' ':
                        (source_row, source_col) = (i, j)
            move.append((row, col))
            move.append((source_row, source_col))
            return move


        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better
        move = []
        _, outstate = self.max_value(state, 0)
        for i in range(5):
                for j in range(5):
                    if state[i][j] == ' ' and outstate[i][j] != ' ':
                        (row, col) = (i, j)
        
        #while not state[row][col] == ' ':
        #    (row, col) = (different_index[0][0], different_index[1][0])

        # ensure the destination (row,col) tuple is at the beginning of the move list
        move.append((row, col))
        return move

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        for i in range(2):
            for j in range(2):
                if state[i][j] != ' ' and state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]:
                    return 1 if state[i][j]==self.my_piece else -1

        # TODO: check / diagonal wins
        for i in range(2):
            for j in range(3,5):
                if state[i][j] != ' ' and state[i][j] == state[i+1][j-1] == state[i+2][j-2] == state[i+3][j-3]:
                    return 1 if state[i][j]==self.my_piece else -1
                
        # TODO: check box wins
        for i in range(4):
            for j in range(4):
                if state[i][j] != ' ' and state[i][j] == state[i][j+1] == state[i+1][j] == state[i+1][j+1]:
                   return 1 if state[i][j]==self.my_piece else -1 

        return 0 # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
