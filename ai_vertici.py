from random import shuffle
from math import factorial

from misc import load_obj, save_obj, format_time

GRAPH = """     
            a
           / \\
          / x \\
         b --- c
        / \\   / \\
       / x \\ / x \\
      d --- e --- f
     / \\   / \\   / \\
    / x \\ / x \\ / x \\
   g --- h --- i --- l
   """

VERTICES = {
    'a':0,
    'b':0,
    'c':0,
    'd':0,
    'e':0,
    'f':0,
    'g':0,
    'h':0,
    'i':0,
    'l':0
}

TRIANGLES = {
    1 : ("a","b","c"),
    2 : ("b","d","e"),
    3 : ("c","e","f"),
    4 : ("d","g","h"),
    5 : ("e","h","i"),
    6 : ("f","i","l")
}

NUMBERS = [0,1,2,3,4,5,6,7,8,9]

def render_solution(solution:dict, graph:str) -> str:
    """
    Replace vertices in the graph string with their values from the solution dictionary and print it.

    Args:
        solution (dict): A dictionary mapping vertex labels to their values.
        graph (str): A string representation of the graph with placeholder vertex labels.

    Returns:
        str: The graph string with vertex labels replaced by their values.
    """
    for v in solution:
        graph = graph.replace(v, str(solution[v]))

    return graph

def check_solution(triangles:dict, vertices:dict, verbose:bool=False) -> bool:
    """
    Check if the current vertex assignment satisfies the condition that the sum of vertex values
    for each triangle is the same.

    Args:
        triangles (dict): A dictionary where each key is a triangle index and each value is a tuple of vertex labels.
        vertices (dict): A dictionary mapping vertex labels to their values.
        verbose (bool): If True, print detailed information about the check process.

    Returns:
        bool: True if all triangles have the same sum, False otherwise.
    """
    last_sum = None
    for v1, v2, v3 in triangles.values():
        curr_sum = vertices[v1] + vertices[v2] + vertices[v3]
        if verbose:
            print("\tt>",v1, v2, v3,"s>",curr_sum)
        if last_sum is None: # First time
            last_sum = curr_sum
        elif last_sum != curr_sum:
            return False
    return True

def solve(vertices:dict, tries=None, bkp_each:int=None, verbose:bool=False) -> dict:
    """
    Attempt to find a valid solution for the vertex values by trying permutations of numbers.

    Args:
        vertices (dict): A dictionary mapping vertex labels to their current values. This dictionary will be updated
                         with the values of the current permutation being tested.
        tries (set, optional): A set of attempted permutations to avoid redundant work. If None, it starts with an empty set.
        bkp_each (int, optional): The number of tries between each backup of attempts to a file. If None, no backups are made.
        verbose (bool, optional): If True, print detailed information about the solving process, including progress and
                                   intermediate results.

    Returns:
        dict: A dictionary mapping vertex labels to their values if a solution is found. Returns None if no solution is found.
    """
    if tries is None:
        tries = set()
    
    max_tries = factorial(len(NUMBERS))
    last_save = 0

    while len(tries) < max_tries:
        shuffle(NUMBERS)
        current_attempt = tuple(NUMBERS)
        
        if current_attempt in tries:
            continue
                
        for i, v in enumerate(vertices):
            vertices[v] = NUMBERS[i]
        
        if verbose:
            seen_space = 100 * len(tries) / max_tries
            print(f"Try #{len(tries)} - {seen_space:.3f}% of the space")
            print(f"\t{vertices}")
        
        if bkp_each and len(tries) - last_save >= bkp_each:
            save_obj(f"bckp.pk", tries)
            last_save = len(tries)
        
        if check_solution(TRIANGLES, vertices):
            return vertices
        
        tries.add(current_attempt)
    
    return None

def find_solutions(vertices, tries=None, bkp_each:int=None, verbose:bool=False):
    """
    Find all possible solutions by repeatedly calling the solve function until no more solutions are found.
    The results are saved to a file named "sols.txt", and the current set of attempted permutations is saved to
    a file named "tries.pk".

    Args:
        vertices (dict): A dictionary mapping vertex labels to their current values. This dictionary is passed to the
                         solve function and updated with the values of the current permutation being tested.
        tries (set, optional): A set of attempted permutations to avoid redundant work. If None, it starts with an empty set.
        bkp_each (int, optional): The number of tries between each backup of attempts to a file. If None, no backups are made.
        verbose (bool, optional): If True, print detailed information about the solving process, including progress and
                                   intermediate results.

    Returns:
        None

    Notes:
        - The "sols.txt" file will contain all found solutions with their details and execution times.
        - The "tries.pk" file will contain the current set of attempted permutations to resume from where it left off
          in future runs.
        - The function removes found solutions from the `tries` set to prevent reprocessing them in future runs.
    """
    import time
    solutions = list()
    
    if tries is None:
        tries = set()
    
    gstart = time.time()
    while True:
        lstart = time.time()
        solution = solve(vertices, tries, bkp_each, verbose)
        lend = time.time()
        
        if solution:
            solution_nums = tuple(solution.values())
            solutions.append(solution_nums)
            # Add the solution to make solve() ignore it
            tries.add(solution_nums)
            with open("sols.txt", "a") as f:
                msg_header = f"Solution {len(solutions)} at try #{len(tries)} : {str(solution)}"
                f.write(msg_header + "\n")
                print(msg_header)
                f.write(render_solution(solution, GRAPH) + "\n")
                f.write(f"Found in: {lend - lstart} s")
                f.write("\n\n")
        else:
            break
    
    print("Total execution time:", format_time(time.time() - gstart), "s")
    
    # Remove the found solutions from `tries` to prevent reprocessing
    tries -= set(solutions)
    save_obj("tries.pk", tries)
    
if __name__ == "__main__":
    import argparse
    # Configure the argument parser
    parser = argparse.ArgumentParser(
        description="Solver for the 'Ai Vertici' puzzle."
    )
    parser.add_argument("--all-solutions", "-a",
                        action="store_true",
                        default=False,
                        help="Find and list all possible solutions to the puzzle. Without this flag, only one solution is found.")
    parser.add_argument("--tries-filepath", "-t",
                        default="tries.pk",
                        type=str,
                        help="Path to the file where previously attempted permutations are stored. Default is 'tries.pk'.")
    parser.add_argument("--bck-each", "-b",
                        default=None,
                        type=int,
                        help="Number of tries after which to backup the current set of attempts to a file. If not specified, no backups are made.")
    parser.add_argument("--verbose", "-v",
                        action="store_true",
                        default=False,
                        help="Print detailed information about the solving process, including progress and intermediate results.")

    # Parse the arguments from the command line
    args = parser.parse_args()
    
    try:
        tries = load_obj(args.tries_filepath)
    except FileNotFoundError:
        print("No previous attempts were found.")
        tries = None
    
    if args.all_solutions:
        find_solutions(VERTICES, tries, args.bck_each, args.verbose)
    else:
        sol = solve(VERTICES, tries, args.bck_each, args.verbose)
        if sol:
            print(render_solution(sol, GRAPH))
        else:
            print("No solution found.")
