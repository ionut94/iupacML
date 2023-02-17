import argparse
import subprocess
from Bio import SeqIO


def parseFile():
    for seq_record in SeqIO.parse("CovidHumanGenomicData.fasta", "fasta"):
        if "N" not in str(seq_record.seq):

            SeqIO.write(seq_record, "1seq.fasta", "fasta")
            bash_command = "./IUPACpal/IUPACpal -f 1seq.fasta -s "+seq_record.id

            process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            # print(output)

            palindrome = seq_record.description + "\n"
            with open("IUPACpal.out", "r") as f:
                test = f.read()
                palindrome += test.split("Palindromes:")[-1]

            with open("output.txt", "a") as f1:
                f1.write(palindrome)

    # host_list = []
    # for seq_record in SeqIO.parse("981105392499-GenomicFastaResults.fasta", "fasta"):
    #     host = seq_record.description.split("|")[-1].split(":")[-1]
    #
    #     if host not in host_list:
    #         host_list.append(host)
    # print(len(host_list))

    # human_list = []
    # for seq_record in SeqIO.parse("981105392499-GenomicFastaResults.fasta", "fasta"):
    #     host = seq_record.description.split("|")[-1].split(":")[-1]
    #
    #     if host in "Tiger":
    #         human_list.append(seq_record)
    # print(len(human_list))
    # SeqIO.write(human_list, "CovidTigerGenomicData", "fasta")

    # host_count = {'Human': 0, 'Unknown': 0, 'Dog': 0, 'Cat': 0, 'Monkey': 0, 'Hamster': 0, 'Mink': 0, 'Lion': 0,
    #               'Tiger': 0}
    # for seq_record in SeqIO.parse("981105392499-GenomicFastaResults.fasta", "fasta"):
    #     host = seq_record.description.split("|")[-1].split(":")[-1]
    #     host_count[host] += 1
    # print(host_count)

    # records = list(SeqIO.parse("981105392499-GenomicFastaResults.fasta", "fasta"))
    #
    # print("Found %i records" % len(records))
    #
    # print("The last record")
    # last_record = records[-1]  # using Python's list tricks
    # print(last_record.id)
    # print(last_record.description)
    # print(repr(last_record.seq))
    # print(len(last_record))
    #
    # print("The first record")
    # first_record = records[0]  # remember, Python counts from zero
    # print(first_record.id)
    # print(first_record.description)
    # print(repr(first_record.seq))
    # print(len(first_record))


# initial block of code that will be read when the file is run
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action='store_const',
                        const=True, default=False)
    parser.add_argument("-i", "--input", help="String to look for in the ", type=str)
    parser.add_argument("--debug", help="DEBUG MODE", action='store_const', const=True, default=False)

    args = parser.parse_args()
    verbosity = args.verbose

    parseFile()
