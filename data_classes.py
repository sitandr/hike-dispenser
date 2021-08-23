class Value:
      name = '<undefined value name>'
      pain = None
      
      def __init__(self, name):
            self.name = name
      def __repr__(self):
            return name
      
class Person:
      name = '<undefined person name>'
      values_optimal = {}
      values_sensitivity = {}

      def __repr__(self):
            return ((self.name) + ' optimal '.join([v + ': ' + str(self.values_optimal[v])
                              for v in self.values_optimal])
                  + ' sens '.join([v + ': ' + str(self.values_sensitivity[v])
                              for v in self.values_sensitivity]))

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
