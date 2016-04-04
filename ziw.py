#coding:utf-8

import zipfile,os



class zipfil():
    def __init__(self,filepath):
        self.mzipfile = zipfile.ZipFile(filepath,'a')


    def unpack(self):
        a =3

    def pack(self):
        pass

def main():
    path = r'C:\Users\Ken\Documents\My Knowledge\Data\908526831@qq.com'
    for root,dir,filenames in os.walk(path):
        for filename in filenames:
            path = os.path.join(root,filename)
            if zipfile.is_zipfile(path):
                f = zipfil(path)


if __name__ == '__main__':
    main()