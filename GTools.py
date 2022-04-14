# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 13:32:39 2017

@author: Dzmitry Afanasenkau
		 e-mail: d.afanasenkov@gmail.com
"""

import numpy as np
import matplotlib.pyplot as plt

def Convert(InFile,OutFile):
    """This function allows using variables in G-code. 
    It accepts an input file (path provided in 'InFileName') containing 
    'pseudo G-code' - a G-code where some coordinates or parameters 
    are written as variablse. These variables should be declared before 
    using with '$' e.g. '$x=10', '$t=1.1' , etc. Each declaration starts 
    with a new line.Then these variable can be used in G-code commands 
    e.g. 'G1 Xi*x1+x2' , 'M30 Pt1' , etc.
    The value of a variable can be changed at any place in the file 
    by using '$' mark e.g. '$x=x+5', '$y=y1+x2', etc. (every expression 
    starts with a new line). The function reads this variable containing 
    file and converts it into ordinarry G-code by replacing variables 
    with numbers and performing mathematical expresions
    and saves the result in the file with path specified in 'OutFileName'
    ---
    Errors of input are still not addressed
    """
    fin = open(InFile,"r")
    fout = open(OutFile,"w")
    Variables =	{
    }
    
    for line in fin:
        #print(line)
        if line[0]=='$':
            cells = line.split('=')
            if len(cells)>1:
                cells[1]=cells[1].strip()
                for key1 in sorted(Variables.keys(),key=len,reverse=True):
                    #print(key1)
                    cells[1]=cells[1].replace(key1,str(Variables[key1]))
                Variables[cells[0][1::]]=eval(cells[1])
        else:
            if (line[0]=='F')|(line[0]=='G')|(line[0]=='X')|(line[0]=='Y')|(line[0]=='Z'):
                 for key1 in sorted(Variables.keys(),key=len,reverse=True):
                     line=line.replace(key1,str(Variables[key1]))
                 cells = line.split(' ')
                 line=''
                 for cell in cells: 
                     if len(cell)>1:
                         cell=cell[0]+str(eval(cell[1::]))
                     line=line+cell+' '
                 line=line+'\n'
                 fout.write(line)
            else:
                fout.write(line)
      
    fin.close()
    fout.close()
    return Variables


def PlotTopView(InFile):
    """Gives a top viev plot of a structure coded in the G-code file
    """
    def NewXY(line,x,y,CoorSysType):
        xnew=x
        ynew=y
        
        if CoorSysType=='abs':
            f=0
        elif CoorSysType=='rel':
            f=1
        else:
            print('Error in coorsinate system type')
               
        cells = line.split(' ')        
        for cell in cells:
            if cell[0]=='X':
                xnew=f*x+eval(cell[1::])
            elif cell[0]=='Y':
                ynew=f*y+eval(cell[1::])
            elif cell[0]=='G':
                pass
            elif cell[0]=='Z':
                pass
            elif cell[0]=='\n':
                pass
            else:
                print('Error: '+line)

        return xnew,ynew
    
    fin = open(InFile,"r")
    CoorSysType='abs'
    pen=0
    x=0
    y=0
    xnew=0
    ynew=0
    color='r'
    
    for line in fin:
        #print(line)
        plt.figure('Main')
        if line[0:3]=="M97":
            pen=1
        if line[0:3]=="M96":
            pen=0
        if line[0:3]=="G90":
            CoorSysType='abs'    
        if line[0:3]=="G91":
            CoorSysType='rel'
        if line[0:5]=='(color':
            cells = line.split('=')
            color=cells[1]
        if (line[0:2]=='G0')|(line[0:2]=='G1')|(line[0]=='X')|(line[0]=='Y'):
            xnew,ynew = NewXY(line,x,y,CoorSysType)        
            #print xnew,ynew            
        if pen==1:
            plt.plot([x,xnew],[y,ynew],color)#new_colors[i])
        x=xnew
        y=ynew
        if line[0:4]=="M282":
            plt.plot([x],[y],color+'s')
               
                 
    fin.close()
    
def Move(InFile,OutFile,dx,dy,dz):
    """This function moves all parts coded in a G-code file 
    (with path 'InFile') by 'dx' , 'dy' , 'dz' and saves the result 
    in a file with path  'OutFile'
    """
    fin = open(InFile,"r")
    fout = open(OutFile,"w")
    CoorSysType='abs'
    
    for line in fin:
        if len(line)>=3:
            if line[0:3]=='G90':
                CoorSysType='abs'
            if line[0:3]=='G91':
                CoorSysType='rel'
                
        if ((line[0]=='F')|(line[0]=='G')|(line[0]=='X')|(line[0]=='Y')|(line[0]=='Z'))&(CoorSysType=='abs'):
            line=line.strip() 
            #print(line)
            cells = line.split(' ')
            line=''
            for cell in cells:
                cell=cell.strip()
                if cell[0]=='X':
                    cell=cell[0]+str(eval(cell[1::])+dx)
                if cell[0]=='Y':
                    cell=cell[0]+str(eval(cell[1::])+dy)
                if cell[0]=='Z':
                    cell=cell[0]+str(eval(cell[1::])+dz)
                line=line+cell+' '
            line=line[0:-1]+'\n' 
            fout.write(line)
        else:
            fout.write(line)
            
    fin.close()
    fout.close()