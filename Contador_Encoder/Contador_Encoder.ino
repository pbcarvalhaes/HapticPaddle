#define ENCODER_A 2
#define ENCODER_B 3

volatile int pos;
volatile bool state_A;
volatile bool state_B;
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
}
void conta_B_K(){
    pos -= 1 - (2*(state_A|state_B));
    state_B = !state_B;
}

void setup() {
  // put your setup code here, to run once:
    pinMode(ENCODER_A, INPUT);
    pinMode(ENCODER_B, INPUT);

    attachInterrupt(digitalPinToInterrupt(ENCODER_A), conta_A, CHANGE);
    attachInterrupt(digitalPinToInterrupt(ENCODER_B), conta_B, CHANGE);

    
}

void loop() {
  // put your main code here, to run repeatedly:
    
}
