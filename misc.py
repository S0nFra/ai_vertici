import pickle
import os

def save_obj(filename, obj, overwrite=True):
    """
    Save an object to a file using pickle.
    
    Args:
    filename (str): Name of the file to save the object to.
    obj (Any): The object to save.
    overwrite (bool): If False, the function will append a number to the filename if a file with the same name exists.
    """
    # Ensure the directory exists
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    if not overwrite:
        file_number = 1
        
        # Split the file name and extension
        file_name, file_extension = os.path.splitext(filename)
        
        # Check if the file already exists
        while os.path.exists(filename):
            # Append the auto-increment number before the extension
            filename = f"{file_name}_{file_number}{file_extension}"
            file_number += 1
    
    # Save the object to the file
    with open(filename, "wb") as file:
        pickle.dump(obj, file)
    
def load_obj(filename):
    """
    Load an object from a file using pickle.
    
    Args:
    filename (str): Name of the file to load the object from.
    
    Returns:
    Any: The loaded object.
    """
    with open(filename, "rb") as file:
        obj = pickle.load(file)
    return obj