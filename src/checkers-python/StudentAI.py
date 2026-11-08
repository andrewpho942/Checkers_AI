from random import randint, random
import math
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class Node():
    def __init__(self, move=None, parent=None, color=None, untried_moves=None):
        self.move = move
        self.parent = parent
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

        root = Node(color=self.opponent[self.color], untried_moves=root_moves)
        
        root_tie_counter = self.board.tie_counter
        
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
                index = randint(0, len(node.untried_moves) - 1)
                move_to_try = node.untried_moves.pop(index)
                
                self.board.make_move(move_to_try, current_turn)
                current_turn = self.opponent[current_turn]
                moves_made_in_selection += 1
                
                new_node = Node(parent=node, move=move_to_try, color=self.opponent[current_turn], untried_moves=self._get_flattened_moves(current_turn))
                node.children.append(new_node)
                node = new_node
                
            # Simulation
            rollout_moves_made = 0
            win_status = self.board.is_win(current_turn)
            rollout_depth_limit = 15  # Stop random moves early to prevent noise and timeouts
            
            while win_status == 0 and rollout_moves_made < rollout_depth_limit:
                sim_moves = self._get_flattened_moves(current_turn)
                if not sim_moves:
                    win_status = self.opponent[current_turn]
                    break
                
                index = randint(0, len(sim_moves) - 1)
                random_move = sim_moves[index]
                self.board.make_move(random_move, current_turn)
                current_turn = self.opponent[current_turn]
                rollout_moves_made += 1
                win_status = self.board.is_win(current_turn)
            
            is_heuristic = False
            if win_status == 0:
                is_heuristic = True
                my_pieces = self.board.black_count if self.color == 1 else self.board.white_count
                opp_pieces = self.board.white_count if self.color == 1 else self.board.black_count
                
                if my_pieces > opp_pieces:
                    win_status = self.color # We have more pieces, count as a win
                elif opp_pieces > my_pieces:
                    win_status = self.opponent[self.color] # They have more pieces, count as a loss
                else:
                    win_status = -1
                    
            # Backpropagation
            if win_status == self.color:
                base_reward = 0.8 if is_heuristic else 1.0
            elif win_status == -1:
                base_reward = 0.5
            else:
                base_reward = 0.2 if is_heuristic else 0.0
            
            discount = 0.99 ** rollout_moves_made # If a rollout takes too many moves to win, the reward shrinks
            final_reward = base_reward * discount # This forces the bot to seek the fastest possible path to capture the final pieces
            
            while node is not None:
                node.visits += 1
                if win_status == node.color:
                    node.wins += final_reward # This move resulted in a win for the player who made it
                elif win_status == -1:
                    node.wins += 0.5 * discount  # Tie
                # If win_status is the opponent's color, node.wins gets +0.0
                node = node.parent
                
            # Undo the moves made during selection and simulation
            total_moves_to_undo = rollout_moves_made + moves_made_in_selection
            for _ in range(total_moves_to_undo):
                self.board.undo()
            
            self.board.tie_counter = root_tie_counter

        best_child = max(root.children, key=lambda c: c.visits)
        self.board.make_move(best_child.move, self.color)
        
        return best_child.move