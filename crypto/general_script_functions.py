#region Import Libraries
import os
import time
#endregion

def clear_terminal():
    '''
    Summary:
    ----------
    Clears terminal
    
    Params:
    ----------
    none

    Outputs:
    ----------
    none
    '''
    os.system('cls' if os.name == 'nt' else 'clear')


def func_perform_time(func):
    '''
    Summary:
    ----------
    Times the execution of a passed function
    
    Params:
    ----------
    func : Object
        function to time performance

    Outputs:
    ----------
    Args, Kwargs : Any
        Args, Kwargs from the passed function
    '''
    def function_timing(*args, **kwargs):
        prog_start = time.perf_counter()
        result = func(*args, **kwargs)
        prog_finish = time.perf_counter()
        run_time = round(prog_finish-prog_start,3)
        print("\t[Performance] " + str(func.__name__) + " --> " + str(run_time) + " sec")
        return result
    return function_timing


