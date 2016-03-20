#coding:gb2312
import zipfile,argparse

#apk查壳特征
pack_ijiami     = ['爱加密',['libexec.so','libexecmain.so']],
pack_apkprotect = ['apkprotect',['apkprotect.com','libAPKProtect.so']],
pack_360        = ['360加固',['libprotectClass.so','libprotectClass_x86.so'
                  'libjiagu.so','libjiagu_art.so','libjiagu.so','libjiagu_x86.so']],
pack_bangbang   = ['梆梆加固企业版',['libDexHelper.so','libDexHelper-x86.so']],
pack_tp         = ['腾讯加固',['libtup.so','libshell.so']],
pack_baidu      = ['百度加固',['libbaiduprotect.so','ibbaiduprotect_x86.so']],
pack_najia      = ['娜迦加固',['libddog.so','libfdog.so','libchaosvmp.so']],
pack_wangqin    = ['网秦加固',['libnqshieldx86.so','libnqshield.so']],
pack_ali        = ['阿里加固',['libmobisec.so','libmobisecx.so']],
pack_tfd        = ['通付盾加固',['libegis.so']],

pak_list = [pack_ijiami ,pack_apkprotect ,pack_360 ,pack_bangbang ,
            pack_tp ,pack_baidu ,pack_najia ,pack_wangqin ,pack_ali ,pack_tfd  ]
#查apk壳
def checkPack( zipfilename):
    for pakcket in pak_list:
        for u in zipfilename:
            if u.split('/')[-1] in pakcket[0][1]:
                return pakcket[0][0]
    return '未加壳或者未知壳'

# 不解压文件，获取文件列表
def getzipfilename(path):
    filename = []
    try:
        zipinfo = zipfile.ZipFile(path,'r')
        zipinfolist = zipinfo.infolist()
    except Exception,e:
        return
    for f in zipinfolist:
        filename.append(f.filename)
    return filename

def main():
    parser = argparse.ArgumentParser(description='apk查壳工具 by Ken' )
    parser.add_argument('-f','--file', help='指定文件' , nargs="+")
    args = parser.parse_args()
    path = args.file
    if path:
        filename = getzipfilename(path[0])
        if not filename:
            print '不是标准apk文件'
            exit()
        print checkPack(filename)
    else:
        print '请选择文件路径'
if __name__ == '__main__':
    main()