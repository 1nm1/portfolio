#region Import Libraries
import os
import time
#endregion

def clear_terminal():
    '''
    Clears terminal 

    INPUTS:     None
    RETURNS:    None
    GLOBAL:     None      
    '''
    os.system('cls' if os.name == 'nt' else 'clear')


def func_perform_time(func):
    '''
    Prints to terminal the execution time for a specific function. Use as a decorator.

    INPUTS:     Object  [Function]    
    RETURNS:    Args, Kwargs from Function
    GLOBAL:     None      
    '''
    def function_timing(*args, **kwargs):
        prog_start = time.perf_counter()
        result = func(*args, **kwargs)
        prog_finish = time.perf_counter()
        run_time = round(prog_finish-prog_start,3)
        print("\t[Performance] " + str(func.__name__) + " --> " + str(run_time) + " sec")
        return result
    return function_timing


