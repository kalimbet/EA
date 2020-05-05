user_id = ""
name = ""
surname = ""
address = ""
residence_country = ""
nationality = ""
sex = ""
email = ""
password = ""
phone_number = ""
birthday_date = ""
role_id = ""
registration_date = ""


hi_user_str = "Hi, "


text_for_testing = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

def get_role_name():
    roles_dic = {
        '1': "Employee",
        '2': "Administrator",
        '3': "Project Manager",
        '4': "Leader",
        '5': "Boss"
    }
    return roles_dic.get(role_id)
