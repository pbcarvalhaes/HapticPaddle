
float theta0;
void setup() {
    // initialize the serial communication:
    Serial.begin(9600);  // set up Serial library at 9600 bps

    theta0 = analogRead(A10);
}

float p=(analogRead(A10)-561)*3.14/(2*270);  //position and conversion in radiants

void loop() {
    p=(analogRead(A10)-theta0)*3.14/(2*270);

    Serial.println(p, 6);
}
