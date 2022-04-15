import sys
from textwrap import dedent


class CLIOption:
    def __init__(self, options, help_text, setter, args_needed=1):
        self.options = options
        self.help = help_text
        self.setter = setter
        self.args_needed = args_needed


class SettingsError(Exception):
    def __init__(self, msg="Wrong arguments!"):
        self.msg = msg


class Settings:
    def __init__(self):
        self._generations = 10
        self._population = 20
        self._to_next_generation = 0.1
        self._fit_to_crossover = 0.3
        self._mutation_probability = 0.02
        self._filepath = None
        self._outputpath = None

    @property
    def generations(self):
        return self._generations

    @property
    def population(self):
        return self._population

    @property
    def to_next_generation(self):
        return self._to_next_generation

    @property
    def fit_to_crossover(self):
        return self._fit_to_crossover

    @property
    def mutation_probability(self):
        return self._mutation_probability

    @property
    def filepath(self):
        return self._filepath

    @property
    def outputpath(self):
        return self._outputpath

    def get_from_cli_args(self):
        possible_options = self.get_possible_options()
        possible_options = {
            option: cli_option
            for cli_option in possible_options
            for option in cli_option.options
        }
        args_left = 0
        cli_option = None
        collected_args = []
        args = sys.argv[1:]
        for arg in args:
            if args_left <= 0:
                if cli_option is not None:
                    cli_option.setter(collected_args)
                eqarg = arg.split('=')
                cli_option = possible_options.get(eqarg[0])
                if cli_option is None:
                    self.set_filepath(arg)
                else:
                    args_left = cli_option.args_needed
                    collected_args.clear()
                    if len(eqarg) > 1:
                        collected_args.extend(eqarg[1:])
                        args_left -= len(eqarg) - 1
            else:
                args_left -= 1
                collected_args.append(arg)
        if cli_option is not None:
            cli_option.setter(collected_args)
        if len(args) == 0:
            self.print_help()
            sys.exit(0)
        elif self._filepath is None:
            raise SettingsError("Missing dataset file path!")

    def get_possible_options(self):
        return [
            CLIOption(
                ['-h', '--help'],
                "Shows help",
                (lambda args:
                    (lambda x: sys.exit(0))(self.print_help())
                 ),
                0
            ),
            CLIOption(
                ['-g', '--generations'],
                "Set amount of generations to create, 10 by default",
                self.set_generations
            ),
            CLIOption(
                ['-p', '--population'],
                "Set each generation population size, 20 by default",
                self.set_population
            ),
            CLIOption(
                ['-n', '--nextgen'],
                "Set amount of individuals that go into next generation, 0.1 by default",
                self.set_to_next_generation
            ),
            CLIOption(
                ['-c', '--crossover'],
                "Set amount of individuals that can crossover to create new generation",
                self.set_fit_to_crossover
            ),
            CLIOption(
                ['-m', '--mutation'],
                "Set probability of mutation of individual, 0.02 by default",
                self.set_mutation_probability
            ),
            CLIOption(
                ['-o', '--output'],
                "Save output to file",
                self.set_outputpath
            )
        ]

    def set_generations(self, args):
        self._generations = int(args[0])

    def set_population(self, args):
        self._population = int(args[0])

    def set_to_next_generation(self, args):
        self._to_next_generation = float(args[0])

    def set_fit_to_crossover(self, args):
        self._fit_to_crossover = float(args[0])

    def set_mutation_probability(self, args):
        self._mutation_probability = float(args[0])

    def set_filepath(self, path):
        self._filepath = self.set_path(
            self._filepath, path, 'Only one dataset')

    def set_outputpath(self, args):
        self._outputpath = self.set_path(
            self._outputpath, args[0], 'At most one output file'
        )

    def set_path(self, current_path, path, filename):
        if current_path is not None:
            raise SettingsError(dedent(
                """\
                    {} is possible in this program!
                    Or you don't know possible options, use -h or --help to see options\
                """.format(filename)
            ))
        return path

    def print_help(self):
        options = self.get_possible_options()
        help_text = dedent("""\
            Travelling salesman problem solver using genetic algorithm

            Usage: python main.py [options] <dataset>
        """)
        for option in options:
            help_text += ' '.join(option.options) + ' -> ' + option.help + '\n'
        help_text += dedent("""
            dataset format:
                JSON file that's array of objects.
                each point/city needs name and x/y coords.
                eg. [
                    {"name":"A", "x":1, "y":1},
                    {"name":"B", "x":2, "y":2}
                ]\
        """)
        print(help_text)


if __name__ == '__main__':
    try:
        x = Settings()
        x.get_from_cli_args()
        print(x.__dict__)
    except SettingsError as e:
        print(e.msg, file=sys.__stderr__)
