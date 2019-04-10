#define ENCODER_A 2
#define ENCODER_B 3
#define TEMPO_A 10

volatile long pos = 0;
double Angulo = 0;
volatile int volta= 0;
float velocidade = 0;
double pos_ant = 0;
double pos_ag = 0;
unsigned long tempo_ant = 0;
unsigned long tempo_ag = 0;
volatile bool state_A = true;
volatile bool state_B = true;
//Do not use volatile variables directly!

void conta_A() {
    if(state_A){
        if(state_B){
            pos+=1;
        }
        else{
            pos-=1;
        }
    }
    else{
        if(state_B){
            pos-=1;
        }
        else{
            pos+=1;
        }
    }
    state_A = !state_A;

    
    /*if (Angulo > 180){
      volta += Angulo / 360;
      Angulo = (Angulo % 360) - 180; 
    }
    else{
      if (Angulo < -180) {
        volta -= Angulo / 360;
        Angulo = (Angulo % 360) - 180;
      }
    }*/
}
void conta_A_K(){
    pos += 1 - (2*(state_A|state_B));
    state_A = !state_A;
}
void conta_B() {
    if(state_B){
        if(state_A){
            pos-=1;
        }
        else{
            pos+=1;
        }
    }
    else{
        if(state_A){
            pos+=1;
        }
        else{
            pos-=1;
        }
    }
    state_B = !state_B;

    
    /*if (Angulo > 180){
      volta += Angulo / 360;
      Angulo = (Angulo % 360); 
    }
    else{
      if (Angulo < -180) {
        volta -= Angulo / 360;
        Angulo = (Angulo % 360);
      }
    }*/
}
void conta_B_K(){
    pos -= 1 - (2*(state_A|state_B));
    state_B = !state_B;
}

void setup() {
  // put your setup code here, to run once:
    Serial.begin(9600);  // set up Serial library at 9600 bps
    
    pinMode(ENCODER_A, INPUT);
    pinMode(ENCODER_B, INPUT);

    state_A = (digitalRead(ENCODER_A) == HIGH);
    state_B = (digitalRead(ENCODER_B) == HIGH);

    attachInterrupt(digitalPinToInterrupt(ENCODER_A), conta_A, CHANGE);
    attachInterrupt(digitalPinToInterrupt(ENCODER_B), conta_B, CHANGE);

    tempo_ag = millis();
}

void loop() {
  // put your main code here, to run repeatedly:

  if(millis() - tempo_ag > TEMPO_A){
    tempo_ant = tempo_ag;
    tempo_ag = millis();
    
    pos_ant = pos_ag; 
    Angulo = (pos*2*(PI/48))/(74.83);
    pos_ag = Angulo;
  
    velocidade = (pos_ag-pos_ant)/(tempo_ag - tempo_ant);
    
    Serial.println(1000*velocidade);
    //Serial.print(" ");
    //Serial.println(tempo_ag);
  }
  //Serial.println(tempo_ag - tempo_ant);

  
}
