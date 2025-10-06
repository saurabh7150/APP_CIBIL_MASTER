import requests
import json

COMMON_BOUNCE_RULES = {
    "HERO": {
        "bounces0_3": [
            (0, "PASS"),
            (1, "R1"),
            (2, "R1"),
            ("3+", "R1")
        ],
        "bounces4_6": [
            (0, "PASS"),
            (1, "R1"),
            (2, "R1"),
            (3, "R1"),
            ("4+", "R1")
        ],
        "bounces7_12": [
            (0, "PASS"),
            (1, "R2"),
            (2, "R1"),
            (3, "R1"),
            ("4+", "R1")
        ],
        "bounces13_24": [
            (0, "PASS"), (1, "PASS"), (2, "PASS"), (3, "PASS"),
            (4, "R1"), (5, "R1"), (6, "R1"), (7, "R1"), ("8+", "R1")
        ],
        "bounces24_60": [
            (0, "PASS"), (1, "PASS"), (2, "PASS"), (3, "PASS"),
            (4, "PASS"), (5, "PASS"), (6, "R1"), (7, "R1"), ("8+", "R1")
        ],
        "bounces0_6": [
            (0, "PASS"), (1, "R1"), (2, "R1"), (3, "R1"), (4, "R1"), ("5+", "R1")
        ],
        "bounces0_9": [
            (0, "PASS"), (1, "PASS"), (2, "PASS"), (3, "PASS"), (4, "PASS"), ("5+", "PASS")
        ],
        "bounces0_12": [
            (0, "PASS"), (1, "PASS"), (2, "PASS"), (3, "PASS"), (4, "PASS"), (5, "PASS"),
            (6, "PASS"), ("7+", "PASS")
        ],
        "bounces0_24": [
            (i, "PASS") for i in range(0, 10)
        ] + [("10+", "PASS")],
        "bounces0_60": [
            (i, "PASS") for i in range(0, 13)
        ] + [("13+", "PASS")]
    },

    "IDFC": {
        "bounces0_3": [
            (0, "PASS"),
            (1, "REJECT"),
            (2, "REJECT"),
            ("3+", "REJECT")
        ],
        "bounces4_6": [
            (0, "PASS"),
            (1, "R2"),
            (2, "R2"),
            (3, "REJECT"),
            ("4+", "REJECT")
        ],
        "bounces7_12": [
            (0, "PASS"),
            (1, "R2"),
            (2, "R2"),
            (3, "REJECT"),
            ("4+", "REJECT")
        ],
        "bounces13_24": [
            (0, "PASS"), (1, "PASS"), (2, "PASS"), (3, "PASS"),
            (4, "REJECT"), (5, "REJECT"), (6, "REJECT"), (7, "REJECT"), ("8+", "REJECT")
        ],
        "bounces24_60": [
            (0, "PASS"), (1, "PASS"), (2, "PASS"), (3, "PASS"), (4, "PASS"), (5, "PASS"),
            (6, "REJECT"), (7, "REJECT"), ("8+", "REJECT")
        ],
        "bounces0_6": [
            (0, "PASS"), (1, "PASS"), (2, "PASS"), (3, "PASS"), (4, "PASS"), ("5+", "PASS")
        ],
        "bounces0_9": [
            (i, "PASS") for i in range(0, 5)
        ] + [("5+", "PASS")],
        "bounces0_12": [
            (i, "PASS") for i in range(0, 7)
        ] + [("7+", "PASS")],
        "bounces0_24": [
            (i, "PASS") for i in range(0, 10)
        ] + [("10+", "PASS")],
        "bounces0_60": [
            (i, "PASS") for i in range(0, 13)
        ] + [("13+", "PASS")]
    },
    "AU": {
        "bounces0_6": [
            (0, "PASS"),
            (1, "R1"),
            (2, "R1"),
            (3, "R1"),
            (4, "R1"),
            ("5+", "R1")
        ],
        "bounces0_9": [
            (0, "PASS"),
            (1, "R1"),
            (2, "R1"),
            (3, "R1"),
            (4, "R1"),
            ("5+", "R1")
        ],
        "bounces0_12": [
            (0, "PASS"),
            (1, "R1"),
            (2, "R1"),
            (3, "R1"),
            (4, "R1"),
            ("5+", "R1")
        ],
        "bounces0_24": [
            (0, "PASS"),
            (1, "R1"),
            (2, "R1"),
            (3, "R1"),
            (4, "R1"),
            ("5+", "R1")
        ],
        "bounces0_60": [
            (0, "PASS"),
            (1, "R1"),
            (2, "R1"),
            (3, "R1"),
            (4, "R1"),
            ("5+", "R1")
        ]
    },

    "CHOLA": {
        "bounces0_6": [
            (0, "PASS"),
            (1, "R1"),
            (2, "R1"),
            (3, "R1"),
            (4, "R1"),
            ("5+", "R1")
        ],
        "bounces0_9": [
            (0, "PASS"),
            (1, "R1"),
            (2, "R1"),
            (3, "R1"),
            (4, "R1"),
            ("5+", "R1")
        ],
        "bounces0_12": [
            (0, "PASS"),
            (1, "R1"),
            (2, "R1"),
            (3, "R1"),
            (4, "R1"),
            ("5+", "R1")
        ],
        "bounces0_24": [
            (0, "PASS"),
            (1, "R1"),
            (2, "R1"),
            (3, "R1"),
            (4, "R1"),
            ("5+", "R1")
        ],
        "bounces0_60": [
            (0, "PASS"),
            (1, "R1"),
            (2, "R1"),
            (3, "R1"),
            (4, "R1"),
            ("5+", "R1")
        ]
    }
}



def get_field(field_path,data):
    current = data
    for key in field_path.split('.'):
        if isinstance(current, dict):
            current = current.get(key)
        elif isinstance(current, list) and key.isdigit():
            current = current[int(key)]
        else:
            return None
    return current
def classify_bounce_count(rules, count):
    for threshold, label in rules:
        if isinstance(threshold, int) and count == threshold:
            return label
        elif isinstance(threshold, str) and threshold.endswith('+'):
            min_val = int(threshold[:-1])
            if count >= min_val:
                return label
    return None  # No rule matched


def classify_mother_bounces(bank_name, bounce_data: dict, include_pass=False):
    bank_rules = COMMON_BOUNCE_RULES.get(bank_name.upper())
    if not bank_rules:
        return {"error": f"Unsupported bank: {bank_name}"}

    result = {}

    for bounce_key, count in bounce_data.items():
        if bounce_key in bank_rules:
            classification = classify_bounce_count(bank_rules[bounce_key], count)

            if classification and (include_pass or classification != "PASS"):
                # Convert bounce_key like "bounces0_24" → "mother_bounce_0-24"
                phase = bounce_key.replace("bounces", "").replace("_", "-")
                output_key = f"mother_bounce{phase}"
                result[output_key] = classification

    return result








def get_cibil_data(pan):
    """Calls the /get_cibil API with the given PAN and returns the data or None."""
    try:
        response = requests.get("https://api-rc-cibil-ei8h.onrender.com/get_cibil", params={"pan": pan})
        if response.status_code == 200:
            return response.json().get("data")
        elif response.status_code == 404:
            print("No CIBIL data found.")
            return None
        else:
            print("Error fetching CIBIL data:", response.json())
            return None
    except Exception as e:
        print("Exception during API call:", str(e))
        return None


def get_mother_account(cibil_data: dict, search_account: str) -> dict | None:
    """
    Fetch account details for a given account number from CIBIL JSON data.

    Args:
        cibil_data (dict): Full CIBIL JSON data.
        search_account (str): Account number to search for.

    Returns:
        dict | None: Account details if found, else None.
    """
    try:
        # Traverse inside data -> credit_report -> accounts
        credit_reports = cibil_data.get("data", {}).get("credit_report", [])
        for report in credit_reports:
            accounts = report.get("accounts", [])
            for account in accounts:
                if account.get("accountNumber") == search_account:
                    return account  # return full account details dict

    except Exception as e:
        print(f"Error while fetching account: {e}")
        return None

    return None  # If not found

