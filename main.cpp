#include "Parameters.h"

#include <string>
#include <Eigen/Dense>


int main(int argc, char ** argv)
{
	if (argc!=2) {
	std::cerr << "usage: " << argv[0] << " <input.toml>" << std::endl;
	exit(-1);
	}
	// Sinon : le nom du fichier est dans argv[1]

	const std::string filename = argv[1];

	/*************************
	* 1 - Lecture de test.toml
	*************************/
	Parameters params;
	params.read_from_file( filename );
	
	if (params.debug) { params.print(); }
	
	/*************************
	* 2 - Vérification de la compilation
	*************************/
	if (params.mode == "test") {
		std::cout << "Mode de test d'exécution (rien n'est calculé)." << std::endl;
	}
	else {

	}
	
	return 0;
}

