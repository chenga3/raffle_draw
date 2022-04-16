import os
import random
import sys


class QuizRepsonse:
    def __init__(self, line):
        # Strip newline char and split by commas.
        values = line.rstrip().split(',')
        # Is this response eligible for prizes?
        self.eligible = values[-1] == "TRUE"
        # How many points did they score?
        self.points = int(values[2].split('/')[0].rstrip())
        # Contact information.
        self.first_name = values[3]
        self.last_name = values[4]
        self.email = values[1]

    def __str__(self):
        return 'Name: ' + self.first_name + ' ' + self.last_name + ' | Email: ' + self.email + ' | Points: ' + str(self.points)


def get_cdf(responses):
    # Returns a list of cumulative sums of points scored by responses.
    cdf = []
    cumulative_sum = 0
    for response in eligible_responses:
        cumulative_sum += response.points
        cdf.append(cumulative_sum)
    return cdf


def get_eligible_responses(responses):
    # Returns a list of responses which are eligible for prizes.
    eligible_responses = []
    for response in responses:
        if response.eligible:
            eligible_responses.append(response)
    return eligible_responses


def get_prize_winners(eligible_responses, seed):
    # Randomly draws two prize winners where chances are weighted proportional to number of points scored.
    random.seed(seed)

    # Draw first place prize winner.
    cdf = get_cdf(eligible_responses)
    first_draw = random.randint(1, cdf[-1])
    for i in range(len(cdf)):
        if first_draw <= cdf[i]:
            first_place = eligible_responses[i]
            eligible_responses.pop(i)
            break

    # Draw second place prize winner.
    cdf = get_cdf(eligible_responses)
    second_draw = random.randint(1, cdf[-1])
    for i in range(len(cdf)):
        if second_draw <= cdf[i]:
            second_place = eligible_responses[i]
            break

    return first_place, second_place


if __name__ == "__main__":

    # Check that we have the correct number of command line arguments.
    if len(sys.argv) < 3:
        print('Usage:\n')
        print('\t py ' + os.path.basename(__file__) +
              ' [responses_file] [seed]\n')
        print('Arguments:\n')
        print('responses_file: CSV file containing quiz responses.')
        print('seed: Seed for random number generator.')
        sys.exit(1)

    # Get filename of CSV file containing quiz responses from command line argument.
    filename = sys.argv[1]
    seed = int(sys.argv[2])

    # Create QuizResponse objects for each response recorded in the file and store in list.
    responses = []
    with open(filename) as f:
        next(f)  # Skip header line.
        for line in f:
            responses.append(QuizRepsonse(line))

    # Filter out ineligible responses.
    eligible_responses = get_eligible_responses(responses)

    # Randomly draw our prize winners - chances are weighted by points scored.
    first_place, second_place = get_prize_winners(eligible_responses, seed)

    print('\nFirst Place Winner !!')
    print(first_place)
    print('\nSecond Place Winner !!')
    print(second_place)
