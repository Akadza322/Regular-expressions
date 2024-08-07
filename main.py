from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re
import os
import operator
import itertools
    
def read_csv(file_name):
    contact_dict = []
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    keys = contacts_list[0]
    values = contacts_list[1:]
    for num, vals in enumerate(values):
        contact_dict.append({})
        for key, val in zip(keys, vals):
            contact_dict[num].update({key: val})
    return contact_dict


def name_fix(in_file):
    contact_dict = read_csv(in_file)
    for a in contact_dict:
        split = a['lastname'].split(' ')
        if len(split) > 1:
            a['lastname'] = split[0]
            a['firstname'] = split[1]
            if len(split) > 2:
                a['surname'] = split[2]

        split = a['firstname'].split(' ')
        if len(split) > 1:
            a['firstname'] = split[0]
            a['surname'] = split[1]
    return contact_dict


def fix_phone(in_file, out_file):
    with open(in_file, encoding="utf8") as f:
        text = f.read()

    pattern_phone = r'(\+7|8)?\s*\(?(\d{3})\)?[\s*-]?(\d{3})[\s*-]?(\d{2})[\s*-]?(\d{2})(\s*)\(?(доб\.?)?\s*(\d*)?\)?'
    fixed_phones = re.sub(pattern_phone, r'+7(\2)\3-\4-\5\6\7\8', text)
    print(fixed_phones)
    with open(out_file, 'w+', encoding="utf8") as f:
        text = f.write(fixed_phones)


def merge_info(contact):
    all_keys = set(contact[0].keys())
    group_list = ['firstname', 'lastname']
    group = operator.itemgetter(*group_list)
    cols = operator.itemgetter(*(all_keys ^ set(group_list)))
    contact.sort(key=group)
    grouped = itertools.groupby(contact, group)

    merge_data = []
    for (firstname, lastname), g in grouped:
        merge_data.append({'lastname': lastname, 'firstname': firstname})
        for gr in g:
            d1 = merge_data[-1]
            for k, v in gr.items():
                if k not in d1 or d1[k] == '':
                    d1[k] = v

    return merge_data


def write_file(file_name, dicts):
    keys = list(dicts[0].keys())
    with open(file_name, "w", encoding="utf8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerow(keys)
        for d in dicts:
            datawriter.writerow(d.values())


def main():
    fix_phone(in_file="phonebook_raw.csv", out_file="phonebook_fixed.csv")
    fixed_names = name_fix(in_file="phonebook_fixed.csv")
    os.remove("phonebook_fixed.csv")
    merged_info = merge_info(fixed_names)
    write_file("phonebook.csv", merged_info)


if __name__ == '__main__':
    main()