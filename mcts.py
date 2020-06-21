"""File to include a base node class to build a tree and other helper functions"""

import random
import usefulconstants as uc
import numpy as np

class Node:
    """The base node class"""
    def __init__(self, state, parent=None, children=None, num=0, score=0.0):
        self.state = state
        self.current_player = self.state.turn

        self.parent = parent
        self.expanded_children = [] if children == None else children

        self.unexpanded_children = self.state.generate_legal_moves()
        random.shuffle(self.unexpanded_children)

        self.num = num
        self.score = score

        self.WIN = 1.0
        self.DRAW = 1/self.state.num_players
        self.LOSS = 0.0
    
    def expand(self) -> tuple:
        """Recursive function to grow tree
        returns the score of a playthrough

        Uses constants for score after certain outcome
        and also constant c for expansion vs exploration
        c == sqrt(2) is default
        """
        c = np.sqrt(2)
        
        # We start from the root
        # If this node has never been used before it has self.num == 0
        if self.num == 0:
            # So we can finish one random playthrough and that is enough
            playthrough = self.state.deepcopy
            ev = playthrough.evaluate()
            # Create a copy of the state and play moves randomly until game ends
            while ev.status == uc.ONGOING:
                move = random.choice(playthrough.generate_legal_moves())
                playthrough.move(move)
            # Now that game has ended get result
            self.num += 1
            if ev.status == uc.WON:
                if self.current_player == ev.player:
                    self.score += self.WIN
                else:
                    self.score += self.LOSS
                return tuple(self.LOSS if i != ev.player else self.WIN for i in self.state.num_players)
            elif ev.status == uc.DRAWN:
                self.score += self.DRAW
                return tuple(1/self.state.num_players for _ in range(self.state.num_players))
            
        # If there are unexpanded children at the root we must expand them
        elif len(self.unexpanded_children) > 0:
            # Select a fresh random child, u, from unexpanded_children
            u_move = self.unexpanded_children.pop()
            u_state = self.state.deepcopy()
            assert u_state.move(u_move) == uc.OK

            # Now add a child to the tree using this new state
            u_node = Node(state=u_state, parent=self)
            self.expanded_children.append(u_node)

            # Expand that into node recursively
            playthrough = u_node.expand()
            
        # If we are not at a leaf we must move further down
        elif len(self.expanded_children) > 0:
            # Select a previously explored leaf to explore further
            best_node = max(self.expanded_children, key=lambda i: i.score/i.num + c * np.sqrt(np.log(self.num)/i.num))
            playthrough = best_node.expand()
        
        # Increment numbers
        self.num += 1
        self.score += playthrough[self.current_player]
        return playthrough