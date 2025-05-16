import os
import csv

def split_csv(path, filename, lines_per_file=10000):
    with open(os.path.join(path,filename), 'r') as csvfile:
        reader = csv.reader(csvfile)
        # headers = next(reader)  # Save the header row?
        file_count = 0
        current_lines = []

        for i, row in enumerate(reader):
            current_lines.append(row)
            if (i + 1) % lines_per_file == 0:
                output_filename = f'output_{file_count}.csv'
                output_file = os.path.join(path,output_filename)
                with open(output_file, 'w', newline='') as outfile:
                    writer = csv.writer(outfile)
                    # writer.writerow(headers)
                    writer.writerows(current_lines)
                file_count += 1
                current_lines = []

        # Write remaining lines to a new file
        if current_lines:
            with open(output_file, 'w', newline='') as outfile:
                writer = csv.writer(outfile)
                # writer.writerow(headers)
                writer.writerows(current_lines)

