import os
import argparse
import subprocess
from Bio import SeqIO


def find_palindromes(arguments):
    cur_path = os.getcwd()
    index = 0

    for seq_record in SeqIO.parse(cur_path + "/" + arguments.file, "fasta"):
        if "N" not in str(seq_record.seq):
            SeqIO.write(seq_record, "1seq.fasta", "fasta")
            bash_command = "./IUPACpal/IUPACpal -f 1seq.fasta -s " + seq_record.id + " -m " + str(
                arguments.min) + " -M " + str(arguments.max) + " -g " + str(arguments.gap) + " -x " + str(
                arguments.mismatches)

            process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

            palindrome = seq_record.description + "\n"
            with open("IUPACpal.out", "r") as f:
                test = f.read()
                palindrome += test.split("Palindromes:")[-1]

            with open(arguments.output, "a") as f1:
                f1.write(palindrome)

            index += 1
            if index == arguments.limit:
                break


def get_count_by_host(filename="981105392499-GenomicFastaResults.fasta"):
    host_count = {'Human': 0, 'Unknown': 0, 'Dog': 0, 'Cat': 0, 'Monkey': 0, 'Hamster': 0, 'Mink': 0, 'Lion': 0,
                  'Tiger': 0}
    for seq_record_fasta in SeqIO.parse(filename, "fasta"):
        host = seq_record_fasta.description.split("|")[-1].split(":")[-1]
        host_count[host] += 1
    print(host_count)


def get_total_count(filename="981105392499-GenomicFastaResults.fasta"):
    records = list(SeqIO.parse(filename, "fasta"))
    print("Found %i records" % len(records))


# initial block of code that will be read when the file is run
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action='store_const',
                        const=True, default=False)
    parser.add_argument("-i", "--input", help="String to look for in the ", type=str)
    parser.add_argument("-o", "--output", help="file where the output will be prinder", type=str, default="output.txt")
    parser.add_argument("-f", "--file", help="Input filename (FASTA format)", type=str,
                        default="CovidHumanGenomicData.fasta")

    parser.add_argument("-l", "--limit", help="Maximum limit of genomes you want to find .", type=int, default="0")
    parser.add_argument("-m", "--min", help="Minimum length.", type=int, default="10")
    parser.add_argument("-M", "--max", help="Maximum length.", type=int, default="100")
    parser.add_argument("-g", "--gap", help="Max permissible gap", type=int, default="100")
    parser.add_argument("-x", "--mismatches", help="Maximum permissible mismatches.", type=int, default="0")

    parser.add_argument("--debug", help="DEBUG MODE", action='store_const', const=True, default=False)

    args = parser.parse_args()
    verbosity = args.verbose

    find_palindromes(args)
