import os,sys
class Table():

    def __init__(self,filepath):
        self.tableself = []
        x = 0
        y = 0
        with open(filepath,'r',encoding='utf-8') as f:
            for line in f.readlines():
                list_row = line.strip("\n").split("\t")
                if len(list_row)>x:x=len(list_row)
                self.tableself.append(list_row)
                y= len(self.tableself)
            f.close()
        self.long = y
        self.wide = x
        self.name = os.path.basename(filepath)
        

    def checkxy(self,x,y):
        if x > self.long:
            raise IndexError("索引x超出了长度")
        elif y > self.wide:
            raise IndexError("索引y超出了长度")


    def makeindex(self,x=0,y=0):
        self.checkxy(x,y)
        print("构建索引，默认第一行第一列为索引，若为其他请指定")
        tableitemx = {}
        tableitemy = {}
        for i in range(len(self.tableself[x])):
            row = []
            for j in self.tableself:
                if self.tableself[x][i] != j[i]:
                    row.append(j[i])
            tableitemx[self.tableself[x][i]] = row
        for s in self.tableself:
            d = s.copy()
            d.remove(s[y])
            tableitemy[s[y]] = d
        self.rowitem = tableitemx
        self.columnitem = tableitemy
    
    #r表示行v表示列
    def getele(self,r,v):
        self.checkxy(r,v)
        return self.tableself[r][v]

    def putele(self,r,v,ele):
        self.checkxy(r,v)
        self.tableself[r][v] = ele

    def printall(self):
        for i in self.tableself:
            print('\t'.join(i))

    def getall(self):
        for i in self.tableself:
            for j in i:
                yield j
            
    def index_to_table(self,index):
        self.tableself = []
        newlist = []
        for key in index.keys():
            newlist.append(key)
            newlist = newlist + index[key]
            self.tableself.append(newlist)
            newlist = []
        return self.tableself



    def write_table(self,filename,tableself):
        with open(filename,'w') as f:
            for i in tableself:
                i = [str(g) for g in i]
                i = '\t'.join(i)
                f.write(i+'\n')
            f.close()
        print('{} 写入成功'.format(filename))

