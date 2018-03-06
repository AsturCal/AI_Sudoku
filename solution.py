
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# Elegant way to generate the two diagonals.
diagonal_units = [[rows[i]+cols[i] for i in range(9)],[rows[i]+cols[-i-1] for i in range(9)]]
# Update the unit list to add the new diagonal units
unitlist = row_units + column_units + square_units + diagonal_units

# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


"""
Three functions for Naked twins. 
    - (Helper)Fine naked twins to find the naked twins separately.
    - (Helper)Eliminate twin values from peers .... helper removes values from peers. 
    - (main) The code requested.
"""
def find_naked_twins(possible_twins, values):
    """
    Store in an array of tuples all values that are actually same 2 numbers in two different boxes 
    """

    naked_twins = []
    for twin1 in possible_twins:
        for twin2 in peers[twin1]:
            if values[twin1] == values[twin2]:
                #actually found a twin....
                naked_twins.append((twin1, twin2))
    return naked_twins

def remove_twin_values(naked_twins, values):
    """
    Iterate over all the pairs of naked twins found.
    - Find peer boxes that have common twins and intersect
    - Iterate over the set of intersecting peers
    - Delete the naked twins values from each of those intersecting peers with 2+ values
    """

    for index in range(len(naked_twins)):
        box1, box2 = naked_twins[index][0], naked_twins[index][1]
        peers1, peers2 = peers[box1], peers[box2]
        peers_intersection = set(peers1).intersection(peers2)
        for peer_box in peers_intersection:
            if len(values[peer_box]) > 1:
                for digit in values[box1]:
                    #Use given function.
                    values = assign_value(values, peer_box, values[peer_box].replace(digit,''))
def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    # TODO: Implement this function!
    # Find all possible twin candidates - boxes with only two values. 
    candidate_twins = [box for box in values.keys() if len(values[box]) == 2]

    naked_twins = find_naked_twins(candidate_twins, values)

    remove_twin_values(naked_twins, values)

    return values

    #raise NotImplementedError


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom to complete this function
    for k,v in values.items():              #for all boxes
       if len(v) == 1:                      #if box has single digit
           for peer in peers[k]:            #remove digit from peers
               values[peer] = values[peer].replace(v,'')
    return values
    #raise NotImplementedError


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    # TODO: Copy your code from the classroom to complete this function
    for unit in unitlist:
        for value in '123456789':
            valuein = [box for box in unit if value in values[box]]
            if len(valuein) == 1: #value is in ONLY one place, must be it
                values[valuein[0]] = value
    return values
    #raise NotImplementedError


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    # TODO: Copy your code from the classroom and modify it to complete this function
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Naked Twins Strategy
        values = naked_twins(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
    #raise NotImplementedError


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy. Actually call the naked twins on reduce. 
    Naked twins is better called in the reduce functions.
    """
    # TODO: Copy your code from the classroom to complete this function
    values = reduce_puzzle(values)
    if values is False:
        return  False #falied misserably sanity check before.
    if all(len(values[s])==1 for s in boxes): #all values = 1 solved.
        return values
    
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]) , s) for s in boxes if len(values[s]) > 1) #minimun lenght and box name for that one!.
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[s]:   #previous minimun
        temp_sudoku = values.copy() #new sudoku
        temp_sudoku[s] = value      #copy one of the values and try to solve by calling recursively.
        result = search(temp_sudoku) #call this function... will invoke reduce_puzzle in first line.
        if result:
            return result
    #raise NotImplementedError


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)
# Remove visual for the time being. 

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')


