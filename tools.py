# modificated funcs from StackOverFlow
import random
import math
import itertools

try:
      import yaml

      class UniqueKeyLoader(yaml.SafeLoader):
           
           def construct_mapping(self, node, deep=False):
               mapping = []
               for key_node, value_node in node.value:
                   key = self.construct_object(key_node, deep=deep)
                   if key in mapping:
                       raise SyntaxError(f'"{key}" is a duplicated key. Please try to make it different.')
                   mapping.append(key)
               return super().construct_mapping(node, deep)

except ImportError:
      print('WARINIG: PyYAML lib not detected, using yaml files is impossible')
      
def print_progress_bar (iteration, total, prefix = '', suffix = '',
                        decimals = 1, length = 50, fill = '█', print_end = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    # modified function from StackOverflow
    
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = length * iteration / total
    extra, real_length = math.modf(filled_length)
    real_length = int(real_length)
    edge = ['-', '░', '▒', '▓'][int(extra*4)] if (length - real_length - 1 >= 0) else ''
    bar = fill * real_length + edge + '-' * (length - real_length - 1)
    print(f'{prefix} |{bar}| {percent}% {suffix}', end = print_end)
    
    # Print New Line on Complete
    if iteration == total: 
        print(' '*length*2, end = '\r')


## my funcs

def get_characteristic(x):
    return 1 + int(math.floor(math.log10(abs(x))))

def better_round(x, signs):
      if x == 0:
            return 0
      
      m = signs - get_characteristic(x)
      return round(x, m) if m > 0 else int(round(x, m))

import bisect

def weighted_random(prob):
    cum_weights = list(itertools.accumulate(prob))
    return bisect.bisect(cum_weights, random.random() * cum_weights[-1],
                                 0, len(cum_weights) - 1)

def auto_complete(array, default_values):
    "Non-clear function, changes array"
    array.extend(default_values[len(array):])
    return array
