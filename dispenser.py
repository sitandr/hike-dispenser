import random

import help_parser
from tools import *
import data_classes
import data_reader

default_value_name = 'v'

def default_optimize_values():
     return {default_value_name: data_classes.Value(default_value_name)}

args = help_parser.parse() # parse all given flags
people, things, to_optimize_values = data_reader.read_data(args)

enable_inacs = False # inaccessibility, slightly decreases speed, so should be tracked

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
                 if value_name != default_value_name:
                      s3 += value_name
                 s3 += f' {round(sum_mass, 5)}/{people[person_name].values_optimal[value_name]} '
            
            s += s1 + ':' + s2 + s3 + '\n'
      return s

# needed for meeting calculation

start_sequence = {name: [] for name in names}

for thing in things:
     name = thing.owner
     if name is None:
          continue
     start_sequence[name].append(thing)
            
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
      sequence = start_sequence
      
      if args.output_file:
          all_text += printer()
      else:
          print(printer())

if args.output_file:
      open(args.output_file, 'w', encoding = 'utf-8').write(all_text)
