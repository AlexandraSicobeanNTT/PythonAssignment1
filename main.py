#Task 1,2,3
import re

def read_log_file(file_path):
    log_entries = []

    with open(file_path, 'r') as f:
        for line in f:
            match = re.match(r"(\d{2}:\d{2}:\d{2}) - \[(\w+)\] - (\w+) ", line)
            if match:
                log_entries.append(match.groups())

    return log_entries

def count_logs_per_type_and_app(log_entries):
    log_count = {'INFO': {'BackendApp': 0, 'FrontendApp': 0, 'API': 0, 'SYSTEM': 0},
                 'DEBUG': {'BackendApp': 0, 'FrontendApp': 0, 'API': 0, 'SYSTEM': 0},
                 'ERROR': {'BackendApp': 0, 'FrontendApp': 0, 'API': 0, 'SYSTEM': 0}}

    prev_info_line = None

    for log_time, log_type, app in log_entries:
        if log_type in log_count and app in log_count[log_type]:
            if log_type == 'INFO':
                if prev_info_line is not None:
                    prev_info_line = None
                else:
                    log_count[log_type][app] += 1
                    prev_info_line = log_time
            else:
                log_count[log_type][app] += 1

    return log_count

def calculate_average_run_time(file_path):
    run_times = {'BackendApp': [], 'FrontendApp': [], 'API': []}

    with open(file_path, 'r') as file:
        for line in file:
            match = re.match(r"(\d{2}:\d{2}:\d{2}) - \[\w+\] - (\w+) has ran successfully in (\d+)ms", line)
            if match:
                log_type, run_time = match.groups()[1], int(match.groups()[2])

                if log_type in run_times:
                    run_times[log_type].append(run_time)

    print("Average successful run time per type of app:")
    for app, run_time_list in run_times.items():
        if run_time_list:
            average_run_time = sum(run_time_list) / len(run_time_list)
            print(f'{app}: {average_run_time}ms')
        else:
            print(f'{app}: No successful runs recorded')

    return run_times

def count_failures_per_app(log_entries):
    failures_count = {'BackendApp': 0, 'FrontendApp': 0, 'API': 0, 'SYSTEM': 0}

    for log_time, log_type, app in log_entries:
        if 'ERROR' in log_type and app in failures_count:
            failures_count[app] += 1

    return failures_count


def main():
    file_path = 'C:/Users/EHARANANR/Downloads/output.txt'

    # Task 1: Read log file
    log_entries = read_log_file(file_path)

    # Task 2: Count logs per type and app
    log_count = count_logs_per_type_and_app(log_entries)

    # Task 4: Count failures per app
    failures_count = count_failures_per_app(log_entries)

    # Display results for task 2
    for log_type, app_count in log_count.items():
        print(f'{log_type} logs per type of app:')
        for app, count in app_count.items():
            print(f'{app}: {count}')
        print()

    #Display results for task 3
    calculate_average_run_time(file_path)
    # Display results for task 4
    print('\nNumber of failures per type of app:')
    for app, count in failures_count.items():
        print(f'{app}: {count}')

if __name__ == "__main__":
    main()
