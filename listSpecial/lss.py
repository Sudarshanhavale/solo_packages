"""
Coded by Sudarshan Havale at 05-08-2019

List Special Shell Command:
    -Returns unique file patterns and details in structured format.

Uses:
    -Provide directory path as an argument to display file information from specified location.

Example:
    -python /script/path/lss.py -path "/target/directory/"
"""

# python imports
import argparse
import os
import re

# Command line parser
parser = argparse.ArgumentParser(description="lss command returns available file details in structured format.")
parser.add_argument('--path', type=str, help='Provide valid directory path to list file details from.')
args = parser.parse_args()


class ListSpecial(object):
    """Displays the unique files/folder patterns with their frame information,
    Also helps to validate render sequences, Aovs and missing frames.
    """

    def __init__(self):
        """Valid Input Directory
        """
        self.path = args.path

        # raise valueError for invalid input directory.
        if not os.path.exists(self.path):
            raise ValueError("Invalid input path: {}"
                             .format(self.path))

    def __get_files(self):
        """Get files from the input directory.

        :return: List of files and folders from input directory
        """

        files_list = sorted(os.listdir(self.path))
        return files_list

    def __unify_patterns(self):
        """Unify all unique file patterns and their frame numbers

        :return: dictionary of unique file patterns as keys and
        list of frame numbers as values.
        """
        # dictionary to store unique file patterns
        file_patterns = {}

        for each_file in self.__get_files():

            # List of digits from current file name
            file_digits = re.findall(r"\d+", each_file)

            if file_digits:
                # Always the last digit would be frame number
                frame_number = file_digits[-1]
                # Converting frame numbers into regex pattern,
                # There could be a better way of doing this.
                frame_pattern = ('%0{}d'.format(len(frame_number)))
                file_pattern = each_file.replace(frame_number, frame_pattern)
                frame_number = int(frame_number)
            else:
                frame_number = int()
                file_pattern = each_file

            # Update dict with unique patterns as
            # keys and list of frame numbers as values.
            if file_pattern in file_patterns.keys():
                file_patterns[file_pattern].append(frame_number)
            else:
                file_patterns.setdefault(file_pattern, [frame_number])

        return file_patterns

    def sorted_frame_patterns(self, num_list):
        """Segregates the continues sequences and
        individual numbers from the given list of integers.

        :param num_list: List of frame numbers
        :return: Nested list of frame sequences, individual number/numbers
        """
        sorted_frame_list = []

        # Create a segregated nested lists of continue numbers
        for idx, item in enumerate(num_list):
            if not idx or item-1 != sorted_frame_list[-1][-1]:
                # Append as new list, if item-1 doesnt match with earlier element
                sorted_frame_list.append([item])
            else:
                # Append into ending nested list, if item-1 matches with earlier element.
                sorted_frame_list[-1].append(item)

        sorted_frame_list = self.__explicit_frame_patterns(sorted_frame_list)
        return sorted_frame_list

    @staticmethod
    def __explicit_frame_patterns(nested_num_list):
        """Get the explicit patterns of sequences and single frames.

        Sequences: startFrame-endFrame
        SingleFrames: coma separated frameNumbers

        :param nested_num_list: Output return by "sorted_frame_patterns"
        :return: List of sequences and single frames in mentioned format
        """
        parsed_frame_list = ""

        for num_list in nested_num_list:
            if len(num_list) > 2:
                # Parsing logic for sequences. Numbers should be more than two.
                parsed_frame_list += (' {}-{}'.format(num_list[0], num_list[-1]))
            else:
                # Parsing logic for individual frames.
                parsed_frame_list += " {}".format(str(",".join(map(str, num_list))))

        return parsed_frame_list

    def print_info(self):
        """Print the output patterns in tabular format.

        Using default string formatting for fancier output but
        external packages like Tabular could be more convenient.

        :return: None
        """

        print ('\n{:>4} {:<30} {:<15}'.format('Count', 'Patterns', 'Range'))
        print ('-' * 70)

        for file_pattern, frame_numbers in self.__unify_patterns().items():
            total_numbers = str(len(frame_numbers))
            frame_range = self.sorted_frame_patterns(frame_numbers)

            if frame_range == " 0":
                frame_range = ""

            print ('{:>5} {:<30} {:<15}'.format(total_numbers, file_pattern, frame_range))

        print ('-' * 70)


def run():
    """Execution function

    :return: None
    """
    obj = ListSpecial()
    obj.print_info()


run()
