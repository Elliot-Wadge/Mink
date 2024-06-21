import numpy as np
from scipy.optimize import curve_fit
import copy

def cmp_dec(comparison: callable) -> callable:
    def new_comparison(self, other):
        if type(self) != type(other):
            raise ValueError(f'cannot compare {type(self).__name__} with {type(other).__name__}')
        else:
            return comparison(self, other)
    return new_comparison


class FitResult:   
    pOpt: np.ndarray
    pCov: np.ndarray 
    pError: np.ndarray
    f: callable
    x: np.ndarray 
    y: np.ndarray
    yErr: np.ndarray = None
    norm_res: np.ndarray
    chisq: float = None
    dof: int 
    
    def __init__(self, pOpt=None, pCov=None, x=None, y=None, f=None, sigma=None):
        self.pOpt = pOpt
        self.pCov = pCov
        self.pError = np.sqrt(np.diag(pCov))
        self.x = x
        self.y = y
        self.f = f
        self.dof = len(self.y) - len(self.pOpt)
        
        if sigma is not None:
            self.yErr = sigma
            self.norm_res = (self.y - self.f(self.x, *self.pOpt))/sigma
            self.chisq = np.sum(self.norm_res**2)/(len(self.y)-len(self.pOpt))
            
    def __str__(self):
        st = f"function = {self.f.__name__}"
        st += " {\n"
        st += '\tfit results:\n'
        for i,par in enumerate(self.pOpt):
            st += f'\t\t{par} +/- {self.pError[i]}\n'
        st += '\n'
        if self.chisq is not None:
            st += f'\treduced chisq = {self.chisq}\n'
        st += f"\tdof = {self.dof}"
        st += "\n\t}"
        return st
    
    @cmp_dec
    def __eq__(self, other):       
        if self.chisq == other.chisq:
            return True
        else:
            return False
     
    @cmp_dec   
    def __lt__(self, other):
        if self.chisq < other.chisq:
            return True
        else:
            return False
    
    @cmp_dec
    def __gt__(self, other):
        if self.chisq > other.chisq:
            return True
        else:
            return False
   

    
def full_return(f: callable) -> callable:
    '''function for decorating the scipy.optimize.curve_fit function to a return a 
    more useful and encapselated result'''
    def new_f(*args, **kwargs):
        kwargs = copy.deepcopy(kwargs)
        # ensure that full output is off
        sigma = None
        # call curve fit as normal
        pOpt, pCov = f(*args, **kwargs)
        # load the results into the Fit Class format
        
        # extract sigma if it was given
        if "sigma" in kwargs.keys():
            try:
                # error must be in absolute sigma for chisq calculation
                if kwargs["absolute_sigma"] == True:
                    sigma = kwargs["sigma"]
                elif kwargs["absolute_sigma"] == False:
                    # mulitply by y if not absolute
                    sigma = kwargs["sigma"]*args[2]
            except KeyError:
                pass
        # load results into the Fit class
        result = FitResult(f=args[0], x=args[1], y=args[2], pOpt=pOpt, pCov=pCov, sigma=sigma)
        return result
    
    return new_f
