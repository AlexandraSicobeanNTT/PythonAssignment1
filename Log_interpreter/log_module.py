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


def read_file(file_path):
    logs = []
    with open(file_path, 'r') as file:
        for line in file:
            log_entry = parse_log_entry(line)
            if log_entry:
                logs.append(log_entry)
    return logs

#ex 4
def find_app_with_most_errors(logs):
    app_error_count = {
        "BackendApp": 0,
        "FrontendApp": 0,
        "API": 0,
        "System": 0
    }

    with open(logs, 'r') as file:
        content = file.readlines()

    for line in content:
        if "[ERROR]" in line:
            if "BackendApp" in line:
                app_error_count["BackendApp"] += 1
            elif "FrontendApp" in line:
                app_error_count["FrontendApp"] += 1
            elif "API" in line:
                app_error_count["API"] += 1
            elif "SYSTEM" in line:
                app_error_count["System"] += 1

    if app_error_count:
        most_errors_app = max(app_error_count, key=app_error_count.get)
        count_error = app_error_count[most_errors_app]

        return most_errors_app, count_error
    else:
        return None, 0


#ex 5
def find_app_with_most_successful_runs(logs):
    app_success_count = {
        "BackendApp": 0,
        "FrontendApp": 0,
        "API": 0,
        "System": 0
    }

    with open(logs, 'r') as file:
        content = file.readlines()

    for line in content:
        if "[INFO]" in line:
            if "BackendApp" in line:
                app_success_count["BackendApp"] += 1
            elif "FrontendApp" in line:
                app_success_count["FrontendApp"] += 1
            elif "API" in line:
                app_success_count["API"] += 1
            elif "SYSTEM" in line:
                app_success_count["System"] += 1

    if app_success_count:
        most_success_app = max(app_success_count, key=app_success_count.get)
        success_count = app_success_count[most_success_app]

        return most_success_app, success_count
    else:
        return None, 0



#ex 6
def find_third_of_day_with_most_failures(logs):
    thirds = {
        "00:00:00 - 07:59:59": 0,
        "08:00:00 - 15:59:59": 0,
        "16:00:00 - 23:59:59": 0
    }

    with open(logs, 'r') as file:
        content = file.readlines()

    for line in content:
        if "[ERROR]" in line:
            timestamp = line.split(" - ")[0]
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

# Usage ex 4
app, error_count = find_app_with_most_errors("../Log_info/output.txt")
print(f"The app with the most failed runs is {app} with {error_count} errors.")

# Usage ex 5
app, success_count = find_app_with_most_successful_runs("../Log_info/output.txt")
print(f"The app with the most successful runs is {app} with {success_count} successful runs.")

# Usage ex 6
third, failure_count = find_third_of_day_with_most_failures("../Log_info/output.txt")
print(f"The {third} time interval had the most failed runs with {failure_count} failures.")

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


def compute_failure_rate_per_app_type(logs):
    app_types = ['BackendApp', 'FrontendApp', 'API', 'SYSTEM']
    failure_rates = []

    for app_type in app_types:
        error_count = sum(1 for log in logs if log.get('app-type') == app_type and log.get('log-type') == 'ERROR')
        total_count = sum(1 for log in logs if log.get('app-type') == app_type)
        failure_rates.append({'app-type': app_type, 'failure_rate': error_count / total_count})

    return failure_rates
