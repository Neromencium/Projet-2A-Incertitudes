import numpy as np
import matplotlib.pyplot as plt


g = 9.81

t_max = 0.1
a, b = 0, 1

n_x = 50
dx = (b-a)/(n_x - 1)

list_x = [a + dx*i for i in range(n_x)]

list_t = [0.0]

list_cond = [1, 1]

list_Dir = np.array([ [10,0],
                      [0,0] ])
list_Neu = np.array([ [0,0],
                      [0,0] ])



def lambda1(U):
    h = U[0] 
    q = U[1]
    return q/h - np.sqrt(g*h)


def lambda2(U):
    h = U[0] 
    q = U[1]
    return q/h + np.sqrt(g*h)


def eval_f(U):
    h = U[0] 
    q = U[1]
    return np.array([ [q],[q**2/h + g*h**2/2] ])


def schema_Vf(U, Un1, dx):
    
    time = 0.0

    # Tableau des valeurs des 2 flux calculés pour chaque maille
    tab_F = np.empty((4,n_x)) 
    
    while(time <= t_max):
        
        print(time)
        
        list_c = []
        
        for i in range(1, n_x-1):  # Boucle sur chaque maille intérieure
            f_Ui = eval_f(U[:,i])  
    
            f_Ui_p1 = eval_f(U[:,i+1])  
            
            f_Ui_m1 = eval_f(U[:,i-1])    
    
            c1 = np.max([ np.abs(lambda1(U[:,i-1])), np.abs(lambda1(U[:,i])),
                         np.abs(lambda2(U[:,i-1])), np.abs(lambda2(U[:,i])) ])      
            
            F1 = (f_Ui_m1 + f_Ui)/2 - c1 * (U[:,i][:,None] - U[:,i-1][:,None])/2
            
            c2 = np.max([ np.abs(lambda1(U[:,i+1])), np.abs(lambda1(U[:,i])),
                         np.abs(lambda2(U[:,i+1])), np.abs(lambda2(U[:,i])) ])   
            
            F2 = (f_Ui + f_Ui_p1)/2 - c2 * (U[:,i+1][:,None] - U[:,i][:,None])/2

            list_c.append( np.max([c1, c2]) )
            
            tab_F[0:2,i] = F1.flatten()
            tab_F[2:4,i] = F2.flatten()


        # --- Maille bord gauche ---
        
        
        f_Ui = eval_f(U[:,0])    

        f_Ui_p1 = eval_f(U[:,1])
    
        if list_cond[0] == 0:
                            
            U_dir = 2*list_Dir[:,0] - U[:,0]
            f_Ui_m1 = eval_f(U_dir)

            c1 = np.max([ np.abs(lambda1(U_dir)), np.abs(lambda1(U[:,0])),
                         np.abs(lambda2(U_dir)), np.abs(lambda2(U[:,0])) ])              
            F1 = (f_Ui_m1 + f_Ui)/2 - c1 * (U[:,0][:,None] - U_dir[:,None])/2
            
        else :
             
            U_neu = U[:,0] - dx*list_Neu[:,0]
            f_Ui_m1 = eval_f(U_neu)
            
            c1 = np.max([ np.abs(lambda1(U_neu)), np.abs(lambda1(U[:,0])),
                         np.abs(lambda2(U_neu)), np.abs(lambda2(U[:,0])) ])              
            F1 = (f_Ui_m1 + f_Ui)/2 - c1 * (U[:,0][:,None] - U_neu[:,None])/2
        

        c2 = np.max([ np.abs(lambda1(U[:,1])), np.abs(lambda1(U[:,0])),
                     np.abs(lambda2(U[:,1])), np.abs(lambda2(U[:,0])) ])   
        F2 = (f_Ui + f_Ui_p1)/2 - c2 * (U[:,1][:,None] - U[:,0][:,None])/2

        list_c.append( np.min([c1, c2]) )

        tab_F[0:2,0] = F1.flatten()
        tab_F[2:4,0] = F2.flatten()
            
            
        # --- Maille bord droit ---
            
        
        f_Ui = eval_f(U[:,n_x - 1])    

        f_Ui_m1 = eval_f(U[:,n_x - 2])
        
        c1 = np.max([ np.abs(lambda1(U[:,n_x - 1])), np.abs(lambda1(U[:,n_x - 2])),
                     np.abs(lambda2(U[:,n_x - 1])), np.abs(lambda2(U[:,n_x - 2])) ])             
        F1 = (f_Ui_m1 + f_Ui)/2 - c1 * (U[:,n_x - 1][:,None] - U[:,n_x - 2][:,None])/2
    
        if list_cond[1] == 0:
                            
            U_dir = 2*list_Dir[:,1] - U[:,n_x - 1]
            f_Ui_p1 = eval_f(U_dir)

            c2 = np.max([ np.abs(lambda1(U_dir)), np.abs(lambda1(U[:,n_x - 1])),
                         np.abs(lambda2(U_dir)), np.abs(lambda2(U[:,n_x - 1])) ])              
            F2 = (f_Ui_p1 + f_Ui)/2 - c2 * (U_dir[:,None] - U[:,n_x - 1][:,None])/2
            
        else :
             
            U_neu = U[:,n_x - 1] + dx*list_Neu[:,1]
            f_Ui_p1 = eval_f(U_neu)
            
            c2 = np.max([ np.abs(lambda1(U_neu)), np.abs(lambda1(U[:,n_x - 1])),
                         np.abs(lambda2(U_neu)), np.abs(lambda2(U[:,n_x - 1])) ])              
            F2 = (f_Ui_p1 + f_Ui)/2  - c2 * (U_neu[:,None] - U[:,n_x - 1][:,None])/2
        
        list_c.append( np.min([c1, c2]) )

        tab_F[0:2, n_x - 1] = F1.flatten()
        tab_F[2:4, n_x - 1] = F2.flatten()
            
            
        # --- Obtention de dt ---
            
        dt = 0.5 * dx / np.max(list_c)


        # --- Calcul du terme source ---
        
        S = np.empty((2,n_x))
        
        for i in range(n_x):
            
            S[0, i] = 0
            
            pos_x = a + (i + 0.5)*dx
            
            h_i = U[0,i]
            
            S[1, i] = g/2  * ( max( 0, h_i + z(pos_x) - max(z(pos_x), z(pos_x + dx)) )**2 - \
                               max( 0, h_i + z(pos_x) - max(z(pos_x), z(pos_x - dx)) )**2 )
            
                
        # --- Màj de la solution ---         

        for i in range(n_x):
           
            Un1[:,i] = U[:,i] - dt/dx * ( tab_F[2:4,i] - tab_F[0:2,i] ) + dt * S[:,i]
        
        U = Un1.copy()

        time += dt

    return U



