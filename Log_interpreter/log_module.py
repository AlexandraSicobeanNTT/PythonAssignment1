import re

def parse_log_entry(line):
    log_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}) - \[(\w+)\] - (.*)')
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

def compute_failure_rate(logs):
    app_types = ['BackendApp', 'FrontendApp', 'API', 'SYSTEM']
    failure_rates = []
    for app_type in app_types:
        error_count = sum(1 for log in logs if log.get('app-type') == app_type and log.get('log-type') == 'ERROR')
        total_count = sum(1 for log in logs if log.get('app-type') == app_type)
        failure_rates.append({'app-type': app_type, 'failure_rate': error_count / total_count})
    return failure_rates





logs = read_file("C:/Users/ESICOBAVX/Downloads/output.txt")
print(compute_failure_rate(logs))