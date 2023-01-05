#!/share/nas2/genome/biosoft/Python/3.8.5/bin/python3.8
import sys,os,argparse
sys.path.append(r"/share/nas1/zhaohc/script/")
from mybio import *

SCRIPTDIR, SCRIPTNAME=os.path.split(os.path.abspath(sys.argv[0]))
#print(os.path.split(os.path.abspath(sys.argv[0])))
thedir = os.path.abspath(sys.argv[0])+'/'
VERSION="v1.0"
AUTHORS="zhaohc"
DESCRIPTION="cat fa"
def arg_parse():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,description=DESCRIPTION,epilog="The End",add_help=False)
    parser.add_argument("-f",dest="file",help="fasta or fastq file ",required = True)
    parser.add_argument("-a", "--all",dest="all", help = "print all sequences", action = 'store_true',default=False)
    parser.add_argument("-v", dest = "version", action = "version", version = DESCRIPTION+" "+VERSION)
    parser.add_argument("-h", "--help",dest="help", help = "show this help message and exit", action = "help")
    args = parser.parse_args()
    print(args)
    return args

def cut_seq(ids):
    seats = 0
    if ids[-1] == ')':
        mark = ids.find('(')
        seats = ids[mark+1:-1]
        ids = ids[:mark]
        seats = seats.strip().split(':')
        seats = [int(i) for i in seats]
    return ids,seats
    a = seq('1.fasta',"fasta")

def save_or_print_seq(a,i,ids,seats):
    if seats == 0:
        with open(ids.replace(' ','_')+'.fasta','w') as f:

            f.write('>'+ids+'\n')
            f.write(a.normolfa(i.seqs))
            f.close()
        return 0
    lenth = seats[1]-seats[0]
    if lenth<1000:
        print(a.normolfa(i.seqs)[seats[0]-1:seats[1]])
    else:
        with open(ids.replace(' ','_')+'.{}-{}.fasta'.format(seats[0],seats[1]),'w') as f:
            
            f.write('>'+ids+'\n')
            f.write(a.normolfa(i.seqs[seats[0]-1:seats[1]]))
            f.close()


def main():
    args = arg_parse()
    all = args.all
    file = args.file
    if file[-1] == 'a':
        a = seq(file,"fasta")
    elif file[-1] == 'q':
        a = seq(file,"fastq")
    print(a.total)
    a.print_all_len(all=all)
    print('method "seqeunce ID(start:end)"')
    s = input('select cat id: ')
    if s == '':
        return 0
    ids,seats = cut_seq(s)
    for i in a.allseq:
        if i.name == ids:
            if seats != 0 and seats[1]-seats[0] < 10000:
                print(a.normolfa(i.seqs[seats[0]:seats[1]]))
            else:
                save_or_print_seq(a,i,ids,seats)
                




if __name__ == "__main__":
    main()
