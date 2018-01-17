class Problem:
	
    # Returns initial state of problem.
    def initialState(self): abstract
	
    # Returns True if state is a goal state, False otherwise.
    def goalTest(self, state): abstract
	
    # Returns list of successors of a state, where each successor is specified 
    # as a pair (action, result).
    def successorFn(self, state): abstract
	    	   
    # Returns cost of reaching result state by taking action on given state.
    def stepCost(self, state, action, result): abstract
    
    # Performs the specified action to get to the specified state.
    def takeAction(self, state, action): abstract

