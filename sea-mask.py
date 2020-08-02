import sys
import os
import subprocess

def WriteOutput(source,formatName,path):
    print('Write')
    cmd=["gpt","Write","-PformatName="+str(formatName),"-Pfile="+str(path),source]
    subprocess.call(cmd)

def LandMask(source):
    print('Sea Mask')
    cmd=["gpt","Land-Sea-Mask","-PlandMask=false","-PshorelineExtension=10","-PuseSRTM=true",source]
    subprocess.call(cmd)

def main():
    
    path1=r"C:\Users\pahar\SAR"
    path2=sys.argv[1]
    source=path1+'\\'+path2
    print(source)
    path=r"C:\Users\pahar\SAR"
    target=path+r"\target.dim"

    LandMask(source)
    print(target)

    writePath=path+r"\original"
    print('Sea Mask Path',writePath)
    WriteOutput(target,"PNG",writePath)
    
if __name__=="__main__":
    main()