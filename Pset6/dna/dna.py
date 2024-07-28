import csv
import sys


def main():
    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        return 1

    # TODO: Read database file into a variable
    database_file = open(sys.argv[1], "r")
    database = csv.DictReader(database_file)
    str_names = database.fieldnames[1:]

    # TODO: Read DNA sequence file into a variable
    sequence_file = open(sys.argv[2], "r")
    sequence = sequence_file.read()

    # TODO: Find longest match of each STR in DNA sequence
    str_count = {}
    for str_type in str_names:
        longest_str = longest_match(sequence, str_type)
        str_count[str_type] = longest_str

    # TODO: Check database for matching profiles
    for person in database:
        found = True
        for str_type in str_names:
            if int(str_count[str_type]) != int(person[str_type]):
                found = False

        if found:
            print(person["name"])
            break

    # Reached end of loop without finding
    if not found:
        print("No match")

    return 0


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):
        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:
            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
