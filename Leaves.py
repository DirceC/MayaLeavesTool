import maya.cmds as cmds
import random

#Global variables
ComponentType=0

#Window function
def MakeUI():
    #delete window if it exists already
    if cmds.window("WinBuild", exists=True):
        cmds.deleteUI("WinBuild")
        
    #MASTER LAYOUT
    cmds.window("WinBuild",t="window",w=400,h=250,s=True)
    cmds.formLayout(nd=100)
    #Branch layout
    cmds.columnLayout( adjustableColumn=True )
    cmds.frameLayout(l="Branch",bgc=(0.2, 0.2, 0.2), bgs=True, en=False, cll=True, cl=True)    
    #Create a cylinder with user input
    cmds.separator(st="none")
    cmds.text("Branch size")
    cmds.separator(st="none")
    cmds.button(l="Create cylinder",c="stick=cmds.polyCylinder(r=1, h=2, sx=20, sy=1, sz=1, ax=(0, 1, 0), rcp=0, cuv=3, ch=1, n='Stick')")
    MakeUI.CylH=cmds.floatSliderGrp(l="Height:",v=1,f=True,min=0.1,max=1000,cc="CylinderCreation()")
    MakeUI.CylR=cmds.floatSliderGrp(l="Radius:",v=1,f=True,min=0.01,max=100)
    MakeUI.CylSA=cmds.intSliderGrp(l="Subdivisions Axis:",v=3,f=True,min=3,max=50)
    MakeUI.CylSH=cmds.intSliderGrp(l="Subdivisions Height:",v=1,f=True,min=1,max=50)
    MakeUI.CylSC=cmds.intSliderGrp(l="Subdivisions Caps:",v=1,f=True,min=1,max=50)
    cmds.setParent("..")  
    #Leaves layout
    cmds.frameLayout(l="Leaves",bgc=(0.2, 0.2, 0.2), bgs=True, en=True, cll=True, cl=False)
    cmds.separator(st="none")
    cmds.text("Multiply an object along a curve, faces, vertex or edges")
    cmds.separator(st="none")
    MakeUI.SelectionFL=cmds.frameLayout(l="Selection",bgc=(0.2, 0.2, 0.2), bgs=True,en=True,cll=True,cl=False)
    cmds.separator(st="none")
    #Radio Button selection of type of objects
    cmds.rowColumnLayout(nc=4,cw=[(1,100),(2,100),(3,100),(4,100)],cat=[(1,"left",25),(2,"left",25),(3,"right",10),(4,"right",10)])
    MakeUI.radio=cmds.radioCollection()
    cmds.radioButton(l="Curve",cc="ComponentType=0",sl=True)
    cmds.radioButton(l="Faces",cc="ComponentType=1")
    cmds.radioButton(l="Vertices",cc="ComponentType=2")
    cmds.radioButton(l="Edges",cc="ComponentType=3")
    cmds.setParent("..")
    cmds.separator(st="none")
    #Buttons layout 
    cmds.rowColumnLayout(nc=2,cw=[(1,210),(2,200)],co=[(1,"right",4),(2,"left",4)])
    #Continue to next area button and go back to change selection button
    MakeUI.ContinueBtn=cmds.button(l="Continue",c="RadioSelection()",w=100,en=True)
    MakeUI.BackBtn=cmds.button(l="Go back",c="RadioBack()",w=100,en=False) 
    cmds.setParent("..") 
    cmds.separator(st="none")
    #Select the objects or/and the curve to place along
    MakeUI.selectedCurve=cmds.textFieldButtonGrp(l="Select the Curve:",ed=False,bl="Select",bc="SelectCRV()",en=False)
    MakeUI.selectedBase=cmds.textFieldButtonGrp(l="Select the base object:",ed=False,bl="Select",bc="SelectBase()",en=False) 
    MakeUI.selectedOBJ=cmds.textFieldButtonGrp(l="Select the object:",ed=False,bl="Select",bc="SelectOBJ()",en=False)
    #Get attributes from the user
    MakeUI.OBJname=cmds.textFieldGrp(l="Name for objects:")
    MakeUI.NumofCopies=cmds.intSliderGrp(l="Number of copies:",v=10,f=True,min=2,max=100)
    MakeUI.ScaleRndMin=cmds.floatSliderGrp(l="Scale min",v=1,f=True,min=0.1,max=10)
    MakeUI.ScaleRndMax=cmds.floatSliderGrp(l="Scale max",v=1,f=True,min=0.1,max=10)
    MakeUI.Randomness=cmds.floatSliderGrp(l="Rotation randomness",v=1,f=True,min=0.5,max=10)
    #Make duplicates 
    MakeUI.populate=cmds.button(l="Populate",c="Populate()",en=False)
    cmds.rowColumnLayout(nc=2,cw=[(1,210),(2,200)],co=[(1,"right",4),(2,"left",4)])
    #Undo or finalize 
    MakeUI.UndoBtn=cmds.button(l="Undo",c="UndoFunc()",w=100,en=False)
    MakeUI.Finalize=cmds.button(l="Finalize",c="FinalizeFun()",w=100,en=False)
    cmds.separator()
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.showWindow()
        
