import re


MESSAGESS = {
    0: "Enter your board dimensions: ",
    1: "Invalid dimensions!",
    2: "Enter the knight's starting position: ",
    3: "Invalid position!",
    4: "Enter your next move: ",
    5: "Invalid move!",
    6: "Here are the possible moves:\n",
    7: "What a great tour! Congratulations!",
    8: "No more possible moves!\nYour knight visited",
    9: "squares!",
    10: "Do you want to try the puzzle? (y/n): ",
    11: "No solution exists!",
    12: "Here's the solution!",
    13: "Invalid input! "
}


def outer_wrapper_with_msgs(msg_enter, msg_invalid):
    def input_wrapper(input_func):
        def wrapper(*args):
            valid_pattern = "^[1-9][0-9]* [1-9][0-9]*$"
            usr_input = input(msg_enter).strip()
            while True:
                if re.match(valid_pattern, usr_input):
                    usr_input = [int(x) for x in usr_input.strip().split()]

                    wrapped_func = input_func(*usr_input, *args)
                    if wrapped_func:
                        return usr_input[0], usr_input[1]
                    else:
                        print(msg_invalid, end="")
                        usr_input = input()
                else:
                    print(msg_invalid)
                    usr_input = input()
        return wrapper
    return input_wrapper


@outer_wrapper_with_msgs(MESSAGESS.get(0), MESSAGESS.get(1))
def input_board_dimensions(*args):
    """Whole functionality is done within a wrapper"""
    return True


@outer_wrapper_with_msgs(MESSAGESS.get(2), MESSAGESS.get(3))
def input_starting_pos(usr_cols, usr_rows, board_cols, board_rows):
    if usr_cols <= board_cols and usr_rows <= board_rows:
        return usr_cols, usr_rows
    else:
        return


@outer_wrapper_with_msgs(MESSAGESS.get(4), MESSAGESS.get(5))
def input_next_move(usr_cols, usr_rows, tree):
    if [usr_cols, usr_rows] in [[x.col, x.row] for x in tree.list_of_possible_moves]:
        return usr_cols, usr_rows
    else:
        return


class Board:
    poss_moves = [[-1, 2], [1, 2], [2, -1], [2, 1], [-2, -1], [-2, 1], [1, -2], [-1, -2]]

    def __init__(self, cols, rows):
        self.cols, self.rows = cols, rows
        self.cell_size = "_" * len(str(self.cols * self.rows))
        self.board = [[self.cell_size for _ in range(self.cols)] for _ in range(self.rows)]
        self.list_of_trees = []

    def clear(self):
        self.board = [[self.cell_size for _ in range(self.cols)] for _ in range(self.rows)]

    def place_move(self, move_or_lst):
        if isinstance(move_or_lst, list):
            for move in move_or_lst:
                self.board[move.row - 1][move.col - 1] = " " * (len(str(board.cols * board.rows)) - 1) + str(move.mark)
        else:
            self.board[move_or_lst.row - 1][move_or_lst.col - 1] = " " * (len(str(board.cols * board.rows)) - 1) + str(move_or_lst.mark)

    def where_can_we_go(self, move):
        lst = []
        for c, r in Board.poss_moves:
            if 1 <= move.col + c <= self.cols and 1 <= move.row + r <= self.rows:
                m = Move(move.col + c, move.row + r)
                lst.append(m)
        lst = [x for x in lst if [x.col, x.row] not in [[x.base_move.col, x.base_move.row] for x in self.list_of_trees]]
        return lst

    def get_num_of_poss_move(self, move):
        return len(self.where_can_we_go(move)) - 1

    def build_tree(self, move):
        base_move = Move(move.col, move.row)
        possible_moves = self.where_can_we_go(base_move)
        possible_moves_with_nums = []
        for move in possible_moves:
            move = Move(move.col, move.row, self.get_num_of_poss_move(move))
            possible_moves_with_nums.append(move)

        return Tree(base_move, possible_moves_with_nums)

    def add_tree(self, tree):
        tree.base_move.mark = "*"
        self.list_of_trees.append(tree)

    def auto(self):
        """
        The recursive part awww yeah!!!
        The function operates on a list of trees which is basically a list of all done moves.
        A move/tree is included only if there is continuation. The last move doesn't have a continuation.
        If we can generate the next move and there's only one square left -> WIN
        """
        if not self.list_of_trees:
            return
        else:
            current_tree = self.list_of_trees[-1]
            next_move = current_tree.choose_move()

            if next_move and len(self.list_of_trees) >= board.cols * board.rows - 1:
                final_sequence = [x.base_move for x in self.list_of_trees] + [next_move]
                for index, move in enumerate(final_sequence, 1):
                    move.mark = index
                self.list_of_trees = []
                return final_sequence
            elif next_move:
                self.list_of_trees.append(self.build_tree(next_move))
                return self.auto()
            else:
                self.list_of_trees.pop()
                return self.auto()

    def __str__(self):
        left_margin = len(str(self.cols * self.rows))

        board = ""
        boarder = f"{' '.rjust(left_margin)}{'-' * (self.cols * (len(self.cell_size) + 1) + 3)}\n"
        board += boarder

        temp_board = self.board.copy()
        temp_board.reverse()

        for index, row in enumerate(temp_board):
            board += f"{str(self.rows - index).rjust(left_margin)}" + f"| {' '.join(row)} |\n"
        board += boarder

        bottom_line = [str(x).rjust(left_margin) for x in range(1, self.cols + 1)]
        board += f"   {' '.join(bottom_line)}"
        return board


