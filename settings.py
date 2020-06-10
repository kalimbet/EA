host = "26.26.247.174"
#host = "localhost"
port = "3000"



menuIndex = 1
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

selected_user_id = ""
selected_user_name = "Name"
selected_user_surname = "Surname"
selected_user_address = ""
selected_user_email = ""
selected_residence_country = ""
selected_nationality = ""
selected_sex = ""
selected_email = ""
selected_password = ""
selected_phone_number = ""
selected_birthday_date = ""
selected_role_id = ""
selected_registration_date = ""


pm_selected_group_id = ""
pm_selected_group_name = "p31"
pm_selected_group_description = "Some group"
pm_selected_group_leader_name = "John"
pm_selected_group_leader_surname = "Smith"


selected_user_last_email = ""


question_status = ''
hi_user_str = "Hi, "

new_user_photo = False

list_employee_for_days = [1, 1, 1, 1, 1]
list_employee_for_weeks = [1, 1, 1, 1]
list_employee_for_months = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

list_leader_for_days = [1, 1, 1, 1, 1]
list_leader_for_weeks = [1, 1, 1, 1]
list_leader_for_months = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

list_of_all_groups = []

recomendation_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
question_text = "Did you finish your task for day?"
question_text_yes = "You have completed the task for day."
question_text_no = "You have not completed the task for day."


employee_average_rating_for_week = '0.0'
employee_average_rating_for_month = '0.0'
employee_average_rating_for_year = '0.0'

average_max_week = '7'
average_max_month = '35'
average_max_year = '140'

leader_name = ''
leader_surname = ''

list_of_users = {}
list_user_last_week = {}
list_leader_last_week = {}
#list_of_groups = {}

zip_name = 'dataset.zip'

def get_role_name(role_id):
    roles_dic = {
        '1': "Employee",
        '2': "Administrator",
        '3': "Project Manager",
        '4': "Leader",
        '5': "Boss"
    }
    return roles_dic.get(role_id)

def get_sex_name(sex_id):
    sex_dic = {
        '1': "Male",
        '2': "Female",
    }
    return sex_dic.get(sex_id)

def get_name_week(day_num):
    name_week_dic = {
        '0': "Monday",
        '1': "Tuesday",
        '2': "Wednesday",
        '3': "Thursday",
        '4': "Friday",
        '5': "Saturday",
        '6': "Sunday",
    }
    return name_week_dic.get(day_num)