MakeUI()

#FUNCTIONS
#Branch creation function
def CylinderCreation():
    stickH=cmds.floatSliderGrp(MakeUI.CylH,en=True,e=True)
    #cmds.setAttr(TempObj[0]+".height",stickH)
    #cmds.setAttr()
    stickR=cmds.floatSliderGrp(MakeUI.CylR,en=True,e=True)
    stickSA=cmds.intSliderGrp(MakeUI.CylSA,en=True,e=True)
    stickSH=cmds.intSliderGrp(MakeUI.CylSH,en=True,e=True)
    stickSC=cmds.intSliderGrp(MakeUI.CylSC,en=True,e=True)

#Enable and disable options based on user selection     
def RadioSelection():
    cmds.button(MakeUI.ContinueBtn,en=False,e=True)
    cmds.button(MakeUI.BackBtn,en=True,e=True) 
    if ComponentType==0:
        cmds.textFieldButtonGrp(MakeUI.selectedCurve,en=True,e=True)
        cmds.textFieldButtonGrp(MakeUI.selectedBase,en=False,e=True)
        cmds.textFieldButtonGrp(MakeUI.selectedOBJ,en=False,e=True)      
    if ComponentType==1:  
        cmds.textFieldButtonGrp(MakeUI.selectedCurve,en=False,e=True)
        cmds.textFieldButtonGrp(MakeUI.selectedBase,en=True,e=True)
        cmds.textFieldButtonGrp(MakeUI.selectedOBJ,en=False,e=True)   
    if ComponentType==2:  
        cmds.textFieldButtonGrp(MakeUI.selectedCurve,en=False,e=True)
        cmds.textFieldButtonGrp(MakeUI.selectedBase,en=True,e=True)
        cmds.textFieldButtonGrp(MakeUI.selectedOBJ,en=False,e=True)       
    if ComponentType==3:  
        cmds.textFieldButtonGrp(MakeUI.selectedCurve,en=False,e=True)
        cmds.textFieldButtonGrp(MakeUI.selectedBase,en=True,e=True)
        cmds.textFieldButtonGrp(MakeUI.selectedOBJ,en=False,e=True)          
       
#Enable and disable options to go back to previous selection  
def RadioBack():
    cmds.button(MakeUI.ContinueBtn,en=True,e=True)
    cmds.button(MakeUI.BackBtn,en=False,e=True)
    cmds.textFieldButtonGrp(MakeUI.selectedCurve,en=False,e=True)
    cmds.textFieldButtonGrp(MakeUI.selectedBase,en=False,e=True)
    cmds.textFieldButtonGrp(MakeUI.selectedOBJ,en=False,e=True) 

#Function to get selected curve from user    
def SelectCRV():
    SelectCRV.selectedCV=cmds.ls(sl=True,o=True)
    print (SelectCRV.selectedCV)
    #Change text in text field to current selection
    cmds.textFieldButtonGrp(MakeUI.selectedCurve,e=True,tx=SelectCRV.selectedCV[0])
    #Enable option to select object to multiply
    cmds.textFieldButtonGrp(MakeUI.selectedOBJ, en=True,e=True)