def print_json_structure(obj, indent=0):
    spacing = "  " * indent
    if isinstance(obj, dict):
        for key, value in obj.items():
            print(f"{spacing}{key}: {type(value).__name__}")
            print_json_structure(value, indent + 1)
    elif isinstance(obj, list):
        print(f"{spacing}list[{len(obj)}]")
        if obj:
            print_json_structure(obj[0], indent + 1)



from datetime import datetime
from dateutil.relativedelta import relativedelta


def has_24_or_more_emis(cibil_data: dict, account_number: str) -> bool:
    """
    Return True if there are 12 or more EMI records (dates) 
    in the last 12 months (excluding current incomplete month).
    """
    today = datetime.today().replace(day=1)  # beginning of current month
    # Build list of last 12 months YYYY-MM (excluding current month)
    months_to_check = [(today - relativedelta(months=i)).strftime("%Y-%m") for i in range(1, 25)]

    credit_reports = cibil_data.get("data", {}).get("credit_report", [])
    for report in credit_reports:
        for account in report.get("accounts", []):
            if account.get("accountNumber") == account_number:
                monthly_status = account.get("monthlyPayStatus", [])

                # Build a set of months actually available in the data
                available_months = {
                    datetime.strptime(r["date"], "%Y-%m-%d").strftime("%Y-%m")
                    for r in monthly_status if "date" in r
                }

                # Count how many expected months are present
                matched = sum(1 for m in months_to_check if m in available_months)
                '''
                # Debug
                print("DEBUG: Months to check =", months_to_check)
                print("DEBUG: Available months =", sorted(available_months))
                print("DEBUG: Matched count =", matched)
                '''
                return matched >= 24

    return False

def has_12_or_more_emis(cibil_data: dict, account_number: str) -> bool:
    """
    Return True if there are 12 or more EMI records (dates) 
    in the last 12 months (excluding current incomplete month).
    """
    today = datetime.today().replace(day=1)  # beginning of current month
    # Build list of last 12 months YYYY-MM (excluding current month)
    months_to_check = [(today - relativedelta(months=i)).strftime("%Y-%m") for i in range(1, 13)]

    credit_reports = cibil_data.get("data", {}).get("credit_report", [])
    for report in credit_reports:
        for account in report.get("accounts", []):
            if account.get("accountNumber") == account_number:
                monthly_status = account.get("monthlyPayStatus", [])

                # Build a set of months actually available in the data
                available_months = {
                    datetime.strptime(r["date"], "%Y-%m-%d").strftime("%Y-%m")
                    for r in monthly_status if "date" in r
                }

                # Count how many expected months are present
                matched = sum(1 for m in months_to_check if m in available_months)
                '''
                # Debug
                print("DEBUG: Months to check =", months_to_check)
                print("DEBUG: Available months =", sorted(available_months))
                print("DEBUG: Matched count =", matched)
                '''
                return matched >= 12

    return False

def has_15_or_more_emis(cibil_data: dict, account_number: str) -> bool:
    """
    Return True if there are 12 or more EMI records (dates) 
    in the last 12 months (excluding current incomplete month).
    """
    today = datetime.today().replace(day=1)  # beginning of current month
    # Build list of last 12 months YYYY-MM (excluding current month)
    months_to_check = [(today - relativedelta(months=i)).strftime("%Y-%m") for i in range(1, 16)]

    credit_reports = cibil_data.get("data", {}).get("credit_report", [])
    for report in credit_reports:
        for account in report.get("accounts", []):
            if account.get("accountNumber") == account_number:
                monthly_status = account.get("monthlyPayStatus", [])

                # Build a set of months actually available in the data
                available_months = {
                    datetime.strptime(r["date"], "%Y-%m-%d").strftime("%Y-%m")
                    for r in monthly_status if "date" in r
                }

                # Count how many expected months are present
                matched = sum(1 for m in months_to_check if m in available_months)
                '''
                # Debug
                print("DEBUG: Months to check =", months_to_check)
                print("DEBUG: Available months =", sorted(available_months))
                print("DEBUG: Matched count =", matched)
                '''
                return matched >= 15

    return False



def has_18_or_more_emis(cibil_data: dict, account_number: str) -> bool:
    """
    Return True if there are 12 or more EMI records (dates) 
    in the last 12 months (excluding current incomplete month).
    """
    today = datetime.today().replace(day=1)  # beginning of current month
    # Build list of last 12 months YYYY-MM (excluding current month)
    months_to_check = [(today - relativedelta(months=i)).strftime("%Y-%m") for i in range(1, 19)]

    credit_reports = cibil_data.get("data", {}).get("credit_report", [])
    for report in credit_reports:
        for account in report.get("accounts", []):
            if account.get("accountNumber") == account_number:
                monthly_status = account.get("monthlyPayStatus", [])

                # Build a set of months actually available in the data
                available_months = {
                    datetime.strptime(r["date"], "%Y-%m-%d").strftime("%Y-%m")
                    for r in monthly_status if "date" in r
                }

                # Count how many expected months are present
                matched = sum(1 for m in months_to_check if m in available_months)
                
                # Debug
                #print("DEBUG: Months to check =", months_to_check)
                #print("DEBUG: Available months =", sorted(available_months))
                #print("DEBUG: Matched count =", matched)
                
                return matched >= 18

    return False

def is_closed_more_than_6_months(cibil_data: dict, account_number: str) -> bool:
    """
    Return True if loan is closed more than 6 months ago.
    Return False if still active or closed within 6 months.
    """
    credit_reports = cibil_data.get("data", {}).get("credit_report", [])
    for report in credit_reports:
        for account in report.get("accounts", []):
            if account.get("accountNumber") == account_number:
                date_closed = account.get("dateClosed", "").strip()

                # If still open
                if not date_closed or date_closed.upper() == "NA":
                    return False

                try:
                    closed_date = datetime.strptime(date_closed, "%Y-%m-%d")
                except ValueError:
                    return False  # invalid format

                six_months_ago = datetime.today() - relativedelta(months=6)

                # ✅ True if closure happened BEFORE 6 months ago
                return closed_date < six_months_ago

    return False  # account not found




def get_multiplier_helper(data, account_number: str, bank: str = "hero") -> list[int]:
    """
    Return all eligible multipliers for given account based on CIBIL score and EMI history.
    """
    cibil_score = int(get_field("data.credit_score", data))
    print("CIBIL Score:", cibil_score)

    is_12_paid = has_12_or_more_emis(data, account_number)
    print("12 EMI Paid:", is_12_paid)

    closed_6months = is_closed_more_than_6_months(data, account_number)
    print("Closed > 6 months:", closed_6months)

    is_24_paid = has_24_or_more_emis(data, account_number)
    print("24 EMI Paid:", is_24_paid)

    
    is_18_paid = has_18_or_more_emis(data, account_number)
    print("18 EMI Paid:", is_24_paid)

    is_15_paid = has_15_or_more_emis(data,account_number)
    print("15 EMI Paid:", is_15_paid)
    
    multipliers = []

    if bank.lower() == "hero":
        # Base: 12 EMI paid + score > 600
        if cibil_score > 600 and is_12_paid:
            multipliers.extend([90, 120, 150])

        # Loan closed > 6 months (independent rule)
        if cibil_score > 600 and closed_6months:
            multipliers.append(90)

        # Stronger case: 24 EMI + high CIBIL
        if 750 <= cibil_score <= 900 and is_24_paid:
            multipliers.append(180)
    

    if bank.lower() == "idfc":
        if cibil_score > 600 and is_12_paid:
            multipliers.extend([120,150])
        if cibil_score > 600 and closed_6months:
            multipliers.extend([120])
        if 750 <= cibil_score <= 900 and is_18_paid:
            multipliers.append(170)
        if 750 <= cibil_score <= 900 and is_24_paid:
            multipliers.append(200)

    if bank.lower() == "piramal":
        if cibil_score > 600 and is_12_paid:
            multipliers.append(170)
        if cibil_score > 600 and closed_6months:
            multipliers.append(140)
        if 750 <= cibil_score <= 900 and is_24_paid:
            multipliers.append(200)
    if bank.lower() == "axis":
        if cibil_score > 600 and is_18_paid:
            multipliers.append(160)
        if cibil_score > 600 and is_24_paid:
            multipliers.append(180)
        if cibil_score > 600 and closed_6months:
            multipliers.append(90)
        if 750 <= cibil_score <= 900 and is_18_paid:
            multipliers.append(160)
        if 750 <= cibil_score <= 900 and is_24_paid:
            multipliers.append(180)
    if bank.lower() == "au":
        if cibil_score > 600 and is_12_paid:
            multipliers.append(100)
        if cibil_score > 600 and closed_6months:
            multipliers.append(100)
    if bank.lower() == "chola":
        if cibil_score > 600 and is_12_paid:
            multipliers.append(90)
        if cibil_score > 600 and closed_6months:
            multipliers.append(90)
    if bank.lower() == "tata":
        if 700 <= cibil_score <= 725 and is_12_paid:
            multipliers.append(140)
        if 700 <= cibil_score <= 725 and is_18_paid:
            multipliers.append(150)
        if 700 <= cibil_score <= 725 and is_24_paid:
            multipliers.append(160)
        if cibil_score>700 and closed_6months:
            multipliers.append(90)
        if 725 <= cibil_score <= 750 and is_12_paid:
            multipliers.append(150)
        if 725 <= cibil_score <= 750 and is_18_paid:
            multipliers.append(170)
        if 725 <= cibil_score <= 750 and is_24_paid:
            multipliers.append(180)
        if 750 <= cibil_score <= 900 and is_12_paid:
            multipliers.append(170)
        if 750 <= cibil_score <= 900 and is_18_paid:
            multipliers.append(180)
        if 750 <= cibil_score <= 900 and is_24_paid:
            multipliers.append(190)
    if bank.lower() == "bajaj":
        if 720 <= cibil_score <= 750 and is_12_paid:
            multipliers.append(150)
        if 720 <= cibil_score <= 750 and is_15_paid:
            multipliers.append(160)
        if cibil_score> 720 and closed_6months:
            multipliers.append(90)
        if 750 <= cibil_score <= 900 and is_18_paid:
            multipliers.append(160)
        if 750 <= cibil_score <= 900 and is_24_paid:
            multipliers.append(180)
    if bank.lower() == "yes bank":
        if cibil_score > 600 and is_12_paid:
            multipliers.append(90)
        if cibil_score> 600 and closed_6months:
            multipliers.extend([90, 150, 160])
    if bank.lower() == "poonawala":
        # 700–725 band
        if 700 <= cibil_score <= 725 and is_12_paid:
            multipliers.append(150)
        if 700 <= cibil_score <= 725 and is_18_paid:
            multipliers.append(160)
        # (700–725 & 24 EMI) -> no multiplier given -> ignore

        # >700 & ML closed > 6 months
        if cibil_score > 700 and closed_6months:
            multipliers.append(90)

        # 725–750 band
        if 725 <= cibil_score <= 750 and is_12_paid:
            multipliers.append(160)
        if 725 <= cibil_score <= 750 and is_18_paid:
            multipliers.append(160)
        if 725 <= cibil_score <= 750 and is_24_paid:
            multipliers.append(170)

        # 750–900 band
        if 750 <= cibil_score <= 900 and is_12_paid:
            multipliers.append(160)
        if 750 <= cibil_score <= 900 and is_18_paid:
            multipliers.append(170)
        if 750 <= cibil_score <= 900 and is_24_paid:
            multipliers.append(200)
    if bank.lower() == "hdfc":
        # ignore: "CIBIL >600 & ≥12 EMI" (no multiplier given)

        # 700–725 band
        if 700 <= cibil_score <= 725 and is_12_paid:
            multipliers.append(120)
        if 700 <= cibil_score <= 725 and is_18_paid:
            multipliers.append(140)
        if 700 <= cibil_score <= 725 and is_24_paid:
            multipliers.append(150)

        # >700 & ML closed > 6 months
        if cibil_score > 700 and closed_6months:
            multipliers.append(90)

        # 725–750 band
        if 725 <= cibil_score <= 750 and is_12_paid:
            multipliers.append(140)
        if 725 <= cibil_score <= 750 and is_18_paid:
            multipliers.append(150)
        if 725 <= cibil_score <= 750 and is_24_paid:
            multipliers.append(160)

        # 750–900 band
        if 750 <= cibil_score <= 900 and is_12_paid:
            multipliers.append(150)
        if 750 <= cibil_score <= 900 and is_18_paid:
            multipliers.append(160)
        if 750 <= cibil_score <= 900 and is_24_paid:
            multipliers.append(180)


    # remove duplicates & sort
    return sorted(set(multipliers))


def inhand_capping_helper(data,bank,account_number):
    cibil_score = int(get_field("data.credit_score", data))
    print("CIBIL Score:", cibil_score)

    is_12_paid = has_12_or_more_emis(data, account_number)
    print("12 EMI Paid:", is_12_paid)

    closed_6months = is_closed_more_than_6_months(data, account_number)
    print("Closed > 6 months:", closed_6months)

    is_24_paid = has_24_or_more_emis(data, account_number)
    print("24 EMI Paid:", is_24_paid)

    
    is_18_paid = has_18_or_more_emis(data, account_number)
    print("18 EMI Paid:", is_24_paid)

    is_15_paid = has_15_or_more_emis(data,account_number)
    print("15 EMI Paid:", is_15_paid)
    cap_max = 0
    if bank == 'hero':
        cap_max = 1000000000000000000
    if bank == "piramal":
        cap_max = 1400000
    if bank == "idfc":
        cap_max = 1000000000000000000
    if bank == "axis":
        cap_max = 1000000000000000000
    if bank == "au":
        cap_max = 1000000000000000000
    if bank == "chola":
        cap_max = 1000000000000000000
    if bank == "tata":
        cap_max = 1000000000000000000
    if bank == "poonawala":
        cap_max = 1000000000000000000
    if bank == "hdfc":
        cap_max = 1000000000000000000
    if bank == "bajaj":
        if 720 <= cibil_score <= 750 and is_12_paid:
            cap_max = 1500000
        if 720 <= cibil_score <= 750 and is_15_paid:
            cap_max = 10000000000000000
        if cibil_score> 720 and closed_6months:
            cap_max = 10000000000000000
        if 750 <= cibil_score <= 900 and is_18_paid:
            cap_max = 1500000
        if 750 <= cibil_score <= 900 and is_24_paid:
            cap_max = 10000000000000000
    if bank == "yes bank":
        if cibil_score > 600 and is_12_paid:
            cap_max = 10000000000000000
        if cibil_score > 600 and closed_6months:
            cap_max = 3000000
    return cap_max

def get_amount_overdue(cibil_data: dict, account_number: str) -> int:
    """
    Fetch amountOverdue for a given account.
    Returns 0 if not found or invalid.
    """
    credit_reports = cibil_data.get("data", {}).get("credit_report", [])
    for report in credit_reports:
        for account in report.get("accounts", []):
            if account.get("accountNumber") == account_number:
                amount_str = account.get("amountOverdue", "0").strip()
                try:
                    return int(amount_str)
                except ValueError:
                    return 0
    return 0



API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0MzUxMzAwNiwianRpIjoiY2NjMWRiNDAtYjczZC00MzNhLWJhNWQtN2NjZGZmOTA1ZDcxIiwidHlwZSI6ImFjY2VzcyIsImlkZW50aXR5IjoidGVuYW50X3h6b3FkekVPS25oRnVOQmx6Z1FaIiwibmJmIjoxNzQzNTEzMDA2LCJleHAiOjIzNzQyMzMwMDYsImVtYWlsIjoiYmFkYWZpbmFuY2VfY29uc29sZUBzdXJlcGFzcy5pbyIsInRlbmFudF9pZCI6InRlbmFudF94em9xZHpFT0tuaEZ1TkJsemdRWiIsInVzZXJfY2xhaW1zIjp7InNjb3BlcyI6WyJ1c2VyIl19fQ.6xj-DckPMlnBb_ZS0kYoUsMyWmVFmcshy_Fz67veBOo"
def get_valuation_helper(vehicle_number):
    url = "https://kyc-api.surepass.app/api/v1/rc/rc-to-idv-details"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "id_number": vehicle_number
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # raises error if not 200
        result = response.json()
        
        if result.get("success"):
            return {
                "rc_number": result["data"]["rc_number"],
                "idv_value": result["data"]["idv_value"],
                "raw": result
            }
        else:
            return {"error": result.get("message", "Unknown error"), "raw": result}
    
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def la1_multiplier_helper(
    eligible_multipliers,
    res: dict,
    valuation,
    data: dict,
    account_number: str,
    bank: str = "hero",
):
    """
    LA1 computation for HERO and IDFC.

    HERO (R1/R2 gating):
      - only R1       -> allow {90}
      - only R2       -> allow {120}
      - both R1 & R2  -> allow {90} (lowest)
      - neither       -> allow {150, 180}
    Eligibility:
      - 90  -> cibil>600 and (>=12 EMI OR ML closed >6m)
      - 120 -> cibil>600 and >=12 EMI
      - 150 -> cibil>600 and >=12 EMI
      - 180 -> 750<=cibil<=900 and >=24 EMI

    IDFC:
      Eligibility & special rule:
      - cibil>600 & >=12 EMI         -> 120 (ONLY if any R2 present) AND 150
      - cibil>600 & ML closed >6m    -> 120 (no R2 required)
      - 750<=cibil<=900 & >=18 EMI   -> 170
      - 750<=cibil<=900 & >=24 EMI   -> 200
      No 90 for IDFC.
    """

    # --- helpers ---
    def has_r1() -> bool:
        return any(v == "R1" for v in res.values())

    def has_r2() -> bool:
        return any(v == "R2" for v in res.values())

    def safe_int(x, default=0):
        try:
            return int(float(x))
        except (TypeError, ValueError):
            return default

    def safe_float(x, default=0.0):
        try:
            return float(x)
        except (TypeError, ValueError):
            return default

    # inputs
    cibil_score = safe_int(get_field("data.credit_score", data), 0)
    val = safe_float(valuation, 0.0)

    # eligibility flags
    is_12_paid = has_12_or_more_emis(data, account_number)
    is_24_paid = has_24_or_more_emis(data, account_number)
    is_15_paid = has_15_or_more_emis(data, account_number)
    # for IDFC 170
    try:
        is_18_paid = has_18_or_more_emis(data, account_number)  # implement similar to 12/24 helper
    except NameError:
        # if you don't have it yet, fallback (treat as False)
        is_18_paid = False

    closed_6months = is_closed_more_than_6_months(data, account_number)

    r1, r2 = has_r1(), has_r2()

    results = {}

    # ---------------- HERO ----------------
    if bank.lower() == "hero":
        # determine allowed multipliers for HERO only
        if r1 and r2:
            allowed = {90}
        elif r1:
            allowed = {90}
        elif r2:
            allowed = {120}
        else:
            allowed = {150, 180}  # 180 still needs stronger eligibility

        for m in eligible_multipliers:
            amt = 0.0

            if m not in allowed:
                results[m] = 0
                continue

            if m == 90:
                # cibil>600 and (>=12 EMI OR ML closed >6m)
                if cibil_score > 600 and (is_12_paid or closed_6months):
                    amt = val * 0.90

            elif m == 120:
                # cibil>600 and >=12 EMI
                if cibil_score > 600 and is_12_paid:
                    amt = val * 1.20

            elif m == 150:
                # cibil>600 and >=12 EMI
                if cibil_score > 600 and is_12_paid:
                    amt = val * 1.50

            elif m == 180:
                # 750<=cibil<=900 and >=24 EMI
                if 750 <= cibil_score <= 900 and is_24_paid:
                    amt = val * 1.80

            results[m] = round(amt, 2) if amt else 0

        return results

    # ---------------- IDFC ----------------
    if bank.lower() == "idfc":
        
        # No separate "allowed set" by R1/R2; we decide per multiplier
        for m in eligible_multipliers:
            amt = 0.0

            if m == 120:
                # Path A: cibil>600 & >=12 EMI & R2 present (table says R2 required)
                cond_a = (cibil_score > 600 and is_12_paid and r2)
                # Path B: cibil>600 & ML closed > 6 months (no R2 required)
                cond_b = (cibil_score > 600 and closed_6months)

                if cond_a or cond_b:
                    amt = val * 1.20

            elif m == 150:
                # cibil>600 & >=12 EMI
                if cibil_score > 600 and is_12_paid:
                    amt = val * 1.50

            elif m == 170:
                # 750<=cibil<=900 & >=18 EMI
                if 750 <= cibil_score <= 900 and is_18_paid:
                    amt = val * 1.70

            elif m == 200:
                # 750<=cibil<=900 & >=24 EMI
                if 750 <= cibil_score <= 900 and is_24_paid:
                    amt = val * 2.00

            # Any multiplier not defined for IDFC (like 90, 180 if not needed) will remain 0
            results[m] = round(amt, 2) if amt else 0

        return results
    if bank.lower() == "piramal":
        for m in eligible_multipliers:
            amt = 0.0

            if m == 170:
                if cibil_score > 600 and is_12_paid:
                    amt = val * 1.70
            if m == 140:
                if cibil_score > 600 and closed_6months:
                    amt = val * 1.40
            if m ==200:
                if 750 <= cibil_score <= 900 and is_24_paid:
                    amt = val * 2.00
            results[m]= round(amt,2) if amt else 0
        return results


    if bank.lower() == "axis":
        for m in eligible_multipliers:
            amt = 0.0

            if m == 160:
                if cibil_score > 600 and is_18_paid:
                    amt = val * 1.60
            if m == 180:
                if cibil_score > 600 and is_24_paid:
                    amt = val * 1.80
            if m ==90:
                if cibil_score > 600 and closed_6months:
                    amt = val * 0.90
            if m == 160:
                if 750 <= cibil_score <= 900 and is_18_paid:
                    amt = val * 1.160
            if m == 180:
                if 750 <= cibil_score <= 900 and is_24_paid:
                    amt = val * 1.80
            results[m]= round(amt,2) if amt else 0
        return results
    if bank.lower() == "au":
        # determine allowed multipliers for HERO only
        if r1:
            allowed = {100}
        

        for m in eligible_multipliers:
            amt = 0.0

            if m not in allowed:
                results[m] = 0
                continue

            if m == 100:
                # cibil>600 and (>=12 EMI OR ML closed >6m)
                if cibil_score > 600 and (is_12_paid or closed_6months):
                    amt = val * 1.0
            results[m] = round(amt, 2) if amt else 0

        return results
    if bank.lower() == "chola":
        # determine allowed multipliers for HERO only
        if r1:
            allowed = {100}
        

        for m in eligible_multipliers:
            amt = 0.0

            if m not in allowed:
                results[m] = 0
                continue

            if m == 100:
                # cibil>600 and (>=12 EMI OR ML closed >6m)
                if cibil_score > 600 and (is_12_paid or closed_6months):
                    amt = val * 1.0
            results[m] = round(amt, 2) if amt else 0

        return results
    if bank.lower() == "tata":
        # determine allowed multipliers for HERO only
        for m in eligible_multipliers:
            amt = 0.0
            # 140: CIBIL 700–725 & ≥12 EMI
            if m == 140:
                if 700 <= cibil_score <= 725 and is_12_paid:
                    amt = val * 1.40
            if m == 150:
                if (700 <= cibil_score <= 725 and is_18_paid) or (725 <= cibil_score <= 750 and is_12_paid):
                    amt = val * 1.50
            if m == 160:
                if 700 <= cibil_score <= 725 and is_24_paid:
                    amt = val * 1.60
            if m == 90:
                if cibil_score > 700 and closed_6months:
                    amt = val * 0.90
            if m == 170:
                if (725 <= cibil_score <= 750 and is_18_paid) or (750 <= cibil_score <= 900 and is_12_paid):
                    amt = val * 1.70
            # 180: CIBIL 725–750 & ≥24 EMI OR 750–900 & ≥18 EMI
            if m == 180:
                if (725 <= cibil_score <= 750 and is_24_paid) or (750 <= cibil_score <= 900 and is_18_paid):
                    amt = val * 1.80
            # 190: CIBIL 750–900 & ≥24 EMI
            if m == 190:
                if 750 <= cibil_score <= 900 and is_24_paid:
                    amt = val * 1.90
            
            results[m] = round(amt, 2) if amt else 0

        return results
    if bank.lower() == "bajaj":
        # determine allowed multipliers for HERO only
        for m in eligible_multipliers:
            amt = 0.0
            # 140: CIBIL 700–725 & ≥12 EMI
            if m == 150:
                if 720 <= cibil_score <= 750 and is_12_paid:
                    amt = val * 1.50
            if m == 160:
                print("jsdhjshdjkshdkjshdkjshdkjshdjk")
                if (720 <= cibil_score <= 750 and is_15_paid) or (750 <= cibil_score <= 900 and is_18_paid):
                    print("sjdshdjkshdkajhdkjshdkajhkh")
                    amt = val * 1.60
            if m == 90:
                if cibil_score > 720 and closed_6months:
                    amt = val * 0.90
            if m == 180:
                if (750 <= cibil_score <= 900 and is_24_paid):
                    amt = val * 1.80
            results[m] = round(amt, 2) if amt else 0
        return results
    if bank.lower() == "yes bank":
        for m in eligible_multipliers:
            amt = 0.0

            if m == 90:
                if cibil_score > 600 and (is_12_paid or closed_6months):
                    amt = 0

            elif m == 150:
                if cibil_score > 600 and is_12_paid:
                    amt = val * 1.50

            elif m == 160:
                if cibil_score > 600 and is_12_paid:
                    amt = val * 1.60

            results[m] = round(amt, 2) if amt else 0

        return results
    if bank.lower() == "poonawala":
        for m in eligible_multipliers:
            amt = 0.0

            if m == 90:
                # CIBIL > 700 & ML loan closed > 6 months
                if cibil_score > 700 and closed_6months:
                    amt = val * 0.90

            elif m == 150:
                # CIBIL 700–725 & >=12 EMI
                if 700 <= cibil_score <= 725 and is_12_paid:
                    amt = val * 1.50

            elif m == 160:
                # Any of these:
                # - CIBIL 700–725 & >=18 EMI
                # - CIBIL 725–750 & >=12 EMI
                # - CIBIL 725–750 & >=18 EMI
                # - CIBIL 750–900 & >=12 EMI
                cond = (
                    (700 <= cibil_score <= 725 and is_18_paid) or
                    (725 <= cibil_score <= 750 and is_12_paid) or
                    (725 <= cibil_score <= 750 and is_18_paid) or
                    (750 <= cibil_score <= 900 and is_12_paid)
                )
                if cond:
                    amt = val * 1.60

            elif m == 170:
                # Any of these:
                # - CIBIL 725–750 & >=24 EMI
                # - CIBIL 750–900 & >=18 EMI
                cond = (
                    (725 <= cibil_score <= 750 and is_24_paid) or
                    (750 <= cibil_score <= 900 and is_18_paid)
                )
                if cond:
                    amt = val * 1.70

            elif m == 200:
                # CIBIL 750–900 & >=24 EMI
                if 750 <= cibil_score <= 900 and is_24_paid:
                    amt = val * 2.00
    
    if bank.lower() == "hdfc":
        for m in eligible_multipliers:
            amt = 0.0

            # direct formula for any eligible multiplier
            if cibil_score > 0:  # optional check, you can drop if not needed
                amt = val * (m / 100.0)

            results[m] = round(amt, 2) if amt else 0

        return results
    
    
    

    # default: if some other bank is passed unintentionally, return zeros for requested multipliers
    for m in eligible_multipliers:
        results[m] = 0
    return results
        
def la3_multiplier_helper(getmultiplier, data,abb,val, account_number,outstanding ,bank="hero"):
    """
    LA3 (HERO): purely formula-based, no `res` checks.
    Mapping from your table:
      - 90: NA (for both 12EMI case and closed>6m case) -> always "NA"
      - 120: (OLD_ML_EMI*2)/0.024 if (cibil > 600 and >=12 EMI)
      - 150: (OLD_ML_EMI*2)/0.024 if (cibil > 600 and >=12 EMI)
      - 180: (OLD_ML_EMI*2)/0.024 if (750<=cibil<=900 and >=24 EMI)
    `EMPTY` rows are ignored (treated as NA).
    """

    def safe_int(val, default=0):
        try:
            return int(float(val))
        except (TypeError, ValueError):
            return default

    # Get CIBIL safely
    cibil_score = safe_int(get_field("data.credit_score", data), default=0)

    # Eligibility conditions
    is_12_paid = has_12_or_more_emis(data, account_number)
    is_24_paid = has_24_or_more_emis(data, account_number)
    is_18_paid = has_18_or_more_emis(data, account_number)
    # closed_6months exists but LA3 uses NA for 90 (ML closed) so it's not used here
    closed_6months = is_closed_more_than_6_months(data, account_number)

    # Find OLD_ML_EMI for the given account
    old_ml_emi = None
    credit_reports = data.get("data", {}).get("credit_report", [])
    for report in credit_reports:
        for account in report.get("accounts", []):
            if account.get("accountNumber") == account_number:
                raw = account.get("emiAmount", "0")
                if isinstance(raw, str):
                    raw = raw.replace(",", "").strip()
                try:
                    old_ml_emi = float(raw)
                except (TypeError, ValueError):
                    old_ml_emi = None
                break

   

    results = {}
    if bank.lower() == "hero":
        for multiplier in getmultiplier:
            # default to "NA" for LA3 when case not applicable
            results[multiplier] = "NA"

            # 90 → NA (both 12-EMI and ML-closed rows are NA in LA3)
            if multiplier == 90:
                continue

            # 120 → (OLD_ML_EMI*2)*0.024 if cibil>600 and >=12 EMI
            if multiplier == 120:
                if cibil_score > 600 and is_12_paid and old_ml_emi is not None:
                    results[multiplier] = (old_ml_emi * 2) / 0.024
                continue

            # 150 → (OLD_ML_EMI*2)*0.024 if cibil>600 and >=12 EMI
            if multiplier == 150:
                if cibil_score > 600 and is_12_paid and old_ml_emi is not None:
                    results[multiplier] = (old_ml_emi * 2) / 0.024
                continue

            # 180 → (OLD_ML_EMI*2)*0.024 if 750<=cibil<=900 and >=24 EMI
            if multiplier == 180:
                if 750 <= cibil_score <= 900 and is_24_paid and old_ml_emi is not None:
                    results[multiplier] = (old_ml_emi * 2) / 0.024
                continue
        # ---------------- IDFC ----------------
    if bank.lower() == "idfc":
        for multiplier in getmultiplier:
            # default to NA
            results[multiplier] = "NA"

            # 120:
            #   - Path A: CIBIL>600 & >=12 EMI → VAL*1.20 (if ABB < 5000 => 0)
            #   - Path B: CIBIL>600 & ML closed >6m → VAL*1.20 (if ABB < 5000 => 0)
            if multiplier == 120:
                if (cibil_score > 600 and is_12_paid) or (cibil_score > 600 and closed_6months):
                    results[multiplier] = 0 if abb < 5000 else round(val * 1.20, 2)
                continue

            # 150:
            #   - CIBIL>600 & >=12 EMI → VAL*1.50 (if ABB < 5000 => 0)
            if multiplier == 150:
                if cibil_score > 600 and is_12_paid:
                    results[multiplier] = 0 if abb < 5000 else round(val * 1.50, 2)
                continue

            # 170:
            #   - 750<=CIBIL<=900 & >=18 EMI → ABB / 0.02379
            if multiplier == 170:
                if 750 <= cibil_score <= 900 and is_18_paid:
                    results[multiplier] = round(abb / 0.02379, 2)
                continue

            # 200:
            #   - 750<=CIBIL<=900 & >=24 EMI → (ABB*0.8) / 0.2379
            if multiplier == 200:
                if 750 <= cibil_score <= 900 and is_24_paid:
                    results[multiplier] = round((abb * 0.8) / 0.2379, 2)
                continue

    # -------- PIRAMAL ---------------------------------------------------------
    if bank.lower() == "piramal":
        for multiplier in getmultiplier:
            # default NA (EMPTY in your table)
            results[multiplier] = "NA"

            # Multiplier 170:
            # CIBIL > 600 & >=12 EMI paid -> ((ABB * 0.667 / 0.02485) + OUTSTANDING)
            if multiplier == 170:
                if cibil_score > 600 and is_12_paid:
                    results[multiplier] = round((abb * 0.667 / 0.02485) + outstanding, 2)
                continue

            # Multiplier 140:
            # CIBIL > 600 & ML loan closed > 6 months -> ((ABB * 0.667 / 0.02485))
            if multiplier == 140:
                if cibil_score > 600 and closed_6months:
                    results[multiplier] = round((abb * 0.667 / 0.02485), 2)
                continue

            # Multiplier 200:
            # 750 <= CIBIL <= 900 & >=24 EMI paid -> ((ABB / 0.02485) + OUTSTANDING)
            if multiplier == 200:
                if 750 <= cibil_score <= 900 and is_24_paid:
                    results[multiplier] = round((abb / 0.02485) + outstanding, 2)
                continue
    if bank.lower() == "axis":
        for multiplier in getmultiplier:
            # default NA (EMPTY in your table)
            results[multiplier] = "NA"

            # Multiplier 170:
            # CIBIL > 600 & >=12 EMI paid -> ((ABB * 0.667 / 0.02485) + OUTSTANDING)
            if multiplier == 160:
                if cibil_score > 600 and is_18_paid:
                    results[multiplier] = round((abb * 1.33 / 0.0243), 2)
                continue

            # Multiplier 140:
            # CIBIL > 600 & ML loan closed > 6 months -> ((ABB * 0.667 / 0.02485))
            if multiplier == 180:
                if cibil_score > 600 and is_24_paid:
                    results[multiplier] = round((abb * 1.33 / 0.0243), 2)
                continue
            if multiplier == 90:
                if cibil_score > 600 and closed_6months:
                    results[multiplier] = round((abb * 1.33 / 0.0243), 2)
                continue
            # Multiplier 200:
            # 750 <= CIBIL <= 900 & >=24 EMI paid -> ((ABB / 0.02485) + OUTSTANDING)
            if multiplier == 160:
                if 750 <= cibil_score <= 900 and is_18_paid:
                    results[multiplier] = round((abb * 1.33 / 0.0243), 2)
            if multiplier == 180:
                if 750 <= cibil_score <= 900 and is_24_paid:
                    results[multiplier] = round((abb * 1.33 / 0.0243), 2)
                continue
    # ---------------- AU (completed) ----------------
    if bank.lower() == "au":
        for multiplier in getmultiplier:
            results[multiplier] = "NA"
            # Only multiplier defined in your table for AU is 100
            if multiplier == 100:
                # Condition A: CIBIL > 600 & >=12 EMI
                cond_a = (cibil_score > 600 and is_12_paid)
                # Condition B: CIBIL > 600 & loan closed > 6 months
                cond_b = (cibil_score > 600 and closed_6months)
                if cond_a or cond_b:
                    # formula: (ABB * 1.33) / 0.0254
                    results[multiplier] = round((abb * 1.33) / 0.0254, 2)
                continue
            
    if bank.lower() == "chola":
        for multiplier in getmultiplier:
            results[multiplier] = "NA"
            # Only multiplier defined in your table for AU is 100
            if multiplier == 90:
                # Condition A: CIBIL > 600 & >=12 EMI
                cond_a = (cibil_score > 600 and is_12_paid)
                # Condition B: CIBIL > 600 & loan closed > 6 months
                cond_b = (cibil_score > 600 and closed_6months)
                if cond_a or cond_b:
                    # formula: (ABB * 1.33) / 0.0254
                    results[multiplier] = round((abb * 1.33) / 0.0254, 2)
                continue
    if bank.lower() == "tata":
        for multiplier in getmultiplier:
            results[multiplier] = "NA"   # default
            # 140: CIBIL 700–725 & ≥12 EMI
            # 140: CIBIL 700–725 & ≥12 EMI
            if multiplier == 140:
                if 700 <= cibil_score <= 725 and is_12_paid:
                    results[multiplier] = round((abb * 2) / 0.024, 2)
                continue

            # 150: CIBIL 700–725 & ≥18 EMI OR 725–750 & ≥12 EMI
            if multiplier == 150:
                if (700 <= cibil_score <= 725 and is_18_paid) or (725 <= cibil_score <= 750 and is_12_paid):
                    results[multiplier] = round((abb * 2) / 0.024, 2)
                continue

            # 160: CIBIL 700–725 & ≥24 EMI
            if multiplier == 160:
                if 700 <= cibil_score <= 725 and is_24_paid:
                    results[multiplier] = round((abb * 2) / 0.024, 2)
                continue

            # 90: CIBIL >700 & loan closed > 6 months
            if multiplier == 90:
                if cibil_score > 700 and closed_6months:
                    results[multiplier] = round((abb * 2) / 0.024, 2)
                continue

            # 170: CIBIL 725–750 & ≥18 EMI OR 750–900 & ≥12 EMI
            if multiplier == 170:
                if (725 <= cibil_score <= 750 and is_18_paid) or (750 <= cibil_score <= 900 and is_12_paid):
                    results[multiplier] = round((abb * 2) / 0.024, 2)
                continue

            # 180: CIBIL 725–750 & ≥24 EMI OR 750–900 & ≥18 EMI
            if multiplier == 180:
                if (725 <= cibil_score <= 750 and is_24_paid) or (750 <= cibil_score <= 900 and is_18_paid):
                    results[multiplier] = round((abb * 2) / 0.024, 2)
                continue

            # 190: CIBIL 750–900 & ≥24 EMI
            if multiplier == 190:
                if 750 <= cibil_score <= 900 and is_24_paid:
                    results[multiplier] = round((abb * 2) / 0.024, 2)
                continue
    if bank.lower() == "bajaj":
        for m in getmultiplier:
            results[m] = "NA"   # default

            # 150: 720–750 & ≥12 EMI
            if m == 150:
                if 720 <= cibil_score <= 750 and is_12_paid:
                    raw_val = (abb * 1.33) / 0.0238
                    cap_limit = (inhand_capping_helper(data, bank, account_number) or 0) + float(outstanding or 0)
                    results[m] = round(min(raw_val, cap_limit), 2)
                continue

            # 160: 750–900 & ≥18 EMI (720–750 & ≥15 EMI = NA)
            if m == 160:
                if 750 <= cibil_score <= 900 and is_18_paid:
                    raw_val = (abb * 1.33) / 0.0238
                    cap_limit = (inhand_capping_helper(data, bank, account_number) or 0) + float(outstanding or 0)
                    results[m] = round(min(raw_val, cap_limit), 2)
                continue

            # 90: >720 & closed > 6 months
            if m == 90:
                if cibil_score > 720 and closed_6months:
                    raw_val = (abb * 2) / 0.0238
                    cap_limit = (inhand_capping_helper(data, bank, account_number) or 0) + float(outstanding or 0)
                    results[m] = round(min(raw_val, cap_limit), 2)
                continue

            # 180: always NA in Bajaj table
            if m == 180:
                continue
    if bank.lower() == "yes bank":
        for multiplier in getmultiplier:
            # default NA (IGNORE/EMPTY in your table)
            results[multiplier] = "NA"

            # Table mapping (LA3 - YES):
            # 90 (>=12 EMI)     -> IGNORE  -> NA
            # 90 (ML closed)    -> EMPTY   -> NA
            # 150               -> ABB/0.0243 (cap at inhand_capping + outstanding)
            # 160               -> ABB/0.0243 (cap at inhand_capping + outstanding)

            if multiplier == 150:
                if cibil_score > 600 and is_12_paid:
                    cap_limit = (inhand_capping_helper(data, "yes", account_number) or 0) + float(outstanding or 0)
                    raw_val = abb / 0.0243
                    results[multiplier] = round(min(raw_val, cap_limit), 2)
                continue

            if multiplier == 160:
                if cibil_score > 600 and is_12_paid:
                    cap_limit = (inhand_capping_helper(data, "yes", account_number) or 0) + float(outstanding or 0)
                    raw_val = abb / 0.0243
                    results[multiplier] = round(min(raw_val, cap_limit), 2)
                continue
    if bank.lower() == "poonawala":
        for multiplier in getmultiplier:
            # same formula for 90, 150, 160, 170, 200, etc.
            results[multiplier] = round((abb * 1.33) / 0.024, 2)
        return results

    if bank.lower() == "hdfc":
        for m in getmultiplier:
            results[m] = round(abb / 0.02300, 2)
        return results


    return results
def la4_max_helper(getmultiplier: list, data: dict, account_number: str, bank: str = "hero"):
    """
    Compute LA4 MAX values for Hero / IDFC.

    getmultiplier : list of eligible multipliers (from get_multiplier_helper)
    data : customer data
    account_number : account number
    bank : which bank rules to apply (default hero)
    """
    results = {}

    # safe cibil fetch
    try:
        cibil_score = int(float(get_field("data.credit_score", data)))
    except (ValueError, TypeError):
        cibil_score = 0

    is_12_paid = has_12_or_more_emis(data, account_number)
    closed_6months = is_closed_more_than_6_months(data, account_number)
    is_24_paid = has_24_or_more_emis(data, account_number)
    is_15_paid = has_15_or_more_emis(data,account_number)
    # IDFC needs 18-EMI check
    try:
        is_18_paid = has_18_or_more_emis(data, account_number)
    except NameError:
        is_18_paid = False

    if bank.lower() == "hero":
        for multiplier in getmultiplier:
            score = 0

            if multiplier == 90:
                # Case 1: CIBIL > 600 & ≥12 EMI Paid
                if cibil_score > 600 and is_12_paid:
                    score = 1000000
                # Case 2: CIBIL > 600 & ML loan closed > 6 months
                elif cibil_score > 600 and closed_6months:
                    score = 2000000

            elif multiplier == 120:
                # Case 3: CIBIL > 600 & ≥12 EMI Paid
                if cibil_score > 600 and is_12_paid:
                    score = 2000000

            elif multiplier == 150:
                # Case 5: CIBIL > 600 & ≥12 EMI Paid
                if cibil_score > 600 and is_12_paid:
                    score = 2000000

            elif multiplier == 180:
                # Case 7: CIBIL 750–900 & ≥24 EMI Paid
                if 750 <= cibil_score <= 900 and is_24_paid:
                    score = 20000000

            results[multiplier] = score

        return results

    if bank.lower() == "idfc":
       
        for multiplier in getmultiplier:
            score = 0

            if multiplier == 120:
                # Path A: CIBIL > 600 & ≥12 EMI → 5,000,000
                if cibil_score > 600 and is_12_paid:
                    score = 5000000
                # Path B: CIBIL > 600 & ML closed > 6 months → 2,000,000
                elif cibil_score > 600 and closed_6months:
                    score = 2000000

            elif multiplier == 150:
                # CIBIL > 600 & ≥12 EMI → 5,000,000
                if cibil_score > 600 and is_12_paid:
                    score = 5000000

            elif multiplier == 170:
                # 750–900 & ≥18 EMI → 2,000,000
                if 750 <= cibil_score <= 900 and is_18_paid:
                    score = 2000000

            elif multiplier == 200:
                # 750–900 & ≥24 EMI → 2,000,000
                if 750 <= cibil_score <= 900 and is_24_paid:
                    score = 2000000

            # Unlisted/EMPTY cases → score stays 0
            results[multiplier] = score
    if bank.lower() == "piramal":
       
        for multiplier in getmultiplier:
            score = 0

            if multiplier == 170:
                # Path A: CIBIL > 600 & ≥12 EMI → 5,000,000
                if cibil_score > 600 and is_12_paid:
                    score = 1500000
                

            elif multiplier == 140:
                # CIBIL > 600 & ≥12 EMI → 5,000,000
                if cibil_score > 600 and closed_6months:
                    score = 1400000

            elif multiplier == 200:
                # 750–900 & ≥24 EMI → 2,000,000
                if 750 <= cibil_score <= 900 and is_24_paid:
                    score = 2000000

            # Unlisted/EMPTY cases → score stays 0
            results[multiplier] = score

        return results
    if bank.lower() == "axis":
       
        for multiplier in getmultiplier:
            score = 0

            if multiplier == 160:
                # Path A: CIBIL > 600 & ≥12 EMI → 5,000,000
                    score = 5000000
                

            elif multiplier == 180:
                    score = 5000000

            elif multiplier == 90:
                    score = 5000000
            elif multiplier == 160:
                    score = 5000000
            
            # Unlisted/EMPTY cases → score stays 0
            results[multiplier] = score

        return results
    if bank.lower() == "au":
        for multiplier in getmultiplier:
            score=0
            if multiplier == 100:
                score = 2000000
            results[multiplier] = score
        return results
    # default for other banks (not set): all zeros
    if bank.lower() == "chola":
        
        for multiplier in getmultiplier:
            score=0
            if multiplier == 90:
                
                score = 2000000
            results[multiplier] = score
        return results
    if bank.lower() == "tata":
        for m in getmultiplier:
            score = 0

            # 140: CIBIL 700–725 & ≥12 EMI
            if m == 140:
                if 700 <= cibil_score <= 725 and is_12_paid:
                    score = 3_500_000

            # 150: CIBIL 700–725 & ≥18 EMI OR 725–750 & ≥12 EMI
            elif m == 150:
                if (700 <= cibil_score <= 725 and is_18_paid) or (725 <= cibil_score <= 750 and is_12_paid):
                    score = 3_500_000

            # 160: CIBIL 700–725 & ≥24 EMI
            elif m == 160:
                if 700 <= cibil_score <= 725 and is_24_paid:
                    score = 3_500_000

            # 90: CIBIL >700 & loan closed >6m
            elif m == 90:
                if cibil_score > 700 and closed_6months:
                    score = 3_500_000

            # 170: CIBIL 725–750 & ≥18 EMI OR 750–900 & ≥12 EMI
            elif m == 170:
                if (725 <= cibil_score <= 750 and is_18_paid) or (750 <= cibil_score <= 900 and is_12_paid):
                    score = 3_500_000

            # 180: CIBIL 725–750 & ≥24 EMI OR 750–900 & ≥18 EMI
            elif m == 180:
                if (725 <= cibil_score <= 750 and is_24_paid) or (750 <= cibil_score <= 900 and is_18_paid):
                    score = 3_500_000

            # 190: CIBIL 750–900 & ≥24 EMI
            elif m == 190:
                if 750 <= cibil_score <= 900 and is_24_paid:
                    score = 3_500_000

            results[m] = score
        return results
    if bank.lower() == "bajaj":
        for m in getmultiplier:
            score = 0

            # 150: 720–750 & ≥12 EMI
            if m == 150:
                if 720 <= cibil_score <= 750 and is_12_paid:
                    score = 2_500_000

            # 160: 720–750 & ≥15 EMI OR 750–900 & ≥18 EMI
            elif m == 160:
                if (720 <= cibil_score <= 750 and is_15_paid):
                    score = 1_500_000
                elif (750 <= cibil_score <= 900 and is_18_paid):
                    score = 2_500_000

            # 90: >720 & closed >6 months
            elif m == 90:
                if cibil_score > 720 and closed_6months:
                    score = 1_500_000

            # 180: 750–900 & ≥24 EMI
            elif m == 180:
                if 750 <= cibil_score <= 900 and is_24_paid:
                    score = 1_500_000

            results[m] = score
        return results
    if bank.lower() == "yes bank":
        for m in getmultiplier:
            score = 0

            # 150: 720–750 & ≥12 EMI
            if m == 150:
                score = 7500000

            # 160: 720–750 & ≥15 EMI OR 750–900 & ≥18 EMI
            elif m == 160:
                score = 7500000
            results[m] = score
        return results
    
    if bank.lower() == "poonawala":
        for m in getmultiplier:
            results[m]= 3500000
        return results
    if bank.lower() == "hdfc":
        for m in getmultiplier:
            results[m]= 3500000
        return results
    for m in getmultiplier:
        results[m] = 0
    return results


def la2_abb_helper(getmultiplier: list, data: dict, account_number: str,abb, bank: str = "hero"):
    """
    Compute LA2-ABB values for Hero.
    For Hero, all cases are NA or EMPTY, so results = "NA".
    """
    results = {}

    if bank.lower() == "hero":
        for multiplier in getmultiplier:
            results[multiplier] = "NA"  # Explicitly mark as NA
    if bank.lower() == "idfc":
        for multiplier in getmultiplier:
            results[multiplier] = "NA"  # Explicitly mark as NA
    if bank.lower() == "piramal":
        for multiplier in getmultiplier:
            results[multiplier] = "NA"  # Explicitly mark as NA
    if bank.lower() == "axis":
        for multiplier in getmultiplier:
            results[multiplier] = "NA"  # Explicitly mark as NA
    if bank.lower() == "au":
        for multiplier in getmultiplier:
            results[multiplier] = "NA"
    if bank.lower() == "chola":
        for multiplier in getmultiplier:
            results[multiplier] = "NA"
    if bank.lower() == "tata":
        for multiplier in getmultiplier:
            results[multiplier] = "NA"
    if bank.lower() == "tata":
        for multiplier in getmultiplier:
            results[multiplier] = "NA"
    if bank.lower() == "bajaj":
        for multiplier in getmultiplier:
            if multiplier == 150:
                results[multiplier]=abb
            else:
                results[multiplier] = "NA"
    if bank.lower() == "yes bank":
        for multiplier in getmultiplier:
            results[multiplier]= "NA"
    if bank.lower() == "poonawala":
        for multiplier in getmultiplier:
            results[multiplier]="NA"
    if bank.lower() == "hdfc":
        for multiplier in getmultiplier:
            results[multiplier]="NA"


    return results




def la5_lowest_helper(la1: dict, la2: dict, la3: dict, la4: dict, bank: str = "hero"):
    """
    Compute LA5 - Lowest of LA1 to LA4 for Hero.
    
    la1, la2, la3, la4: dict outputs from respective helpers
    bank: which bank rules to apply (default hero)
    """
    results = {}

    
    all_multipliers = set(la1.keys()) | set(la2.keys()) | set(la3.keys()) | set(la4.keys())
    for multiplier in all_multipliers:
        values = []
        # collect only valid (non-NA, non-empty) values
        if la1.get(multiplier) not in (None, 0, "NA"):
            values.append(la1[multiplier])
        if la2.get(multiplier) not in (None, 0, "NA"):
            values.append(la2[multiplier])
        if la3.get(multiplier) not in (None, 0, "NA"):
            values.append(la3[multiplier])
        if la4.get(multiplier) not in (None, 0, "NA"):
            values.append(la4[multiplier])
        # choose lowest if there are valid values
        results[multiplier] = min(values) if values else "NA"

    return results


def get_value_phase2(pan_number,
    vehicle_number,
    account_number=None,
    abb_hero=None,
    abb_idfc=None,
    abb_piramal=None,
    abb_axis=None,
    abb_au=None,
    abb_chola=None,
    abb_tata=None,
    abb_bajaj=None,
    abb_yes_bank=None,
    abb_poonawala=None,
    abb_hdfc=None):
    # Get CIBIL data
    cibil_data = get_cibil_data(pan_number)

    # Get car data
    rc_api_url = "https://api-rc-cibil-ei8h.onrender.com/fetch_car"
    payload = {"id_number": vehicle_number}
    headers = {"Content-Type": "application/json"}
    response = requests.post(rc_api_url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception("RC API call failed")

    data_car = response.json()

    data = {
    "bounces0_3": 1,
    "bounces4_7": 2,
    "bounces8_12": 3,
    "bounces13_24": 0,
    "bounces24_60": 7,
    "bounces0_6": 5,
    "bounces0_12":5
    }
    banks = [
    "hero", "idfc", "piramal", "axis", "au",
    "chola", "tata", "bajaj", "yes bank",
    "poonawala", "hdfc"
    ]
    
    print("PAN Number:", pan_number)
    print("Vehicle Number:", vehicle_number)
    print("Account Number:", account_number)
    print("ABB Hero:", abb_hero)
    print("ABB IDFC:", abb_idfc)
    print("ABB Piramal:", abb_piramal)
    print("ABB Axis:", abb_axis)
    print("ABB AU:", abb_au)
    print("ABB Chola:", abb_chola)
    print("ABB Tata:", abb_tata)
    print("ABB Bajaj:", abb_bajaj)
    print("ABB Yes Bank:", abb_yes_bank)
    print("ABB Poonawala:", abb_poonawala)
    print("ABB HDFC:", abb_hdfc)
    



    
    ABB = 0
    for bank in banks:
        print(f"\n====================== {bank.upper()} ======================")
        if bank.lower() == "hero":
            ABB = abb_hero
        elif bank.lower() == "idfc":
            ABB = abb_idfc
        elif bank.lower() == "piramal":
            ABB = abb_piramal
        elif bank.lower() == "axis":
            ABB = abb_axis
        elif bank.lower() == "au":
            ABB = abb_au
        elif bank.lower() == "chola":
            ABB = abb_chola
        elif bank.lower() == "tata":
            ABB = abb_tata
        elif bank.lower() == "bajaj":
            ABB = abb_bajaj
        elif bank.lower() == "yes bank":
            ABB = abb_yes_bank
        elif bank.lower() == "poonawala":
            ABB = abb_poonawala
        elif bank.lower() == "hdfc":
            ABB = abb_hdfc
        else:
            ABB = 0  # fallback if unknown bank


        print(f"Using ABB for {bank.upper()}: {ABB}")

        getmultiplier = get_multiplier_helper(cibil_data, account_number, bank)
        print("get multiplier:", getmultiplier)

        inhand_capping = inhand_capping_helper(cibil_data, bank, account_number)
        print("inhand_capping:", inhand_capping)

        res = classify_mother_bounces(bank, data)
        print("res:", res)

        amount_overdue = get_amount_overdue(cibil_data, account_number)
        print("Amount Overdue:", amount_overdue)

        valuation_details = get_valuation_helper(vehicle_number)
        valuation = float(valuation_details["idv_value"])
        print("valuation of car:", valuation)

        la1_multiplier = la1_multiplier_helper(getmultiplier, res, valuation, cibil_data, account_number, bank=bank)
        print("LA1:", la1_multiplier)

        la2_scores = la2_abb_helper(getmultiplier, cibil_data, account_number, ABB, bank=bank)
        print("LA2:", la2_scores)

        la3_scores = la3_multiplier_helper(getmultiplier, cibil_data, ABB, valuation, account_number, amount_overdue, bank=bank)
        print("LA3:", la3_scores)

        la4_scores = la4_max_helper(getmultiplier, cibil_data, account_number, bank=bank)
        print("LA4:", la4_scores)

        la5_scores = la5_lowest_helper(la1_multiplier, la2_scores, la3_scores, la4_scores, bank=bank)
        print("LA5:", la5_scores)
    # Combine and return data
    return {
        "cibil_data": cibil_data,
        "vehicle_data": data_car
    }
