import random


names = None
things = None
to_optimize_values = None
people = None
enable_inacs = False

def generate_transfer_from_seqence(seq):
     # very slow
     all_transfer = {(n1, n2): [] for n1 in names for n2 in names}
     # what FIRST GIVES (and second takes)
     for to in seq:
          for thing in seq[to]:
               if thing.owner is not None and thing.owner != to:
                    all_transfer[thing.owner, to].append(thing) # owner GIVES
                    
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

def transfer_move(transfer, thing, from_, to_):
      if thing.owner is None: return 0
      add_energy = 0

      if thing.owner != from_:
            transfer[thing.owner, from_].remove(thing)
       
            if not (transfer[thing.owner, from_] or transfer[from_, thing.owner]): # removed all, transfer is deleted -> good
                 add_energy -= people[from_].inaccessibility + people[thing.owner].inaccessibility
                 
      if thing.owner != to_:
            
            if not (transfer[thing.owner, to_] or transfer[to_, thing.owner]): # before addition was empty; transfer created -> bad
                 add_energy += people[to_].inaccessibility    + people[thing.owner].inaccessibility
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
