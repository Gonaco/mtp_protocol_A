#include "io.h"
#include "aux.h"

#define MAX_INDEX 24

uint32_t rout_ip_dir;
int rout_ip_l;
int interface;
uint32_t ip_dir;
int error,errorw = 0;
short offset;
int i;
int nz, naccess = 0;
int numberOfHashtables;
double searchingTime;
int fixed_bit24;
struct timeval initialTime, finalTime;
short *rout_table24 = NULL;
short *rout_table8 = NULL;

int proccessedPackets, totalTime = 0;
double tableAccesses = 0;

void creatingTable(){

  printf("\n\tIniciando Hash Table de 2^24...\n");
  
  rout_table24 = (short *)calloc((size_t) pow(2,MAX_INDEX), sizeof(short));
  unsigned int turn = 1;
  int lbyte;
  short fbyte;
  int extension24;
  int extension8;
  short ntable;
  int potencia8;

  printf("\tExtrayendo RIB...\n");

  while(error != REACHED_EOF){//Debemos tener en cuenta que da una iteración de más hasta darse cuenta del EOF.
    
    error=readFIBLine(&rout_ip_dir, &rout_ip_l, &interface);    
    	
    //Variables necesarias para el cálculo de las posiciones
    fixed_bit24 = 24-rout_ip_l;
    lbyte = rout_ip_dir/pow(2,32-MAX_INDEX);
    		
    if(fixed_bit24 < 0){ //Para prefijos mayores de 24

      fbyte = ((short) rout_ip_dir)%((short) pow(2,(32-MAX_INDEX)));
      offset = *(rout_table24+lbyte);
      potencia8 = 32-rout_ip_l;
      extension8 = 1<<potencia8;
	  
      if(offset < 0){ // Si en esa subnet ya existe tabla de tamaño 256 no se crea, solo si no tiene
	
	ntable = -1*offset;
	for(i=fbyte+ntable*256; i<fbyte+ntable*256+extension8; i++){
	  *(rout_table8+i)=(short) interface;
	}


      }else{ // La subnet no existe previamente
	
	if(turn == 1){
	  printf("\t\tIniciando Hash Table de 2^8...\n");
	  rout_table8 = (short *)calloc((size_t)pow (2,(32-MAX_INDEX)), sizeof(short));
	}else{
	  rout_table8 = (short *)realloc(rout_table8, 256*turn*sizeof(short));
	}
	for (i = 0; i<256; i++){//Rellenamos toda la tabla con la interfaz de la rout_table24, excepto lo nuevo
	  if(i<fbyte || i>(fbyte+extension8-1)){
	    *(rout_table8+i+(turn-1)*256) = offset;
	  }else{
	    *(rout_table8+i+(turn-1)*256) = (short) interface;
	  }
	}
	*(rout_table24+lbyte)=(-1)*(turn-1);
	turn++;
      }


      
    }else{ //Para prefijos menores de 24
      extension24 = 1<<fixed_bit24;
      for(i = 0; i < extension24; i++){ //La cantidad de huecos en la tabla a rellenar pertenecientes a la subred viene dado por su rout_ip_l (2^rout_ip_l)
	*(rout_table24+i+lbyte) = (short)interface; //La posición en la tabla es la rout_ip_dir que se nos da (*prefix = n[0]*pow(2,24) + n[1]*pow(2,16) + n[2]*pow(2,8) + n[3];) 
      }
    }
  }
}

void lookUp(){
  while(errorw != REACHED_EOF){
    errorw=readInputPacketFileLine(&ip_dir);
    proccessedPackets++;
	
    if(errorw != OK && errorw != REACHED_EOF){
      printIOExplanationError(errorw);
    }else{
      int ip_dir_div24 = ip_dir/pow(2,(32-MAX_INDEX));
      short interface_id = *(rout_table24+ip_dir_div24);
      numberOfHashtables = 1;
      tableAccesses++;
      gettimeofday(&finalTime,NULL);
      if(interface_id < 0){
	numberOfHashtables++;
    tableAccesses++;
	short ip_dir_div8 = ip_dir%((int) pow(2,(32-MAX_INDEX)));
	//Cogemos el dato
	printOutputLine(ip_dir, (int) *(rout_table8+ip_dir_div8+(-1)*interface_id*256), &initialTime, &finalTime, &searchingTime, numberOfHashtables);
      }else{
	//Cogemos el dato
	printOutputLine(ip_dir, (int) *(rout_table24+ip_dir_div24), &initialTime, &finalTime, &searchingTime, numberOfHashtables);
	      
      }
      totalTime += searchingTime;
	  
    }  
	  
  }
}


int main(int argc, char *argv[]){
  printf("\nIniciando RL...\n");
  if(argc!=3){
    printf("Introduzca RIB y direcciones, ni más ni menos.\n");
    return 0;
  }else{

    gettimeofday(&initialTime, NULL);
    printf("Analizando archivos: %s %s\n", argv[1], argv[2]);
    error=initializeIO(argv[1], argv[2]); 
    if(error != OK){
      printIOExplanationError(error);
      return error;
    }else{
      printf("Creando FIB...\n");
      creatingTable();
      
      if(error != OK && error != REACHED_EOF){
	printIOExplanationError(error);
	return error;
      }else{

	printf("Buscando interfaces...\n");

       	lookUp();

      }
    }
  }
  printf("Imprimiendo Resumen de la acción...\n");
  printSummary(proccessedPackets, tableAccesses/proccessedPackets, totalTime/proccessedPackets);
  printf("Liberando memoria (Tablas Hash)...\n");
  free(rout_table24);
  free(rout_table8);
  printf("Cerrando archivos...\n");
  freeIO();
  printf("Fin del proceso.\n\n");
  return 0;	
    
}
