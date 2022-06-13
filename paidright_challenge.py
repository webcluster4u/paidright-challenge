"""
This module solves the PaidRight code challenge

Author : Mahdi Bazarganigilani
Date : 13/6/2022
Functions:
    parse_input: this method parses two possible combinations of inputs and generates the output CSV file

Usage:
    1- python paidright_challenge.py "[ ['a','b','c'], [1,2,null], [2,3,4], [5,null,6] ]"
    2- python paidright_challenge.py "[ { 'a':1, 'b':2 }, { 'a': 2, 'b':3, 'c':4 }, { 'c':6, 'a':5 } ]"
"""
import csv
import sys
import traceback
import re
import json
import os

def parse_input():
    """
    A function to parse two possible input combinations
    :return: the CSV output file named output.csv
    """
    number_of_arguments = len(sys.argv)
    if number_of_arguments != 2:
        print("ERROR: Only one string argument should be provided to the program. program exists")
        sys.exit(1)
    else:
        if sys.argv[1].strip() == "":
            print("ERROR: Input argument is null. program exists")
            sys.exit(1)

    path = 'output.csv'
    match_first = "^\[(\[[^\[\]]*\]\,)*(\[[^\[\]]*\]){1}\]$"
    match_second = "^\[(\{[^\{\}]*\}\,)*(\{[^\{\}]*\}){1}\]$"
    input = sys.argv[1].strip()
    input = "".join(input.split())
    m_first = re.search(match_first, input)
    m_second = re.search(match_second, input)

    if not m_first is None:
        # remove whitespaces
        elems = input.split("],[")
        elems = [x.replace("[", "").replace("]", "").replace('"', '').replace("'", "").replace("null", "") for x in
                 elems]
        header = elems[0].split(",")
        # add head_line
        head_line = ["---" for x in range(len(header))]
        data = [x.split(',') for x in elems[1:len(elems)]]
        try:
            print("INFO: Writing your data to a CSV file")
            f = open(path, 'w', encoding='UTF8', newline='')
            writer = csv.writer(f)
            # write the header
            writer.writerow(header)
            writer.writerow(head_line)
            # write multiple rows
            writer.writerows(data)
            f.close()
            print("INFO: Successfully wrote your data to a CSV file at '{}'".format(os.getcwd()+"\\"+path))
        except Exception:
            print(traceback.format_exc())
            print("ERROR: Can not write your input to CSV. program exists")
            sys.exit(1)

    if not m_second is None:
        inp = json.loads(input.replace("'", '"'))
        keys = [set(x.keys()) for x in inp]
        header = set()
        for x in keys:
            header = header | x
        header = sorted(list(header))
        # add head_line
        head_line = {}
        for x in header:
            head_line[x] = "---"
        try:
            print("INFO: Writing your data to CSV file")
            f = open(path, 'w', encoding='UTF8', newline='')
            writer = csv.DictWriter(f, fieldnames=header)
            # write the header
            writer.writeheader()
            writer.writerow(head_line)
            # write multiple rows
            writer.writerows(inp)
            print("INFO: Successfully wrote your data to a CSV file at '{}'".format(os.getcwd()+"\\"+path))
            f.close()
            sys.exit(0)
        except Exception:
            print(traceback.format_exc())
            print("ERROR: Can not write your input to CSV. program exists")
            sys.exit(1)

    if m_first is None and m_second is None:
        print("ERROR: The input does not match the required format. program exists")
        sys.exit(1)


if __name__ == '__main__':
    parse_input()
