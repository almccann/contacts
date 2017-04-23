import csv

google = 'google.csv'
new_apple = 'new_apple.vcf'

with open(google, encoding='utf-16') as google_csv, open(new_apple, 'w') as apple_writer:
    google_reader = csv.reader(google_csv)
    fieldnames = next(google_reader)
    google_dict_reader = csv.DictReader(google_csv, fieldnames=fieldnames)

    for row in google_dict_reader:
        if row['Phone 1 - Type'] == 'Mobile':
            row['Phone 1 - Type'] = 'CELL'
        if row['Phone 2 - Type'] == 'Mobile':
            row['Phone 2 - Type'] = 'CELL'
        if row['Phone 3 - Type'] == 'Mobile':
            row['Phone 3 -Type'] = 'CELL'
        if row['Group Membership'] != '* My Contacts':
            row['Group Membership'] = row['Group Membership'][18:].replace(' ::: ', ',')

        email1 = 'EMAIL;TYPE=INTERNET;TYPE=' + row['E-mail 1 - Type'][2:].upper() + ':' + row['E-mail 1 - Value'] + '\n' if row['E-mail 1 - Value'] else ''
        email2 = 'EMAIL;TYPE=INTERNET;TYPE=' + row['E-mail 2 - Type'].upper() + ':' + row['E-mail 2 - Value'] + '\n' if row['E-mail 2 - Value'] else ''
        email3 = 'EMAIL;TYPE=INTERNET;TYPE=' + row['E-mail 3 - Type'].upper() + ':' + row['E-mail 3 - Value'] + '\n' if row['E-mail 3 - Value'] else ''
        phone1 = 'TEL;TYPE=' + row['Phone 1 - Type'] + ':' + row['Phone 1 - Value'] + '\n' if row['Phone 1 - Value'] else ''
        phone2 = 'TEL;TYPE=' + row['Phone 2 - Type'] + ':' + row['Phone 2 - Value'] + '\n' if row['Phone 2 - Value'] else ''
        phone3 = 'TEL;TYPE=' + row['Phone 3 - Type'] + ':' + row['Phone 3 - Value'] + '\n' if row['Phone 3 - Value'] else ''
        org = 'ORG:' + row['Organization 1 - Name'] + '\n' if row['Organization 1 - Name'] else ''
        title = 'TITLE:' + row['Organization 1 - Title'] + '\n' if row['Organization 1 - Title'] else ''
        groups = 'CATEGORIES:' + row['Group Membership'] + '\n' if row['Group Membership'] != '* My Contacts' else ''

        record = 'BEGIN:VCARD\n' + \
                'VERSION:3.0\n' + \
                'FN:' + row['Name'] + '\n' + \
                'N:' + row['Family Name'] + ';' + row['Given Name'] + ';;;\n' + \
                email1 + \
                email2 + \
                email3 + \
                phone1 + \
                phone2 + \
                phone3 + \
                org + \
                title + \
                groups + \
                'END:VCARD\n'

        apple_writer.write(record)
