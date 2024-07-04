#Function to fix phone number format in the database
def fix_phone_number(phone):
    #if phone starts with 0 then remove 0 and add +254 or if phone starts with 7 then add +254
    if phone[0] == "0":
        phone = "+254" + phone[1:]
    elif phone[0:3] == "254":
        phone = "+" + phone
    elif phone[0] > "0" and phone[0] <= "7":
        phone = "+254" + phone
    return phone