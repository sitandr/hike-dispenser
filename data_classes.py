to_optimize = []

class Person:
      name = '<undefined name>'
      values_optimal = {}
      values_sensitivity = {}

      def __repr__(self):
            return ((self.name) + ' optimal '.join([v + ': ' + str(self.values_optimal[v])
                              for v in self.values_optimal])
                  + ' sens '.join([v + ': ' + str(self.values_sensitivity[v])
                              for v in self.values_sensitivity]))

class Thing:
      name = '<undefined name>'
      values = {}
      owner = None
      moral = 0
      
      def __repr__(self):
            return (self.name + ' ' +
                    ' '.join([v + ': ' + str(self.values[v])
                              for v in self.values]) +
                    f' owned by {self.owner} with moral debuff {self.moral}')
