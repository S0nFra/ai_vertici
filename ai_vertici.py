from random import shuffle
from math import factorial

from misc import load_obj, save_obj

T = """     
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

vertices = {
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

triangles = {
    1 : ("a","b","c"),
    2 : ("b","d","e"),
    3 : ("c","e","f"),
    4 : ("d","g","h"),
    5 : ("e","h","i"),
    6 : ("f","i","l")
}

numbers = [0,1,2,3,4,5,6,7,8,9]

def print_board(solution) -> str:
    board = T
    for i, v in enumerate(vertices):
        board = board.replace(v, str(solution[i]))
    print(board)
    return board

def check_solution(triangles:dict, vertices:dict, verbose=False) -> bool:
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

def solve(tries=None, save_each=None) -> dict:
    if tries is None:
        tries = set()
    
    max_tries = factorial(len(numbers))
    last_save = 0

    while len(tries) < max_tries:
        shuffle(numbers)
        current_attempt = tuple(numbers)
        
        if current_attempt in tries:
            continue
                
        for i, v in enumerate(vertices):
            vertices[v] = numbers[i]
        
        seen_sapce = 100*len(tries)/max_tries
        print(f"Trie #{len(tries)} - {seen_sapce:.3f}% of the space")
        print(f"\t{vertices}")
        print(f"Seen {seen_sapce:.3f}% of the space")
        
        if save_each and len(tries) - last_save >= save_each:
            save_obj("tries.pk", tries)
            last_save = len(tries)
        
        if check_solution(triangles, vertices):
            return vertices
        
        tries.add(current_attempt)
    
    return None
            
# if __name__ == "__main__":
#     import time
#     solustions = list()
#     tries = set()
#     try:
#         tries = load_obj("true_tries.pk")
#     except FileNotFoundError as e:
#         print("No previous attempts were found")
    
#     while True:
#         start = time.time()
#         solution = solve(tries, 10000)
#         end = time.time()
        
#         if solution:
#             solution_nums = tuple(solution.values())
#             solustions.append(solution_nums)
#             tries.add(solution_nums)
#             with open("sols.txt","a") as f:
#                 f.write(f"Sol. {len(solustions)} : {str(solution)}\n")
#                 f.write(print_board(solution_nums)+"\n")
#                 f.write(f"Exec. time: {end-start} s")
#                 f.write("\n\n")
#         else:
#             break
    
#     tries -= set(solustions)
#     save_obj("true_tries.pk", tries)
