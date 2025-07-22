 
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
            self._pathname = pathname
  
        def __str__(self):
            return f"CustomFile object for: {self._pathname}"
  
        def read_lines(self):
          if not os.path.exists(self._pathname):
              raise FileNotFoundError(f"{self._pathname} not found")
          with open(self._pathname, 'r') as file:
              for content in file:
                  yield content.strip()

        @property
        def file(self):
            return self._pathname
    
        @classmethod
        def create_all(cls, path):
            return list(map(cls, path))
    
        @file.setter
        def file(self, new_path):
            self._pathname = new_path

        @staticmethod
        def has_txt_ext(pathname):
            return pathname.lower().endswith('.txt')  

        def __add__(self, other):
        #Merges the two files 
            output = "merged.txt"
            with open(output, mode='w') as out:
                for line in self.read_lines():
                    out.write(line + '\n')
                for line in other.read_lines():
                    out.write(line + '\n')
            return CustomFile(output)
    
        @deco("red")
        def show_info(self):
    #Print the file path in red, then reset color
            print(f"Path name: {self._pathname}")

class MultiFile(CustomFile):
    #A subclass of CustomFile that can merge any number of text files
    
    @classmethod
    def concat(cls, *file_objs, output_path="merged_all.txt"):
        #Concatenate the contents of all given CustomFile (or MultiFile) instancesinto a single output file, then return a new MultiFile pointing at it
        with open(output_path, "w") as out:
            for fo in file_objs:
                for line in fo.read_lines():
                    out.write(line + "\n")
        return cls(output_path)

    def __add__(self, other):
    #Override __add__ to merge *two* files via concat for convenience
        return self.concat(self, other, output_path="merged.txt")






    

