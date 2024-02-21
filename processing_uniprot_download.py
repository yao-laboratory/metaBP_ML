import sys
import time

def process_file(input_file, output_file):
    with open(input_file, 'r') as in_file:
        lines = in_file.readlines()
        with open(output_file, 'w') as out_file:
            for i, line in enumerate(lines):
                if line[0] == '>':
                    # header processing
                    header = line
                    new_header_list = []
                    first_space_loc = header.find(' ')
                    protein_id = header[0:first_space_loc]
                    new_header_list.append(protein_id)
                    os_loc = header.find('OS=', first_space_loc)
                    protein_type = header[first_space_loc + 1 : os_loc - 1]
                    new_header_list.append(protein_type)
                    ox_loc = header.find('OX=', os_loc)
                    os_value = header[os_loc + 3 : ox_loc - 1]
                    new_header_list.append(os_value)
                    space_after_ox = header.find(' ', ox_loc)
                    ox_value = header[ox_loc + 3 : space_after_ox]
                    new_header_list.append(ox_value)
                    new_header = '\t'.join(new_header_list)+'\n'
                    out_file.write(new_header)
                else:
                    if len(line) < 60 or i == len(lines) or lines[i+1][0] == '>':
                        out_file.write(line)
                    else:
                        out_file.write(line[:-1])

def main(argv):
    start_time = time.time()
    inputfilename = argv[0]
    outputfilename = argv[1]
    process_file(inputfilename, outputfilename)
    end_time = time.time()
    print(end_time-start_time)

if __name__ == "__main__":
    main(sys.argv[1:])