To run example:

Install mem4py as in the instructions:https://github.com/pthedens/mem4py#installation
BUT: use the testing branch as I had to make some small changes in mem4py to make it work
git clone https://github.com/NikolausKurcz/mem4py.git
cd mem4py
git checkout testing
pip3 install -e .

Install Openfoam 2212, Precice 2.5 and pyprecice

Install RBFMeshMotionSolver from https://github.com/solids4foam/solids4foam/tree/master/src/RBFMeshMotionSolver
I think its possible to only install the RBFMeshMotionSolver without installing solids4foam


In one Terminal run ./Allrun from Fluid folder

In other Terminal run python3 main.py from Solid Folder