#Function to select base object    
def SelectBase():
    SelectBase.selectedBase=cmds.ls(sl=True,o=True)
    #Change text in text field to current selection
    cmds.textFieldButtonGrp(MakeUI.selectedBase,e=True,tx=SelectBase.selectedBase[0])
    print(SelectBase.selectedBase)
    #Enable option to select object to multiply
    cmds.textFieldButtonGrp(MakeUI.selectedOBJ, en=True,e=True)
        
#Function to select object to multiply    
def SelectOBJ():
    SelectOBJ.selectedObj=cmds.ls(sl=True,o=True)
    print(SelectOBJ.selectedObj)
    #Change text in text field to current selection
    cmds.textFieldButtonGrp(MakeUI.selectedOBJ,e=True,tx=SelectOBJ.selectedObj[0])
    #Enable button to multiply
    cmds.button(MakeUI.populate,en=True, e=True)

#Function to multiply the object         
def Populate():
    #Get variables from the user
    Populate.NumCopies=cmds.intSliderGrp(MakeUI.NumofCopies,q=True,v=True)
    Populate.randMinScale=cmds.floatSliderGrp(MakeUI.ScaleRndMin,q=True,v=True)
    Populate.randMaxScale=cmds.floatSliderGrp(MakeUI.ScaleRndMax,q=True,v=True)
    Populate.Username=cmds.textFieldGrp(MakeUI.OBJname,q=True,tx=True) 
    Populate.rotRand=cmds.floatSliderGrp(MakeUI.Randomness,q=True,v=True)
    #Enable and disable buttons
    cmds.button(MakeUI.UndoBtn,en=True, e=True)
    cmds.button(MakeUI.Finalize,en=True, e=True)
    cmds.button(MakeUI.populate,en=False, e=True)
    #Multiply based on user selection
    if ComponentType==0:
        MultiplyCurve()
    if ComponentType==1:  
        MultiplyFaces()
    if ComponentType==2:  
        MultiplyVertices()
    if ComponentType==3:  
        MultiplyEdges()   
        
#Function that places objects along a curve        
def MultiplyCurve():
    #Create a temporary locator
    cmds.spaceLocator(n="MainLoc")
    #Select the curve and create an animation path to move the objects along
    cmds.select(SelectCRV.selectedCV[0],add=True)        
    cmds.pathAnimation(fm=True,f=True,fa="x",ua="y",inverseFront=False,stu=0,etu=Populate.NumCopies)
    cmds.selectKey("motionPath1_uValue")
    cmds.keyTangent(itt="linear",ott="linear")   
    #Create a group
    ParentGroup=cmds.group(em=True,n="Stacks")
    #Cycle for creating the duplicates
    for obj in range(0,Populate.NumCopies):
        #Get attributes from user
        RandScale=random.uniform(Populate.randMinScale,Populate.randMaxScale)
        RandRot=random.uniform(0,360)
        cmds.currentTime(obj,e=True)
        CurX=cmds.getAttr("MainLoc.tx")
        CurY=cmds.getAttr("MainLoc.ty")
        CurZ=cmds.getAttr("MainLoc.tz")
        CurRotY=cmds.getAttr("MainLoc.ry")    
        #Select object, duplicate and move to new position
        cmds.select(SelectOBJ.selectedObj,r=True)
        tempObj=cmds.duplicate()
        cmds.setAttr(tempObj[0]+".tx",CurX)
        cmds.setAttr(tempObj[0]+".ty",CurY)
        cmds.setAttr(tempObj[0]+".tz",CurZ)
        cmds.setAttr(tempObj[0]+".rx",RandRot*Populate.rotRand)
        cmds.setAttr(tempObj[0]+".ry",RandRot*Populate.rotRand)
        cmds.setAttr(tempObj[0]+".rz",RandRot*Populate.rotRand)
        #change scale and move object to parent group
        cmds.scale(RandScale,RandScale,RandScale)
        cmds.parent(tempObj[0],"Stacks",r=False)   

