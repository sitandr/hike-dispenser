import data_classes
import os
from tools import *
import help_parser

def get_person_by_name(people, name):
      try:
            return next((p for p in people if p.name == name))

      except StopIteration:
            raise AttributeError(f'No such owner: {name}')
      
def read_data(args):
      '''
      Opens and parses files specified in args object;
      Adds config to args properties 
      '''

      def default_optimize_values():
            return {args.v_name_default: data_classes.Value(args.v_name_default)}

      to_optimize_values = {}
      
      if args.people_and_things_file is not None:
          # "classic", simple way
          
          try: # catch errors of file reading
              people_file, things_file = args.people_and_things_file
              assert os.path.isfile(people_file) and os.path.isfile(things_file)
              
          except AssertionError:
              raise AttributeError('Invalid file')
           
          try:
              people = []

              data_classes.Value.pain = args.pain_multiply
              to_optimize_values = default_optimize_values()
              
              for line in open(people_file, encoding = 'utf-8'):
                    if not len(line) or line[0] == '#':
                        continue
                     
                    current = line.strip().split()
                    if not len(current):
                          continue
                     
                    if args.auto_complete: current[1:] = auto_complete(current[1:], [10, 10])
                    
                    p = data_classes.Person()
                    p.name = current[0]
                    p.values_optimal     = {args.v_name_default: float(current[1])}
                    p.values_sensitivity = {args.v_name_default: float(current[2])}

                    people.append(p)
                    

              things = []
              for line in open(things_file, encoding = 'utf-8'):
                  
                    if not len(line) or line[0] == '#':
                        continue
                      
                    current = line.strip().split()
                    
                    if not len(current):
                          continue
                    
                    if args.auto_complete: current[1:] = auto_complete(current[1:], [1.0, None, 0.0])

                    t = data_classes.Thing()
                    t.name   = current[0]
                    t.values = {args.v_name_default: float(current[1])}
                    t.owner  = (None if current[2] == 'None' else
                                      get_person_by_name(people, current[2]))

                    t.moral  = float(current[3])

                    things.append(t)

                    
                    
          except IndexError:
              raise SyntaxError('Invalid file input length'
                                + ('. Try -a option to automaticly add insufficient values.' if not  args.auto_complete else '') +
                                f' Error in line:\n{line}')

          except (TypeError, ValueError):
              raise SyntaxError(f'Invalid file input. Error in line:\n{line}')



      elif args.yaml_file is not None:
           
           assert os.path.isfile(args.yaml_file)
           import yaml
           
           data = yaml.load(open(args.yaml_file, encoding = 'utf-8'), Loader = UniqueKeyLoader)

           if 'config' in data:
                for attribute in data['config']:
                     if help_parser.is_default(args, attribute): # command (args) has more priority
                          setattr(args, attribute, data['config'][attribute])
                     
           data_classes.Value.pain = args.pain_multiply

           data_classes.Person.inaccessibility = args.inaccessability_default

           if 'optimize' in data:
                for v_name in data['optimize'].keys():
                     
                     v = data_classes.Value(v_name)
                     if 'pain' in data['optimize'][v_name]: v.pain = data['optimize'][v_name]['pain']

                     to_optimize_values[v_name] = v
           else:
                to_optimize_values[v_name] = default_optimize_values()

           people = []
           for person_name in data['people']:
                
                p = data_classes.Person()
                d_p = data['people'][person_name]
                
                p.name = person_name
                
                if 'inacs' in d_p:
                     p.inaccessability = d_p['inacs']
                     
                for v in to_optimize_values:

                     p.values_optimal[v] = (d_p[v]['opt']
                                            if (v in d_p and 'opt' in d_p[v]) else
                                            args.opt_default)
                     
                     p.values_sensitivity[v] = (d_p[v]['sens']
                                                if (v in d_p and 'sens' in d_p[v]) else
                                                args.sens_default)
                people.append(p)

           things = []
           for thing_name in data['things']:
                t = data_classes.Thing()

                t.name = thing_name
                d_thing = data['things'][thing_name]
                
                if 'owr' in d_thing:
                     t.owner = get_person_by_name(people, d_thing['owr'])
                     t.moral = d_thing['mrl']

                t.values = {v: d_thing[v] if v in d_thing else 0 for v in to_optimize_values}

                things.append(t)
      else:
           raise AttributeError('No input data provided')

      # now check whether is correct

      names = [p.name for p in people]
      u_names = set(names)

      if len(u_names) < len(names):
            for n in u_names:
                  names.remove(n)

            raise AttributeError('Names are not unic:' + ', '.join(names))
      
      return people, things, to_optimize_values
