class fastq():
    def __init__(self,name,seqs,discript,score):
        self.name = name[1:]
        self.seqs =seqs
        self.discript = discript
        self.score = score
        self.len = len(seqs)

    def printseq(self):
        print('@{}\n{}\n{}\n{}'.format(self.name,self.seqs,self.discript,self.score))
        return '@{}\n{}\n{}\n{}\n'.format(self.name,self.seqs,self.discript,self.score)


class fasta():
    def __init__(self,name,seqs):
        self.name = name[1:]
        self.seqs =seqs
        self.len = len(seqs)
    def printseq(self):
        #print('{}\n{}\n'.format(self.name,self.seqs))
        return '>{}\n{}\n'.format(self.name,self.seqs)


class seq(fastq,fasta):
    def __init__(self,file,atype):
        if atype == "fastq" :
            self.allseq = self.openfq(file)
        elif atype == "fasta":
            self.allseq = self.openfa(file)
        self.total = len(self.allseq)
        self.type = atype

    def openfq(self,file):
        with open(file,"r") as fq:
            i = 1
            allseq= []
            for f in fq.readlines():
                f = f.strip()
                if i == 1 and f[0]=='@':
                    name = f
                    i += 1
                    continue
                elif i == 2:
                    seqs = f
                    i += 1
                    continue
                elif i == 3:
                    discript = f
                    i += 1
                    continue
                elif i == 4:
                    score = f
                    i = 1
                    sequences = fastq(name,seqs,discript,score)
                    allseq.append(sequences)
                fq.close()
            return allseq

    def openfa(self,file):
        with open(file,"r") as fa:
            allseq= []
            name = ''
            seqs = ''
            i = 1
            for f in fa.readlines():
                f = f.strip()
                if f == '':
                    continue
                if f[0]=='>':
                    if i != 1:
                        sequences = fasta(name,seqs)
                        allseq.append(sequences)
                    name = f
                    seqs = ''
                    i += 1
                else:
                    seqs += f
                fa.close()
            sequences = fasta(name,seqs)
            allseq.append(sequences)
        return allseq
                    

    #大于或等于某个长度的序列综合
    def statistic_len(self,lens):
        point = 0
        for i in self.allseq:
            if i.len >= lens:
                point += 1
        return point
        
    def cut_section(self,k,v):
        for i in self.allseq:
            i.seqs = i.seqs[k-1:v]
            print('{}\t{}'.format(i.name,len(i.seqs)))

    def rm_seq(self,id):
        for i in self.allseq:
            if i.name == id:
                self.allseq.remove(i)
        return self.allseq



    def normolfa(slef,seqs:str):
        j=1
        newseq=''
        for i in seqs:
            if j == 60:
                newseq += i +'\n'
                j=1
            else:
                newseq +=i
                j+=1
        return newseq


    def write_seq(self,prefix,normol=False):
        if self.type == 'fastq':
            with open(prefix+'.fastq','w') as f:
                for i in self.allseq:
                    f.write(i.printseq())
                f.close()
        elif self.type == 'fasta':
            if normol:
                with open(prefix+'.fasta','w') as f:
                    for i in self.allseq:
                        i.seqs = self.normolfa(i.seqs)
                        f.write(i.printseq())
                    f.close()
            else:
                with open(prefix+'.fasta','w') as f:
                    for i in self.allseq:
                        f.write(i.printseq())
                    f.close()

    def GC_stat(self,seqs):
        stat = {'G':0,'C':0,'A':0,'T':0,'N':0,'R':0,'Y':0,'M':0,'K':0,'S':0,'W':0,'H':0,'B':0,'V':0,'D':0}
        degenerate = {'N':['A','T','C','G'],
            'R':['A','G'],
            'Y':['C','T'],
            'M':['A','C'],
            'K':['G','T'],
            'S':['G','C'],
            'W':['A','T'],
            'H':['A','T','C'],
            'B':['G','T','C'],
            'V':['G','A','C'],
            'D':['G','A','T']}
        for i in seqs:
            stat[i] = stat[i]+1
        self.stat = stat
        return (stat['G']+stat['C']+stat['S'])/len(seqs)

    def N50_stat(self):
        longdict = {}
        long = 0
        for i in self.allseq:
            long += len(i.seqs)
            longdict[i.name] = len(i.seqs)
        self.long = long
        middle = long/2
        sortlist = []
        seqname = list(longdict.keys())
        for i in range(1,len(seqname)):
            for j in range(len(seqname)-i):
                if longdict[seqname[j]] < longdict[seqname[j+1]]:
                    seqname[j],seqname[j+1] = seqname[j+1],seqname[j]
        N50 = 0
        for i in range(len(seqname)):
            middlelong = sum([longdict[s] for s in seqname[:i+1]])
            if middle < middlelong:
                self.N50 = longdict[seqname[i]]
                self.N50naem = seqname[i]
                break
        return i+1
        

    def print_all_len(self,all=False):
        allGC = 0
        N50seqs = self.N50_stat()
        #print(N50seqs)
        for i in self.allseq:
            GC = self.GC_stat(i.seqs.upper())
            allGC += GC
            if not all:
                if self.total < 20 or len(i.seqs) >= self.N50 :print('ID: {}\tlenth:{}\tGC:{:.4}%'.format(i.name,len(i.seqs),GC*100))
            else:
                print('ID: {}\tlenth:{}\tGC:{:.4}%'.format(i.name,len(i.seqs),GC*100))
        print('\nall total seq: {} ,long: {} bp ,GC: {:.4}% ,N50: {} ({} sequences)\n'.format(self.total,self.long,allGC/self.total*100,self.N50,N50seqs))
    def overturn(self):
        pair = {'A':'T','T':'A','G':'C','C':'G'}
        for i in self.allseq:
            newseqs = ''
            for j in i.seqs:
                newseqs += pair[j]
            i.seqs = newseqs
    
    def removeID(self,id:list):
        for i in self.allseq:
            if i.name in id:
                self.allseq.remove(i)
                print('remove {}'.format(i.name))
