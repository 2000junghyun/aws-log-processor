# Human-Readable VPC Flow Log Parser
## Problem

- The log file contains only two fields: `timestamp` and `message`, which makes analysis difficult.
- The default time format is in UNIX epoch time, making it hard to interpret.

## Solution

- Refined the log fields for better structure and clarity:
    
    ```python
    python
    CopyEdit
    fieldnames = [
        'timestamp', 'version', 'account_id', 'interface_id',
        'srcaddr', 'dstaddr', 'srcport', 'dstport',
        'protocol', 'packets', 'bytes', 'start',
        'end', 'action', 'log_status'
    ]
    
    ```
    
- Converted UNIX epoch time to human-readable time in LA timezone.
- Designed the script so input and output file names can be easily customized.

## Results

### Before
![스크린샷 2025-06-13 113724](https://github.com/user-attachments/assets/3355914b-39d9-464d-a233-60957f417209)

### After
![스크린샷 2025-06-13 113801](https://github.com/user-attachments/assets/5fd01bae-cb9d-4ed3-9952-900c5eb76109)


## Expected Benefits

- Enables generation of a structured base file for more precise log filtering.
- Makes timestamps easier to interpret by using a more readable time format.
