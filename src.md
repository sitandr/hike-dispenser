# Automatic hike dispenser

This little program is created to help with planning a group hiking trip. One of the problems is distribution of cargo, such as tents, axes, pots, food, guitars e.t.c. The problem becomes more complicated due to need of transfer if cargo isn't carried by it's owner, various cargo capacities (by mass) and weight sensitivity of different people. This command line tool provides ready (although non-ideal) solution out of box. It uses annealing and... that's all.

## Usage

### Plain text 

First, it can be a plain text file. In this case it is impossible to use major part of features, such as multi-parametric optimizing, file config e.t.c. However, it is much simpler and quicker to create. In addition, this way doesn't need pyYaml lib. As required input it takes two files with people and things description. Both files should contain text with line = one person/thing. Empty lines or comments (start with «\#») are possible. Here is the example of usage:

1. **People** file:

   ```
   # first column is person name, then optimal value, then sensitivity 
   # (number of times this person pain increases when optimal weight added)
   
   Alice	 5   15
   Bob   	 7   10
   Superman 100 3
   
   # 		(kg)
   ```

2. **Things** file:

   ```
   # first column is thing name, then it's value (weight or smth like this),
   # then it's owner and moral pain if it is carried by someone else 
   # (for ex. Alice don't want to leave guitar)
   
   Rice		2	Bob    	 0
   Guitar 	 	5   Alice  	 7
   Tent		5   Alice  	 1
   Supweapon  50	Superman 50
   
   #		  (kg)
   ```

3. Command:

`python dispenser.py [OPTIONS] -t <people file> <things file>`

### YAML

`YAML` is a human-friendly data format with lots of features that could be used as input for this program. Usage of YAML allows using anchors, inheritance, infinities e.t.c. Full syntax description: [Wiki](https://en.wikipedia.org/wiki/YAML#Syntax), [Official spec](http://yaml.org/spec/1.2/spec.html). This input format will be further developed, whereas plain text cannot support more features (cost is too high). Currently, root chapters are (this order is recommended, but not necessary):

1. **Config** (optional)

   ​	There you can specify any command line options that will be used by default. However, it can be still overridden by directly command line.

   `config: <option name>: <option value>`

2.  **Optimize** (optional)

   ​	Specifies parameters that should be optimized (*global values*). It must be dictionary with keys that are names of optimized and values (also dicts) that specify it characteristics. Currently available:

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
 
```



## Options

The full list:

```
place_where_should_be_help_inserted
```

Using examples from `tests/` :

 `python dispenser.py -t tests/p.txt tests/t.txt`

Or, using `YAML`:

`python dispenser.py -y tests/multi_test.yaml`

## Theory

The value that is optimized is "pain". To count it, the program assumes
that it is exponentially over weight increasing. That helps to strictly
limit extra weights.
