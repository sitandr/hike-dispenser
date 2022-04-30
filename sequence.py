import random
import itertools

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

        # inaccessibility, slightly decreases speed, so should be tracked
        self.enable_inacs = any([p.inaccessibility for p in people])

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
    def create_random(people, things, to_optimize_values):
        
        seq = {p: [] for p in people}

        for thing in things:
            p = random.choice(people)
            seq[p].append(thing)

        s = Sequence(seq, people, things, to_optimize_values)
        return s


    def generate_transfer(self):
        seq = self.seq
        "slow function that generates {(from, to): thing}"
        
        transfer = {(p1, p2): [] for p1 in self.people for p2 in self.people}
        
        # what FIRST GIVES (and second takes)
        for to in seq:
            for thing in seq[to]:
                if thing.owner is not None and thing.owner != to:
                    transfer[thing.owner, to].append(thing) # owner GIVES

        return transfer

    def generate_pain_map(self):
        return {p: p.personal_pain(self.seq[p], self.optimize_values)
                    for p in self.people}

    def count_pain(self):
        "sums all pain"

        # needed only for output; optimizing this is senselessly
        pain = 0
        for p in self.people:
            pain += p.personal_pain(self.seq[p], self.optimize_values)

        if self.enable_inacs:
            p_meet = list(itertools.chain(*self.generate_transfer().keys(),
                                       *self.generate_transfer().keys()))

            for p in p_meet:
                pain += p.inaccessibility

        return pain
