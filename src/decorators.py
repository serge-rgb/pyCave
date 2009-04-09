def debug(f):
    '''
    Decorator.
    Function will enable pyCave debugging bjust for itself.
    Won\'t change anything if debugging is already enabled.
    '''
    def decorator(*args,**kargs):
        prevState = pyCaveOptions['debug']
        pyCaveOptions['debug'] = True
        f(*args,**kargs)
        pyCaveOptions['debug'] = prevState
        decorator.__name__ = f.__name__
    return decorator

class callparent():
    def __init__(self,parent):
        self.parent = parent
        
    def __call__(self,f):
        name = f.__name__
        self.parentFunc = None
        
        try:
            self.parentFunc = getattr(self.parent,name)
        except:
            print 'Decorator warning: No method on parent'
            return f
            
        def new_f(*args,**kargs):
            self.parentFunc(*args,**kargs)
            f(*args,**kargs)
            
        return new_f
    
