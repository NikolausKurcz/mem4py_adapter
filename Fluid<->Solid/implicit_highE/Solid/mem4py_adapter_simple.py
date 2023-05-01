# cython: profile=False, cdivision=True, boundcheck=False, wraparound=False, nonecheck=False, language_level=3
import sys, time, os, shutil
import numpy as np
import precice as pr
import colorama

from colorama import Fore, Style

np.set_printoptions(threshold=sys.maxsize)


class Mem4PyAdapter:

    def __init__(self, mem4py):
        

        self.solver = mem4py


        self.iteration = 0
 
        self.interface_indices = np.unique(np.asarray(self.solver.Nm)[np.asarray(self.solver.elFSI), 1:4].flatten())


        participant_name = "mem4py"
        configuration_file_name = "../preCICE.xml"
        mesh_name_nodes = "Structure_Nodes"
        mesh_name_cell_centers = "Structure_CellCenters"

        write_data_name = "Displacement"
        read_data_name = "Stress"

        # set up precice interface. proc no, nprocs
        self.interface = pr.Interface(participant_name, configuration_file_name,0,1)

        # get interface information
        mesh_id_nodes = self.interface.get_mesh_id(mesh_name_nodes)
        self.write_data_id = self.interface.get_data_id(write_data_name, mesh_id_nodes)

        mesh_id_cc = self.interface.get_mesh_id(mesh_name_cell_centers)
        self.read_data_id = self.interface.get_data_id(read_data_name, mesh_id_cc)

        # initialize interface node and cell center vectors

        self.displacements = np.zeros((len(self.interface_indices), 3))
        nodes = np.zeros((len(self.interface_indices), 3))
        nodes[:, 0] = np.copy(np.asarray(self.solver.X)[self.interface_indices])
        nodes[:, 1] = np.copy(np.asarray(self.solver.Y)[self.interface_indices])
        nodes[:, 2] = np.copy(np.asarray(self.solver.Z)[self.interface_indices])
        
        self.solver.computeCellCentre3D(np.asarray(self.solver.elFSI))
        cc = np.copy(self.solver.cc)
        
        # prepare nodal IDs
        self.node_ids = self.interface.set_mesh_vertices(mesh_id_nodes, nodes)
        self.cc_ids = self.interface.set_mesh_vertices(mesh_id_cc, cc)
        
        self.dt = self.interface.initialize()
        
       
        
        self.interface.initialize_data()
        

    def run_coupling(self):

        print('Starting coupling loop.')
        

        # start coupling loop
        while self.interface.is_coupling_ongoing():
        
            # writing iteration checkpoint
            if self.interface.is_action_required(pr.action_write_iteration_checkpoint()):
            
                datatemp = self.solver       
                temp = self.iteration
         
                print("WRITING iteration checkpoint")
                self.interface.mark_action_fulfilled(pr.action_write_iteration_checkpoint())

            # check if interface data is available
            if self.interface.is_read_data_available():
                self.read_data = self.interface.read_block_vector_data(self.read_data_id, self.cc_ids) 
                print("READING DATA FROM PRECICE")
                
            # run solver
            self.solver.Sx = np.copy(self.read_data[:,0]) 
            self.solver.Sy = np.copy(self.read_data[:,1])
            self.solver.Sz = np.copy(self.read_data[:,2])


            print(" ")
            print("Starting FEA.")
            print(" ")

            startTime = time.time()
            
            self.solver.time = self.iteration
        
            self.solver.solve()
            
            
            self.displacements[:, 0] = np.asarray(self.solver.X) -np.asarray(self.solver.X0)
            self.displacements[:, 1] = np.asarray(self.solver.Y) -np.asarray(self.solver.Y0)
            self.displacements[:, 2] = np.asarray(self.solver.Z) -np.asarray(self.solver.Z0)
            
            
            
            endTime = time.time()
            time_taken = endTime-startTime
        
            print("FEM took {} seconds".format(time_taken))
            
            
            self.iteration += 1
            self.solver.time = self.iteration
            
            

            if self.interface.is_write_data_required(self.dt):
                self.interface.write_block_vector_data(self.write_data_id, self.node_ids, self.displacements)
                print("WRITING DATA TO PRECICE")
                
                
            self.dt = self.interface.advance(self.dt)
         
                
            if self.interface.is_action_required(pr.action_read_iteration_checkpoint()):
                
                self.solver = datatemp 
                self.iteration =  temp
                print("READING iteration checkpoint")
                
                self.interface.mark_action_fulfilled(pr.action_read_iteration_checkpoint())
            else:
                print("mem4py: Timestep converged.")
                

        self.interface.finalize()

        


        