class Move:
    def __init__(self, col, row, mark="X"):
        self.col, self.row = col, row
        self.mark = mark

    def __str__(self):
        return f"Move: {[self.col, self.row, self.mark]}"


class Tree:
    def __init__(self, base_move, lst_of_possible_moves):
        self.base_move = base_move
        self.list_of_possible_moves = lst_of_possible_moves
        self.chosen_moves = []

    def __str__(self):
        return f"Tree: {self.base_move.__str__(), [x.__str__() for x in self.list_of_possible_moves], [x.__str__() for x in self.chosen_moves]}"

    def choose_move(self):
        if self.list_of_possible_moves:
            self.list_of_possible_moves.sort(key=lambda x: x.mark)
            self.chosen_moves.append(self.list_of_possible_moves[0])
            return self.list_of_possible_moves.pop(0)
        else:
            return False


if __name__ == "__main__":
    board = Board(*input_board_dimensions())
    starting_move = Move(*input_starting_pos(board.cols, board.rows))
    usr = input(MESSAGESS.get(10)).strip()
    while True:
        if re.match("^n$", usr):
            board.list_of_trees.append(board.build_tree(starting_move))
            result = board.auto()
            if result:
                print(MESSAGESS.get(12))
                board.place_move(result)
                print(board)
            else:
                print(MESSAGESS.get(11))
            break
        elif re.match("^y$", usr):
            board.list_of_trees.append(board.build_tree(starting_move))
            result = board.auto()
            if not result:
                print(MESSAGESS.get(11))
                break
            else:
                board.place_move(starting_move)
                tree = board.build_tree(starting_move)
                board.add_tree(tree)
                board.place_move(tree.list_of_possible_moves)
                print(board)
                while True:
                    board.clear()
                    current_move = Move(*input_next_move(tree))
                    board.place_move(current_move)

                    tree = board.build_tree(current_move)
                    board.add_tree(tree)

                    board.place_move([t.base_move for t in board.list_of_trees[:-1]])
                    board.place_move(tree.list_of_possible_moves)

                    if len(board.list_of_trees) >= board.cols * board.rows:
                        print(board)
                        print(MESSAGESS.get(7))
                        break
                    elif len(tree.list_of_possible_moves) < 1:
                        print(board)
                        print(f"{MESSAGESS.get(8)} {len(board.list_of_trees)} {MESSAGESS.get(9)}")
                        break
                    else:
                        print(board)
                break
        else:
            usr = input(MESSAGESS.get(13)).strip()
            
