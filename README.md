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
  --pain_multiply PAIN_MULTIPLY
                        Default pain (at optimal weight); default is 10
  -u UPDATE_FREQ, --update_freq UPDATE_FREQ
                        Number of iterations between updating bar/log; default
                        is 1_000

```

Using examples from `tests/` :

 `python dispenser.py -t tests/p.txt tests/t.txt`

Or, using `YAML`:

`python dispenser.py -y tests/multi_test.yaml`

### Theory

The value that is optimized is "pain". To count it, the program assumes
that it is exponentially over weight increasing. That helps to strictly
limit extra weights.
