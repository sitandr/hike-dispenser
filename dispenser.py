import random

import help_parser
import data_reader

from tools import print_progress_bar, better_round
from optimize import optimized_rand_move
from sequence import Sequence



args = help_parser.parse() # parse all given flags
people, things, optimize_values = data_reader.read_data(args)


def print_meet(transfer):
     s = ''

     for p in people:
         s += p.name + ' :\n'

         for to_p in people:
            if to_p == p:
                continue
            
            if transfer[p, to_p]:
                s += f'\t-> {to_p.name}: ' + ' '.join([t.name for t in transfer[p, to_p]]) + '\n'
            
            if transfer[to_p, p]:
                s += f'\t{to_p.name} ->: ' + ' '.join([t.name for t in transfer[to_p, p]]) + '\n'
     return s

def print_haul(seq):
     s = ''
     for p in seq.seq: # let's iterate over seq instead people; seq could not contain certain person
         things = seq.seq[p]
         
         s1 = '{:<15}'.format(p.name)
         s2 = '{:<80}'.format(', '.join(sorted([thing.name for thing in things])))
         s3 = ' '
         
         for value_name in optimize_values:
              sum_mass = sum([thing.values[value_name] for thing in things])
              if value_name != args.v_name_default:
                 s3 += value_name
              s3 += f' {better_round(sum_mass, 3)}/{better_round(p.values_optimal[value_name], 2)} '
         
         s += s1 + ':' + s2 + s3 + '\n'
     return s


         

# create "out" func that would work as file/print output
if args.output_file:
     all_text = ''
     def out(t): global all_text; all_text += t
else:
     out = print

if not args.print_own:
     for attempt in range(args.epoch_number):
         
         sequence = Sequence.create_random(people, things, optimize_values)
         transfer = sequence.generate_transfer() # IMPORTANT: transfer is updated only if inacs enabled
         pain_map = sequence.generate_pain_map()
         
         if not args.disable_progress_info:
             print(f'Epoch {attempt + 1}/{args.epoch_number}')
             
         for i in range(args.iteration_number):
             T = args.start_temperature*10**(-i/args.gradient)
             optimized_rand_move(T*random.random(), transfer, sequence, pain_map)
                 
             if not i%args.update_freq:
                 
                 if args.print_log:
                     print(round(sequence.count_pain(), 2), round(T, 3))
                     
                 elif not args.disable_progress_info:
                     print_progress_bar(i, args.iteration_number, prefix = 'Progress:',
                                    suffix = 'Complete')
                 

         if not args.disable_progress_info and not args.print_log:
              print_progress_bar(args.iteration_number, args.iteration_number)
              
         text = (f'\nAttempt {attempt + 1}. Total pain: {sequence.count_pain()}. Full info:\n'
                + print_haul(sequence))

         if args.meeting_print:
              text += '\n' + print_meet(sequence.generate_transfer()) # regenerate because may not be supported
         
         out(text)
         
else:
     # print just owners
     out(print_haul(Sequence.create_owner_only(people, things, optimize_values)))

     

if args.output_file:
     open(args.output_file, 'w', encoding = 'utf-8').write(all_text)
