import random
import copy
import argparse
# from contextlib import contextmanager
import os, sys
# from io import StringIO
import math

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
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = length * iteration / total
    extra, real_length = math.modf(filled_length)
    real_length = int(real_length)
    edge = ['-', '░', '▒', '▓'][int(extra*4)] if (length - real_length - 1 >= 0) else ''
    bar = fill * real_length + edge + '-' * (length - real_length - 1)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = print_end)
    # Print New Line on Complete
    if iteration == total: 
        print(' '*length*2, end = '\r')
        

parser = argparse.ArgumentParser(description='This program dispenses things to people (mininmizing total pain) \
using annealing. As input it takes file with people descriptions (for each in each line there is name, \
optimal_weight and weight_sensevity (number of times pain increases when mass increased by optimal_mass)\
in this order, separated by spaces/tabs) and things descriptions \
(similarly, in each line there is name, weight, owner and number of pain he gains from giving it to anybody else \
in this order separated by spaces/tabs). Default values are designed to <10 people and <50 things, so if your \
values are larger, it\'s recommended to change the default values. This means increasing number of iterations \
to get better result. If you do so, it\'s also recommended to increase gradient proportionally. However, the situation \
may be different, so it\'s best to modify according to circumstances.')

parser.add_argument('people_file', type=str, help='Input file with people data')
parser.add_argument('things_file', type=str, help='Input file with things data')

parser.add_argument('-o', '--output_file', dest = 'output_file', default = None,
                    help='Output file; if not specified, stdout is used')

parser.add_argument('-w', '--print_own', dest = 'print_own', action='store_true',
                    help='Print just current owners; useful for an overview')

parser.add_argument('-l', '--print_log', dest = 'print_log', action='store_true',
                    help='Print total pain and temperature instead of progress bars')

parser.add_argument('-a', '--auto_complete', dest = 'auto_complete', action='store_true',
                    help='Allows not full completed data files; people are auto-completed with 10 optimal_weight \
                            and 10 sensevity; things have 1 kg mass and don\'t belong to anybody.')

parser.add_argument('-d', '--disable_progress_info', dest = 'disable_progress_info', action='store_true',
                    help='No progress info')

parser.add_argument('-e', '--epoch_number', dest = 'epoch_number', type=int, default = 3,
                    help='Default number of general attempts; default is 3')

parser.add_argument('-i', '--iteration_number', dest = 'iteration_number', type=int, default = 300_000,
                    help='Default number of iteration in each attempt; if not specified, equals to 300_000')

parser.add_argument('-g', '--gradient', dest = 'gradient', type=float, default = 100_000,
                    help='Number of iterations it takes to decrease temperature in 10 times; default is 100_000')

parser.add_argument('-t', '--start_temperature', dest = 'start_temperature', type=float, default = 50,
                    help='Start temperature; default is 50 (pains)')

parser.add_argument('-p', '--pain_multiply', dest = 'pain_multiply', type=float, default = 15,
                    help='Default pain (at optimal weight); default is 15')

parser.add_argument('-u', '--update_freq', dest = 'update_freq', type=int, default = 1_000,
                    help='Number of iterations between updating bar/log; default is 1_000')


##parser.add_argument('-c', '--cyrillic_for_cmd', dest = 'cyrillic_for_cmd', action='store_true',
##                    help = 'Use if you have problems with encoding')
args = parser.parse_args()

##if args.cyrillic_for_cmd:
##      os.dup2(1, 2)
##      print_orig = print
##      def print(*args):
##          @contextmanager
##          def redirected(out):
##              sys.stdout = out
##              try:
##                  yield
##              finally:
##                  sys.stdout = sys.__stdout__
##       
##          out = StringIO()
##       
##          with redirected(out=out):
##              print_orig(*args)
##              result = out.getvalue().encode('1251', errors = 'ignore')
##       
##          sys.stdout.buffer.write(result)
##          sys.stdout.flush()
          
assert os.path.isfile(args.people_file) and os.path.isfile(args.things_file)



def auto_complete(array, default_values):
    array.extend(default_values[len(array):])
    return array

try:
    people = {}
    for line in open(args.people_file, encoding='utf-8'):
          if not len(line) or line[0] == '#':
              continue
          current = line.strip().split()
          if not len(current):
                continue
          if args.auto_complete: current[1:] = auto_complete(current[1:], [10, 10])
          people[current[0]] = float(current[1]), float(current[2])
          
    names = list(people.keys())

    things = []
    for line in open(args.things_file, encoding='utf-8'):
          if not len(line) or line[0] == '#':
              continue
          current = line.strip().split()
          if not len(current):
                continue
          if args.auto_complete: current[1:] = auto_complete(current[1:], [1.0, None, 0.0])
          things.append([current[0], float(current[1]),
                         (None if current[2] == 'None' else current[2]), float(current[3])])
          
    for thing in things:
          assert thing[2] in names or thing[2] == None
