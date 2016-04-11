#coding=utf-8
import win32clipboard as w,win32con,re
import sys

help = \
"""new.py [Options]
    -        #SHA1前面去掉加上--
    sha1     #获取(剪切板内)木马库中的SHA1
    s        #获取剪切板内的SHA1
    HEX      #去除16进制空格
    hashsig  #获取木马库HashSig
    number   #统计每行在文件里出现次数
    arcinfo  #匹配信息
"""
#所有操作内容取自剪切板


Data = 0
 
def GetText():                              #获取剪切板
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_TEXT)
    w.CloseClipboard()
    return d

def SetText(aString):                       #存入剪切板
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_TEXT, aString)
    w.CloseClipboard()
    
#--------------------------------------    
def __():#添加或去掉剪切板内SHA1前面的--
    global Data 
    if re.match('--\s{0,3}(\w{40})',Data):
        Data = '\n'.join(re.findall('--\s{0,3}(\w{40})',Data))
    else:
        Text = re.findall('\w{40}',Data)
        Text[0] = '--'+Text[0]
        Data = '\n--'.join(Text).rstrip('-')
#--------------------------------------
def HEX():#16进制(剪切板内)去掉空格
    global Data 
    Data = ''.join(Data.split())
#--------------------------------------
def SHA1(n):#木马库(剪切板内)提取SHA1
    global Data
    if re.match('0x\w{8}\,0x\w{16} \/\/ (\w{40})',Data): 
        Data = '\n'.join(re.findall('0x\w{8}\,0x\w{16} \/\/ (\w{40})',Data))    #只在木马库格式内匹配SHA1
    elif n == 1:
        Data = '\n'.join(re.findall('\w{40}',Data))                             #任意格式匹配SHA1
#--------------------------------------
def HasSig():#获取木马库hashsig
    global Data     
    if re.match('0x\w{8}\,0x\w{16}',Data): 
        Data = '\n'.join(re.findall('0x\w{8}\,0x\w{16}',Data))
#--------------------------------------
def arcinfo():
    global Data
    try:#尝试打开arcinfo.log如果没有还是用剪切板内数据
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
    #统计每行在在文件里出现次数,用于统计木马库
    #运行前去掉木马库注释
    import operator
    global Data  
    count_dict = {}
    for line in Data.split("\n"):
        line = line.strip()
        count = count_dict.setdefault(line, 0) #在字典中查询,...
        count += 1
        count_dict[line] = count
    sorted_count_dict = sorted(count_dict.iteritems(), key=operator.itemgetter(1), reverse=True)
    Data = ""
    for item in sorted_count_dict:
        Data = Data + item[0] + "," + str(item[1]) + "\n"

def main(i):
    if i=="-":#SHA1前面去掉加上--
        __()
    elif i=="sha1":#获取(剪切板内)木马库的SHA1
        SHA1(0)    
    elif i=="s":#获取剪切板内的SHA1
        SHA1(1)   
    elif i=="HEX":#去除16进制空格
        HEX()
    elif i=="hashsig":#获取木马库HashSig
         HasSig()
    elif i=="number":#统计每行在在文件里出现次数
        number()
    elif i=="arcinfo":#匹配信息
        arcinfo()
    else:
        print help
    
if __name__ == '__main__':
    for i in sys.argv:
        Data = GetText()#获取剪切板内数据
                        # arcinfo number
        main(i)         # hashsig number  切出HashSig 在统计分别出现次数
                        # ............ 等等
        SetTe