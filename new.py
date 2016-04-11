#coding=utf-8
import win32clipboard as w,win32con,re
import sys

help = \
"""new.py [Options]
    -        #SHA1ǰ��ȥ������--
    sha1     #��ȡ(���а���)ľ����е�SHA1
    s        #��ȡ���а��ڵ�SHA1
    HEX      #ȥ��16���ƿո�
    hashsig  #��ȡľ���HashSig
    number   #ͳ��ÿ�����ļ�����ִ���
    arcinfo  #ƥ����Ϣ
"""
#���в�������ȡ�Լ��а�


Data = 0
 
def GetText():                              #��ȡ���а�
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_TEXT)
    w.CloseClipboard()
    return d

def SetText(aString):                       #������а�
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_TEXT, aString)
    w.CloseClipboard()
    
#--------------------------------------    
def __():#��ӻ�ȥ�����а���SHA1ǰ���--
    global Data 
    if re.match('--\s{0,3}(\w{40})',Data):
        Data = '\n'.join(re.findall('--\s{0,3}(\w{40})',Data))
    else:
        Text = re.findall('\w{40}',Data)
        Text[0] = '--'+Text[0]
        Data = '\n--'.join(Text).rstrip('-')
#--------------------------------------
def HEX():#16����(���а���)ȥ���ո�
    global Data 
    Data = ''.join(Data.split())
#--------------------------------------
def SHA1(n):#ľ���(���а���)��ȡSHA1
    global Data
    if re.match('0x\w{8}\,0x\w{16} \/\/ (\w{40})',Data): 
        Data = '\n'.join(re.findall('0x\w{8}\,0x\w{16} \/\/ (\w{40})',Data))    #ֻ��ľ����ʽ��ƥ��SHA1
    elif n == 1:
        Data = '\n'.join(re.findall('\w{40}',Data))                             #�����ʽƥ��SHA1
#--------------------------------------
def HasSig():#��ȡľ���hashsig
    global Data     
    if re.match('0x\w{8}\,0x\w{16}',Data): 
        Data = '\n'.join(re.findall('0x\w{8}\,0x\w{16}',Data))
#--------------------------------------
def arcinfo():
    global Data
    try:#���Դ�arcinfo.log���û�л����ü��а�������
        file = open("arcinfo.log")
        Data = file.read()
    except:
        pass
                                                                    #                  sha1: 5cfa487096c2ec4bb8258fab92de303f0e81ec3a
    Data1 = '\n'.join(re.findall('arctype: AT_[a-z]{2,6}',Data))    #               arctype: AT_xx
    Data2 = '\n'.join(re.findall('peflags: PEF_[a-z]{4}.*',Data))   #               peflags: PEF_xxxx 
                                                                    #             file_size: == 0x2800
                                                                    #           peovly_size: == 0x0
                                                                    #            peexp_size: == 0x0
                                                                    #            peimp_size: == 0x3c
                                                                    #            peres_size: == 0x428
                                                                    #            petls_size: == 0x0
                                                                    #          pesect_count: == 0x8
                                                                    #         pexsect_count: == 0x3
                                                                    #          peent_sectno: 0
                                                                    #         dt_excp_count: == <unk>
                                                                    #      dt_syscall_count: == <unk>
                                                                    #     dt_syscallp_count: == <unk>
                                                                    #     dt_dropfile_count: == <unk>
                                                                    #      dt_subproc_count: == <unk>
                                                                    #    [X] peimplib_count: == 2
                                                                    #    [X] peimpsym_count: == 17    
                                                                    #         hash_headtail: 0x0000000000
                                                                    #        hash_peent_adj: 0x0000000000
                                                                    #       hash_peent_sect: 0x00000000000
                                                                    #   hash_peent_secthead: 0x0000000000
                                                                    #   hash_peent_sectback: 0x0000000000
    Data3 = '\n'.join(re.findall('hash_.+\: 0x\w{10,12}',Data))     #  hash_peovly_headtail: 0x0000000000    
    Data4 = '\n'.join(re.findall('hashsig: 0x\w{8}\,0x\w{16}',Data))#               hashsig: 0x6ca3a9e0,0x95b6607316b3c0f8

    Data = Data1 + "\n" + Data2 + "\n" + Data3 + "\n" + Data4
#--------------------------------------
def number():
    #ͳ��ÿ�������ļ�����ִ���,����ͳ��ľ���
    #����ǰȥ��ľ���ע��
    import operator
    global Data  
    count_dict = {}
    for line in Data.split("\n"):
        line = line.strip()
        count = count_dict.setdefault(line, 0) #���ֵ��в�ѯ,...
        count += 1
        count_dict[line] = count
    sorted_count_dict = sorted(count_dict.iteritems(), key=operator.itemgetter(1), reverse=True)
    Data = ""
    for item in sorted_count_dict:
        Data = Data + item[0] + "," + str(item[1]) + "\n"

def main(i):
    if i=="-":#SHA1ǰ��ȥ������--
        __()
    elif i=="sha1":#��ȡ(���а���)ľ����SHA1
        SHA1(0)    
    elif i=="s":#��ȡ���а��ڵ�SHA1
        SHA1(1)   
    elif i=="HEX":#ȥ��16���ƿո�
        HEX()
    elif i=="hashsig":#��ȡľ���HashSig
         HasSig()
    elif i=="number":#ͳ��ÿ�������ļ�����ִ���
        number()
    elif i=="arcinfo":#ƥ����Ϣ
        arcinfo()
    else:
        print help
    
if __name__ == '__main__':
    for i in sys.argv:
        Data = GetText()#��ȡ���а�������
                        # arcinfo number
        main(i)         # hashsig number  �г�HashSig ��ͳ�Ʒֱ���ִ���
                        # ............ �ȵ�
        SetTe