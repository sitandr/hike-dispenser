import data_classes
import os
from tools import *
import help_parser

INF = float('inf')

def get_person_by_name(people, name):
      try:
            return next((p for p in people if p.name == name))

      except StopIteration:
            raise AttributeError(f'No such owner: {name}')

def default_optimize_values(args):
            return {args.v_name_default: data_classes.Value(args.v_name_default)}

def read_data(args):
      '''
      Opens and parses files specified in args object;
      Adds config to args properties 
      '''
      
      if args.people_and_things_file is not None:
          # "classic", simple way
          people, things, to_optimize_values = read_simple(args)

      elif args.yaml_file is not None:
           people, things, to_optimize_values = read_yaml(args)
      else:
           raise AttributeError('No input data provided')

      # now check whether is correct

      names = [p.name for p in people]
      u_names = set(names)

      if len(u_names) < len(names):
            for n in u_names:
                  names.remove(n)

            raise AttributeError('Names are not unic:' + ', '.join(names))

      if args.auto_scale:
            for v in to_optimize_values:
                  things_mass = sum((t.values[v] for t in things))
                  people_mass = sum((p.values_optimal[v] for p in people))

                  k = things_mass/people_mass

                  for p in people:
                        p.values_optimal[v] *= k
      
      return people, things, to_optimize_values

def person_from_dict(data, name, args, to_optimize_values):
      p = data_classes.Person()
      
      p.name = name
      if 'inacs' in data: p.inaccessability = data['inacs']
      
      for v in to_optimize_values:

         p.values_optimal[v] = (data[v]['opt']
                                if (v in data and 'opt' in data[v]) else
                                args.opt_default)
         
         p.values_sensitivity[v] = (data[v]['sens']
                                    if (v in data and 'sens' in data[v]) else
                                    args.sens_default)
         p.fixed_values[v] = 0
      return p

def thing_from_dict(data, name, args, people, to_optimize_values):
      t = data_classes.Thing()

      t.name = name
      if 'owr' in data:
         t.owner = get_person_by_name(people, data['owr'])
      
      if 'mrl' in data:
         t.moral = data['mrl']
         if t.moral == INF:
               t.fixed = t.owner

      if 'fixed' in data:                
         t.fixed = get_person_by_name(people, data['fixed']) if data['fixed'] is not True else t.owner
      

      t.values = {v: data[v] if v in data else 0 for v in to_optimize_values}
      return t

def read_yaml(args):
     if not(os.path.isfile(args.yaml_file)):
            raise AttributeError('Invalid file path')
     import yaml
     
     data = yaml.load(open(args.yaml_file, encoding = 'utf-8'), Loader = UniqueKeyLoader)

     if 'config' in data:
          for attribute in data['config']:
               if help_parser.is_default(args, attribute): # command (args) has more priority
                    setattr(args, attribute, data['config'][attribute])
               
     data_classes.Value.pain = args.pain_multiply
     data_classes.Person.inaccessibility = args.inaccessability_default


     if 'optimize' in data:
          to_optimize_values = {}
          for v_name in data['optimize']:
               
               v = data_classes.Value(v_name)
               if 'pain' in data['optimize'][v_name]: v.pain = data['optimize'][v_name]['pain']

               to_optimize_values[v_name] = v
     else:
          to_optimize_values[v_name] = default_optimize_values(args)

     people = []
     for person_name in data['people']:
          try:
                people.append(person_from_dict(data['people'][person_name], person_name,
                                               args, to_optimize_values))
          except Exception as e:
                raise AttributeError(str(e) + f'\nParsing error at "{person_name}" data: \n'
                                           + str(data['people'][person_name]))

     things = []
     for thing_name in data['things']:
          try:
                things.append(thing_from_dict(data['things'][thing_name], thing_name, args, people, to_optimize_values))
          except Exception as e:
                raise AttributeError(str(e) + f'\n\nParsing error at "{thing_name}" data:\n'
                                           + str(data['things'][thing_name]))

     return people, things, to_optimize_values

def person_from_list(plist, args):
      p = data_classes.Person()
      p.name = plist[0]
      p.values_optimal     = {args.v_name_default: float(plist[1])}
      p.values_sensitivity = {args.v_name_default: float(plist[2])}
      p.fixed_values[args.v_name_default] = 0
      return p

def thing_from_list(tlist, people, args):
      t = data_classes.Thing()
      t.name   = tlist[0]
      t.values = {args.v_name_default: float(tlist[1])}
      t.owner  = (None if tlist[2] == 'None' else
                    get_person_by_name(people, tlist[2]))

      t.moral  = float(tlist[3])
      t.fixed = None
      return t

def split_strip_comment(line):
      line = line.strip()
      if not len(line) or line[0] == '#':
            return
      return line.split()

def read_simple(args):
      
      people_file, things_file = args.people_and_things_file
      if not(os.path.isfile(people_file) and os.path.isfile(things_file)):
            raise AttributeError('Invalid file path')

      try:
        people = []

        data_classes.Value.pain = args.pain_multiply
        to_optimize_values = default_optimize_values(args)
        
        for line in open(people_file, encoding = 'utf-8'):
              current = split_strip_comment(line)
              if not current: continue
              if args.auto_complete: current[1:] = auto_complete(current[1:], [10, 10])
              
              people.append(person_from_list(current, args))
              

        things = []
        for line in open(things_file, encoding = 'utf-8'):
              current = split_strip_comment(line)
              if not current: continue
              if args.auto_complete: current[1:] = auto_complete(current[1:], [1.0, None, 0.0])

              things.append(thing_from_list(current, people, args))

              
              
      except IndexError:
        raise SyntaxError('Invalid file input length'
                          + ('. Try -a option to automaticly add insufficient values.' if not  args.auto_complete else '') +
                          f' Error in line:\n{line}')

      except (TypeError, ValueError):
        raise SyntaxError(f'Invalid file input. Error in line:\n{line}')
      
      return people, things, to_optimize_values
