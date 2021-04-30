import pandas as pd

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    fields = ['Text for Training', 'Category', 'Sub Category', 'Case Subject', 'Language']
    category_fields = ['Category', 'Sub Category']

    file_data = pd.read_csv('qa-training-data-2021-04-28.csv', usecols=fields)

    file_data['Sub Category'] = file_data['Sub Category'].fillna('')
    file_data['Category'] = file_data['Category'].fillna('')
    file_data['Text for Training'] = file_data['Text for Training'].fillna('')
    file_data['Language'] = file_data['Language'].fillna('')
    file_data['Case Subject'] = file_data['Case Subject'].fillna('')

    # Remove duplicates
    file_data = file_data.drop_duplicates(subset=['Text for Training'])

    # Initialize Data
    data = {
        'Text for Training': [],
        'Category': [],
        'Sub Category': [],
        'Case Subject': [],
        'Language': []
    }

    count_file = pd.read_csv('split_total.csv')
    count_file['Sub Category'] = count_file['Sub Category'].fillna('')
    desired_output = []
    for count_row in count_file.itertuples():
        count = 0
        for row in file_data.itertuples():
            if row[2] == count_row[1] and row[3] == count_row[2]:
                if count < count_row[4]:
                    data['Text for Training'].append(row[1])
                    data['Category'].append(row[2])
                    data['Sub Category'].append(row[3])
                    data['Case Subject'].append(row[4])
                    data['Language'].append(row[5])
                    count += 1
                else:
                    break

    # Desired Output File
    df = pd.DataFrame(data)
    df.to_csv('split_english_data.csv', index=False)
