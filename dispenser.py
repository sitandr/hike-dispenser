import random
import os, sys

import yaml

from help import parse
from tools import *



          

args = parse()

if hasattr(args, "people_and_things_file"):
    # "classic" way
    
    try: # catch errors of file reading
        people_file, things_file = args.people_and_things_file
        assert os.path.isfile(people_file) and os.path.isfile(things_file)
        people = {}
        for line in open(people_file, encoding = 'utf-8'):
              if not len(line) or line[0] == '#':
                  continue
              current = line.strip().split()
              if not len(current):
                    continue
              if args.auto_complete: current[1:] = auto_complete(current[1:], [10, 10])
              people[current[0]] = float(current[1]), float(current[2])
              
        names = list(people.keys())

        things = []
        for line in open(things_file, encoding = 'utf-8'):
            
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

    except AssertionError:
        raise SyntaxError(f'Owner of thing ({thing}) does not exist.')

elif hasattr(args, "yaml_file"):
     ...
     
else:
     raise AttributeError('No input data provided')

def generate_sequence():
      sequence = {name: [] for name in names}

      for thing in things:
            name = random.choice(names)
            sequence[name].append(thing)
      return sequence

def personal_pain(things, person):

      # special function is needed to optimize calculating pain from random move
      pain = sum(thing[3] for thing in things if thing[2] != person)
            
      sum_mass = sum([thing[1] for thing in things])
      good_mass, endurance = people[person]
      pain += args.pain_multiply * endurance**(sum_mass/good_mass - 1)
      return pain

def count_pain(seq):
    
      # needed only for output; optimizing this is senselessly
      pain = 0
      for person in seq:
            pain += personal_pain(seq[person], person)
      return pain


def optimized_rand_move(seq, extra_energy):
    
      from_p, to_p = random.sample(names, 2)
      things_from, things_to = seq[from_p], seq[to_p]
      
      if not len(things_from):
            # interrupt if person we want to take from hasn't things at all
            return

      # to count energy difference should be known only the energy that changes
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
                        
                  if not i%args.update_freq:
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
      # print just owners
      sequence = {name: [] for name in names}
      
      for thing in things:
            name = thing[2]
            if name is None:
                  continue
            sequence[name].append(thing)
      
      if args.output_file:
          all_text += printer()
      else:
          print(printer())

if args.output_file:
      open(args.output_file, 'w', encoding = 'utf-8').write(all_text)
