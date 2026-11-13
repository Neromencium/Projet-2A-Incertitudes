import numpy as np
import matplotlib.pyplot as plt


g = 9.81

t_max = 5
a, b = 0, 1

n_x = 100
dx = (b-a)/(n_x - 1)

list_x = [a + dx*i for i in range(n_x)]

time = 0.0
list_t = [0.0]

list_cond = [0, 0]

list_Dir = np.array([ [10,0],
                      [0,0] ])
list_Neu = np.array([ [0,0],
                      [0,0] ])

# Tableau des valeurs des 2 flux calculés pour chaque maille
tab_F = np.empty((2,n_x)) 



# Fonction associée à la batymétrie
def z(x):
    return x


def lambda1(U):
    h = U[0,:] 
    q = U[1,:]
    return q - np.sqrt(g*h)


def lambda2(U):
    h = U[0,:] 
    q = U[1,:]
    return q + np.sqrt(g*h)


def eval_f(U):
    h = U[0,:] 
    q = U[1,:]
    return np.array([ [q],[q**2/h + g*h**2/2] ])


def schema_Vf(U,dx):
    
    while(time <= t_max):
        
        list_c = []
        
        for i in range(1, n_x-1):  # Boucle sur chaque maille intérieure
            f_Ui = eval_f(U[:,i])  
    
            f_Ui_p1 = eval_f(U[:,i+1])  
            
            f_Ui_m1 = eval_f(U[:,i-1])
    
    
            c1 = np.max([ np.abs(lambda1(U[:,i-1])), np.abs(lambda1(U[:,i])),
                         np.abs(lambda2(U[:,i-1])), np.abs(lambda2(U[:,i])) ])              
            F1 = (f_Ui_m1 + f_Ui)/2 - c1 * (U[:,i] - U[:,i-1])/2
            
            c2 = np.max([ np.abs(lambda1(U[:,i+1])), np.abs(lambda1(U[:,i])),
                         np.abs(lambda2(U[:,i+1])), np.abs(lambda2(U[:,i])) ])   
            F2 = (f_Ui + f_Ui_p1)/2 - c2 * (U[:,i+1] - U[:,i])/2

            list_c.append( np.min([c1, c2]) )
            
            tab_F[i,0] = F1
            tab_F[i,1] = F2


            # --- Maille bord gauche ---
        
        
            f_Ui = eval_f(U[:,0])    

            f_Ui_p1 = eval_f(U[:,1])
        
            if list_cond[0] == 0:
                                
                U_dir = 2*list_Dir[:,0] - U[:,0]
                f_Ui_m1 = eval_f(U_dir)

                c1 = np.max([ np.abs(lambda1(U_dir)), np.abs(lambda1(U[:,0])),
                             np.abs(lambda2(U_dir)), np.abs(lambda2(U[:,0])) ])              
                F1 = (f_Ui_m1 + f_Ui)/2 - c1 * (U[:,0] - U_dir)/2
                
            else :
                 
                U_neu = U[:,0] - dx*list_Neu[:,0]
                f_Ui_m1 = eval_f(U_neu)
                
                c1 = np.max([ np.abs(lambda1(U_neu)), np.abs(lambda1(U[:,0])),
                             np.abs(lambda2(U_neu)), np.abs(lambda2(U[:,0])) ])              
                F1 = (f_Ui_m1 + f_Ui)/2 - c1 * (U[:,0] - U_neu)/2
            

            c2 = np.max([ np.abs(lambda1(U[:,1])), np.abs(lambda1(U[:,0])),
                         np.abs(lambda2(U[:,1])), np.abs(lambda2(U[:,0])) ])   
            F2 = (f_Ui + f_Ui_p1)/2 - c2 * (U[:,1] - U[:,0])/2

            list_c.append( np.min([c1, c2]) )

            tab_F[0,0] = F1
            tab_F[0,1] = F2
            
            
            # --- Maille bord droit ---
            
            
            f_Ui = eval_f(U[:,n_x - 1])    

            f_Ui_m1 = eval_f(U[:,n_x - 2])
            
            c1 = np.max([ np.abs(lambda1(U[:,n_x - 1])), np.abs(lambda1(U[:,n_x - 2])),
                         np.abs(lambda2(U[:,n_x - 1])), np.abs(lambda2(U[:,n_x - 2])) ])             
            F1 = (f_Ui_m1 + f_Ui)/2 - c1 * (U[:,n_x - 1] - U[:,n_x - 2])/2
        
            if list_cond[1] == 0:
                                
                U_dir = 2*list_Dir[:,1] - U[:,n_x - 1]
                f_Ui_p1 = eval_f(U_dir)

                c2 = np.max([ np.abs(lambda1(U_dir)), np.abs(lambda1(U[:,n_x - 1])),
                             np.abs(lambda2(U_dir)), np.abs(lambda2(U[:,n_x - 1])) ])              
                F2 = (f_Ui_p1 + f_Ui)/2 - c2 * (U_dir - U[:,n_x - 1])/2
                
            else :
                 
                U_neu = U[:,n_x - 1] + dx*list_Neu[:,1]
                f_Ui_p1 = eval_f(U_neu)
                
                c2 = np.max([ np.abs(lambda1(U_neu)), np.abs(lambda1(U[:,n_x - 1])),
                             np.abs(lambda2(U_neu)), np.abs(lambda2(U[:,n_x - 1])) ])              
                F2 = (f_Ui_p1 + f_Ui)/2  - c2 * (U_neu - U[:,n_x - 1])/2
            
            list_c.append( np.min([c1, c2]) )

            tab_F[n_x - 1,0] = F1
            tab_F[n_x - 1,1] = F2
            
            
        dt = np.min(dx/(2*list_c)) 

        pos_x = a
        for i in range(n_x):
            
            




U = np.empty((2,n_x))
Un1 = np.empty((2,n_x))





