
class Value:
      name = '<undefined value name>'
      pain = None
      
      def __init__(self, name):
            self.name = name

      def __repr__(self):
            return self.name
      
class Person:
      name = '<undefined person name>'
      inaccessibility = 0
      
      def __init__(self):
            self.values_optimal = {}
            self.values_sensitivity = {}
      
      def __repr__(self):
            return ((self.name) + ' optimal ' + ' '.join([v + ': ' + str(self.values_optimal[v])
                              for v in self.values_optimal])
                  + ' sens ' + ' '.join([v + ': ' + str(self.values_sensitivity[v])
                              for v in self.values_sensitivity]))

      def personal_pain(self, personal_things, to_optimize_values):
            """
            function needed to optimize calculating pain from random move
            IMPORTANT: pass any THIS P'S THINGS (imp for optimizing because they don't match "staged") 
            """

            # for rand_move we can optimize, but it doesn't really hurts

            pain = sum(thing.moral for thing in personal_things if thing.owner != self.name)

            for value_name in to_optimize_values:
                 sum_mass = sum([thing.values[value_name] for thing in things])

                 optimal = self.values_optimal[value_name]
                 sens    = self.values_sensitivity[value_name]
                 pain += to_optimize_values[value_name].pain * sens ** (sum_mass/optimal - 1)

            return pain

class Thing:
      name = '<undefined thing name>'
      values = {}
      owner = None
      moral = 0
      
      def __repr__(self):
            return (self.name + ' ' +
                    ' '.join([v + ': ' + str(self.values[v])
                              for v in self.values]) +
                    f' owned by {self.owner} with moral debuff {self.moral}')



      
