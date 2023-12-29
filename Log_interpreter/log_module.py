import re

from datetime import datetime


def parse_log_entry(line):
    log_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}) - \[(\w+)] - (.*)')
    match = log_pattern.match(line)
    if match:
        timestamp, log_type, message = match.groups()
        app_type = re.search(r'(BackendApp|FrontendApp|API|SYSTEM)', message)
        app = app_type.group() if app_type else None
        return {'timestamp': timestamp, 'log-type': log_type, 'app-type': app, 'message': message}
    else:
        return None

# read file function
def read_file(file_path):
    logs = []
    with open(file_path, 'r') as file:
        for line in file:
            log_entry = parse_log_entry(line)
            if log_entry:
                logs.append(log_entry)
    return logs

#ex 4
def find_app_with_most_errors(file_path):
    app_error_count = {
        "BackendApp": 0,
        "FrontendApp": 0,
        "API": 0,
        "System": 0
    }

    logs = read_file(file_path)

    for log_entry in logs:
        if log_entry['log-type'] == 'ERROR':
            app = log_entry['app-type']
            if app in app_error_count:
                app_error_count[app] += 1

    if app_error_count:
        most_errors_app = max(app_error_count, key=app_error_count.get)
        error_count = app_error_count[most_errors_app]

        return most_errors_app, error_count
    else:
        return None, 0


# ex 5
def find_app_with_most_successful_runs(file_path):
    app_success_count = {
        "BackendApp": 0,
        "FrontendApp": 0,
        "API": 0,
        "System": 0
    }

    logs = read_file(file_path)

    for log_entry in logs:
        if log_entry['log-type'] == 'INFO':
            app = log_entry['app-type']
            if app in app_success_count:
                app_success_count[app] += 1

    if app_success_count:
        most_success_app = max(app_success_count, key=app_success_count.get)
        success_count = app_success_count[most_success_app]

        return most_success_app, success_count
    else:
        return None, 0


# ex 6
def find_third_of_day_with_most_failures(file_path):
    thirds = {
        "00:00:00 - 07:59:59": 0,
        "08:00:00 - 15:59:59": 0,
        "16:00:00 - 23:59:59": 0
    }

    logs = read_file(file_path)

    for log_entry in logs:
        if log_entry['log-type'] == 'ERROR':
            timestamp = log_entry['timestamp']
            hour = int(timestamp.split(":")[0])

            if hour >= 0 and hour <= 7:
                thirds["00:00:00 - 07:59:59"] += 1
            elif hour >= 8 and hour <= 15:
                thirds["08:00:00 - 15:59:59"] += 1
            elif hour >= 16 and hour <= 23:
                thirds["16:00:00 - 23:59:59"] += 1

    if thirds:
        most_failures_third = max(thirds, key=thirds.get)
        failure_count = thirds[most_failures_third]

        return most_failures_third, failure_count
    else:
        return None, 0


# ex 7
def longest_and_shortest_successful_runtime_per_app_type(logs):
    app_types = ['BackendApp', 'FrontendApp', 'API', 'SYSTEM']
    runtimes = {app_type: {'max_runtime': float('-inf'), 'min_runtime': float('inf')} for app_type in app_types}
    filtered_logs = [log for log in logs if log.get('log-type') == 'INFO']

    for log in filtered_logs[1::2]:
        message = log.get('message')
        max_runtime = runtimes[log.get('app-type')]['max_runtime']
        min_runtime = runtimes[log.get('app-type')]['min_runtime']
        number_pattern = r'\d+'
        matches = re.findall(number_pattern, message)
        found_number = int(matches[0]) if matches else None
        if found_number > max_runtime:
            runtimes[log.get('app-type')]['max_runtime'] = found_number
        if found_number < min_runtime:
            runtimes[log.get('app-type')]['min_runtime'] = found_number

    print(runtimes)


# ex 8
def hour_of_the_day_with_most_activity_per_app_type(logs):
    app_types = ['BackendApp', 'FrontendApp', 'API', 'SYSTEM']
    hourly_logs = {app_type: {hour: 0 for hour in range(24)} for app_type in app_types}
    hours_with_most_activity = []

    for log in logs:
        timestamp = log.get('timestamp')
        timestamp_datetime = datetime.strptime(timestamp, '%H:%M:%S')
        hour = timestamp_datetime.hour
        hourly_logs[log.get('app-type')][hour] += 1

    for app_type in hourly_logs:
        max_hour = max(hourly_logs[app_type], key=hourly_logs[app_type].get)
        hours_with_most_activity.append({app_type: max_hour})

    return hours_with_most_activity

# ex 9
def compute_failure_rate_per_app_type(logs):
    app_types = ['BackendApp', 'FrontendApp', 'API', 'SYSTEM']
    failure_rates = []

    for app_type in app_types:
        error_count = sum(1 for log in logs if log.get('app-type') == app_type and log.get('log-type') == 'ERROR')
        total_count = sum(1 for log in logs if log.get('app-type') == app_type)
        failure_rates.append({'app-type': app_type, 'failure_rate': error_count / total_count})

    return failure_rates


# Main
# Create a dictionary mapping method names to their corresponding functions
methods = {
    "App with Most Errors and how many ": find_app_with_most_errors, # ex 4
    "App with Most Successful Runs and how many": find_app_with_most_successful_runs, # ex 5
    "Third of Day with Most Failures": find_third_of_day_with_most_failures, # ex 6
    # rest of the methods here
}

# Iterate over the dictionary and execute each method
for method_name, method_func in methods.items():
    result = method_func("../Log_info/output.txt")
    print(f"{method_name}: {result}")
    print()