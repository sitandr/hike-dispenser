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
   
   #		   (kg)
   ```

3. Command:

`python dispenser.py [OPTIONS] -t <people file> <things file>`

### YAML

`YAML` is a user-friendly data format  

### Options

The full list:

```
place_where_should_be_help_inserted
```

Using examples from `tests/` :

 `python dispenser.py -t tests/p.txt tests/t.txt`

Or, using `YAML`:

`python dispenser.py -y tests/multi_test.yaml`

### Theory

The value that is optimized is "pain". To count it, the program assumes
that it is exponentially over weight increasing. That helps to strictly
limit extra weights.
