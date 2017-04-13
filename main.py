import csv

google = 'google.csv'
linkedin = 'linkedin.csv'
new_google = 'new_google.csv'

def return_linkedin_dupe(last_name, first_name):
    with open(linkedin, encoding='utf-8') as linkedin_csv:
        reader = csv.DictReader(linkedin_csv)
        dupe = None
        for row in reader:
            if last_name == row['LastName'] and first_name == row['FirstName']:
                dupe = row

        return dupe         

def return_google_dupe(last_name, first_name):
    with open(google, encoding='utf-16') as google_csv:
        reader = csv.DictReader(google_csv)
        dupe = None
        for row in reader:
            if last_name == row['Family Name'] and first_name == row['Given Name']:
                dupe = row

        return dupe

with open(linkedin, encoding='utf-8') as linkedin_csv, open(google, encoding='utf-16') as google_csv, open(new_google, 'w', encoding='utf-16') as new_google_csv:
    google_reader = csv.reader(google_csv)
    fieldnames = next(google_reader)
    google_dict_reader = csv.DictReader(google_csv, fieldnames=fieldnames)
    linkedin_dict_reader = csv.DictReader(linkedin_csv)
    google_writer = csv.DictWriter(new_google_csv, fieldnames)
    google_writer.writeheader()

    # update duplicate (exiting) Google contacts with LinkedIn tags and additional information
    for row in google_dict_reader:
        dupe = return_linkedin_dupe(row['Family Name'], row['Given Name'])
        if dupe: 
            print('updating existing Google contact ' + row['Given Name'] + ' ' + row['Family Name'])
            tags = dupe['Tags'][1:-1].split(', ') 
            for tag in tags:
                row['Group Membership'] += ' ::: ' + tag 
            row['Organization 1 - Title'] = dupe['Position']
            row['Organization 1 - Name'] = dupe['Company']
            if not row['E-mail 1 - Value']:
                row['E-mail 1 - Value'] = dupe['EmailAddress']
                row['E-mail 1 - Type'] = '* Work'
            elif not row['E-mail 2 - Value']:
                row['E-mail 2 - Value'] = dupe['EmailAddress']
                row['E-mail 2 - Type'] = '* Work'
            elif not row['E-mail 3 - Value']:
                row['E-mail 3 - Value'] = dupe['EmailAddress']
                row['E-mail 3 - Type'] = '* Work'
            else:
                row['E-mail 4 - Value'] = dupe['EmailAddress']
                row['E-mail 4 - Type'] = '* Work'
        google_writer.writerow(row)
       
    # add new LinkedIn connections to Google contacts
    for row in linkedin_dict_reader:
        dupe = return_google_dupe(row['LastName'], row['FirstName'])
        # connection not in Google
        if dupe is None and row['EmailAddress']:
            print('adding new Google contact ' + row['FirstName'] + ' ' + row['LastName'])
            tags = row['Tags'][1:-1]
            tag = '* My Contacts'
            if tags:
                tag += ' ::: ' + tags.replace(', ', ' ::: ')
            google_writer.writerow({
                'Name': row['FirstName'] + ' ' + row['LastName'],
                'Given Name': row['FirstName'],
                'Family Name': row['LastName'],
                'Group Membership': tag,
                'E-mail 1 - Type': '* Work',
                'E-mail 1 - Value': row['EmailAddress']
                })
