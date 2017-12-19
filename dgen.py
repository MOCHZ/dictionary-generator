#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
import argparse
import itertools

__author__ = "Zorko"
__copyright__ = "Copyright 2017, Zorko"
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Zorko"
__email__ = "contact@zorko.co"


class CharacterSets(object):
    alpha = []
    numbers = []
    symbols = []
    limits = []
    all_chars = []

    def __init__(self, alpha, numbers, symbols, limits):
        self.alpha = alpha
        self.numbers = numbers
        self.symbols = symbols
        self.limits = limits
        self.all_chars = alpha + numbers + symbols


def main():
    # Arguments
    parser = argparse.ArgumentParser(description='')

    # String arguments
    parser.add_argument('-f', '--file', default="word_list.txt", type=str, help="Output filename")

    # Integer arguments
    parser.add_argument('-min', '--min_length', default=1, type=int, help="Minimum word length, default is 1")
    parser.add_argument('-max', '--max_length', default=16, type=int, help="Maximum word length, default is 16")
    
    # Boolean arguments
    parser.add_argument('-a', '--alpha_only', default=False, action="store_true",
                        help="Letters only, can be combined with -As or --add_symbols for non-english letters." +
                        "To enforce a specific case add -L or -U respectively")

    parser.add_argument('-n', '--numeric_only', default=False, action="store_true",
                        help="Numbers 0-9 only")

    parser.add_argument('-L', '--lowercase_only', default=False, action="store_true",
                        help="Use only lowercase letters")

    parser.add_argument('-U', '--uppercase_only', default=False, action="store_true",
                        help="Use only uppercase letters")

    parser.add_argument('-S', '--allow_space', default=False, action="store_true",
                        help="Allow the use of space")

    parser.add_argument('-As', '--add_symbols', default=False, action="store_true",
                        help="Add special symbols such as @#$+ and non-english characters")

    parser.add_argument('-Au', '--add_uppercase', default=False, action="store_true",
                        help="Add uppercase letters")

    parser.add_argument('-Al', '--add_lowercase', default=False, action="store_true",
                        help="Add lowercase letters")

    parser.add_argument('-An', '--add_numbers', default=False, action="store_true",
                        help="Add numbers")

    arguments = validate_arguments(parser.parse_args())

    dictionary = build_dictionary(arguments)
    print(dictionary)

    return


def validate_arguments(arguments):
    error_msg = 'Check your input: %s'

    # Min length cannot be greater than the max length, that is just logic.
    if arguments.min_length > arguments.max_length:
        sys.exit(error_msg % 'min_length cannot be greater than max_length')

    if arguments.max_length < 1 or arguments.min_length < 1:
        sys.exit(error_msg % 'min_length and max_length must be greater than 0')

    # Forcing upper and lower case at the same time is prohibited!
    if arguments.lowercase_only and arguments.uppercase_only:
        sys.exit(error_msg % 'lowercase_only and uppercase_only cannot be selected at the same time')

    if arguments.add_lowercase and arguments.uppercase_only:
        sys.exit(error_msg % 'add_lowercase and uppercase_only cannot be selected at the same time')

    if arguments.add_uppercase and arguments.uppercase_only:
        sys.exit(error_msg % 'add_uppercase and uppercase_only cannot be selected at the same time')

    if arguments.add_uppercase and arguments.lowercase_only:
        sys.exit(error_msg % 'add_uppercase and lowercase_only cannot be selected at the same time')

    if arguments.add_lowercase and arguments.lowercase_only:
        sys.exit(error_msg % 'add_lowercase and lowercase_only cannot be selected at the same time')

    if arguments.add_numbers and arguments.lowercase_only:
        sys.exit(error_msg % 'add_numbers and lowercase_only cannot be selected at the same time')

    if arguments.add_numbers and arguments.uppercase_only:
        sys.exit(error_msg % 'add_numbers and uppercase_only cannot be selected at the same time')

    # Numeric only removes the possibility to use case sensitivity and any other characters,
    # with the only exception of space and special characters.
    if arguments.alpha_only and arguments.numeric_only:
        sys.exit(error_msg % 'alpha_only and numeric_only cannot be selected at the same time')

    if arguments.add_symbols and arguments.numeric_only:
        sys.exit(error_msg % 'add_symbols and numeric_only cannot be selected at the same time')

    if arguments.add_numbers and arguments.numeric_only:
        sys.exit(error_msg % 'add_numbers and numeric_only cannot be selected at the same time')

    if arguments.add_lowercase and arguments.numeric_only:
        sys.exit(error_msg % 'add_lowercase and numeric_only cannot be selected at the same time')

    if arguments.add_uppercase and arguments.numeric_only:
        sys.exit(error_msg % 'add_uppercase and numeric_only cannot be selected at the same time')

    if (arguments.numeric_only and arguments.lowercase_only) or (arguments.numeric_only and arguments.uppercase_only):
        sys.exit(error_msg % 'unable to enforce specific case with only numeric values')

    return arguments


def list_to_chr(int_list):
    return [chr(i) for i in int_list]


def build_dictionary(arguments):
    the_characters = get_symbols(arguments)
    count = 0

    if os.path.isfile(arguments.file):
        sys.exit('%s already exists' % arguments.file)

    try:
        file = open(arguments.file, 'w')
        line_count = 0

        for i in list(range(arguments.min_length, arguments.max_length + 1)):
            tmp_list = itertools.permutations(''.join(the_characters.all_chars), i)

            for tmp_item in tmp_list:
                count += 1
                line_count += 1
                if count == 1000000:
                    time.sleep(2)
                    count = 0
                new_line = ''.join(tmp_item) + "\n"
                file.writelines(new_line)

    except IOError:
        file.close()
        sys.exit('There was an issue with creating the dictionary!')
    finally:
        file.close()
        print('Dictionary was written to %s' % arguments.file)
        print('%s passwords added' % line_count)

    return arguments.file


def get_symbols(arguments):
    # Characters to add into the list
    alpha = {
        "lower": list_to_chr(list(range(97, 123))),
        "upper": list_to_chr(list(range(65, 91)))
    }

    # Numbers; 0-9
    numbers = list_to_chr(list(range(48, 58)))

    # Special characters
    symbols = {
        "symbols": list_to_chr(list(range(33, 48)) + list(range(58, 65)) + list(range(91, 97)) + list(range(123, 255))),
        "space": hex(32)
    }

    # Password length
    string_length = {min: arguments.min_length, max: arguments.max_length}

    # Selected character groups
    selected_characters = []
    selected_numbers = []
    selected_symbols = []

    # Add characters before returning an Object
    if not arguments.alpha_only or arguments.numeric_only:
        selected_numbers.extend(numbers)

    if not arguments.numeric_only:
        if not arguments.uppercase_only and (arguments.lowercase_only or arguments.add_lowercase):
            selected_characters.extend(alpha["lower"])

        if not arguments.lowercase_only and (arguments.uppercase_only or arguments.add_uppercase):
            selected_characters.extend(alpha["upper"])

        if arguments.add_symbols:
            selected_symbols.extend(symbols["symbols"])

    if arguments.allow_space:
        selected_symbols.append(symbols["space"])

    char_set = CharacterSets(selected_characters, selected_numbers, selected_symbols, string_length)

    return char_set


if __name__ == '__main__':
    main()
