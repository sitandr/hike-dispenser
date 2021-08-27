import random

import help_parser
import data_reader

from tools import print_progress_bar
import time

import optimize
from optimize import optimized_rand_move, generate_sequence, generate_transfer_from_seqence


args = help_parser.parse() # parse all given flags
people, things, to_optimize_values = data_reader.read_data(args)

enable_inacs = any([people[p].inaccessibility for p in people])
# inaccessibility, slightly decreases speed, so should be tracked

names = list(people.keys())

try:
     for thing in things:
              assert thing.owner in names or thing.owner == None
              
except AssertionError:
     raise SyntaxError(f'Owner of thing ({thing}) does not exist.')

def print_meet(seq):
     s = ''

     for person_name in seq:
          s += person_name + ' :\n'

          for to_p in seq:
               if to_p >= person_name:
                    continue
               
               if transfer[person_name, to_p]:
                    s += f'\t-> {to_p} ' + ' '.join([t.name for t in transfer[person_name, to_p]]) + '\n'
               
               if transfer[to_p, person_name]:
                    s += f'\t {to_p}->' + ' '.join([t.name for t in transfer[to_p, person_name]]) + '\n'
     return s

def print_haul(seq):
      s = ''
      for person_name in seq:
            things = seq[person_name]
            
            s1 = '{:<15}'.format(person_name)
            s2 = '{:<80}'.format(', '.join(sorted([thing.name for thing in things])))
            s3 = ' '
            
            for value_name in to_optimize_values:
                 sum_mass = sum([thing.values[value_name] for thing in things])
                 if value_name != args.v_name_default:
                      s3 += value_name
                 s3 += f' {round(sum_mass, 5)}/{people[person_name].values_optimal[value_name]} '
            
            s += s1 + ':' + s2 + s3 + '\n'
      return s


            

# create "out" func that would work as file/print output
if args.output_file:
     all_text = ''
     def out(t): global all_text; all_text += t
else:
     out = print

optimize.names = names
optimize.people = people
optimize.things = things
optimize.to_optimize_values = to_optimize_values
optimize.enable_inacs = enable_inacs

if not args.print_own:
      for attempt in range(args.epoch_number):
          
            sequence = generate_sequence()
            transfer = generate_transfer_from_seqence(sequence)
            
            if not args.disable_progress_info:
                  print(f'Epoch {attempt + 1}/{args.epoch_number}')
                  
            for i in range(args.iteration_number):
                  T = args.start_temperature*10**(-i/args.gradient)
                  optimized_rand_move(transfer, sequence, T*random.random())
                        
                  if not i%args.update_freq:
                        if args.print_log:
                              print(round(count_pain(sequence), 2), round(T, 3))
                              
                        elif not args.disable_progress_info:
                              print_progress_bar(i, args.iteration_number, prefix = 'Progress:',
                                                 suffix = 'Complete')

            if not args.disable_progress_info and not args.print_log:
                 print_progress_bar(args.iteration_number, args.iteration_number)
                 
            text = (f'\nAttempt {attempt + 1}. Total pain: {optimize.count_pain(sequence)}. Full info:\n'
                    + print_haul(sequence))

            if args.meeting_print:
                 text += '\n' + print_meet(sequence)
            
            out(text)
            
else:
      # print just owners

      start_sequence = {name: [] for name in names}

      for thing in things:
          name = thing.owner
          if name is None:
               continue
          start_sequence[name].append(thing)
      
      out(print_haul(start_sequence))

if args.output_file:
      open(args.output_file, 'w', encoding = 'utf-8').write(all_text)
