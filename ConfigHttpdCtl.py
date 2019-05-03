#-*- coding: utf-8 -*-
#! /usr/bin/python2
'''
'''


class ConfigHttpdCtl:
    array_contents = []
    section = []
    bRead = False
    splitword = ' '
    sec_start = '<'
    sec_end = '>'
    def __init__(self):
        #print 'init'
        self.array_contents = []
        self.section = []
    
    def sections(self):
        print 'sections %d' % len(self.section)
        try:
            #while i < len(self.section):
            for i in self.section:
                print "[%d] %s"%(i,self.array_contents[i])
        except Exception as e:
            print 'except %s' % e
    
    def printall(self):
        con_len = len(self.array_contents)
        print 'printall %d' % con_len
        if con_len > 0 :
            i = 0
            while i < con_len:
                print "[%d] %s"%(i, self.array_contents[i])
                i = i +1

    def setfileEtc(self, fname, key, val):    
        try:
            fp = open(fname, 'a')
            if fp:
                fp.close()
            
            self.read(fname)
            #print 'after read'
            self.setEtcVal(key,val)
            #print 'after set'
            #self.sections()
            self.write(fname)
        except Exception as e:
            print 'except %s' % e
        return
    def setEtcVal(self, key, val):
        
        bFind = False
        len_conts = len(self.array_contents)
        lineno = -1
        workno = -1

        #print "setEtcVal len_conts[%d]" % (len_conts)
        while lineno < len_conts-1:
            lineno = lineno +1
            line = self.array_contents[lineno]
            #print "setEtcVal [%d] %s" % (lineno,line)
            if len(line) == 0 or line[0] in '# <\t':
                continue
            k,v = self._splitkeyval(line)
            #print "setEtcVal  %s %s" % (k,v)
            if len(k) > 0 :
                #print "setEtcVal work line %d"% lineno
                workno = lineno
                if key == k:
                    bFind = True
                    break

        #print "setEtcVal len_conts[%d]" % (len_conts)       
        if bFind == True:
            self.array_contents[lineno] = "%s %s"%(key,val)
        elif lineno >= len_conts -1 :
            #print "setEtcVal append"
            self.array_contents.append("%s %s"%(key,val))

        return lineno
        
    def getEtcVal(self, key):
        ret = ""
        bFind = False
        len_conts = len(self.array_contents)
        lineno = -1
        #print "getEtcVal len_conts[%d]" % (len_conts)
        while lineno < len_conts-1:
            lineno = lineno +1
            line = self.array_contents[lineno]
            #print "getEtcVal [%d] %s" % (lineno,line)
            if len(line) == 0 or line[0] in '# <\t':
                continue
            k,v = self._splitkeyval(line)
            print "getEtcVal  %s %s" % (k,v)
            if k == key:
                bFind = True
                ret = v
                break
            
        return bFind, ret
    

    def insertSection(self, section):
        #bFindSec = self._findsection(section)
        k, v = self._splitkeyval(section)
        self.array_contents.append('<'+section+'>')
        self.array_contents.append('</'+k+'>')
        self.section.append(len(self.array_contents)-2)
        self._updateSection(len(self.array_contents), 2)
        return
        

    def setfile(self, fname, section, key, val):
        try:
            fp = open(fname, 'a')
            if fp:
                fp.close()
            
            self.read(fname)
            #print 'after read'
            self.set(section,key,val)
            print 'after set'
            self.write(fname)
        except Exception as e:
            print 'except %s' % e
            
        return

    def set(self, section, key, val):
        #print 'set sec[%s] key[%s] val[%s]' %(section,key,val)
        len_conts = len(self.array_contents)
        cnt_sec = len(self.section)
        bFindSec, secIdx = self._findsection(section)
        if bFindSec == True:
            #print 'set after find secIdx[%s] sec[%s]' %(secIdx,self.section[secIdx])
            lineno = self.section[secIdx]
            lineEndSec = self._getEndOfSection(secIdx)
            #print "set EndSecton %d"%(lineEndSec)
            bWrok = False
            lastKeyIdx = self.section[secIdx];
            while lineno < len_conts-1:
                lineno = lineno +1

                bDoDataSplit = False
                if (lineno < lineEndSec):
                    bDoDataSplit = True
                    
                #print "set [%d] lencon[%d]"  % (lineno,len_conts)
                if bDoDataSplit == True:
                    line = self.array_contents[lineno]
                    line = line.lstrip(' ')
                    if line != None and len(line) > 0:

                        if line[0] in '#;!':
                            continue
                        k, v = self._splitkeyval(line)
                        #print "set split data [%d] fKey[%s] %s %s"  % (lineno, key, k, v)                        
                        if len(k) > 0:
                            lastKeyIdx = lineno
                        if k == key:
                            bWrok = True
                            self.array_contents[lineno] = ("    %s %s"%(k,val))
                            break;
                        #else 
                            #continue
                #print "set break [%d] "  % (lineno)
                #break
                
            #print "set bWork[%d] lKey[%d]"  % (bWrok,lastKeyIdx)
            if bWrok == False:
                # key + val 생성
                self.array_contents.insert(lastKeyIdx+1, ("    %s %s"%(key,val)))
                #print "set after insert "

                self._updateSection(secIdx)
                
        else:

            print "set before insert section"
            age = input("Your age? ")
            self.insertSection(section)
                
            self.set( section, key, val)
            
        return

    def get(self, section, key):
        #print 'get sec[%s] key[%s]' %(section,key)
        ret = ""
        
        len_conts = len(self.array_contents)
        cnt_sec = len(self.section)
        bFindSec, secIdx = self._findsection(section)
        if bFindSec == True:
            #print "get Findsecton %d"%(self.section[secIdx])
            lineno = self.section[secIdx]
            lineEndSec = self._getEndOfSection(secIdx)
            print "get EndSecton %d"%(lineEndSec)
            while lineno <= len_conts:
                lineno = lineno +1

                bDoDataSplit = False
                if (lineno < lineEndSec):
                    bDoDataSplit = True
                    
                if bDoDataSplit == True:
                    line = self.array_contents[lineno]
                    line = line.lstrip(' ')
                    print "get after ltrip [%d]%s"%(lineno, line)
                    if line != None and len(line) > 0:

                        if line[0] in '#;!':
                            continue
                        k, v = self._splitkeyval(line)
                        #print "split data [%s] [%s]"  % (k, v)
                        if k == key:
                            ret = v
                            break
                else:
                    break;

        return ret

    
    def write(self,filename):
        try:
            fp = open(filename, 'w')
            if fp:
                len_con = len(self.array_contents)
                i = 0
                while i < len_con:
                    #print 'write %s' % self.array_contents[i]
                    fp.write( self.array_contents[i] + '\n' )
                    i = i + 1
                fp.close()
        except Exception as e:
            print 'except %s' % e
            
        return

    def read(self,filename):
        try:
            fp = open(filename, 'rw')
            if fp:
                self._read(fp)
                fp.close()

        except Exception as e:
            print 'except %s' % e
        return 
        
    def _splitkeyval(self, line):
        #print "_splitkeyval line %s" % (line)
        key = ""
        val = ""
        findsplit = line.find(' ')
        #print "_splitkeyval find %d" % (findsplit)
        if findsplit < len(line):
            key = line[0:findsplit]
            val = line[findsplit+1:]
            
        #print "_splitkeyval data [%s] [%s]"  % (key,val)
        return key,val

    def _updateSection(self, secIdx, _add = 1):
        i = secIdx+1
        cnt_sec = len(self.section)
        while i < cnt_sec:
            self.section[i] = self.section[i] +_add
            i = i + 1
        return
    
    def _getNextSection(self,_secIdx):
        bNext = False
        retVal = None
        cnt_sec = len(self.section)
        i = _secIdx
        if i+1 < cnt_sec:
            bNext = True
            retVal = i+1
        return bNext, retVal
        
    def _getEndOfSection(self,_secIdx):
        retVal = None
        lineno = self.section[_secIdx]
        len_con = len(self.array_contents)
        while lineno < len_con:
            lineno = lineno +1
            line = self.array_contents[lineno]
            #print "_getEndOfSection [%s]" % line
            if len(line) > 1 and line[0]== self.sec_start and line[1] == '/':
                retVal = lineno
                break
        
        return retVal
        
    def _findsection(self,section):
        retBool = False
        retVal    = 0
        cnt_sec = len(self.section)
        i = 0
        #print "_findsection cnt_sec[%d] [%s]" % (cnt_sec,section)
        while i < cnt_sec:
            idxSec = self.section[i]
            #print "_findsection inwhile[%d][%s]" % (idxSec,self.array_contents[idxSec])
            if self.array_contents[self.section[i]] == '<'+section+'>':
                retBool = True
                retVal = i
                break
            i = i + 1
            
        return retBool, retVal

    
    def _read(self, fp):
        
        lineno = 0
        cnt_sec = 0
        self.array_contents = []
        self.section = []
        while True:
            line = fp.readline()
            if not line:
                break
            line = line.strip('\n')
            #print '_read line [%s]' % line
            self.array_contents.append(line)
            
            if len(line) != 0 and line[0] == self.sec_start and (line[1] != '/'):
                #print "in %s len [%d]" % (line, len(line) )
                
                if line[len(line)-1]== self.sec_end:
                    #print "out ]"
                    self.section.append(lineno)
                    cnt_sec = cnt_sec+1
            lineno = lineno + 1
            
        #print 'sec cnt[%d]' % cnt_sec
        return lineno
        
