#!/share/nas2/genome/biosoft/Python/3.7.3/bin/python
from Bio import SeqIO
import os,sys,argparse
from multiprocessing import Pool, current_process

SCRIPTDIR, SCRIPTNAME=os.path.split(os.path.abspath(sys.argv[0]))
#print(os.path.split(os.path.abspath(sys.argv[0])))
thedir = os.path.abspath(sys.argv[0])+'\\'
VERSION="v1.1"
AUTHORS="zhaohc"
DESCRIPTION="""fq to fa

input 
-i fastq_file  
    or  
-l fastq_list_file 
eg:
/.../1.fq
/.../2.fq
/.../3.fq
/.../4.fq
"""
def arg_parse():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,description=DESCRIPTION,epilog="The End",add_help=False)
    parser.add_argument("-f",dest="file",help="fastq files,provide one or more fq file path ,use ',' separate ",default='')
    parser.add_argument("-l",dest="list",help="fastq path list file ",default='')
    parser.add_argument("-o",dest="outdir",help="fasta output path",default='')
    parser.add_argument("-t",dest="thread",help="theard num,default=4",default=4,type=int)
    parser.add_argument("-v", dest = "version", action = "version", version = DESCRIPTION+" "+VERSION)
    parser.add_argument("-h", "--help",dest="help", help = "show this help message and exit", action = "help")
    args = parser.parse_args()
    print(args)
    return args

def fq_fa(my_file,prefix):

    #with open(my_file) as handle:

    record=SeqIO.parse(my_file, "fastq")

    SeqIO.write(record,prefix+'.fasta',"fasta")

    #handle.close()

def run_to_fa(file,out):
    prefix = os.path.basename(file)
    prefix = os.path.splitext(prefix)[0]
    prefix = os.path.join(out,prefix)
    fq_fa(file,prefix)
    print('{} already write in {}'.format(file,prefix+'.fasta'))

def main():
    args = arg_parse()
    file = args.file
    listf = args.list
    out = args.outdir
    thread = args.thread
    if file:
        fqlist = file.strip().split(',')
        if len(fqlist) < thread:thread = len(fqlist)
        pool = Pool(processes=thread)
        task_list = []
        for i in fqlist:
            files = i.strip()
            task1 =  pool.apply_async(run_to_fa, (files,out))
            task_list.append(task1)
        pool.close()
        pool.join()
    elif listf:
        pool = Pool(processes=thread)
        task_list = []
        with open(listf,'r') as f:
            for i in f:
                files = i.strip()
                #run_to_fa(files,out)
                task1 =  pool.apply_async(run_to_fa, (files,out))
                task_list.append(task1)
            f.close()
        pool.close()
        pool.join()

if __name__ == "__main__":
    main()
