import time
import numpy as np
import sys

import mem4py as m4p

import matplotlib.pyplot as plt
import pstats, cProfile
import mem4py_adapter_simple as mem4py_adapter


def main():

    print('Starting FSI Cavity Test')
    FSI_Cavity()

    
def FSI_Cavity():

    inputName = "testmembrane2"

    elStruc = {}
    elStruc["fixAll"] = {"set": "BC",
                         "type": "fixAll"}

    elStruc["Membrane"] = {"set": "ELEMENT",
                         "type": "MW",
                         "FSI" : True,
                         "pressure" : 0,
                         "h": 0.002,       
                         "E": 250E5, #was 250        
                         "density": 500,
                         "nu": 0
                         }  
                   
    problem = {"dim": 3,
               "msh": inputName,
               "wrinkling_model": "Jarasjarungkiat",
               "solver": "KDR",
               "method": "Barnes",
               "follower_pressure": True,
               "maxIterDR": 1000,
               "epsilon_R": 1E-7,
               "epsilon_KE": 1E-15,
               "gravity": False,
               "g": [0, -9.81, 0],
               "elStruc": elStruc
               }

    csm = m4p.Mem4py(problem)
    csm2 = mem4py_adapter.Mem4PyAdapter(csm)
    csm2.run_coupling()


   

if __name__ == "__main__":

    # cProfile.runctx("main()", globals(), locals(), "main.prof")
    # s = pstats.Stats("main.prof")
    # s.strip_dirs().sort_stats("time").print_stats()
    
    start = time.time()
    main()
    end = time.time()
    print("Simulation took {} seconds.\n".format(end - start))
