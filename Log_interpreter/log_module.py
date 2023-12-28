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
