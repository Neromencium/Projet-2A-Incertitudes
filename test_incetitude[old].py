import numpy as np
import matplotlib.pyplot as plt


test_cas = 2



# Définition du modèle
if test_cas == 1:
    def M(X):
        return -5*X[0]**2 - X[0]*X[1] - 6*X[0]*X[2] + 10*X[2]

elif test_cas == 2:
    def M(X):
        if (X[2]-0.5) <= 0 :
            return X[0] + X[2]*X[1] + 10*X[0]
        else :
            return X[0] + X[2]*X[1]

# Les deltas analytiques
if test_cas == 1:
    M_moy_analytic = np.array([8.5, 0.5, 7])
    M_var_analytic = np.array([137/12, 1/12, 3])

elif test_cas == 2:
    M_moy_analytic = np.array([6, 0.5, 5.5])
    M_var_analytic = np.array([25, 1/12, 8])




# Approximation décentré de la dérivée
def deriv_approx(f, x, dx, i):
    arr_dx = np.zeros(np.shape(x))
    arr_dx[i] = dx
    return ( f(x+arr_dx)-f(x) ) / dx



#################################



dX = 1e-1*np.ones(3) # Variation de la variable
n = 1000 # Nombre de tirages


# Liste des tirages
list_X = []
for i in range(n):
    list_X.append( np.random.uniform(size=3) )

# Liste des delta 1 et delta 2
list_delta1 = []
list_delta2 = []
    

# Calcul des indices de Morris
for i in range(3):
    somme = 0
    
    for k in range(n):
        somme += np.abs( deriv_approx(M, list_X[k], dX[i], i) )
    list_delta1.append(1/n * somme)
    
    somme = 0
    for k in range(n):
        somme += np.abs( deriv_approx(M, list_X[k], dX[i], i) )**2
    list_delta2.append(1/n * somme)


list_delta1 = np.array(list_delta1) # Liste des moyennes
list_delta2 = np.array(list_delta2) - list_delta1**2 # Liste des variances



#Tracé du résultat
list_nom = ["x1", "x2", "x3"]
list_col = ["red", "blue", "green"]

plt.figure()
plt.scatter(list_delta1, list_delta2, color = list_col)
plt.scatter(M_moy_analytic, M_var_analytic, marker="x", color = list_col)

for i in range(3):
    plt.annotate(
        list_nom[i],                        # Le texte à afficher
        (list_delta1[i], list_delta2[i]),   # Les coordonnées du point (x, y)
        textcoords="offset points",         # Comment positionner le texte
        xytext=(5, 5),                      # Décalage en pixels (x+5, y+5) depuis le point
        ha='left'                           # Alignement horizontal ('left', 'center', 'right')
    )
    
plt.grid()
plt.show()
