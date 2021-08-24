# Automatic hike dispenser

This little program is created to help with planning a group hiking trip. One of the problems is distribution of cargo, such as tents, axes, pots, food, guitars e.t.c. The problem becomes more complicated due to need of transfer if cargo isn't carried by it's owner, various cargo capacities (by mass) and weight sensitivity of different people. This command line tool provides ready (although non-ideal) solution out of box. It uses annealing and... that's all.

## Theory

The value that is optimized is "pain". To count it, the program assumes that it is exponentially over weight increasing. That helps to strictly limit overload on some persons.

## Usage

### Plain text 

First, it can be a plain text file. In this case it is impossible to use major part of features, such as multi-parametric optimizing, file config e.t.c. However, it is much simpler and quicker to create. In addition, this way doesn't need pyYaml lib. As required input it takes two files with people and things description. Both files should contain text with line = one person/thing. Empty lines or comments (start with «\#») are possible. Here is the example of usage:

1. **People** file:

   ```
   # first column is person name, then optimal value, then sensitivity 
   # (number of times this person pain increases when optimal weight added)
   
   Alice	 5   15
   Bob   	 7   10
   Superman 100 20
   
   # 		(kg)
   ```

2. **Things** file:

   ```
   # first column is thing name, then it's value (weight or smth like this),
   # then it's owner and moral pain if it is carried by someone else 
   # (for ex. Alice don't want to leave guitar)
   
   Spaghetti   1   None	 0
   Rice		2	Bob    	 0
   Guitar 	 	5   Alice  	 7
   Tent		5   Alice  	 1
   Supweapon  50	Superman 50
   
   #		  (kg)
   ```

3. Command:

`python dispenser.py -t <people file> <things file> [OPTIONS]`

### YAML

`YAML` is a human-friendly data format with lots of features that could be used as input for this program. Usage of YAML allows using anchors, inheritance, infinities e.t.c. Full syntax description: [Wiki](https://en.wikipedia.org/wiki/YAML#Syntax), [Official spec](http://yaml.org/spec/1.2/spec.html). This input format will be further developed, whereas plain text cannot support more features (cost is too high). Currently, root chapters are (this order is recommended, but not necessary):

1. **Config** (optional)

   ​	There you can specify any command line options that will be used by default. However, it can be still overridden by directly command line.

   `config: <option name>: <option value>`

2.  **Optimize** (optional)

   ​	Specifies parameters that should be optimized (*global values*). It must be dictionary with keys that are names of optimized and values (also dicts) that specify it characteristics. If not specified, **v** (value) only is used at default parameters. Currently available:

   1. **Pain** (multiply) specially for this parameter, default is 10 (look at `pain_multiply` in *Options*). Can be used to set priorities of pain.

   `optimize: <global value name>: <parameter name>: <parameter value>`

3. **Variables** (optional)

   ​	This chapter hasn't any function by itself. However, it **can** be used to set YAML anchors without any risk of undesirable effects.

   `variables: - &<var name>: <var value>`

4. **People** (required)

   ​	Replacement for *people* file. Names are keys, values are *global variables* or special parameters. For each *global value* **must** be specified `opt` (optimal value) and `sens` (sensitivity).

   `people: <name>: {<global variable>: {opt: <optimal global value>, sens: <sensitivity>}, {<special parameters name>: <special parameter value>}}`

5. **Things** (required)

   ​	Replacement for *values* file. Thing names are keys, for each *global value* **can** be specified this thing value, default is *0*. Also can be specified `owr` (owner of this thing, if no, **None** is used). And `mrl` (moral pain gained when is carried by someone else).

   `things: <thing name>: {<global variable>: <value>, [owr: <owner name>, mrl: <moral pain>]}`

Example of full file:

```yaml
config:
  iteration_number: 200_000 # too easy
  update_freq:	      3_000 # don't need much log

optimize:
  mass: {}
  size: {pain: 3} # less priority

people:
  Alice:
    mass: {opt: 5,  sens: 15} # small weight
    size: {opt: 10, sens: 10} # but large backpack
    
  Bob:
    mass: {opt: 7,  sens: 10} # more strength
    size: {opt: 7,  sens: 20} # but less backpack size
    
  Superman:
    mass: {opt: 100, sens: 20} # superweight
    size: {opt:  20, sens: 30} # but not so big backpack

things:
  Spaghetti: # don't belong to anybody
    mass: 1
    size: 1
    
  Rice:
    mass: 2
    size: 1
    own: Bob
    mrl: 0
    
  Guitar: # don't take place in backpack, size = 0, default
    mass: 5
    own: Alice
    mrl: 7
    
  Tent:
    mass: 5
    size: 5
    own: Alice
    mrl: 1
    
  Supweapon:
    mass: 50
    size: 15
    own: Superman
    mrl: 50
```

Command:

`python dispenser.py -y <yaml file> [OPTIONS]`

## Options

The full list:

```

  -h, --help            show this help message and exit
  -t PEOPLE_AND_THINGS_FILE PEOPLE_AND_THINGS_FILE, --people_and_things_files PEOPLE_AND_THINGS_FILE PEOPLE_AND_THINGS_FILE
                        Input files with people and thing data, used with
                        things file instead of yaml
  -y YAML_FILE, --yaml_file YAML_FILE
                        Input file with all data in yaml
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Output file; if not specified, stdout is used
  -w, --print_own       Print just current owners; useful for an overview
  -l, --print_log       Print total pain and temperature instead of progress
                        bars
  -a, --auto_complete   Allows not full completed text data files; people are
                        auto-completed with 10 optimal_weight and 10
                        sensevity; things have 1 kg mass and don't belong to
                        anybody.
  -d, --disable_progress_info
                        No progress info
  -e EPOCH_NUMBER, --epoch_number EPOCH_NUMBER
                        Default number of general attempts; default is 3
  -i ITERATION_NUMBER, --iteration_number ITERATION_NUMBER
                        Default number of iteration in each attempt; if not
                        specified, equals to 300_000
  -g GRADIENT, --gradient GRADIENT
                        Number of iterations it takes to decrease temperature
                        in 10 times; default is 100_000
  -T START_TEMPERATURE, --start_temperature START_TEMPERATURE
                        Start temperature; default is 50 (pains)
  -u UPDATE_FREQ, --update_freq UPDATE_FREQ
                        Number of iterations between updating bar/log; default
                        is 1_000
  --pain_multiply PAIN_MULTIPLY
                        Default pain (at optimal weight); default is 10
  --opt_default OPT_DEFAULT
                        Default optimal value; default is 10
  --sens_default SENS_DEFAULT
                        Default optimal value; default is 10

```

Using examples from `tests/` :

 `python dispenser.py -t tests/p.txt tests/t.txt [OPTIONS]`

Or, using `YAML`:

`python dispenser.py -y tests/multi_test.yaml [OPTIONS]`



