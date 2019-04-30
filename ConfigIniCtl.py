#-*- coding: utf-8 -*-
#! /usr/bin/python2
'''
'''


class ConfigIniCtl:
    array_contents = []
    section = []
    def __init__(self):
        array_contents = []
        section = []
    
    def sections(self):
        print 'sections %d' % len(self.section)
        try:
            #while i < len(self.section):
            for i in self.section:
                print self.array_contents[i]
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

    def insertSection(self, section):
        self.array_contents.insert(0, '['+section+']')
        self.section.insert(0,0)
        self._updateSection(0)
        return
        
    def setfile(self, fname, section, key, val):
        try:
            fp = open(fname, 'a')
            if fp:
                fp.close()
            
            self.read(fname)
            self.set(section,key,val)
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
            bNextSec, secIdxNext = self._getNextSection(secIdx)
            bWrok = False
            lastKeyIdx = self.section[secIdx];
            while lineno < len_conts-1:
                lineno = lineno +1

                bDoDataSplit = False
                if bNextSec == False:
                    bDoDataSplit = True
                elif (bNextSec == True and lineno < self.section[secIdxNext]):
                    bDoDataSplit = True
                    
                #print "set [%d] lencon[%d]"  % (lineno,len_conts)
                if bDoDataSplit == True:
                    line = self.array_contents[lineno]
                    
                    if line != None and len(line) > 0:
                        # exclude string(comment,include, etc...)
                        if line[0] in '#;!':
                            continue
                        k, v = self._splitkeyval(line)
                        #print "set split data [%d] fKey[%s] %s %s"  % (lineno, key, k, v)                        
                        if len(k) > 0:
                            lastKeyIdx = lineno
                        if k == key:
                            bWrok = True
                            self.array_contents[lineno] = ("%s=%s"%(k,val))
                            break;
                        #else 
                            #continue
                #print "set break [%d] "  % (lineno)
                #break
                
            #print "set bWork[%d] lKey[%d]"  % (bWrok,lastKeyIdx)
            if bWrok == False:
                # key + val split
                self.array_contents.insert(lastKeyIdx+1, ("%s=%s"%(key,val)))
                # update setction indexs
                self._updateSection(secIdx)
                
        else:

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
            bNextSec, secIdxNext = self._getNextSection(secIdx)
            #print "get NextSecton %d"%(self.section[secIdxNext])
            while lineno <= len_conts:
                lineno = lineno +1

                bDoDataSplit = False
                if bNextSec == False:
                    bDoDataSplit = True
                elif (bNextSec == True and lineno < self.section[secIdxNext]):
                    bDoDataSplit = True
                    
                if bDoDataSplit == True:
                    line = self.array_contents[lineno]
                    
                    if line != None and len(line) > 0:

                        if line[0] in '#;!':
                            continue
                        k, v = self._splitkeyval(line)
                        #print "split data %s %s"  % (k, v)
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
        data = line.split('=')
        
        if len(data) >= 2:
            key = data[0]
            val = data[1]
            
        #print "_splitkeyval data %s %s"  % (key,val)
        return key,val
    
    def _updateSection(self, secIdx):
        i = secIdx+1
        cnt_sec = len(self.section)
        while i < cnt_sec:
            self.section[i] = self.section[i] +1
            i = i + 1 
        return
        
    def _getLastKeyIdx(self,_sec):
        bGet = False
        retIdx = 0
        len_conts = len(self.array_contents)
        cnt_sec = len(self.section)
        bFindSec, secIdx = self._findsection(_sec)
        lineno = self.section[secIdx]
        if bFindSec == True:
            bNextSec, secIdxNext = self._getNextSection(secIdx)
            while lineno <= len_conts:
                lineno = lineno +1
                bDoDataSplit = False
                if bNextSec == False:
                    bDoDataSplit = True
                elif (bNextSec == True and lineno < self.section[secIdxNext]):
                    bDoDataSplit = True
                    
                if bDoDataSplit == True:
                    line = self.array_contents[lineno]
                    
                    if line != None and len(line) > 0:

                        if line[0] in '#;!':
                            continue
                        k, v = self._splitkeyval(line)
                        #print "split data %s %s"  % (k, v)
                        if k > 0:
                            bGet = True
                            retIdx = lineno
                else:
                    break;
        
        return bGet, retIdx
        
    def _getNextSection(self,_secIdx):
        bNext = False
        retVal = None
        cnt_sec = len(self.section)
        i = _secIdx
        if i+1 < cnt_sec:
            bNext = True
            retVal = i+1
        return bNext, retVal
        
    def _findsection(self,section):
        retBool = False
        retVal    = 0
        cnt_sec = len(self.section)
        i = 0
        while i < cnt_sec:
            if self.array_contents[self.section[i]] == '['+section+']':
                retBool = True
                retVal = i
                break
            i = i + 1
            
        return retBool, retVal
    def _read(self, fp):
        
        lineno = 0
        cnt_sec = 0
        self.array_contents = []
        while True:
            line = fp.readline()
            if not line:
                break
            line = line.strip('\n')
            #print 'line [%s]' % line
            self.array_contents.append(line)
            
            if len(line) != 0 and line[0] == '[':
                #print "in %s len [%d]" % (line, len(line) )
                
                if line[len(line)-1]== ']':
                    #print "out ]"
                    self.section.append(lineno)
                    cnt_sec = cnt_sec+1
            lineno = lineno + 1
            
        #print 'sec cnt[%d]' % cnt_sec
        return lineno
        
