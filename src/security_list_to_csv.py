#%%
import json
import jmespath
import argparse

import pandas         as pd

from termcolor        import cprint
from project_logger   import ProjectLogger


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help = "input filename", nargs=1, required=True)
    parser.add_argument("-o", "--output", help = "output filename", nargs=1, required=True)
    args = parser.parse_args()

    return args


def load_input_file(inputfile):
    with open(inputfile) as f:
        data = json.load(f)
    return data


def main(args):
    ProjectLogger.info('Starting main()')
    cprint("-" * 40, "green", attrs=["bold"])
    cprint("Security List to CSV", "green", attrs=["bold"])
    cprint("-" * 40, "green", attrs=["bold"])

    input_file = args.input[0]
    output_file = args.output[0]

    cprint("Input file: \t " + input_file, "green")
    cprint("Output file:\t " + output_file, "green")
    cprint("-" * 40, "green", attrs=["bold"])

    dData = load_input_file(input_file)
    ProjectLogger.dictionary_debug(dData, 'dData')
    print(f"{len(dData)=}")
    # print(dData)


if __name__ == "__main__":
    args = parse_arguments()

    main(args)
