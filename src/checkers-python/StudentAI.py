from random import randint, random
import math
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class Node():
    def __init__(self,board=None, move=None, color=None, untried_moves=None):
        self.board = board
        self.move = move
        self.color = color
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = untried_moves if untried_moves is not None else []

    def ucb1(self, exploration_weight=1.41):
        if self.visits == 0:
            return float('inf')  # Return infinity for unvisited nodes
        return (self.wins / self.visits) + exploration_weight * math.sqrt(math.log(self.parent.visits) / self.visits)

class StudentAI():
    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
        self.simulation_limit = 500 
        
    def _get_flattened_moves(self, color):
        moves = self.board.get_all_possible_moves(color)
        return [m for piece_moves in moves for m in piece_moves]
    
    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
            
        root_moves = self._get_flattened_moves(self.color) # flatten the list of moves for the current color
        if not root_moves:
            return Move([])

        root = Node(self.board, parent=None, move=move, color=self.opponent[self.color], untried_moves=root_moves)
        
        for _ in range(self.simulation_limit): # Number of iterations for MCTS
            node = root
            moves_made_in_selection = 0
            current_turn = self.color
        
            # Selection
            while not node.untried_moves and node.children:
                node = max(node.children, key=lambda c: c.ucb1())
                self.board.make_move(node.move, current_turn)
                current_turn = self.opponent[current_turn]
                moves_made_in_selection += 1
                
            # Expansion
            if node.untried_moves:
                move = node.untried_moves.pop()
                
                self.board.make_move(move, current_turn)
                current_turn = self.opponent[current_turn]
                moves_made_in_selection += 1
                
                new_node = Node(self.board, parent=node, move=move, color=current_turn, untried_moves=self._get_flattened_moves(current_turn))
                node.children.append(new_node)
                node = new_node
                
            # Simulation
            rollout_moves_made = 0
            win_status = self.board.is_win(current_turn)
            
            while win_status == 0:
                sim_moves = self._get_flattened_moves(current_turn)
                if not sim_moves:
                    break
                    
                random_move = random.choice(sim_moves)
                self.board.make_move(random_move, current_turn)
                current_turn = self.opponent[current_turn]
                rollout_moves_made += 1
                win_status = self.board.is_win(current_turn)
            
            # Backpropagation
            if win_status == self.color:
                result = 1.0
            elif win_status == -1:
                result = 0.5 # Tie
            else:
                result = 0.0

            while node is not None:
                node.visits += 1
                node.wins += result
                node = node.parent
            
            # Undo the moves made during selection and simulation
            total_moves_to_undo = rollout_moves_made + moves_made_in_selection
            for _ in range(total_moves_to_undo):
                self.board.undo()

        best_child = max(root.children, key=lambda c: c.ucb1(exploration_weight=0))
        self.board.make_move(best_child.move, self.color)
        
        return best_child.move