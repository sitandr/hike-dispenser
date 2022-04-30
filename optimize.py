import random

def transfer_move(transfer, thing, from_, to_):
      if thing.owner is None: return 0
      add_energy = 0

      if thing.owner != from_: # from_ got from owner
            transfer[thing.owner, from_].remove(thing)
       
            if not (transfer[thing.owner, from_] or transfer[from_, thing.owner]):
                 # removed all, from_-owner transfer is deleted -> good

                 add_energy -= from_.inaccessibility + thing.owner.inaccessibility
                 
      if thing.owner != to_: # gives not to owner
            
            if not (transfer[thing.owner, to_] or transfer[to_, thing.owner]):
                 # before this addition was empty; transfer created -> bad

                 add_energy += to_.inaccessibility + thing.owner.inaccessibility

            transfer[thing.owner, to_].append(thing)

      return add_energy
                 
def optimized_rand_move(transfer, sequence, pain_map, extra_energy):
    
      from_p, to_p = random.sample(sequence.seq.keys(), 2)
      things_from, things_to = sequence.seq[from_p], sequence.seq[to_p]

      if not len(things_from):
            # interrupt if person we want to take from hasn't things at all
            return

      # to count energy difference should be known only the energy that changes
      e_f = pain_map[from_p]
      e_t = pain_map[to_p]

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

      pain_map[from_p] = from_p.personal_pain(things_from, sequence.optimize_values)
      pain_map[to_p] = to_p.personal_pain(things_to, sequence.optimize_values)
                  
      final_energy = pain_map[from_p] + pain_map[to_p]

      if final_energy + extra_energy + add_energy > start_energy:
            reverse()
            pain_map[from_p] = e_f
            pain_map[to_p] = e_t

