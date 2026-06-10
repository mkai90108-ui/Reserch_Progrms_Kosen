#include <Mouse.h>
int x=0;
int y=0;

int memx=0;
int memy=0;

int move_x=0;
int move_y=0;

int timer=0;

void setup() {
  Serial1.begin(19200);
  Mouse.begin();

}

void loop() {
  if(Serial1.available()){
    String message = Serial1.readStringUntil('\n'); // 文字列を受信
    //Serial1.println(message);
    int input_x = stringToInteger(message.substring(0, 4));
    int input_y = stringToInteger(message.substring(4, 8));
    if (input_x==1000 && input_y==1000){
      Mouse.release();
      
      moveabs2(0,0,memx,-memy);
      memx = 0;
      memy = 0;
    }else{
      Mouse.press();
      if(input_x>=1000){
        input_x=0-input_x+1000;
      }
      if(input_y>=1000){
        input_y=0-input_y+1000;
      }
      moveabs2(input_x, -input_y,memx,-memy);
      memx=input_x;
      memy=input_y;
      
    }
    //Serial1.println(String(input_x)+","+String(input_y));
    //Serial1.println(String(x)+","+String(y));
    //Mouse.move(firstPart,secondPart);
  }
}

void moveabs1(int mx, int my){
  int vx;
  int vy;
    
  while(mx!=0 || my!=0){
    if(mx>=100){
      vx=100;
      mx=mx-100;
    }else if(mx<=-100){
      vx=-100;
      mx=mx+100;
    }else{
      vx=mx;
      mx=0;
    }
    if(my>=100){
      vy=100;
      my=my-100;
    }else if(my<=-100){
      vy=-100;
      my=my+100;
    }else{
      vy=my;
      my=0;
    }
    Mouse.move(vx, vy,0);
    delay(100);
  }
}

void moveabs2(int mx, int my, int mex, int mey){
  int vx=0;
  int vy=0;

  if(mx>mex){
    vx=mx-mex;
  }else if(mx<mex){
    vx=-(-mx+mex);
  }

  if(my>mey){
    vy=my-mey;
  }else if(my<mey){
    vy=-(-my+mey);
  }

  moveabs1(vx, vy);
  //Serial.println(String(mx)+","+String(my)+","+String(mex)+","+String(mey)+","+String(vx)+","+String(vy));
}

int stringToInteger(String input) {
  // Stringから整数に変換
  return input.toInt();
}
