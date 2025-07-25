import os
import csv
import json
import pytz
from datetime import datetime

INPUT_FOLDER = 'C:/Users/Admin/Desktop/AWS/Logs/CloudTrail/ManagementEvent-US-esat-1-0624'
OUTPUT_FILE = 'ManagementEvent-US-esat-1-0624.csv'
FIELDNAMES = {
    "eventTime": "eventTime",
    "eventName": "eventName",
    "eventSource": "eventSource",
    "userName": "userIdentity.userName",
    "sourceIPAddress": "sourceIPAddress",
    "awsRegion": "awsRegion",
    "errorCode": "errorCode",
    "errorMessage": "errorMessage",
    "readOnly": "readOnly",
    "mfaAuthenticated": "userIdentity.sessionContext.attributes.mfaAuthenticated",
    "sessionCredentialFromConsole": "sessionCredentialFromConsole",
    "eventType": "eventType"
}

def main():
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(list(FIELDNAMES.keys()))  # CSV 헤더

        for filename in os.listdir(INPUT_FOLDER):
            if filename.endswith('.json'):
                full_path = os.path.join(INPUT_FOLDER, filename)
                with open(full_path, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                        records = data.get('Records', [])
                        for record in records:
                            row = []
                            for field, path in FIELDNAMES.items():
                                value = get_nested_value(record, path)
                                if field == 'eventTime' and value:
                                    value = convert_to_la_time(value)
                                row.append(value if value is not None else "")
                            writer.writerow(row)
                    except Exception as e:
                        print(f"[ERROR] File to parse files: {filename} - {e}")

    print(f"[Complete] output file: {OUTPUT_FILE}")


# 중첩 JSON 키 접근 함수
def get_nested_value(data, key_path):
    keys = key_path.split('.')
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key, None)
        else:
            return None
    return data


# UTC → LA 시간대 변환
def convert_to_la_time(utc_str):
    try:
        utc = pytz.utc
        la = pytz.timezone('America/Los_Angeles')
        utc_time = datetime.strptime(utc_str, '%Y-%m-%dT%H:%M:%SZ')
        la_time = utc_time.replace(tzinfo=utc).astimezone(la)
        return la_time.strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return utc_str  # 변환 실패 시 원본 유지


if __name__ == "__main__":
    main()