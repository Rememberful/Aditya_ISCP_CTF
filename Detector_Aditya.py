import pandas as pd
import json
import re

# Load the dataset
df = pd.read_csv('iscp_pii_dataset_-_Sheet1.csv')

# Define PII categories and regex patterns
standalone_pii_keys = {
    "phone": r"^\d{10}$",
    "aadhar": r"^\d{12}$",
    "passport": r"^[A-Z]\d{6,7}$",
    "upi_id": r"^\w+@\w+$"
}

combinatorial_pii_keys = [
    "name", "email", "address", "device_id", "ip_address"
]

def process_record(record):
    """
    Detects and redacts PII from a JSON string.
    Returns the redacted JSON string and a boolean indicating if PII was found.
    """
    try:
        data = json.loads(record)
    except json.JSONDecodeError:
        return record, False

    is_pii = False
    redacted_data = data.copy()

    # Check for combinatorial PII
    combinatorial_count = sum(key in data and key in combinatorial_pii_keys for key in data.keys())
    if combinatorial_count >= 2:
        is_pii = True
        for key in combinatorial_pii_keys:
            if key in redacted_data:
                redacted_data[key] = "[REDACTED_PII]"

    # Check for standalone PII and redact them
    for key, pattern in standalone_pii_keys.items():
        if key in data and re.match(pattern, str(data[key])):
            is_pii = True
            redacted_data[key] = "[REDACTED_PII]"
    
    # Additional specific checks
    if 'contact' in data and re.match(r"^\d{10}$", str(data['contact'])):
        is_pii = True
        redacted_data['contact'] = "[REDACTED_PII]"
    
    # A `username` key could contain an email address, which is PII.
    if 'username' in data and '@' in str(data['username']):
        is_pii = True
        redacted_data['username'] = "[REDACTED_PII]"

    
    return json.dumps(redacted_data), is_pii

# Apply the function to each row
df[['redacted_data_json', 'is_pii']] = df['data_json'].apply(lambda x: pd.Series(process_record(x)))

# Create the final output DataFrame with the required columns
output_df = df[['record_id', 'redacted_data_json', 'is_pii']]

# Save the output to a new CSV file
output_csv_filename = "redacted_output_candidate_full_name.csv"
output_df.to_csv(output_csv_filename, index=False)

print(f"\nSaved redacted data to {output_csv_filename}")