#Function that places objects over faces    
def MultiplyFaces():
    cmds.select(SelectBase.selectedBase)
    cmds.ConvertSelectionToFaces()  
    selFaces=cmds.ls(sl=True,fl=True)
    print(selFaces)
    lenght=len(selFaces)
    ParentGroup=cmds.group(em=True,n="Stacks")
    print(lenght)    
    for i in range(0,Populate.NumCopies):
        cmds.select(SelectOBJ.selectedObj,r=True)
        tempObj=cmds.duplicate()
        randFace=random.uniform(0,lenght)
        selectedFace = selFaces[int(randFace)]
        cmds.select(selectedFace)
        facePosition = cmds.xform(selectedFace, q=True, ws=True, t=True)
        cmds.select(tempObj)
        cmds.move(facePosition[0],facePosition[1],facePosition[2])    
        RandRot=random.uniform(0,360)    
        cmds.setAttr(tempObj[0]+".rx",RandRot*Populate.rotRand)
        cmds.setAttr(tempObj[0]+".ry",RandRot*Populate.rotRand)
        cmds.setAttr(tempObj[0]+".rz",RandRot*Populate.rotRand)
        cmds.parent(tempObj[0],"Stacks",r=False)

#Function that places objects over vertices
def MultiplyVertices():
    cmds.select(SelectBase.selectedBase)
    cmds.ConvertSelectionToVertices()  
    selVert=cmds.ls(sl=True,fl=True)
    print(selVert)
    lenght=len(selVert)
    ParentGroup=cmds.group(em=True,n="Stacks")
    print(lenght)    
    for i in range(0,Populate.NumCopies):
        cmds.select(SelectOBJ.selectedObj,r=True)
        tempObj=cmds.duplicate()
        randVert=random.uniform(0,lenght)
        selectedVert = selVert[int(randVert)]
        cmds.select(selectedVert)
        VertPosition = cmds.xform(selectedVert, q=True, ws=True, t=True)
        cmds.select(tempObj)
        cmds.move(VertPosition[0],VertPosition[1],VertPosition[2])    
        RandRot=random.uniform(0,360)    
        cmds.setAttr(tempObj[0]+".rx",RandRot*Populate.rotRand)
        cmds.setAttr(tempObj[0]+".ry",RandRot*Populate.rotRand)
        cmds.setAttr(tempObj[0]+".rz",RandRot*Populate.rotRand)
        cmds.parent(tempObj[0],"Stacks",r=False)

#Function that places objects over edges
def MultiplyEdges():
    cmds.select(SelectBase.selectedBase)
    cmds.ConvertSelectionToEdges()  
    selEdge=cmds.ls(sl=True,fl=True)
    print(selEdge)
    lenght=len(selEdge)
    ParentGroup=cmds.group(em=True,n="Stacks")
    print(lenght)    
    for i in range(0,Populate.NumCopies):
        cmds.select(SelectOBJ.selectedObj,r=True)
        tempObj=cmds.duplicate()
        randVert=random.uniform(0,lenght)
        selectedEdge = selEdge[int(randVert)]
        cmds.select(selectedEdge)
        EdgePosition = cmds.xform(selectedEdge, q=True, ws=True, t=True)
        cmds.select(tempObj)
        cmds.move(EdgePosition[0],EdgePosition[1],EdgePosition[2])    
        RandRot=random.uniform(0,360)    
        cmds.setAttr(tempObj[0]+".rx",RandRot*Populate.rotRand)
        cmds.setAttr(tempObj[0]+".ry",RandRot*Populate.rotRand)
        cmds.setAttr(tempObj[0]+".rz",RandRot*Populate.rotRand)
        cmds.parent(tempObj[0],"Stacks",r=False)
        
#Function to go back to change values                      
def UndoFunc():
    if cmds.objExists("MainLoc"):
        cmds.select("MainLoc")
        cmds.delete()
    cmds.select("Stacks")
    cmds.delete()
    cmds.button(MakeUI.UndoBtn,en=False, e=True)
    cmds.button(MakeUI.Finalize,en=False, e=True)
    cmds.button(MakeUI.populate,en=True, e=True)

#Function to end     
def FinalizeFun():
    if cmds.objExists("MainLoc"):
        cmds.select("MainLoc")
        cmds.delete()
    cmds.select("Stacks")
    cmds.rename("Stacks",Populate.Username)    
    cmds.deleteUI("WinBuild")
    
    
    
    