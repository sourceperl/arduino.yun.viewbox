#include <Wire.h> 
#include <Bridge.h>
#include <Process.h>
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
Process p;

void setup()
{
  // init Serial
  Serial1.begin(250000);
  // init LCD panel (20 chars, 4 lines)
  lcd.begin(20,4);
  lcd.home();   
  lcd.print("Yun startup");
  // /sbin/reboot take time to stop linux
  // this delay fix this
  delay(10000);
  lcd.setCursor(0, 1);
  lcd.print("Bridge start...");
  // init bridge
  Bridge.begin();
  lcd.print("OK");
  delay(4000);
  // start python script
  lcd.setCursor(0, 2);
  lcd.print("Python start...");
  p.runShellCommand("python /root/bin/yun.py >/dev/null 2>/dev/null&");
  delay(2000);
  lcd.print("OK");
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
  delay(150);

  Bridge.get("line_2", txt_buffer, sizeof(txt_buffer));
  lcd.setCursor(0, 1);
  lcd.print(txt_buffer);
  delay(150);

  Bridge.get("line_3", txt_buffer, sizeof(txt_buffer));
  lcd.setCursor(0, 2);
  lcd.print(txt_buffer);
  delay(150);

  Bridge.get("line_4", txt_buffer, sizeof(txt_buffer));
  lcd.setCursor(0, 3);
  lcd.print(txt_buffer);
  delay(150);
}
