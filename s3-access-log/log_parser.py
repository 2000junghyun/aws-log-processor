import os
import csv
import glob

LOG_DIR = '/Users/admin/Downloads/s3-logs/06/12'
OUTPUT_FILE = '06-12-2025.csv'
FIELDNAMES = [
    'bucket_owner', 'bucket', 'datetime', 'remote_ip', 'requester', 'request_id',
    'operation', 'key', 'request_uri', 'http_status', 'error_code',
    'bytes_sent', 'object_size', 'total_time', 'turnaround_time',
    'referrer', 'user_agent', 'version_id', 'host_id', 'signature_version',
    'cipher_suite', 'auth_type', 'endpoint', 'tls_version',
    'access_point_arn', 'acl_required'
]

def main():
    print(f"Processed folder path: {LOG_DIR}")
    print(f"Log folder path to process: {LOG_DIR}")

    rename_files_to_txt(LOG_DIR)
    merge_logs_to_csv(LOG_DIR, OUTPUT_FILE)


def rename_files_to_txt(root_dir):
    count = 0
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            old_path = os.path.join(dirpath, filename)
            if not old_path.endswith('.txt'):
                new_path = old_path + '.txt'
                os.rename(old_path, new_path)
                count += 1
    print(f"Number of files renamed to .txt: {count}")


def merge_logs_to_csv(log_dir, output_csv):
    log_files = glob.glob(os.path.join(log_dir, '**/*.txt'), recursive=True)
    parsed_count = 0

    with open(output_csv, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(FIELDNAMES)

        for file_path in log_files:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line in file:
                    if line.strip() == '':
                        continue
                    try:
                        row = parse_log_line(line)
                        writer.writerow(row)
                        parsed_count += 1
                    except Exception:
                        continue
    print(f"Successfully parsed log lines: {parsed_count}")
    print(f"Number of log files processed: {len(log_files)}")


def parse_log_line(line):
    parts = line.strip().split()
    if len(parts) < 15:
        raise ValueError("Insufficient number of fields")

    datetime_str = parts[2].strip('[') + ' ' + parts[3].strip(']')
    cleaned_parts = parts[:2] + [datetime_str] + parts[4:]
    return cleaned_parts[:len(FIELDNAMES)]


if __name__ == "__main__":
    main()