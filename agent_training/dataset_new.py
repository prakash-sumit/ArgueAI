import csv

# Initialize empty lists for rules and cases
rules = []
all_cases = []

# Open and read the CSV file
with open('/Users/sumitprakash/Desktop/ArgueAI_ppo/agent_training/dataset_updated.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    # Skip the header row if it exists
    #next(csv_reader, None)
    
    i = 0
    for row in csv_reader:
        if (i > 31):
            break

        rule = row[1].strip()  # Get the rule from the first column
        cases = row[3].split('|')  # Split cases by '|'
        cases = [case.strip() for case in cases]  # Remove leading/trailing spaces
        
        # Add each case and its corresponding rule to the lists
        for case in cases:
            rules.append(i)
            all_cases.append(case)
        i += 1

# Now, 'rules' contains all the corresponding rules, and 'all_cases' contains all the cases
print("Rules:", rules)
print("Cases:", all_cases)
print (len(rules))
print(len(all_cases))


# Define the file name
csv_file = 'Prosecutor_labels.csv'

# Combine the arrays into pairs of corresponding elements
data = zip(rules, all_cases)

# Open the CSV file in write mode
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)

    # Write a header row if needed
    # writer.writerow(['Array 1', 'Array 2'])

    # Write the data row by row
    for row in data:
        writer.writerow(row)

print(f'Data written to {csv_file} successfully.')

