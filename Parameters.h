/**
* Une classe qui stocke/encapsule les différents paramètres du code de calcul.
* Cette classe pourrait être remplie depuis un fichier de paramètres.
**/

#ifndef _PARAMETERS_H
#define _PARAMETERS_H

#include <string>
#include <iostream>
#include <Eigen/Dense>
#include <toml11/single_include/toml.hpp>

class Parameters
{
   public:
   double t_final = 0.0;             // Temps final
   double dx = 0.0;                  // Pas
   int nx = 0;                       // Nombre de mailles
   double Lx = 1.0;                  // Longueur du domaine

   std::vector<double> x;             // Coordonnées des mailles
   std::vector<double> h;             // Hauteurs d'eau
   std::vector<double> u;             // Vitesses
   std::vector<double> z;             // Topographie
   

   std::string output = "";           // Nom du fichier de sortie ; "" pour aucun
   Eigen::VectorXd X_0;                // Condition initiale
   std::string mode = "integration";     // Mode d'exécution ?
   bool debug = false;                // Affichage du debug ?
   
   std::string integrator_name = "Euler";      // Schéma d'intégration
   
   // Attributs calculés automatiquement :
   unsigned int n_iterations = 0;              // Nombre d'itérations
   bool save_output = false;                   // Enregistrement du fichier de sortie
   
   // Construit les paramètres à partir du nom de fichier
   void read_from_file( const std::string & filename );
   // Affiche le contenu de la classe vers l'output (par défaut : std::cout), comme par exemple un fichier.
   void print( std::ostream & output = std::cout ) const;
   
   // Doit être appelé pour mettre à jour le nombre d'itérations si dt ou t_final a été modifié
   void update_n_iterations();
   
   toml::value tomlfile;        // La structure de données lue par toML pour utilisation ultérieure
};

#endif