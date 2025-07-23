
# project_venv.py
# This module defines CustomFile and MultiFile classes for reading and merging multiple text files.
# It demonstrates the use of generators, static methods, class methods, decorators alongside the required ANSI color.
# This module also includes object-oriented features such as inheritance and method overriding.

import os
import functools

ANSI_COLORS = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "reset": "\033[0m"
}

def deco(color: str):
    #Decorator factory: switches terminal to ANSI color, runs the func,then resets color back to default
    #Args - It is the color string for the desired ANSI color
    #Returns - A decorator that applies the color to the output of the decorated function
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # switch to the requested color
            print(ANSI_COLORS.get(color, ""), end="")
            # call the original method/function
            result = func(*args, **kwargs)
            # reset back to normal
            print(ANSI_COLORS["reset"], end="")
            return result
        return wrapper
    return decorator


class CustomFile:
    #It will manage reading from a file by using a generator
        
        def __init__(self, pathname):
        # def__init__ Initializes a CustomFile object with a file path
        # Pathname assigns a path to the file.    
            self._pathname = pathname
           

        def __str__(self):
        # Return a string representation of the CustomFile object
        # The return value is a string that includes the file path
            return f"CustomFile object for: {self._pathname}"
        

        def read_lines(self):
        # Generator that reads lines from the file, stripping whitespace
        # Yields each line as a stripped string  
          if not os.path.exists(self._pathname):
              raise FileNotFoundError(f"{self._pathname} not found")
          with open(self._pathname, 'r') as file:
              for content in file:
                  yield content.strip()


        @property
        def file(self):
        # Getter for the file property, returns the pathname   
            return self._pathname
    
        @classmethod
        def create_all(cls, path):
        # Class method to create CustomFile objects for a list of file paths
        # Args - path: a list of file paths
        # Returns - A list of CustomFile objects for each path     
            return list(map(cls, path))
    
        @file.setter
        def file(self, new_path):
        # Setter for the file property, updates the pathname
        # Its main purpose is to set a new file path
        # Args - new_path: the new file path to set
        # Returns - None 
            self._pathname = new_path

        @staticmethod
        def has_txt_ext(pathname):
        # Static method to check if a file has a .txt extension
        # Args - pathname: the file path to check
        # Returns - True if the file has a .txt extension, False otherwise     
            return pathname.lower().endswith('.txt')  

        def __add__(self, other):
        #Merges the two files 
        # Args - other: another CustomFile object to merge with
        # Returns - A new CustomFile object containing the merged contents of both files
            output = "merged.txt"
            with open(output, mode='w') as out:
                for line in self.read_lines():
                    out.write(line + '\n')
                for line in other.read_lines():
                    out.write(line + '\n')
            return CustomFile(output)
    
        @deco("red")
        def show_info(self):
        #Print file path in red, then reset color
            print(f"Path name: {self._pathname}")

class MultiFile(CustomFile):
    #subclass of CustomFile, merges many text files
    
    @classmethod
    def concat(cls, *file_objs, output_path="merged_all.txt"):
        # This concatenates the contents of the CustomFile into a single output file, then return a new MultiFile object
        # Args - file_objs: a list of CustomFile objects to concatenate
        with open(output_path, "w") as out:
            for fo in file_objs:
                for line in fo.read_lines():
                    out.write(line + "\n")
        return cls(output_path)

    def __add__(self, other):
        # Overrides the __add__ method to merge MultiFile objects
        # Args - other: another CustomFile object to merge with
        # Returns - A new MultiFile object containing the merged contents of both files
        return self.concat(self, other, output_path="merged.txt")






    