list_c_x = np.array([a + (i + 0.5) * dx for i in range(n_x)])

# Fonction topographie z(x)
def z(x):
    # Test 1 : Bosse gaussienne au milieu
    return 0.2 * np.exp(-20.0 * (x - 0.5)**2)
    # Test 2 (Rupture de barrage) : Fond plat
    # return np.zeros_like(x)

# --- CHOIX DU TEST INITIAL ---
test_choisi = 2  # 1 pour Lac au repos, 2 pour Rupture de barrage

U = np.empty((2, n_x))

if test_choisi == 1:
    # --- TEST 1 : Lac au repos ---
    eta_0 = 1.0  # Cote de la surface libre plate
    for i in range(n_x):
        h_i = max(0.0, eta_0 - z(list_c_x[i]))
        q_i = 0.0
        U[:, i] = [h_i, q_i]
        
elif test_choisi == 2:
    # --- TEST 2 : Rupture de barrage (fond plat) ---
    for i in range(n_x):
        if list_c_x[i] < 0.5:
            h_i = 2.0
        else:
            h_i = 1.0
        q_i = 0.0
        U[:, i] = [h_i, q_i]

# Tableau pour stocker la solution au temps suivant
Un1 = np.empty_like(U)



U = schema_Vf(U, Un1, dx)


plt.figure()
plt.plot(list_c_x, U[0,:], label="Hauteur d'eau h")
plt.plot(list_c_x, z(np.array(list_c_x)), label="Topographie z")
plt.plot(list_c_x, U[0,:] + z(np.array(list_c_x)), label="Surface libre (h+z)", linestyle="--")
plt.legend()
plt.xlabel("x")
plt.ylabel("Hauteur (m)")
plt.show()
