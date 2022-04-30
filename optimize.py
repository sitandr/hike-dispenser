import random


names = None
things = None
to_optimize_values = None
people = None
enable_inacs = False


def transfer_move(transfer, thing, from_, to_):
      if thing.owner is None: return 0
      add_energy = 0

      if thing.owner != from_:
            transfer[thing.owner, from_].remove(thing)
       
            if not (transfer[thing.owner, from_] or transfer[from_, thing.owner]):
                 # removed all, transfer is deleted -> good

                 add_energy -= people[from_].inaccessibility + people[thing.owner].inaccessibility
                 
      if thing.owner != to_:
            
            if not (transfer[thing.owner, to_] or transfer[to_, thing.owner]):
                 # before this addition was empty; transfer created -> bad

                 add_energy += people[to_].inaccessibility + people[thing.owner].inaccessibility

            transfer[thing.owner, to_].append(thing)

      return add_energy
                 
def optimized_rand_move(transfer, seq, extra_energy):
    
      from_p, to_p = random.sample(seq.keys(), 2)
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
                  add_energy += transfer_move(transfer, things_from[thing_from], from_p, to_p)
                  add_energy += transfer_move(transfer, things_to[thing_to], to_p, from_p)
            things_from[thing_from], things_to[thing_to] = (things_to[thing_to],
                                                            things_from[thing_from])
            
            def reverse():
                  things_from[thing_from], things_to[thing_to] = (things_to[thing_to],
                                                            things_from[thing_from])
                  if enable_inacs:
                       transfer_move(transfer, things_from[thing_from], to_p, from_p)
                       transfer_move(transfer, things_to[thing_to],     from_p, to_p)
      else:
            # move
            thing = things_from.pop(thing_from)
            things_to.append(thing)
            if enable_inacs: add_energy += transfer_move(transfer, thing, from_p, to_p)
                 
            def reverse():
                  if enable_inacs: transfer_move(transfer, thing, to_p, from_p)
                  things_from.append(things_to.pop())
                  
      final_energy = (personal_pain(things_from, from_p) +
                      personal_pain(things_to, to_p))

      if final_energy + extra_energy + add_energy > start_energy:
            reverse()
