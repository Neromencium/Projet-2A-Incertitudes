#include "Parameters.h"
#include <toml11/single_include/toml.hpp>
#include <iostream>

/**
* Lit le paramètre 'name' (sous la forme []) dans le fichier toml.
* Renvoie un VectorX<T> (avec T=double ou int, par exemple).
* Exemple : const Eigen::VectorXi N = get_VectorX_from_toml<int>( tomlfile, "N" );
*/
Eigen::VectorXd get_VectorXd_from_toml( const toml::value & tomlfile, const std::string & name )
{
    // On aimerait bien faire ça, mais ce n'est pas possible :
    // return toml::find<Eigen::VectorXd>(tomlfile, name);
    // On doit le faire en 2 étapes et passer par un "Map" de Eigen...
    std::vector<double> vec = toml::find<std::vector<double>>(tomlfile, name);
    const Eigen::VectorXd result = Eigen::Map<Eigen::VectorXd>(vec.data(), vec.size());
    return result;
}


void Parameters::read_from_file( const std::string & filename )
{
    this->tomlfile = toml::parse(filename, toml::spec::v(1,1,0));
    
    // Récupère chaque paramètre
    this->t_final = toml::find<double>(this->tomlfile, "t_final");
    this->dx = toml::find<double>(this->tomlfile, "dx");
    this->Lx = toml::find<double>(this->tomlfile, "Lx");
    this->nx = std::ceil(this->Lx/this->dx);
    this->output = toml::find<std::string>(this->tomlfile, "output");
    this->mode = toml::find<std::string>(this->tomlfile, "mode");
    this->integrator_name = toml::find<std::string>(this->tomlfile, "integrator");
    this->X_0 = get_VectorXd_from_toml(this->tomlfile,"X_0");
    
    this->output = this->output+this->integrator_name+".dat";

    // Les paramètres optionnels
    if (this->tomlfile.contains("debug")) {
        this->debug = toml::find<bool>(this->tomlfile, "debug");
    }
    
    // Vérification de la cohérence des paramètres
    if (this->dx < 1e-12) {
        std::cerr << "dx ne peut pas être si petit ! " << this->dx << std::endl;
        exit(-2);
    }
    if (this->t_final < this->dx) {
        std::cerr << "t_final doit être >= dx ! " << this->t_final << std::endl;
        exit(-2);
    }
    if (this->X_0.size()==0) {
        std::cerr << "La condition initiale doit être définie !" << std::endl;
        exit(-2);
    }
    
    // Traitement des paramètres déduits :
    this->update_n_iterations();
    
    if (this->output!="") {
        this->save_output = true;
    }
}

void Parameters::print( std::ostream & output ) const
{
    output << "# ------------------------" << std::endl;
    output << "# Temps final : " << this->t_final << std::endl;
    output << "# Pas : " << this->dx << std::endl;
    output << "# Nombre d'itérations : " << this->n_iterations << std::endl;
    output << "# Mode : " << this->mode << std::endl;
    if (this->save_output) {
        output << "# Fichier de sortie : " << this->output << std::endl;
    }
    else {
        output << "# Pas de fichier de sortie." << std::endl;
    }
    output << "# Condition initiale : " << this->X_0.transpose() << std::endl;
    output << "# Intégratrice : " << this->integrator_name << std::endl;
    output << "# Debug : " << this->debug << std::endl;
    output << "# ------------------------" << std::endl;
}

void Parameters::update_n_iterations()
{
    // A MODIFIER : Il faut adapter dt à chaque maille
    double dt = 0.0;
    this->n_iterations = int(ceil(this->t_final/dt));
    // Fait en sorte que le pas de temps tombe exactement sur le temps final
    this->dx = this->t_final / this->n_iterations;
}