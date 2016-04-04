#coding:utf-8
import re,os

def GetHashList():  #从扫描日志中读取hash列表
   file_path = r"D:\1.txt"
   file_data = open(file_path).read()
   hash_list = re.findall("(\w{40})",file_data,re.S)
   return hash_list
def WtiteFile(Trojan_hash,file_path):
    file_data = open(file_path,'r').read()
    tmp_data = file_data
    for hash in Trojan_hash:
        rep = r'[\w,]*\s*\"[\w\/\.]*\"\s\/\/\s%s\s\([\w\.]*\).*?\n'%hash
        data =  re.findall(rep,file_data,re.S)
        if data:
            print data
            tmp_data=re.sub(rep,"",tmp_data,flags=re.S)
    file = open(file_path,"w+")
    file.write(tmp_data)
    file.close()
def DeleteHash(TrojanHashList=None):
    for root,dirs,filenames in os.walk("C:\Users\Ken\Documents\My Knowledge\Data\908526831@qq.com"):#r"E:\OneDriver\OneDrive\troj"):
        for filename in filenames:
            if 'name' in filename:
                file_path = root +"\\" + filename
                file_data = open(file_path,"r+").read()
                WtiteFile(TrojanHashList,file_path)
if __name__ == '__main__':
    DeleteHash()
    Hash_list = GetHashList()
    DeleteHash(Hash_list)
