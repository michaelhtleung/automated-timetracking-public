import sys

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))
print(sys.argv[1])

# Passing >> as an argument requires escaping each symbol, so hypothetically, the cron job will still run correctly.
# (automated-timetracking) mhtl@mhtl-G551VW:~/Projects/automated-timetracking$ python3 accepting_arguments_example.py >> foo.txt
# (automated-timetracking) mhtl@mhtl-G551VW:~/Projects/automated-timetracking$ cat foo.txt
# Number of arguments: 1 arguments.
# Argument List: ['accepting_arguments_example.py']

# (automated-timetracking) mhtl@mhtl-G551VW:~/Projects/automated-timetracking$ python3 accepting_arguments_example.py \>\> foo.txt
# Number of arguments: 3 arguments.
# Argument List: ['accepting_arguments_example.py', '>>', 'foo.txt']

for i in range(100000):
    print(i)
    if (i == 200):
        sys.exit()
