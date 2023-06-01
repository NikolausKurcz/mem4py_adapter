To run example: 

1) Install mem4py as in the instructions:https://github.com/pthedens/mem4py#installation   
  BUT: use the testing branch as I had to make some small changes in mem4py to make it work  
  git clone https://github.com/NikolausKurcz/mem4py.git  
  cd mem4py  
  git checkout testing  
  pip3 install -e .  

    
2) Install Openfoam 2212, Precice 2.5 and pyprecice     
3) In one Terminal run ./Allrun from Fluid folder    
4) In other Terminal run python3 main.py from Solid Folder  
