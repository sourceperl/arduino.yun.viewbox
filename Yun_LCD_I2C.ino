#include <Wire.h> 
#include <Bridge.h>
// LCD I2C lib available at https://bitbucket.org/fmalpartida/new-liquidcrystal/wiki/Home
#include <LiquidCrystal_I2C.h>

// init I2C LCD for PCF8574 chip
#define I2C_ADDR 0x27 
#define BACKLIGHT_PIN 3 
#define En_pin 2 
#define Rw_pin 1 
#define Rs_pin 0 
#define D4_pin 4 
#define D5_pin 5 
#define D6_pin 6 
#define D7_pin 7 
LiquidCrystal_I2C lcd(I2C_ADDR,En_pin,Rw_pin,Rs_pin,D4_pin,D5_pin,D6_pin,D7_pin,BACKLIGHT_PIN,POSITIVE); 

void setup()
{
  // LCD panel (20 chars, 4 lines)
  lcd.begin(20,4);
  lcd.home();   
  lcd.print("Yun startup...");
  // init bridge
  Bridge.begin();
  delay(2000);
  lcd.clear();
}

void loop()
{
  /* update lines 1 to 4 via datastore vars "line_#" */
  char txt_buffer[21];

  Bridge.get("line_1", txt_buffer, sizeof(txt_buffer));
  lcd.setCursor(0, 0);
  lcd.print(txt_buffer);
  
  Bridge.get("line_2", txt_buffer, sizeof(txt_buffer));
  lcd.setCursor(0, 1);
  lcd.print(txt_buffer);

  Bridge.get("line_3", txt_buffer, sizeof(txt_buffer));
  lcd.setCursor(0, 2);
  lcd.print(txt_buffer);
  
  Bridge.get("line_4", txt_buffer, sizeof(txt_buffer));
  lcd.setCursor(0, 3);
  lcd.print(txt_buffer);
  
  delay(500);
}
