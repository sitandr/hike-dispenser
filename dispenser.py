import random

import help_parser
import data_reader

from tools import print_progress_bar, better_round
from optimize import optimized_rand_move
from sequence import Sequence

args = help_parser.parse()  # parse all given flags


def print_meet(seq):
    gen_transfer = seq.generate_full_transfer()  # regenerate because may not be supported
    s = ""

    for p in seq.people:
        s += p.name + " :\n"

        for to_p in seq.people:
            if to_p == p:
                continue

            if gen_transfer[p, to_p]:
                s += (
                    f"\t-> {to_p.name}: "
                    + " ".join([t.name for t in gen_transfer[p, to_p]])
                    + "\n"
                )

            if gen_transfer[to_p, p]:
                s += (
                    f"\t{to_p.name} ->: "
                    + " ".join([t.name for t in gen_transfer[to_p, p]])
                    + "\n"
                )
    return s


def print_haul(seq):
    s = ""
    fs = seq.full_seq()

    for p in seq.people:
        things = fs[p]

        s1 = "{:<15}".format(p.name)
        s2 = "{:<80}".format(", ".join(sorted([thing.name for thing in things])))
        s3 = "\n "

        for value_name in seq.optimize_values:
            sum_mass = sum([thing.values[value_name] for thing in things])

            if value_name != args.v_name_default:
                s3 += value_name

            s3 += f" {better_round(sum_mass, 3)}/{better_round(p.values_optimal[value_name], 2)} "

        s += s1 + ": " + s2 + s3 + "\n" + "—" * 20 + "\n"
    return s


# create "out" func that would work as file/print output
all_text = ""
if args.output_file:

    def out(t):
        global all_text
        all_text += t

else:
    out = print

if not args.print_own:
    for attempt in range(args.epoch_number):
        people, things, optimize_values = data_reader.read_data(args)
        sequence = Sequence.create_random(people, things, optimize_values)

        transfer = (
            sequence.generate_transfer()
        )  # IMPORTANT: transfer is updated only if inacs enabled
        pain_map = sequence.generate_pain_map()
        pain = sequence.count_pain()

        for i in range(args.iteration_number + args.finalize):
            T = (
                args.start_temperature * 10 ** (-i / args.gradient)
                if i < args.iteration_number
                else 0
            )
            pain += optimized_rand_move(
                T * random.random(), transfer, sequence, pain_map
            )

            if not i % args.update_freq:

                if args.print_log:
                    print(round(sequence.count_pain(), 2), round(T, 3))

                elif not args.disable_progress_info:
                    print_progress_bar(
                        i,
                        args.iteration_number + args.finalize,
                        prefix=f"Attempt {attempt + 1}. Progress:",
                        suffix=f"Complete. Pain: {pain:.2f}",
                    )

        if not args.disable_progress_info and not args.print_log:
            print_progress_bar(args.iteration_number, args.iteration_number)

        text = (
            f"\nAttempt {attempt + 1}. Total pain: {sequence.count_pain()}. Full info:\n"
            + print_haul(sequence)
        )

        if args.meeting_print:
            text += "\n" + print_meet(sequence)

        out(text)

else:
    people, things, optimize_values = data_reader.read_data(args)

    # print just owners
    seq = Sequence.create_owner_only(people, things, optimize_values)
    out(print_haul(seq))
    text = f"\n Total pain: {seq.count_pain()}\n"
    if args.meeting_print:
        text += "\n" + print_meet(seq)

    out(text)

if args.output_file:
    with open(args.output_file, "w", encoding="utf-8") as f:
        f.write(all_text)
