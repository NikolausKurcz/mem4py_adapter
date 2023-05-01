# mem4py_adapter

Trying to couple the fem solver mem4py with openFoam using preCICE. 

Plan is to recreate the FSI lid driven cavity example which is for example explained here (but in 3D): 
https://kratosmultiphysics.github.io/Examples/fluid_structure_interaction/validation/fsi_lid_driven_cavity/

As a basis the example case from the mbdyn adapter is taken from: 
https://github.com/precice/mbdyn-adapter parts of the example is also from https://github.com/Hag3nL/mbdyn-adapter


Uses: 
mem4py (https://github.com/pthedens/mem4py)
preCICE 2.5 
OpenFOAM-2212
