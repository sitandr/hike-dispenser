import data_classes
import os
from tools import *
import help_parser

def read_data(args):
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
              people = {}
              
              data_classes.Value.pain = args.pain_multiply
              to_optimize_values = default_optimize_values()
              
              for line in open(people_file, encoding = 'utf-8'):
                    if not len(line) or line[0] == '#':
                        continue
                     
                    current = line.strip().split()
                    if not len(current):
                          continue
                     
                    if args.auto_complete: current[1:] = auto_complete(current[1:], [10, 10])
                    people[current[0]] = data_classes.Person()
                    people[current[0]].name = current[0]
                    people[current[0]].values_optimal     = {args.v_name_default: float(current[1])}
                    people[current[0]].values_sensitivity = {args.v_name_default: float(current[2])}
                    

              things = []
              for line in open(things_file, encoding = 'utf-8'):
                  
                    if not len(line) or line[0] == '#':
                        continue
                      
                    current = line.strip().split()
                    
                    if not len(current):
                          continue
                    
                    if args.auto_complete: current[1:] = auto_complete(current[1:], [1.0, None, 0.0])
                    things.append(data_classes.Thing())
                    
                    things[-1].name   = current[0]
                    things[-1].values = {args.v_name_default: float(current[1])}
                    things[-1].owner  = (None if current[2] == 'None' else current[2])
                    things[-1].moral  = float(current[3])

                    
                    
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
           people = {}

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

           for person_name in data['people']:
                
                people[person_name] = data_classes.Person()
                people[person_name].name = person_name
                
                if 'inacs' in data['people'][person_name]:
                     people[person_name].inaccessability = data['people'][person_name]['inacs']
                     
                for v in to_optimize_values:
                     current_p = data['people'][person_name]
                                         
                     people[person_name].values_optimal[v] = (current_p[v]['opt']
                                                              if (v in current_p and 'opt' in current_p[v]) else
                                                              args.opt_default)
                     
                     people[person_name].values_sensitivity[v] = (current_p[v]['sens']
                                                                  if (v in current_p and 'sens' in current_p[v]) else
                                                                   args.sens_default)
                
           things = []
           for thing_name in data['things']:
                things.append(data_classes.Thing())
                things[-1].name = thing_name
                d_thing = data['things'][thing_name]
                
                if 'owr' in d_thing:
                     things[-1].owner = d_thing['owr']
                     things[-1].moral = d_thing['mrl']
                things[-1].values = {v: d_thing[v] if v in d_thing else 0 for v in to_optimize_values}
      else:
           raise AttributeError('No input data provided')

      return people, things, to_optimize_values
