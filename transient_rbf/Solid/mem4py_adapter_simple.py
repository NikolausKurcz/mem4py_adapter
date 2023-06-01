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
        
        T = self.dt
        # start coupling loop
        while self.interface.is_coupling_ongoing():
        
            # writing iteration checkpoint
            if self.interface.is_action_required(pr.action_write_iteration_checkpoint()):
            
                  
                X = self.solver.X 
                Y = self.solver.Y 
                Z = self.solver.Z 
                q1 = self.solver.u 
                q2 = self.solver.V 
                uDot = self.solver.uDot
                uDotDot = self.solver.uDotDot
                J11Vec = self.solver.J11Vec
                J12Vec = self.solver.J12Vec
                J22Vec = self.solver.J22Vec

                MV = self.solver.MV
                MinvR = self.solver.MinvR
                R = self.solver.R       
                RHS0 = self.solver.RHS0    
                Minv = self.solver.Minv
                M = self.solver.M      
                diagK = self.solver.diagK
                qq0 = self.solver.qq0
                
                RHS = self.solver.RHS 
                Ew = self.solver.Ew 
                RF = self.solver.RF 
                Fint = self.solver.Fint 
                #R = self.solver.R 
                M = self.solver.M 
                P = self.solver.P 
                #theta_vec = self.solver.theta_vec 
                counter = self.solver.time 
                time_array = self.solver.time_array 
                ke = self.solver.kinetic_energy
                se = self.solver.strain_energy 
                #temp = self.iteration
                datatemp2 = self.solver
                Ew = self.solver.Ew
                RF = self.solver.RF
                t = self.solver.t
                T = self.solver.props["T"]
               
                
                
                
         
                print("WRITING iteration checkpoint")
                self.interface.mark_action_fulfilled(pr.action_write_iteration_checkpoint())

            # check if interface data is available
            if self.interface.is_read_data_available():
                self.read_data = self.interface.read_block_vector_data(self.read_data_id, self.cc_ids) 
                print("READING DATA FROM PRECICE")
                
            # run solver
            #datatemp2 = self.solver
            self.solver.Sx = np.copy(self.read_data[:,0]) 
            self.solver.Sy = np.copy(self.read_data[:,1])
            self.solver.Sz = np.copy(self.read_data[:,2])


            print(" ")
            print("Starting FEA.")
            print(" ")

            startTime = time.time()
            

            self.solver.solve()
            
            
            self.displacements[:, 0] = np.asarray(self.solver.X) -np.asarray(self.solver.X0)
            self.displacements[:, 1] = np.asarray(self.solver.Y) -np.asarray(self.solver.Y0)
            self.displacements[:, 2] = np.asarray(self.solver.Z) -np.asarray(self.solver.Z0)
            
            
            
            endTime = time.time()
            time_taken = endTime-startTime
        
            print("FEM took {} seconds".format(time_taken))
            
            
           
            
            

            if self.interface.is_write_data_required(self.dt):
                self.interface.write_block_vector_data(self.write_data_id, self.node_ids, self.displacements)
                print("WRITING DATA TO PRECICE")
                
                
            self.dt = self.interface.advance(self.dt)
            
            
         
                
            if self.interface.is_action_required(pr.action_read_iteration_checkpoint()):
                
                self.solver.X = X
                self.solver.Y = Y
                self.solver.Z = Z
                self.solver.u = q1
                self.solver.V = q2
                self.solver.uDot = uDot
                self.solver.uDotDot = uDotDot
                self.solver.J11Vec = J11Vec
                self.solver.J12Vec = J12Vec
                self.solver.J22Vec  = J22Vec
                self.solver.MV = MV
                self.solver.MinvR = MinvR
                self.solver.R = R       
                self.solver.RHS0 = RHS0    
                self.solver.Minv = Minv    
                self.solver.M = M       
                self.solver.diagK = diagK  
                self.solver.qq0 = qq0

                
                self.solver.RHS = RHS
                self.solver.Ew = Ew
                self.solver.RF = RF
                self.solver.Fint = Fint
                #self.solver.R = R
                self.solver.M = M
                self.solver.P = P
                #self.solver.theta_vec = theta_vec
                self.solver.time = counter
                self.kinetic_energy = ke
                self.strain_energy = se
                #self.iteration =  temp
                self.solver.props["T"] = T
                self.solver.time_array = time_array
                self.solver.t = t
                
                self.solver.Ew = Ew
                self.solver.RF = RF
                print("READING iteration checkpoint")
                
               

                self.solver = datatemp2 
                self.interface.mark_action_fulfilled(pr.action_read_iteration_checkpoint())
            else:
                T = self.solver.time_array[-1] + self.dt
                self.solver.props["T"] = T
                self.solver.props["dt"] = 0.01
                self.solver.props["T0"]  = T-self.dt
                self.iteration += 1
                self.solver.time = self.iteration
                self.solver.qq0 = self.solver.qq
                print("mem4py: Timestep converged.")
                

        self.interface.finalize()

        


        
