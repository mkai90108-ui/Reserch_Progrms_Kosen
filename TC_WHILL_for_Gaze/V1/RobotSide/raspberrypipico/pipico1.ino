int i=0;
int j=0;
String S;
void setup() {
  Serial.begin(19200);
  Serial1.begin(19200);
}

void loop() {
  if(Serial.available()){
    i=0;
    j=0;
    String val = Serial.readStringUntil('\n');
    //val.trim();
    int len = val.length();
    if(len==13){
      Serial1.println(val);
      //Serial.println(val);
      S = val;
    }
  }else{
    i=i+1;
  }
  if(i>=1 && 0==i%5 && i<=200){
    Serial1.println(S);
    //Serial.println(S);
  }
  if(i>=5000){
    j=1;
    i=0;
    Serial1.println("1000100000000");
    //Serial.println("1000100000000");
    S="1000100000000";
  }

  //Serial.println(i);
  delay(1);
}
