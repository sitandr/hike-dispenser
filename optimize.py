import random

def transfer_move(transfer, thing, from_, to_):
      if thing.owner is None: return 0
      add_energy = 0

      if thing.owner != from_:
            transfer[thing.owner, from_].remove(thing)
       
            if not (transfer[thing.owner, from_] or transfer[from_, thing.owner]):
                 # removed all, transfer is deleted -> good

                 add_energy -= from_.inaccessibility + thing.owner.inaccessibility
                 
      if thing.owner != to_:
            
            if not (transfer[thing.owner, to_] or transfer[to_, thing.owner]):
                 # before this addition was empty; transfer created -> bad

                 add_energy += to_.inaccessibility + thing.owner.inaccessibility

            transfer[thing.owner, to_].append(thing)

      return add_energy
                 
def optimized_rand_move(transfer, sequence, extra_energy):
    
      from_p, to_p = random.sample(sequence.seq.keys(), 2)
      things_from, things_to = sequence.seq[from_p], sequence.seq[to_p]

      if not len(things_from):
            # interrupt if person we want to take from hasn't things at all
            return

      # to count energy difference should be known only the energy that changes
      start_energy = (from_p.personal_pain(things_from, sequence.to_optimize_values) +
                      to_p.personal_pain(things_to, sequence.to_optimize_values))

      thing_from_index = random.randrange(len(things_from))
      thing_from = things_from[thing_from_index]
      
      add_energy = 0
      
      if random.random() < 0.5 and len(things_to):
            # swap
            thing_to_index = random.randrange(len(things_to))
            thing_to = things_from[thing_from_index]

            if sequence.enable_inacs:
                  add_energy += transfer_move(transfer, thing_from, from_p, to_p)
                  add_energy += transfer_move(transfer, thing_to, to_p, from_p)

            things_from[thing_from_index], things_to[thing_to_index] = (thing_to, thing_from)
            
            def reverse():
                  things_from[thing_from], things_to[thing_to] = (thing_from, thing_to)

                  if sequence.enable_inacs:
                       transfer_move(transfer, thing_from, to_p, from_p)
                       transfer_move(transfer, thing_to,     from_p, to_p)
      else:
            # move
            thing = things_from.pop(thing_from)
            things_to.append(thing)
            if sequence.enable_inacs: add_energy += transfer_move(transfer, thing, from_p, to_p)
                 
            def reverse():
                  if sequence.enable_inacs: transfer_move(transfer, thing, to_p, from_p)
                  things_from.append(things_to.pop())
                  
      final_energy = (from_p.personal_pain(things_from, sequence.to_optimize_values) +
                      to_p.personal_pain(things_to, sequence.to_optimize_values))

      if final_energy + extra_energy + add_energy > start_energy:
            reverse()
