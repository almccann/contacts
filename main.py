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
                print('dupe found!', row['FirstName'], row['LastName'])
                dupe = row

        return dupe         

with open(google, encoding='utf-16') as google_csv, open(new_google, 'w', encoding='utf-16') as new_google_csv:
    google_reader = csv.reader(google_csv)
    fieldnames = next(google_reader)
    google_dict_reader = csv.DictReader(google_csv, fieldnames=fieldnames)
    google_writer = csv.DictWriter(new_google_csv, fieldnames)
    google_writer.writeheader()

    for row in google_dict_reader:
        dupe = return_linkedin_dupe(row['Family Name'], row['Given Name'])
        if dupe: 
            tags = dupe['Tags'][1:-1].split(', ') 
            for tag in tags:
                print('adding ' + tag + ' to ' + row['Given Name'] + ' ' + row['Family Name'])
                row['Group Membership'] += ' ::: ' + tag 
        google_writer.writerow(row)
