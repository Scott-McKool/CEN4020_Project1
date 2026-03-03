from __future__ import annotations

class Result:
    '''The result of attempting an action that is not guarenteed.\n
    .success() returns if the attempted action was successfull.\n
    .obj() returns either an object (if the action resuts in an object) or none.\n
    .description() returns a string that is a description of the result.'''
    data        : tuple[object, str]
    successful  : bool

    def __init__(self, obj: object, description: str = "Description missing"):
        self.data = (obj, description)

    def success(self) -> bool:
        '''Did the attempted action succeed?'''
        return self.successful

    def obj(self) -> object:
        '''The returned object'''
        return self.data[0]
        
    def description(self) -> str:
        '''The description of the result'''
        return self.data[1] or "Description missing."
    
    def __str__(self):
        if self.success():
            return f"Successful: {self.description()}"
        
        if not self.success():
            return f"Unsuccessful: {self.description()}"

class Err(Result):
    '''Error variant of a result.'''
    def __init__(self, description = "Description missing"):
        super().__init__(None, description)
        self.successful = False

class OK(Result):
    ''''Successful variant of result.'''
    def __init__(self, obj = None, description = "Description missing"):
        super().__init__(obj, description)
        self.successful = True