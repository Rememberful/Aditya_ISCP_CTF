# ISCP 2.0 SOC-PII-Challenge – Real-Time PII Redactor

This repository contains my submission for the **Real-Time PII Defense** challenge as part of the Flipkart **ISCP 2.0 SOC-PII-Challenge**.  
The project aims to detect and redact **Personally Identifiable Information (PII)** from data streams **in real time**, while maintaining high accuracy and low latency.

---

## Challenge Overview

Flipkart’s security audit uncovered logs leaking personal data (names, addresses, etc.) via external APIs. Fraudsters exploited this data for OTP scams and unauthorized refunds.

**Goal:**  
Build a system that can:
- Identify PII (both standalone and combinatorial)
- Redact sensitive data in real time
- Maintain high accuracy and low latency

---

## Features

### Standalone PII Detection
- Phone numbers (10-digit)
- Aadhar numbers (12-digit)
- Passport numbers (Indian alphanumeric format)
- UPI IDs (user@bank-style)

### Combinatorial PII Detection
- Full names (first + last)
- Email addresses
- Physical addresses (street, city, pin)
- Device IDs / IP addresses (contextually tied)

### Smart Redaction Patterns
| Original | Redacted |
|----------|----------|
| 9876543210 | 98XXXXXX10 |
| 1234 5678 9012 | 12XXXXXXXX12 |
| rahul.kumar@upi | raXXX@upi |
| John Smith | JXXX SXXXX |

### Output
Sanitized CSV with:
- `record_id`
- `redacted_data_json`
- `is_pii` (True/False)

**Sample Output:**
```csv
record_id,redacted_data_json,is_pii

## Usage

1. **Clone the repository:**
```bash
git clone https://github.com/Rememberful/Aditya_ISCP_CTF.git
cd Aditya_ISCP_CTF
python detector_Aditya.py iscp_pii_dataset_-_Sheet1.csv

redacted_output_shyam_sunder.csv

1,"{""phone"": ""98XXXXXX10"", ""order_value"": 1299}",True
2,"{""name"": ""JXXX SXXXX"", ""email"": ""joXXX@gmail.com""}",True
