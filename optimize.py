import random
from tools import weighted_random
import math

def transfer_cost(from_, to):
      if to.name in from_.special:
            return from_.special[to.name]
      if from_.name in to.special:
            return to.special[from_.name]

      return from_.inaccessibility + to.inaccessibility

def transfer_move(transfer, thing, from_, to_):
      if thing.owner is None: return 0
      add_energy = 0
      
      if thing.owner == from_:
            add_energy += thing.moral
      elif thing.owner == to_:
            add_energy -= thing.moral

      if thing.owner != from_: # got not from owner
            transfer[thing.owner, from_].remove(thing)

            if not (transfer[thing.owner, from_] or transfer[from_, thing.owner]):
                 # removed all, from_-owner transfer is deleted -> good

                 add_energy -= transfer_cost(from_, thing.owner)

      if thing.owner != to_: # gives not to owner

            if not (transfer[thing.owner, to_] or transfer[to_, thing.owner]):
                 # before this addition was empty; transfer created -> bad

                 add_energy += transfer_cost(to_, thing.owner)

            transfer[thing.owner, to_].append(thing)

      return add_energy
                 
def optimized_rand_move(extra_energy, transfer, sequence, pain_map) -> float:
      from_p_i = weighted_random(pain_map)
      to_p_i = weighted_random((math.log(i+1) + 1 for i in pain_map))

      if from_p_i == to_p_i:
            return 0
      
      from_p, to_p = sequence.people[from_p_i], sequence.people[to_p_i]
      things_from, things_to = sequence.seq[from_p], sequence.seq[to_p]

      if not len(things_from):
            # interrupt if person we want to take from hasn't things at all
            return 0

      # to count energy difference should be known only the energy that changes
      e_f = pain_map[from_p_i]
      e_t = pain_map[to_p_i]

      start_energy = e_f + e_t 

      thing_from_index = random.randrange(len(things_from))
      thing_from = things_from[thing_from_index]
      
      add_energy = 0
      
      if random.random() < 0.5 and len(things_to):
            # swap
            thing_to_index = random.randrange(len(things_to))
            thing_to = things_to[thing_to_index]

            if sequence.enable_inacs:
                  add_energy += transfer_move(transfer, thing_from, from_p, to_p)
                  add_energy += transfer_move(transfer, thing_to, to_p, from_p)

            things_from[thing_from_index], things_to[thing_to_index] = (thing_to, thing_from)
            
            def reverse():
                  things_from[thing_from_index], things_to[thing_to_index] = (thing_from, thing_to)

                  if sequence.enable_inacs:
                       transfer_move(transfer, thing_from, to_p, from_p)
                       transfer_move(transfer, thing_to, from_p, to_p)
      else:
            # move
            thing = things_from.pop(thing_from_index)
            things_to.append(thing)
            if sequence.enable_inacs: add_energy += transfer_move(transfer, thing, from_p, to_p)

            def reverse():
                  if sequence.enable_inacs: transfer_move(transfer, thing, to_p, from_p)
                  things_from.append(things_to.pop())

      pain_map[from_p_i] = from_p.personal_pain(things_from, sequence.optimize_values)
      pain_map[to_p_i] = to_p.personal_pain(things_to, sequence.optimize_values)

      final_energy = pain_map[from_p_i] + pain_map[to_p_i]

      if final_energy + add_energy > start_energy + extra_energy:
            reverse()
            pain_map[from_p_i] = e_f
            pain_map[to_p_i] = e_t
            return 0

      return (final_energy + add_energy) - start_energy

