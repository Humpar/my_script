import os,sys,argparse
import time
import subprocess as sp
from multiprocessing import Process, current_process

class makeconfig():
    def __init__(self,configfile,outpath,*cfg):
        self.configfile = configfile
        self.filename = os.path.basename(configfile)
        self.outfile = os.path.join(outpath,self.filename)
        self.cfg = cfg
        

    def make(self):
        if  len(self.cfg) != self.checkfile():
            raise ValueError('输入的配置参数与配置文件中不符')
        else:
             self.cfgtext= self.writhfile()

    def writhfile(self):
        with open(self.configfile,'r') as cof:
            content = cof.read()
            cof.close()
        with open(self.outfile,'w') as of:
            of.write(content.format(*self.cfg))
            of.close()
        return content.format(*self.cfg)

    def checkfile(self):
        maxnum = 0
        with open(self.configfile,'r') as cof:
            content = cof.read()
            for i in range(len(content)):
                if content[i] == '{':
                    if content[i+1].isdigit():
                        if maxnum< int(content[i+1]):maxnum = int(content[i+1])
                    else:
                        continue
            cof.close()
        return maxnum

class writeconfig(makeconfig):
    def __init__(self, configfile, outpath, text,*cfg):
        self.text = text
        super().__init__(configfile, outpath, *cfg)

    def make(self):
        self.writhfile()
    
    def writhfile(self):
        with open(self.outfile,'w') as of:
            of.write(self.text)
            of.close()
        return self.text


class worhstation():
    def __init__(self,step,path,name,app,*cfg,cfgtype='-',**config):
        self.name = name
        self.path = path
        self.app = app
        self.cfg = cfg
        self.config = config
        self.ctype = cfgtype
        self.workpath = os.path.join(path,step+name,'work')
        self.outpath = os.path.join(path,step+name,'output')
        self.shpath = os.path.join(self.workpath,self.name+'.sh')
        self.makepath(self.workpath)
        self.makepath(self.outpath)

    def work(self):
        if not self.checkfinish():
            self.shcmd = self.makesh()
            self.runcmd()

    def thread_work(self):
        thread = Process(target=self.work, args=())
        thread.start()
        #记得.join卡住程序
        return thread

    def makepath(self,path):
        if not os.path.exists(path): 
            os.makedirs(path)
        
    def config_manege(self):
        cfg =''
        if self.ctype == '-':
            for k,v in self.config.items():
                cfg += ' -{} {}'.format(k,v)
        elif self.ctype == '':
            cfg = ' '.join(list(self.cfg))
        else:
            cfg =''
        return cfg

    def makesh(self):
        shcmd = ''
        cfg = self.config_manege()
        shcmd = self.app + cfg
        shpath = self.shpath
        #shcmd += '{} >>{}.log 2>&1 '.format(shcmd,shpath)
        with open(shpath,'w') as s:
            s.write(shcmd)
        return shcmd
    

    def checkfinish(self):
        start,ctime = self.get_time()
        if os.path.exists(self.shpath+'.finish'):
            print('[{}] / [check:]/ {}已经完成'.format(start,self.shpath))
            return True
        else:
            print('[{}] / [check:]/ {}没有完成'.format(start,self.shpath))
            return False

    def runcmd(self):
        log = os.path.join(self.path,'log')
        start,ctime = self.get_time()
        print('[{}] / [start:]/   {} >>{} 2>&1 &'.format(ctime,self.shpath,log))
        runcmd('{} >>{} 2>&1 '.format(self.shcmd,log))
        #os.system('{} >>{} 2>&1 '.format(self.shpath,log))
        open(self.shpath+'.finish','w').close()
        end,ctime = self.get_time()
        print('[{}] / [finish:]/  nohup {} >>{} 2>&1 &'.format(ctime,self.shpath,log))
        print('step {},消耗时间：{}s'.format(self.name,end-start))

    def get_time(self):
        return time.time(),time.ctime()

    def search_path_or_file(self,name,searchpath,ctype='file'):
        if ctype == 'file':
            for root,dirs,files in os.walk(searchpath):
                if name in files:
                    return os.path.join(root,name)
        elif ctype == 'path':
            for root,dirs,files in os.walk(self.outpath):
                if name in dirs:
                    return os.path.join(root,name)
        else:
            print('输入类型错误,ctype=”file“ or ctype=”path“')
            raise ValueError('输入类型错误,ctype=”file“ or ctype=”path“')
        print('结果目录中没有找到{}'.format(name))
        raise ValueError('结果目录中没有找到{}'.format(name))
        
    def search_out(self,name,ctype='file'):
        #ctype = 'file' or 'path'
        if self.checkfinish():
            files = self.search_path_or_file(name,self.outpath,ctype=ctype)
            return files
        else:
            print('{}没有完成，获取结果无效'.format(self.shpath))
        

class workvoid(worhstation):
    def __init__(self, step, path, name, app, *cfg, cfgtype='-', **config):
        super().__init__(step, path, name, app, *cfg, cfgtype=cfgtype, **config)
        ...
    def work(self):
        return super().work()


def runcmd(cmd):
    work = sp.run(cmd,shell=True,capture_output=True,encoding="utf-8")
    if work.returncode != 0:
        err = "error: {} the cmd failed".format(cmd)
        raise Exception(err)
    return work.stdout,work.stderr



def readsh(shfile):
    with open(shfile,'r') as sh:
        app = sh.read().strip()
        sh.close()
    return app


def readcfg(file):
    cfg = {}
    with open(file,'r') as f:
        for i in f:
            if i[0] == '#' or i[0] == '\n':continue
            i = i.strip().split(':')
            cfg[i[0]] = ':'.join(i[1:])
        f.close()
    return cfg

def writecfg(adict:dict,cfgfile):
    with open(cfgfile,'a') as cfg:
        for k,v in adict.items():
            line = "{}:{}\n".format(k,v)
            cfg.write(line)
        cfg.close()
    return cfgfile
        
def read_cmd_result(cmd):
    os.system(cmd+'>out')
    cmdout = open('out','r').read()
    os.system('rm out')
    return cmdout

def times():
    import time
    t=time.ctime()
    c=t.split(' ')
    #print(c)
    时间=['星期','月','日期','时间','年']
    day={}
    for i in range(len(c)):
        day[时间[i]]=c[i]
    month={'Jan':'1','Fed':'2','Mar':'3','Apr':'4',
    'May':'5','June':'6','July':'7',
    'Aug':'8','Sept':'9','Oct':'10'
    ,'Nov':'11','Dec':'12'}                                                  
    date='{} 年 {} 月 {} 日 '.format(day['年'],month[day['月']],day['日期'])
    return date