except IndexError:
    raise SyntaxError('Invalid file input length'
                      + ('. Try -a option to automaticly add insufficient values.' if not  args.auto_complete else '') +
                      f' Error in line:\n{line}')
except (TypeError, ValueError):
    raise SyntaxError(f'Invalid file input. Error in line:\n{line}')
def generate_sequence():
      sequence = {name: [] for name in names}

      for thing in things:
            name = random.choice(names)
            sequence[name].append(thing)
      return sequence

def personal_pain(things, person):
      
      pain = sum(thing[3] for thing in things if thing[2] != person)
            
      sum_mass = sum([thing[1] for thing in things])
      good_mass, endurance = people[person]
      #if sum_mass > good_mass:
      #      pain += endurance*(sum_mass - good_mass)**2
      pain += args.pain_multiply * endurance**(sum_mass/good_mass - 1)
      return pain

def count_pain(seq):
      pain = 0
      for person in seq:
            pain += personal_pain(seq[person], person)
      return pain

def rand_move():
      sequence_ = copy.deepcopy(sequence)
      
      from_p, to_p = random.sample(names, 2)

      from_things = sequence_[from_p]
      
      if not len(from_things):
            return rand_move()
            
      
      #print(len(from_things))
      
      thing = from_things.pop(random.randrange(len(from_things)))
      sequence_[to_p].append(thing)
      return sequence_

def optimized_rand_move(seq, extra_energy):
      from_p, to_p = random.sample(names, 2)
      things_from, things_to = seq[from_p], seq[to_p]
      
      if not len(things_from):
            return
      
      start_energy = (personal_pain(things_from, from_p) +
                      personal_pain(things_to, to_p))

      thing_from = random.randrange(len(things_from))
      
      if random.random() < 0.5 and len(things_to):
            # swap
            thing_to = random.randrange(len(things_to))
            things_from[thing_from], things_to[thing_to] = (things_to[thing_to],
                                                            things_from[thing_from])
            def reverse():
                  things_from[thing_from], things_to[thing_to] = (things_to[thing_to],
                                                            things_from[thing_from])
      else:
            # move
            thing = things_from.pop(thing_from)
            things_to.append(thing)
            
            def reverse():
                  things_from.append(things_to.pop())
                  
      final_energy = (personal_pain(things_from, from_p) +
                      personal_pain(things_to, to_p))

      if final_energy + extra_energy > start_energy:
            reverse()
      
def printer():
      s = ''
      for person in sequence:
            things = sequence[person]
            sum_mass = sum([thing[1] for thing in things])
            s1 = '{:<15}'.format(person)
            s2 = '{:<80}'.format(', '.join(sorted([thing[0] for thing in things])))
            s3 = f' {round(sum_mass, 5)}/{people[person][0]}'
            
            s += s1 + ':' + s2 + s3 + '\n'
      return s

all_text = ''
if not args.print_own:
      for attempt in range(args.epoch_number):
            sequence = generate_sequence()
            if not args.disable_progress_info:
                  print(f'Epoch {attempt + 1}/{args.epoch_number}')
                  
            for i in range(args.iteration_number):
                  T = args.start_temperature*10**(-i/args.gradient)
                  optimized_rand_move(sequence, T*random.random())
##                  new_seq = rand_move()
##                  
##                  if count_pain(new_seq) - count_pain(sequence) < T*random.random():
##                        sequence = new_seq
                        
                  if not i%1000:
                        if args.print_log:
                              print(round(count_pain(sequence), 2), round(T, 3))
                        elif not args.disable_progress_info:
                              print_progress_bar(i, args.iteration_number, prefix = 'Progress:',
                                                 suffix = 'Complete')

            print_progress_bar(args.iteration_number, args.iteration_number, prefix = 'Progress:',
                                                 suffix = 'Complete')
            text = (f'\nAttempt {attempt + 1}. Total pain: {count_pain(sequence)}. Full info:\n'
                    + printer())
            
            if args.output_file:
                  all_text += text
            else:
                  print(text)
            
else:
      sequence = {name: [] for name in names}
      for thing in things:
            name = thing[2]
            if name is None:
                  continue
            sequence[name].append(thing)
      print(printer())

if args.output_file:
      open(args.output_file, 'w', encoding = 'utf-8').write(all_text)
