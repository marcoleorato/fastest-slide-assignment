import sys
import argparse


def main(argv):
    # Add a few utility arguments to use a custom file and choose the alternative traverse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', default=sys.path[0] + '/input', type=str, help='The path to the input file')
    parser.add_argument('-a', '--alt', default=False, action='store_true', help='Use the alternative top-down traverse. Useful with bigger input files')
    # Parse the possible arguments ignoring unknown ones
    args, unknown = parser.parse_known_args(argv)

    try:
        # Open the input file with a generator
        data = input_generator(args.file)

        # Choose the method to use, default is args.alt = False
        if args.alt:
            # Top down traverse use read the file and calculate the path row by row
            lowest_path = top_down_traverse(data)
        else:
            # Bottom up traverse read the whole file in memory and use the rows starting from the last one
            lowest_path = bottom_up_traverse(data)

        print('The lowest path found was: ' + str(lowest_path))
    except IOError:
        print('The file "' + args.file + '" can not be found')

    return


def bottom_up_traverse(data):
    # All the lines are needed so this exhaust the whole generator putting all the data in a list
    data = list(data)

    # Initialize the "current" variable
    # Important for if the pyramid has depth = 1
    current = data[-1]
    # Initialize the "previous" variable needed for the loop in every other case
    previous = current

    # Loop on all the other lines in the input
    # Since we go from the bottom we reverse the list and skip the first line which is already in "previous"
    for current in reversed(data[:-1]):
        for j in range(0, len(current)):
            # Going bottom up the previous row will always have 1 more element, so j+1 won't be out of bound
            current[j] = current[j] + min(previous[j], previous[j + 1])

        previous = current

    # Current is an array but at this point it will have only 1 element
    return current[0]


def top_down_traverse(data):
    # Initialize the generator and "current" variable
    # Important for if the pyramid has depth = 1
    current = next(data)
    # Initialize the "previous" variable needed for the loop in every other case
    previous = current

    # Loop on all the other lines in the input
    # Being a generator the first line was already read and is not present anymore
    for current in data:
        # Set the max valid index of the previous list, needed to avoid out of bound exceptions
        max_index = len(previous) - 1
        for j in range(0, len(current)):
            # max(j - 1, 0) ensure that in the case of i = 0  we don't try to read -1
            # min(j, max_index) avoid out of bound on the last element as "current" is 1 element bigger than "previous"
            current[j] = current[j] + min(previous[max(j - 1, 0)], previous[min(j, max_index)])

        previous = current

    # Return the lowest path found
    return min(current)


def input_generator(file):
    f = open(file, 'r')

    # Read the first line indicating how many rows there are
    row_number = int(f.readline())
    # Only read up to the number indicated
    for i in range(0, row_number):
        row = f.readline()
        # Split the line to remove the newline characters at the end
        row = row.splitlines()[0]
        yield [int(x) for x in row.split(' ') if x]

    f.close()


if __name__ == '__main__':
    main(sys.argv)
