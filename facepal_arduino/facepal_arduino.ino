#include <MeMegaPi.h>
#include <ros.h>
#include <std_msgs/Int32.h>
#include <std_msgs/Float32.h>
#include <std_msgs/Int32MultiArray.h>

//INITIALISATION DES 4 MOTEURS
MeEncoderOnBoard Encoder_1(SLOT1);
MeEncoderOnBoard Encoder_2(SLOT2);
MeEncoderOnBoard Encoder_3(SLOT3);
MeEncoderOnBoard Encoder_4(SLOT4);

//INITIALISATION DE NOEUD ROSSERIAL
ros::NodeHandle nh;

//LES VARIABLES DE DONNEES POUR LES ANGLES
//"commands" reçoit les angles
//"positions" envoie les angles  
std_msgs::Int32MultiArray commands;
std_msgs::Int32MultiArray positions;

//DEFINITION DU TOPIC SUR LEQUEL ROSSERIAL PUBLIE LES ANGLES
ros::Publisher pub("motors_positions", &positions);

//POSITIONS DE DEPART
int pos1=0;
int pos2=0;
int pos3=0;
int pos4=0;

//FONCTIONS PAR DEFAUT POUR INTERROMPRE LES MOTEURS A LA FIN DU MOUVEMENT (1/4)
void isr_process_encoder1(void)
{
  if(digitalRead(Encoder_1.getPortB()) == 0)
  {
    Encoder_1.pulsePosMinus();
  }
  else
  {
    Encoder_1.pulsePosPlus();;
  }
}

//(2/4)
void isr_process_encoder2(void)
{
  if(digitalRead(Encoder_2.getPortB()) == 0)
  {
    Encoder_2.pulsePosMinus();
  }
  else
  {
    Encoder_2.pulsePosPlus();;
  }
}

//(3/4)
void isr_process_encoder3(void)
{
  if(digitalRead(Encoder_3.getPortB()) == 0)
  {
    Encoder_3.pulsePosMinus();
  }
  else
  {
    Encoder_3.pulsePosPlus();;
  }
}

//(4/4)
void isr_process_encoder4(void)
{
  if(digitalRead(Encoder_4.getPortB()) == 0)
  {
    Encoder_4.pulsePosMinus();
  }
  else
  {
    Encoder_4.pulsePosPlus();;
  }
}

//LA FONCTION APPELLEE A CHAQUE RECEPTION DE DONNEES VIA ROSSERIAL
void callBackFunction(const std_msgs::Int32MultiArray &inputMessage){

  //ATTACHEMENT DES FONCTIONS D'INTERRUPTIONS SUR LES 4 MOTEURS
  attachInterrupt(Encoder_1.getIntNum(), isr_process_encoder1, RISING);
  attachInterrupt(Encoder_2.getIntNum(), isr_process_encoder2, RISING);
  attachInterrupt(Encoder_3.getIntNum(), isr_process_encoder3, RISING);
  attachInterrupt(Encoder_4.getIntNum(), isr_process_encoder4, RISING);
  
  //MISE DE "commands" A LA MÊME TAILLE QUE "inputMessage"(MESSAGE RECU)
  commands.data_length = inputMessage.data_length;
  commands.data = (int32_t*)realloc(commands.data, commands.data_length * sizeof(int32_t));
  
  //STOCKAGE DES VALEURS DU TABLEAU RECU VIA ROSSERIAL DANS UNE VARIABLE "commands"
  for (uint16_t i = 0; i < commands.data_length; i++) {
    commands.data[i] = inputMessage.data[i];
  }
  
  //MOUVEMENT DES ROBOTS EN FONCTION DES DONNEES RECUES
  Encoder_1.moveTo(commands.data[0], commands.data[1]);
  Encoder_2.moveTo(commands.data[2], commands.data[3]);
  Encoder_3.moveTo(commands.data[4], commands.data[5]);
  Encoder_4.moveTo(commands.data[6], commands.data[7]);
  
}

//DEFINITION DU TOPIC DEPUIS LEQUEL ROSSERIAL RECOIT LES ANGLES
ros::Subscriber<std_msgs::Int32MultiArray> sub("motors_commands", &callBackFunction);

void setup()
{
  //INITIALISATION DU NOEUD ROSSERIAL
  nh.initNode();
  positions.data_length = 3;

  positions.data = (int32_t*)malloc(positions.data_length * sizeof(int32_t));

  //DEFINITION DU PWM DES MOTEURS (PUISSANCE MOYENNE DELIVREE)
  TCCR1A = _BV(WGM10);
  TCCR1B = _BV(CS11) | _BV(WGM12);

  TCCR2A = _BV(WGM21) | _BV(WGM20);
  TCCR2B = _BV(CS21);

  //INITIALISATION DES PARAMETRES DES MOTEURS (PAR DEFAUT DEPUIS MBLOCK) (1/4)
  Encoder_1.setPulse(7);
  Encoder_1.setRatio(26.9);
  Encoder_1.setPosPid(1.8,0,1.2);
  Encoder_1.setSpeedPid(0.18,0,0);
  //(2/4)
  Encoder_2.setPulse(7);
  Encoder_2.setRatio(26.9);
  Encoder_2.setPosPid(1.8,0,1.2);
  Encoder_2.setSpeedPid(0.18,0,0);
  //(3/4)
  Encoder_3.setPulse(7);
  Encoder_3.setRatio(26.9);
  Encoder_3.setPosPid(1.8,0,1.2);
  Encoder_3.setSpeedPid(0.18,0,0);
  //(4/4)
  Encoder_4.setPulse(7);
  Encoder_4.setRatio(26.9);
  Encoder_4.setPosPid(1.8,0,1.2);
  Encoder_4.setSpeedPid(0.18,0,0);

  //ACTIVATION DU PUBLISHER
  nh.advertise(pub);

  //ABONNEMENT AU TOPIC "/motors_commands"
  nh.subscribe(sub);
}

void loop(){

  //ICI :
  //".loop()" SERT A MAINTENIR LE MOTEUR EN MOUVEMENT JUSQU'A L'ANGLE VOULU
  //".updateSpeed" SERT A RAFRACHIR LA VITESSE DU MOTEUR
  //".updateCurPos" SERT A RAFRAICHIR LA POSITION DU MOTEUR (1/4)
  Encoder_1.loop();
  Encoder_1.updateSpeed();
  //Encoder_1.updateCurPos();
  //(2/4)
  Encoder_2.loop();
  Encoder_2.updateSpeed();
  Encoder_2.updateCurPos();
  //(3/4)
  Encoder_3.loop();
  Encoder_3.updateSpeed();
  Encoder_3.updateCurPos();
  //(4/4)
  Encoder_4.loop();
  Encoder_4.updateSpeed();
  Encoder_4.updateCurPos();

  //ENREGISTREMENT DES ANGLES MIS A JOUR DANS LE TABLEAU "positions"
  positions.data[0] = Encoder_1.getCurPos();
  positions.data[1] = Encoder_2.getCurPos();
  positions.data[2] = Encoder_3.getCurPos();
  positions.data[3] = Encoder_4.getCurPos();

  //PUBLICATION DU TABLEAU
  pub.publish(&positions);

  //MISE EN BOUCLE DU NOEUD
  nh.spinOnce();

  //DELAI POUR NE PAS SATURER LA MEMOIRE
  //SINON PROBLEMES D'ALLOCATION DYNAMIQUE
  delay(1);

}



