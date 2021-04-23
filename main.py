import pandas as pd
import glob


def normalize(arr, t_min, t_max):
    norm_arr = []
    diff = t_max - t_min
    diff_arr = max(arr) - min(arr)
    for i in arr:
        temp = (((i - min(arr)) * diff) / diff_arr) + t_min
        norm_arr.append(temp)
    return norm_arr


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    fields = ['Text for Training', 'Category', 'Sub Category', 'Case Subject', 'Language']
    category_fields = ['Category', 'Sub Category']
    all_files = glob.glob('Cleaning' + "/*.csv")

    file_data = pd.DataFrame()
    for filename in all_files:
        read_file = pd.read_csv(filename, usecols=fields)
        file_data = pd.concat([file_data, read_file], axis=0)

    file_data['Sub Category'] = file_data['Sub Category'].fillna('')
    file_data['Category'] = file_data['Category'].fillna('')
    file_data['Text for Training'] = file_data['Text for Training'].fillna('')
    file_data['Language'] = file_data['Language'].fillna('')
    file_data['Case Subject'] = file_data['Case Subject'].fillna('')
    file_data = file_data[((file_data['Text for Training'] != '') &
                           (file_data['Category'] == 'Other') &
                           ((file_data['Sub Category'] == 'COVID-19') |
                            (file_data['Sub Category'] == 'Duplicate') |
                            (file_data['Sub Category'] == 'Physical Return') |
                            (file_data['Sub Category'] == 'Rebilling'))) |
                          ((file_data['Category'] == 'Customer Care Support') &
                           ((file_data['Sub Category'] == 'General Support') |
                            (file_data['Sub Category'] == 'Masterdata Update') |
                            (file_data['Sub Category'] == 'OTIF') |
                            (file_data['Sub Category'] == 'Tolerance'))) |
                          ((file_data['Category'] == 'Complaint') &
                           ((file_data['Sub Category'] == 'Log') |
                            (file_data['Sub Category'] == 'Follow up'))) |
                          ((file_data['Sub Category'] == '') & ((file_data['Category'] == 'Documentation') |
                                                                (file_data['Category'] == 'Order Amendment') |
                                                                (file_data['Category'] == 'Distribution') |
                                                                (file_data['Category'] == 'Product Enquiry') |
                                                                (file_data['Category'] == 'Pricing') |
                                                                (file_data['Category'] == 'Credit/Debit Request') |
                                                                (file_data['Category'] == 'New Order')))]

    # Get Count of each category ans sub-category
    # subcategory_data = pd.DataFrame(file_data.pivot_table(index=category_fields, aggfunc='size'))
    # subcategory_data.rename(columns={0: 'Count'}, inplace=True)

    # Normalized the Array
    # normalized_array_1d = normalize(subcategory_data['Count'].values,
    #                                 min(subcategory_data['Count'].values),
    #                                 25000)
    # subcategory_data['Normalized Count'] = [int(a) for a in normalized_array_1d]

    # Count Output File
    # subcategory_data.to_csv('output.csv')

    # Desired Output File

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

    count_file = pd.read_csv('output_normalized.csv')
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
        print(count_row[1] + " " + count_row[2] + " " + str(count))

    # Desired Output File
    # df = pd.DataFrame(data)
    # df.to_csv('remove_dup.csv', index=False)
