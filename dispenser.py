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

enable_inacs = any([people[p].inaccessibility for p in people]) # inaccessibility, slightly decreases speed, so should be tracked

names = list(people.keys())

try:
     for thing in things:
              assert thing.owner in names or thing.owner == None
              
except AssertionError:
     raise SyntaxError(f'Owner of thing ({thing}) does not exist.')



def generate_transfer_from_seqence(seq):
     # very slow
     all_transfer = {(n1, n2): [[],[]] for n1 in names for n2 in names if n1 < n2}
     # first is what FIRST GIVES (and second takes), second — what second gives
     for to in seq:
          for thing in seq[to]:
               if thing.owner is not None and thing.owner != to:
                    if thing.owner < to:
                         all_transfer[thing.owner, to][0].append(thing) # owner GIVES
                    else:
                         all_transfer[to, thing.owner][1].append(thing) # to TAKES
     return all_transfer

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

def tuple_sort(a, b):
     return (a, b) if a<=b else (b,a)

def transfer_move(thing, from_, to_):
      if thing.owner is None: return 0
      add_energy = 0

      if thing.owner != from_:
            print(transfer, thing, tuple_sort(thing.owner, from_))
            transfer[tuple_sort(thing.owner, from_)].remove(thing) # TODO: owner = from ?
       
            if not any(transfer[tuple_sort(thing.owner, from_p)]): # removed all, transfer is deleted -> good
                 add_energy -= from_p.inaccessibility + thing.owner.inaccessibility
                 
      if thing.owner != to_:
            
            if not any(transfer[tuple_sort(thing.owner, to_)]): # before addition was empty; transfer created -> bad
                 add_energy += to_.inaccessibility    + thing.owner.inaccessibility
            # weight decrease?
            transfer[tuple_sort(thing.owner, to_)].append(thing)
      return add_energy
                 
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
      
      add_energy = 0
      
      if random.random() < 0.5 and len(things_to):
            # swap
            thing_to = random.randrange(len(things_to))
            if enable_inacs:
                  add_energy += transfer_move(things_from[thing_from], from_p, to_p)
                  add_energy += transfer_move(things_to[thing_to], to_p, from_p)
            things_from[thing_from], things_to[thing_to] = (things_to[thing_to],
                                                            things_from[thing_from])
            
            def reverse():
                  things_from[thing_from], things_to[thing_to] = (things_to[thing_to],
                                                            things_from[thing_from])
                  if enable_inacs:
                       transfer_move(things_from[thing_from], to_p, from_p)
                       transfer_move(things_to[thing_to], from_p, to_p)
      else:
            # move
            thing = things_from.pop(thing_from)
            things_to.append(thing)
            if enable_inacs: add_energy += transfer_move(thing, from_p, to_p)
                 
            def reverse():
                  if enable_inacs: transfer_move(thing, to_p, from_p)
                  things_from.append(things_to.pop())
                  
      final_energy = (personal_pain(things_from, from_p) +
                      personal_pain(things_to, to_p))

      if final_energy + extra_energy + add_energy > start_energy:
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
            transfer = generate_transfer_from_seqence(sequence)
            
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

            if not args.disable_progress_info and not args.print_log:
                 print_progress_bar(args.iteration_number, args.iteration_number)
                 
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
