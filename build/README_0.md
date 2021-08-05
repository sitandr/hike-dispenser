# Automatic hike dispenser

This little program is created to help with planning a group hiking trip. One of the problems is distribution of cargo, such as tents, axes, pots, food, guitars e.t.c. The problem becomes more complicated due to need of transfer if cargo isn't carried by it's owner, various cargo capacities (by mass) and weight sensitivity of different people. This command line tool provides ready (although non-ideal) solution out of box. It uses annealing and… that's all.

## Usage

As required input it takes files with people description and things. Both files should contain text with line = one person/thing. Empty lines or comments (start with «#») are possible.

`python dispenser.py [OPTIONS] <people file> <things file>`

### Options

The full list:
