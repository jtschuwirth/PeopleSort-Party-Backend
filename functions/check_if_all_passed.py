def check_if_all_passed(table):
    scan_response = table.scan()
    have_passed = [item["turn_status"] for item in scan_response['Items']]
    if "playing" in have_passed:
        return False
    else:
        return True
