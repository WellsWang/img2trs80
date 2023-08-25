# -*- coding: utf-8 -*-

import sys
import numpy as np
from PIL import Image

def image2array(img):

    arr = np.array(Image.open(img), dtype='uint8')
    return arr

def output_array(arr):
    for row in range(len(arr)):
        for col in range(len(arr[row])):
            print("▓" if arr[row][col] else " ",end="")
        print("")

def array2data(arr):
    if len(arr)==0:
        return None
        
    data = []
    if len(arr)%3>0:
        rb= 3-len(arr)%3
    else: rb=0
    if len(arr[0])%2>0:
        cb=2-len(arr[0])%2
    else: cb=0
    
    if cb:
        for r in range(len(arr)):
            for i in range(cb):
                arr[r].append(0)
    if rb:
        for i in range(rb):
            row=[]
            for c in range(len(arr[0])):
                row.append(0)
            arr.append(row)
            
    data.append(int(len(arr)/3))
    data.append(int(len(arr[0])/2))

    for r in range(data[0]):
        for c in range(data[1]):
            d=0
            for y in range(3):
                for x in range(2):
                    d += arr[r*3+y][c*2+x]*pow(2,2*y+x)
            data.append(d)

    return data
    
def data2basic(data,startlinenum=100, tab=0):


    basic = "{} C={}:R={}:T={}\n{} GOSUB 5000\n".format(startlinenum, data[1], data[0], tab, startlinenum+10)
    for i in range(data[0]):
        basic += "{} DATA ".format(startlinenum+1000+i*10)
        basic += ", ".join(map(str,data[2+data[1]*i:2+data[1]*i+data[1]]))
        basic += "\n"
        
    basic +="""
4999 END
5000 FOR Y=1 TO R
5010 PRINT TAB(T);
5020 FOR X=1 TO C
5030 READ D
5040 PRINT CHR$(D+128);
5050 NEXT X
5060 PRINT ""
5070 NEXT Y
5090 RETURN
"""
    
    return basic
    

if __name__ == '__main__':
    if len(sys.argv)>1:
        #try:
        arr = image2array(sys.argv[1])
        output_array(arr)
        data = array2data(arr)
        print(data2basic(data))
#        print(len(data))
#        data = array2data(arr, True)
#        print(data)
#        print(len(data),int(len(data)/2+1))
        #except:
        #    print("Error on open image file, please check the image file.")
    else:
        print("-= Image to Array =- \n Usage:\n img2arr.py <filename>")