import random

class Sequence:

    def __init__(self, seq, people, things, optimize_values):
        """
        seq: {person: [thing]}
        people: list of Person
        things: list of Thing
        optimize_values: list of Value
        """

        self.seq = seq
        self.people = people
        self.things = things
        self.optimize_values = optimize_values

    @staticmethod
    def create_owner_only(people, things, optimize_values):
        "create sequence with only owners' things"
        seq = {p: [] for p in people}

        for thing in things:
            name = thing.owner
            if name is None:
                continue

            seq[name].append(thing)

        return Sequence(seq, people, things, optimize_values)
    
    @staticmethod
    def create_random(names):
        
        seq = {name: [] for name in names}

        for thing in things:
            name = random.choice(names)
            s.seq[name].append(thing)

        s = Sequense(seq)
        return sequence


    def generate_transfer(self):
        seq = self.seq
        "slow function that generates {(from, to): thing}"
        
        all_transfer = {(n1, n2): [] for n1 in names for n2 in names}
        
        # what FIRST GIVES (and second takes)
        for to in seq:
            for thing in seq[to]:
                if thing.owner is not None and thing.owner != to:
                    all_transfer[thing.owner, to].append(thing) # owner GIVES
                    
        return all_transfer

    def count_pain(self):
        "sums all p's pain"

        # needed only for output; optimizing this is senselessly
        pain = 0
        for p in people:
            pain += p.personal_pain(self.seq[p.name])

        return pain
