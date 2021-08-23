import random
import os, sys

import yaml

from help import parse
from tools import *
import data_classes

args = parse() # parse all given flags

data_classes.Value.pain = args.pain_multiply
to_optimize_values = {}

if args.people_and_things_file != None:
    # "classic", simple way
    
    try: # catch errors of file reading
        people_file, things_file = args.people_and_things_file
        assert os.path.isfile(people_file) and os.path.isfile(things_file)
        
    except AssertionError:
        raise AttributeError('Invalid file')
     
    try:
        people = {}
        to_optimize_values = {'value': data_classes.Value('value')}
        for line in open(people_file, encoding = 'utf-8'):
              if not len(line) or line[0] == '#':
                  continue
               
              current = line.strip().split()
              if not len(current):
                    continue
               
              if args.auto_complete: current[1:] = auto_complete(current[1:], [10, 10])
              people[current[0]] = data_classes.Person()
              people[current[0]].name = current[0]
              people[current[0]].values_optimal     = {'value': float(current[1])}
              people[current[0]].values_sensitivity = {'value': float(current[2])}
              

        things = []
        for line in open(things_file, encoding = 'utf-8'):
            
              if not len(line) or line[0] == '#':
                  continue
                
              current = line.strip().split()
              
              if not len(current):
                    continue
              
              if args.auto_complete: current[1:] = auto_complete(current[1:], [1.0, None, 0.0])
              things.append(data_classes.Thing())
              
              things[-1].name   = current[0]
              things[-1].values = {'value': float(current[1])}
              things[-1].owner  = (None if current[2] == 'None' else current[2])
              things[-1].moral  = float(current[3])

              
              
    except IndexError:
        raise SyntaxError('Invalid file input length'
                          + ('. Try -a option to automaticly add insufficient values.' if not  args.auto_complete else '') +
                          f' Error in line:\n{line}')

    except (TypeError, ValueError):
        raise SyntaxError(f'Invalid file input. Error in line:\n{line}')



elif args.yaml_file != None:
     
     assert os.path.isfile(args.yaml_file)
     import yaml
     
     data = yaml.load(open(args.yaml_file, encoding = 'utf-8'), Loader = UniqueKeyLoader)
     people = {}
     
     for v_name in data['optimize'].keys():
          
          v = data_classes.Value(v_name)
          if 'pain' in data['optimize'][v_name]: v.pain = data['optimize'][v_name]['pain']

          to_optimize_values[v_name] = v

     for person_name in data['people']:
          
          people[person_name] = data_classes.Person()
          people[person_name].name = person_name
          
          for v in data['people'][person_name]:
               people[person_name].values_optimal[v] = data['people'][person_name][v]['opt']
               people[person_name].values_sensitivity[v] = data['people'][person_name][v]['sens']

     things = []
     for thing_name in data['things']:
          things.append(data_classes.Thing())
          things[-1].name = thing_name
          d_thing = data['things'][thing_name]
          
          if 'owr' in d_thing:
               things[-1].owner = d_thing['owr']
               things[-1].moral = d_thing['mrl']
          things[-1].values = {v: d_thing[v] if v in d_thing else 0 for v in to_optimize_values}
else:
     raise AttributeError('No input data provided')

names = list(people.keys())

try:
     for thing in things:
              assert thing.owner in names or thing.owner == None
except AssertionError:
     raise SyntaxError(f'Owner of thing ({thing}) does not exist.')

def generate_sequence():
      sequence = {name: [] for name in names}

      for thing in things:
            name = random.choice(names)
            sequence[name].append(thing)
      return sequence

def personal_pain(things, person_name):

      # special function is needed to optimize calculating pain from random move
      pain = sum(thing.moral for thing in things if thing.owner != person_name)

      for value_name in to_optimize_values:
           sum_mass = sum([thing.values[value_name] for thing in things])
           
           optimal = people[person_name].values_optimal[value_name]
           sens    = people[person_name].values_sensitivity[value_name]
           pain += to_optimize_values[value_name].pain * sens ** (sum_mass/optimal - 1)
           # TODO: pain_multiply <- file
      return pain

def count_pain(seq):
    
      # needed only for output; optimizing this is senselessly
      pain = 0
      for person_name in seq:
            pain += personal_pain(seq[person_name], person_name)
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
      for person_name in sequence:
            things = sequence[person_name]
            
            s1 = '{:<15}'.format(person_name)
            s2 = '{:<80}'.format(', '.join(sorted([thing.name for thing in things])))
            s3 = ' '
            
            for value_name in to_optimize_values:
                 sum_mass = sum([thing.values[value_name] for thing in things])
                 if value_name != 'value':
                      s3 += value_name
                 s3 += f' {round(sum_mass, 5)}/{people[person_name].values_optimal[value_name]} '
            
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
            name = thing.owner
            if name is None:
                  continue
            sequence[name].append(thing)
      
      if args.output_file:
          all_text += printer()
      else:
          print(printer())

if args.output_file:
      open(args.output_file, 'w', encoding = 'utf-8').write(all_text)
