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


        self.set_fixed()
        
        # inaccessibility, slightly decreases speed, so should be tracked
        self.enable_inacs = any([p.inaccessibility or len(p.special) for p in people])

    def set_fixed(self):
        "remove fixed things from seq and add to fixed"

        self.fixed = {p: [] for p in self.people}
        for thing in self.things:
            p = thing.fixed
            if p is None:
                continue

            for p2 in self.people:
                if thing in self.seq[p2]:
                    self.seq[p2].remove(thing)
                    break
            
            self.fixed[p].append(thing)

            for v in self.optimize_values:
                p.fixed_values[v] += thing.values[v]

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
    def create_fixed_only(people, things, optimize_values):
        "create sequence with only fixed things"
        seq = {p: [] for p in people}

        for thing in things:
            name = thing.fixed
            if name is None:
                continue

            seq[name].append(thing)

        return Sequence(seq, people, things, optimize_values)
    
    @staticmethod
    def create_random(people, things, to_optimize_values, start_with_owner=True):
        
        seq = {p: [] for p in people}

        for thing in things:
            if start_with_owner and thing.owner != None:
                p = thing.owner
            else:
                p = random.choice(people)

            seq[p].append(thing)

        s = Sequence(seq, people, things, to_optimize_values)
        return s


    def generate_transfer(self):
        from data_classes import Person, Thing
        seq = self.seq
        "slow function that generates {(from, to): thing}"
        
        transfer: dict[tuple[Person, Person], list[Thing]] = {(p1, p2): [] for p1 in self.people for p2 in self.people}

        # what FIRST GIVES (and second takes)
        for to in seq:
            for thing in seq[to]:
                if thing.owner is not None and thing.owner != to:
                    transfer[thing.owner, to].append(thing) # owner GIVES

        return transfer

    def generate_pain_map(self):
        return [p.personal_pain(self.seq[p], self.optimize_values)
                    for p in self.people]

    def full_seq(self):
        'return seq united with fix; very slow — copies seq'
        full = {p: self.seq[p].copy() for p in self.seq}

        for p in self.fixed:
            full[p].extend(self.fixed[p])

        return full

    def generate_full_transfer(self):
        "slow function that generates {(from, to): thing} from full seq"
        seq = self.full_seq()
        
        transfer = {(p1, p2): [] for p1 in self.people for p2 in self.people}
        
        # what FIRST GIVES (and second takes)
        for to in seq:
            for thing in seq[to]:
                if thing.owner is not None and thing.owner != to:
                    transfer[thing.owner, to].append(thing) # owner GIVES

        return transfer

    def count_pain(self):
        "sums all pain"
        from optimize import transfer_cost

        # needed only for output; optimizing this is senselessly
        pain = 0
        for p in self.people:
            pain += p.personal_pain(self.seq[p], self.optimize_values)

        if self.enable_inacs:
            meetings = (sorted(pair, key=lambda p: p.name) for (pair, data) in self.generate_transfer().items() if len(data) > 0)
            for m in meetings:
                pain += transfer_cost(m[0], m[1])

        return pain
    
