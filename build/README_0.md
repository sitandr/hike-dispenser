# Automatic hike dispenser

This little program is created to help with planning a group hiking trip. One of the problems is distribution of cargo, such as tents, axes, pots, food, guitars e.t.c. The problem becomes more complicated due to need of transfer if cargo isn't carried by it's owner, various cargo capacities (by mass) and weight sensitivity of different people. This command line tool provides ready (although non-ideal) solution out of box. It uses annealing and… that's all.

## Usage

As required input it takes YAML file with people description and things. Usage of YAML allows using anchors, inheritance, infinities e.t.c. Full syntax description: [Wiki](https://en.wikipedia.org/wiki/YAML#Syntax), [Official spec](http://yaml.org/spec/1.2/spec.html#id2803362).

`python dispenser.py [OPTIONS] <yaml file>`

### Options

The full list:
