class State:
    """Abstract class"""
    def __init__(self, grid, num_players, **kwargs):
        self.grid = grid
        self.num_players = num_players
        raise NotImplementedError

    def move(self, move: str):
        """ if not legal move:
                return 'ILLEGAL'
            else:
                return 'OK'
        """
        raise NotImplementedError
    
    # Code inspired by https://stackoverflow.com/questions/652276/is-it-possible-to-create-anonymous-objects-in-python
    class Evaluation(object):
        def __new__(cls, **attrs):
            instance = object.__new__(cls)
            instance.__dict__ = attrs
            return instance
    
    def evaluate(self):
        """Return tuple of normalised scores for each
        player
        # example
        scores = [self.evalfor(i) for i in range(self.num_players)]
        total = sum(scores)
        norm_scores = [x/total for x in scores]
        return tuple(norm_scores)
        """
        
        raise NotImplementedError
    
    def evalfor(self, player):
        """Evaluate probability of player winning
        Definite win = 1
        Definite loss = 0
        Otherwise 'undefined'
        """
        
        raise NotImplementedError