# postmodification version of text.covidtxt file. Outputs pastetextcovid.txt file.
# - States the total number of palindromes 
# - Finds and the longest palindrome 

# version 2

from Bio import SeqIO
import numpy as np
import pandas as pd

# Declaration for txt output
count = 0
max_palindrome = 0
palindrome = ""
pal_no_str = ''
pal_first = ''
pal_second = ''
accuracy = 0
palindrome_length = 0
palindrome_list = []
single_palindrome = ""
finished_palindrome = False
max_palindrome_list = []

# Declaration for the csv output
data = []
data_name_list = []

f = open("processed_palindromes.txt", "w")

with open("palindromes_output.txt") as fp:
    all_file = fp.readlines()

    first_time = True

    for line in all_file:
        if 'gb:' in line:
            if first_time:
                data_name = line
                data_name_list = [line]
                first_time = False
            else:
                # writes the number of palindromes from the previous count.
                pal_no_str = "Number of palindromes found = " + str(count) + '\n'
                data_name_list.append(count)
                max_pal_str = "Max palindrome size = " + str(max_palindrome) + '\n'
                data_name_list.append(max_palindrome)
                data_name_list += max_palindrome_list
                palindrome_list.sort(reverse=True)
                palindrome = ''

                data.append(data_name_list)
                for elem in palindrome_list:
                    palindrome += elem[1]
                    data.append([elem[2], elem[3], elem[0]])
                f.write(data_name + pal_no_str + max_pal_str + str(max_palindrome_list) + '\n' + palindrome + '\n')

                data_name = line
                data_name_list = [line]
                palindrome_list = []

                max_palindrome = 0
                max_palindrome_list = []
                count = 0

        elif '|' in line:
            count += 1
            palindrome_length = line.count('|')
            single_palindrome += line

        elif len(line.split()) == 3:
            x = line.split()
            if max_palindrome < abs(int(x[2]) - int(x[0])):
                max_palindrome = int(x[2]) - int(x[0])
                max_palindrome_list = [x[1]]

            elif max_palindrome == abs(int(x[2]) - int(x[0])):
                max_palindrome_list.append(x[1])

            for seq_record in SeqIO.parse("CovidHumanGenomicData.fasta", "fasta"):
                if seq_record.id in data_name:
                    if int(x[0]) < int(x[2]):
                        single_palindrome = line
                        if (int(x[0]) - 20) > 0:
                            pal_first = str(seq_record.seq[(int(x[0]) - 20):(int(x[2]))])
                        else:
                            pal_first = str(seq_record.seq[:(int(x[2]))])
                    else:
                        pal_second = str(seq_record.seq[(int(x[2])):(int(x[0]) + 20)])
                        finished_palindrome = True
                        palindrome_length_with_gaps = int(x[0]) - int(x[2]) + 1
                        accuracy = palindrome_length / palindrome_length_with_gaps
                    break

            if finished_palindrome:
                palindrome_for_csv = single_palindrome + line
                single_palindrome += line + '\n' + pal_first + '...' + pal_second + '\n' + \
                                     'Accuracy = ' + str(palindrome_length) + ' / ' + \
                                     str(palindrome_length_with_gaps) + ' = ' + \
                                     str(accuracy) + '\n \n-------------------------------------- \n \n'
                padding = pal_first + '...' + pal_second
                palindrome_list.append((accuracy, single_palindrome, palindrome_for_csv, padding))

                pal_first = ''
                pal_second = ''
                finished_palindrome = False

    max_pal_str = "Max palindrome size = " + str(max_palindrome) + '\n'
    data_name_list.append(max_palindrome)
    pal_no_str = "Number of palindromes found = " + str(count) + '\n'
    data_name_list.append(count)

    palindrome_list.sort(reverse=True)
    palindrome = ''

    data.append(data_name_list)
    for elem in palindrome_list:
        palindrome += elem[1]
        data.append([elem[2], elem[3], elem[0]])

    f.write(data_name + pal_no_str + max_pal_str + str(max_palindrome_list) + '\n' + palindrome)


df = pd.DataFrame(data)
df.to_csv("test.csv")
f.close()


