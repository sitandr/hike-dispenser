import argparse

parser = argparse.ArgumentParser(
    description="This program dispenses things to people (mininmizing total pain) \
      using annealing. As input it takes file with people descriptions (for each in each line there is name, \
      optimal_weight and weight_sensevity (number of times pain increases when mass increased by optimal_mass)\
      in this order, separated by spaces/tabs) and things descriptions \
      (similarly, in each line there is name, weight, owner and number of pain he gains from giving it to anybody else \
      in this order separated by spaces/tabs). Default values are designed to <10 people and <50 things, so if your \
      values are larger, it's recommended to change the default values. This means increasing number of iterations \
      to get better result. If you do so, it's also recommended to increase gradient proportionally. However, the situation \
      may be different, so it's best to modify according to circumstances."
)

parser.add_argument(
    "-t",
    "--people_and_things_files",
    dest="people_and_things_file",
    nargs=2,
    type=str,
    help="Input files with people and thing data,\
                    used with things file instead of yaml",
)

parser.add_argument(
    "-y",
    "--yaml_file",
    dest="yaml_file",
    type=str,
    help="Input file with all data in yaml",
)

parser.add_argument(
    "-o",
    "--output_file",
    dest="output_file",
    default=None,
    help="Output file; if not specified, stdout is used",
)

parser.add_argument(
    "-w",
    "--print_own",
    dest="print_own",
    action="store_true",
    help="Print just current owners; useful for an overview",
)

parser.add_argument(
    "-m",
    "--meeting_print",
    dest="meeting_print",
    action="store_true",
    help="Print all transfer ways",
)

parser.add_argument(
    "-i",
    "--inaccessability_default",
    dest="inaccessability_default",
    type=float,
    default=0,
    help="Default inaccessability; default is 0; adding any inaccessability decreases speed at ~20%%",
)

parser.add_argument(
    "-s",
    "--auto_scale",
    dest="auto_scale",
    action="store_true",
    help="Scale weight to match total weight",
)

parser.add_argument(
    "-l",
    "--print_log",
    dest="print_log",
    action="store_true",
    help="Print total pain and temperature instead of progress bars",
)

parser.add_argument(
    "-d",
    "--disable_progress_info",
    dest="disable_progress_info",
    action="store_true",
    help="No progress info",
)

parser.add_argument(
    "-u",
    "--update_freq",
    dest="update_freq",
    type=int,
    default=2_000,
    help="Number of iterations between updating bar/log; default is 1_000",
)

parser.add_argument(
    "-a",
    "--auto_complete",
    dest="auto_complete",
    action="store_true",
    help="Allows not full completed TEXT data files; people are auto-completed with 10 optimal_weight \
                            and 10 sensevity; things have 1 kg mass and don't belong to anybody.",
)

parser.add_argument(
    "-E",
    "--epoch_number",
    dest="epoch_number",
    type=int,
    default=3,
    help="Default number of general attempts; default is 3",
)

parser.add_argument(
    "-I",
    "--iteration_number",
    dest="iteration_number",
    type=int,
    default=300_000,
    help="Default number of steps (iterations) in each attempt; if not specified, equals to 300_000",
)

parser.add_argument(
    "-G",
    "--gradient",
    dest="gradient",
    type=float,
    default=100_000,
    help="Number of steps it takes to decrease temperature in 10 times; default is 100_000",
)

parser.add_argument(
    "-T",
    "--start_temperature",
    dest="start_temperature",
    type=float,
    default=50,
    help="Start temperature; default is 50 (pains)",
)

parser.add_argument(
    "-F",
    "--finalize",
    dest="finalize",
    type=int,
    default=50_000,
    help="Number of steps without temperature to settle the result, default is 50_000.\
                          Not included into iteration_number",
)

parser.add_argument(
    "--pain_multiply",
    dest="pain_multiply",
    type=float,
    default=10,
    help="Default pain (at optimal weight); default is 10",
)

parser.add_argument(
    "--opt_default",
    dest="opt_default",
    type=float,
    default=10,
    help="Default optimal value; default is 10",
)

parser.add_argument(
    "--sens_default",
    dest="sens_default",
    type=float,
    default=10,
    help="Default optimal value; default is 10",
)

parser.add_argument(
    "--v_name_default",
    dest="v_name_default",
    type=str,
    default="v",
    help="Default value name; default is «v»",
)

parser.add_argument(
    "--moral_default",
    dest="moral_default",
    type=float,
    default=0.1,
    help="Default moral cost; default is 0.1",
)


def parse():
    # parse part
    return parser.parse_args()


def is_default(args, attribute):
    return getattr(args, attribute) == parser.get_default(attribute)
