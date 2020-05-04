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


def get_role_name():
    roles_dic = {
        '1': "Employee",
        '2': "Administrator",
        '3': "Project Manager",
        '4': "Leader",
        '5': "Boss"
    }
    return roles_dic.get(role_id)
