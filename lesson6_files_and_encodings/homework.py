import json
import csv
import openpyxl


""" 1 """
byte_string = b'r\xc3\xa9sum\xc3\xa9'
utf8_encoded_string = byte_string.decode(encoding='utf-8')
print(utf8_encoded_string)

latin1_byte_string = utf8_encoded_string.encode(encoding='latin1')
print(latin1_byte_string)

latin1_encoded_string = latin1_byte_string.decode(encoding='latin1')
print(latin1_encoded_string)

""" 2 """
# file_path = 'homework_task2.txt'
# input_words = input('Введите 4 слова через пробел: ')
# a, b, c, d = input_words.split()
#
#
# with open(file_path, 'w', encoding='utf-8') as write_file:
#     for word in a, b:
#         write_file.write(word + '\n')
#
# with open(file_path, 'a', encoding='utf-8') as edit_file:
#     for word in c, d:
#         edit_file.write(word + '\n')

""" 3 """
dict_ = {
    111111: ('Alex', 34),
    111112: ('Olga', 8),
    111113: ('Ann', 32),
    111114: ('Andrew', 35),
    111115: ('Irina', 57),
    111116: ('George', 20)
}

def write_dict_to_json(file_name, some_dict):
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(some_dict, json_file, indent=4)

# write_dict_to_json('homework_task3.json', dict_)

""" 4 """
def load_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as read_file:
        json_dict = json.load(read_file)
        return json_dict

def write_json_to_csv(file_name, json_data: dict):
    with open(file_name, 'w', encoding='utf-8') as csv_file:
        file_writer = csv.writer(csv_file, delimiter=",", lineterminator="\n")
        file_writer.writerow(["id", "name", "age", "phone"])

        for num, (id_, (name, age)) in enumerate(json_data.items()):
            phone = f'+375-44-500-55-5' + (num if num >= 10 else f"0{num}")
            file_writer.writerow(
                [id_, name, age, phone]
            )

json_ = load_json('files/homework_task3.json')
write_json_to_csv('files/homework_task4.csv', json_data=json_)

""" 5 """
def from_csv_to_excel(csv_f_name, excel_f_name):
    wb = openpyxl.Workbook()
    sheet = wb.active

    with open(csv_f_name, 'r', encoding='utf-8') as rfile:
        csv_lines = list(csv.reader(rfile, delimiter=","))

        persons_columns = [f'Person_{i}' for i in range(1, len(csv_lines))]
        ids_list = [group[0] for group in csv_lines]
        names_list = [group[1] for group in csv_lines]
        phones_list = [group[-1] for group in csv_lines]

        persons_columns.insert(0, '')
        for lines in persons_columns, ids_list, names_list, phones_list:
            sheet.append(lines)


        # row_names = list(filter(lambda n: n != 'age', next(file_reader)))
        # for i, name in enumerate(row_names, start=start_index):
        #     sheet.cell(row=i, column=1).value = name
        #
        # for idx, (id_, name, _, phone) in enumerate(file_reader, start=start_index):
        #     sheet.cell(row=1, column=idx).value = f'Person{idx - 1}'
        #
        #     for row_num, item in enumerate((id_, name, phone), start=start_index):
        #         sheet.cell(row=row_num, column=idx).value = item

    wb.save(excel_f_name)


from_csv_to_excel(csv_f_name='homework_task4.csv', excel_f_name='homework_task112.xlsx')


