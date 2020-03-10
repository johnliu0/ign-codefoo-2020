"""
IGN Code Foo 10 Submission

Author: John Liu
Date: Monday, March 10, 2020
"""

import csv

# name of csv file to read
# note that quest.csv is a stripped-down version of what the application provides
# containing only start dates, durations, rewards, and quest name
INPUT_FILE = 'quest.csv'
# index of the column representing the quest names
NAME_COLUMN_IDX = 0
# index of the column representing the start dates
START_COLUMN_IDX = 1
# index of the column representing the duration
DURATION_COLUMN_IDX = 2
# index of the column representing the reward in rupees
REWARD_COLUMN_IDX = 3
# how many days Link has to do quests
NUM_DAYS = 31

body_data = []

# read csv file
with open(INPUT_FILE, encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    # read body data
    for row in reader:
        row_parsed = []
        for i in range(len(row)):
            # add the name as a string and other data as integers
            if i == NAME_COLUMN_IDX:
                row_parsed.append(row[i])
            else:
                row_parsed.append(int(row[i]))
        body_data.append(row_parsed)

def find_max_earnings():
    """Computes the max amount of rupees that Link can earn.

    Solution explanation:
    This is a classic dynamic programming problem.

    Suppose max_earnings[x][y] gives the max possible earnings for the days in the range [x, y].
    The answer we want to find is max_earnings[1][31].

    We first build an array that will keep track of every subproblem we solve.
    Then we will build another array that keeps track of the optimal
    "k" value (this is explained later on).

    Example: max_earnings[i][j] gives the most optimal solution in the range [i, j].

    Then, we take a bottom-up approach and compute optimal solutions for the smallest
    subproblems. Assume i < j, then we have two cases:

    (1) i == j (Base Case) then recurs[i][j] == 0, since no Quest takes one day to finish.
    (2) i < j: {max_earnings[i][k] + max_earnings[k][j], job[i,j]}
                for some k in range [i + 1, j + 1]
                and for some job if it starts on i and ends on j
                if there is no job that ranges on this date range, job[i,j] = 0
    
    We essentially compute the optimal solution for all 1 day length time periods, 2 day length time periods,
    3 day length time periods, ..., n day length time periods.
    
    Then the final solution is simply max_earnings[1][31].

    *** Algorithmic Analysis ***
    
    Time complexity: O(n^3)
    Space complexity: O(n^2)

    This solution uses dynamic programming and is compatible with any Quest board as long as
    a name, start date, duration, and reward is provided. Since DP is used, we also solve
    every single subproblem, e.g. what is the maximum reward we can get for days 10 to 15.

    """

    # build a list of jobs that can be performed
    # by extracting the start date, duration, reward, and quest index into a list of tuples
    # of the form (start, end, reward, quest index)
    jobs = []
    for i in range(len(body_data)):
        jobs.append((
            body_data[i][START_COLUMN_IDX],
            body_data[i][START_COLUMN_IDX] + body_data[i][DURATION_COLUMN_IDX],
            body_data[i][REWARD_COLUMN_IDX],
            i))
    
    # initialize a 2d array to keep track of solutions to recurrences (subproblems)
    # use (NUM_DAYS + 1)x(NUM_DAYS + 1), since dates are one-indexed
    max_earnings = []
    for i in range(NUM_DAYS + 1):
        max_earnings.append([])
        for j in range(NUM_DAYS + 1):
            max_earnings[-1].append(0)
    
    # initialize another 2d array to keep track of our optimal "k" values
    # which gives the optimal solution for max_earnings[i][k] + max_earnings[k][j].
    # this will be in the form (k, quest_idx)
    # if the optimal solution for i, j is a job that spans i, j, then let k = -1
    # and quest_idx be the index of the quest that corresponds to i,j
    # k = -1 is rather arbitrary; it won't conflict with a date
    # of course if no job spans this date, then quest_idx will be -1 as well
    k_values = []
    for i in range(NUM_DAYS + 1):
        k_values.append([])
        for j in range(NUM_DAYS + 1):
            k_values[-1].append((-1, -1))
    
    # let L be j-i
    for L in range(1, NUM_DAYS):
        # let i be the starting index (start date), which is in the range [1, NUM_DAYS - L]
        for i in range(1, NUM_DAYS - L + 1):
            # let j be the ending index (end date), which is in range [i, NUM_DAYS]
            j = i + L

            # highest earnings from a job that starts on day i and ends on day j
            single_job_earnings = 0
            quest_idx = -1
            for job_i in range(len(jobs) - 1, -1, -1):
                if jobs[job_i][0] == i and jobs[job_i][1] == j:
                    # update the single_job_learnings and quest_idx if necessary
                    if jobs[job_i][2] > single_job_earnings:
                        single_job_earnings = jobs[job_i][2]
                        quest_idx = jobs[job_i][3]
                    # remove this job as it has been visited
                    jobs.pop(job_i)
            
            # first assume that the best job we can get from i to j is single_job_earnings
            # which may or may not be 0 (a job may or may not exist that lasts from i to j)
            max_earnings[i][j] = single_job_earnings
            k_values[i][j] = (-1, quest_idx)

            # then iterate through the subrecurrences and see if we can find a better one
            # let k be the value between i and j so that we may compute max_earnings(i, k) + max_earnings(k, j)
            for k in range(i + 1, j):
                # if we discover that a subcombination of jobs is better than
                # what we currently have at i to j, then update it
                job_earnings_combined = max_earnings[i][k] + max_earnings[k][j]
                if job_earnings_combined > max_earnings[i][j]:
                    max_earnings[i][j] = job_earnings_combined
                    k_values[i][j] = (k, -1)

    return (max_earnings, k_values)

def print_max_earnings(max_earnings, k_values, i, j):
    k, quest_idx = k_values[i][j]
    # if k == -1, then the optimal solution is a job that spans [start, end]
    if k == -1:
        # of course, a job might not actually exist in the range [start, end]
        if quest_idx != -1:
            name = body_data[quest_idx][NAME_COLUMN_IDX]
            start = body_data[quest_idx][START_COLUMN_IDX]
            duration = body_data[quest_idx][DURATION_COLUMN_IDX]
            earnings = max_earnings[i][j]
            print('{0:<30} {1:>5} {2:>5} {3:>10}'.format(name, start, start + duration, earnings))
            #print (f'{name}\t\t\twhich begins on day {start} and ends on day {start + duration} and rewards {earnings} rupees')
    else:
        print_max_earnings(max_earnings, k_values, i, k)
        print_max_earnings(max_earnings, k_values, k, j)

if __name__ == '__main__':
    print()
    print('Quest Reward Optimizer: IGN Code Foo Summer 2020')
    print('Author: John Liu')
    print()

    max_earnings, k_values = find_max_earnings()
    print(f'The maximum amount of rupees that Link can earn in {NUM_DAYS} days is {max_earnings[1][NUM_DAYS]}.')
    print(f'To achieve this, Link should do the following quests in order: ')
    print('{0:<30} {1:>5} {2:>5} {3:>10}'.format('Quest', 'Start', 'End', 'Reward'))
    print_max_earnings(max_earnings, k_values, 1, NUM_DAYS)

    print()


