#define ENCODER_A 2
#define ENCODER_B 3
#define TEMPO_A 10000

volatile long pos = 0;
double velocidade = 0;
double pos_ant = 0;
double pos_ag = 0;
unsigned long tempo_ant = 0;
unsigned long tempo_ag = 0;
volatile bool state_A = true;
volatile bool state_B = true;
//Do not use volatile variables directly!

const double to_radians = 2.0*(PI/48.0)/74.83;

void conta_A() {
    if(state_A){
        if(state_B){
            pos++;
        }
        else{
            pos--;
        }
    }
    else{
        if(state_B){
            pos--;
        }
        else{
            pos++;
        }
    }
    state_A = !state_A;
}
void conta_A_K(){
    pos += 1 - ((state_A|state_B)<<1);
    state_A = !state_A;
}
void conta_B() {
    if(state_B){
        if(state_A){
            pos--;
        }
        else{
            pos++;
        }
    }
    else{
        if(state_A){
            pos++;
        }
        else{
            pos--;
        }
    }
    state_B = !state_B;
}
void conta_B_K(){
    pos -= 1 - ((state_A|state_B)<<1);
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

    tempo_ag = micros();
}

void loop() {
  // put your main code here, to run repeatedly:

  if(micros() - tempo_ag >= TEMPO_A){
    tempo_ant = tempo_ag;
    tempo_ag = micros();
    
    pos_ant = pos_ag;
    pos_ag = pos*to_radians;
  
    velocidade = (pos_ag-pos_ant)/((tempo_ag - tempo_ant)/1000.0);
    
    Serial.println(1000*velocidade, 5);
  }

  
}
