#include <Wire.h>  // Only needed for Arduino 1.6.5 and earlier
#include "SSD1306.h" // alias for `#include "SSD1306Wire.h"`
#include <ESP8266WiFi.h>
#include "string.h"
#include <ArduinoHttpClient.h>
#include <ArduinoJson.h>
#include "tinyxml2.h"
#include "SoftTimer.h"
#include "Esp.h"
#include "images.h"

#include <DNSServer.h>            //Local DNS Server used for redirecting all requests to the configuration portal
#include <ESP8266WebServer.h>     //Local WebServer used to serve the configuration portal
#include <WiFiManager.h>          //https://github.com/tzapu/WiFiManager WiFi Configuration Magic

#define TIME_BETWEEN_SCREEN_UPDATE 1000
#define TIME_BETWEEN_TRAINS_SCRAP 30000
#define OFFSET_BETWEEN_TRAINS_SCRAP 5000

WiFiClient wclient;
const char* server = "54.171.231.139";
const int flaskPort = 7000;

HttpClient httpclient_params_server = HttpClient(wclient, server, flaskPort);
HttpClient httpclient_transilien_server = HttpClient(wclient, "api.transilien.com");


typedef struct {
  char** buffer;
  int nbr_char_par_ligne;
  int nbr_lignes;
  char header[100];
  int first_train_received;
  long gare_depart;
  long gare_arrivee;
} Ecran_t;

Ecran_t* ecrans;

int ecran_courant  = 1;
int nbr_ecrans=0;

SSD1306  display(0x3c, D2, D1);


SoftTimer timer;  // create the timer object for get trains
class EventTrains : public EventBase
{
public:
    int index_ecran;
};
EventTrains* events_trains;

int debug = 1;

void print_debug(String mess){
  if (debug == 1)
      Serial.println(mess);
}


char** parse_api_transilien_response(char* resp, int nbr_max_lignes, /*output*/ int* nbr_lignes) {

        tinyxml2::XMLDocument doc;
        doc.Parse( resp );
        tinyxml2::XMLElement* trainElement = doc.FirstChildElement( "passages" )->FirstChildElement( "train" );

        int cpt_trains = 0;

        char** ret = (char**) malloc( nbr_max_lignes * sizeof(char*) );

        while (trainElement != NULL) {
          const char* train = trainElement->FirstChildElement( "date" )->GetText();
          print_debug( "Train:" + String(train) );
          const char* mode = trainElement->FirstChildElement( "date" )->Attribute("mode");
          const char* etat = trainElement->FirstChildElement( "date" )->Attribute("etat");
          if (etat == NULL)
            etat = "Normal";
          print_debug( "Mode:" + String(mode));
          print_debug( "Etat:" + String(etat) );
          
          trainElement = trainElement->NextSiblingElement();

          char* temp = (char*) malloc(100*sizeof(char));
          char* temp_start=temp;

          *temp++ = *mode;

          while (*train != 0x20)
            train++;

          while (*train != 0){
            *temp++ = *train++;
          }

          *temp++ = ' ';

          while (*etat != 0){
            *temp++ = *etat++;
          }

          *temp = 0;
          *(ret + cpt_trains) = temp_start;

          cpt_trains+=1;

          if (cpt_trains > nbr_max_lignes-1)
            break;
          
        }

        print_debug("Nbr Trains:" + String(cpt_trains));

        if (cpt_trains > 0) {
          for (int i=0;i<cpt_trains-1;i++){
            print_debug(*(ret+i));
          }
        }

        *nbr_lignes = cpt_trains;
        return ret;
        
}


void fetch_ecrans_configuration() {

  String response;
  int statusCode = 0;


  print_debug("making GET request to get screens configurations");
  httpclient_params_server.get("/screens/info?num_serie=" + String(ESP.getChipId()));

  Serial.println("/screens/info?num_serie=" + String(ESP.getChipId()));

  // read the status code and body of the response
  statusCode = httpclient_params_server.responseStatusCode();
  response = httpclient_params_server.responseBody();

  print_debug("Status code: " + String(statusCode));
  print_debug("Response: ");
  print_debug(response);

  if (statusCode == 200) {

    DynamicJsonBuffer jsonBuffer;
    JsonObject& root = jsonBuffer.parseObject(response);
  
    nbr_ecrans = root["nbr_ecrans"];
  
    print_debug("nbr_ecrans:" + String(nbr_ecrans));
  
    ecrans = (Ecran_t*) malloc(nbr_ecrans*sizeof(Ecran_t));
    
    for (int i = 0; i < nbr_ecrans; i++) {
  
      ecrans[i].nbr_char_par_ligne = root["ecrans"][i]["nbr_chars_par_ligne"];
      ecrans[i].nbr_lignes = root["ecrans"][i]["nbr_lignes"];
      strcpy(ecrans[i].header, root["ecrans"][i]["header"]);
      ecrans[i].first_train_received = 0;
      ecrans[i].gare_depart = root["ecrans"][i]["gare_depart"];
      ecrans[i].gare_arrivee = root["ecrans"][i]["gare_arrivee"];
      
      ecrans[i].buffer = (char**) malloc(ecrans[i].nbr_lignes*sizeof(char*));
      for (int j = 0; j < ecrans[i].nbr_lignes; j++)
          ecrans[i].buffer[j] = (char*) malloc(ecrans[i].nbr_char_par_ligne*sizeof(char));
    }
  
    
    for (int i = 0; i < nbr_ecrans; i++) {
      print_debug("size header:" + String(String(ecrans[i].header).length()));
      memcpy(ecrans[i].buffer[0], ecrans[i].header, String(ecrans[i].header).length()+1);
    }

    if (nbr_ecrans > 0) {
      print_debug("nb chars par ligne:" + String(ecrans[0].nbr_char_par_ligne));
      print_debug("nbr lignes:" + String(ecrans[0].nbr_lignes));
      print_debug("header:" + String(ecrans[0].header));
      print_debug("gare depart:" + String(ecrans[0].gare_depart));
      print_debug("gare arrivee:" + String(ecrans[0].gare_arrivee));
    } else {

      display.clear();
      display.drawXbm(38,0, cross_width, cross_height, cross_bits);
      display.setTextAlignment(TEXT_ALIGN_LEFT);
      display.setFont(ArialMT_Plain_10);
      display.drawString(10, 52, "Pas d\'arrêt enregistré");
      display.display();      

    }

  }
  
}

void get_horaires_train(int ecran_index){

  String response;
  int statusCode = 0;
  
  httpclient_transilien_server.beginRequest();
  httpclient_transilien_server.get("/gare/" + String(ecrans[ecran_index].gare_depart) + "/depart/" + String(ecrans[ecran_index].gare_arrivee));
  httpclient_transilien_server.sendBasicAuth("tnhtn595", "NUh53e4u");
  httpclient_transilien_server.endRequest();

  print_debug("/gare/" + String(ecrans[ecran_index].gare_depart) + "/depart/" + String(ecrans[ecran_index].gare_arrivee));

  // read the status code and body of the response
  statusCode = httpclient_transilien_server.responseStatusCode();
  response = httpclient_transilien_server.responseBody();

  print_debug("Status code: " + String(statusCode));
  print_debug("Response: ");
  print_debug(response);

  if (statusCode == 200) {

      char* resp_api_transilien = (char*) malloc(response.length()*sizeof(char));
    
      response.toCharArray(resp_api_transilien, response.length());
    
      int nbr_lignes;
    
      char** lignes = parse_api_transilien_response(resp_api_transilien, ecrans[ecran_index].nbr_lignes-1, &nbr_lignes);
    
      free(resp_api_transilien);
    
      print_debug("nbr lignes de train parsees:" + String(nbr_lignes));
    
      for (int i = 1; i < ecrans[ecran_index].nbr_lignes; i++){
          for (int j = 0; j < ecrans[ecran_index].nbr_char_par_ligne; j++)
            ecrans[ecran_index].buffer[i][j] = 0;
      }
    
      if (nbr_lignes > 0) {
        for (int i=1;i<nbr_lignes+1;i++){
          char* temp = *(lignes+i-1);
          int j=0;
          while (*temp != 0)
              ecrans[ecran_index].buffer[i][j++] = *temp++;
        }
      } else {
          memcpy(ecrans[ecran_index].buffer[1], "Pas de trains", strlen("Pas de trains"));
          memcpy(ecrans[ecran_index].buffer[2], "Plus d\'info sur", strlen("Plus d\'info sur"));
          memcpy(ecrans[ecran_index].buffer[3], "transilien.com", strlen("transilien.com"));        
      }
    
      for (int i=0;i<nbr_lignes;i++){
        free(*(lignes+i));
      }
    
      free(lignes);
    
      for (int i=0;i<ecrans[ecran_index].nbr_lignes;i++){
        print_debug(ecrans[ecran_index].buffer[i]);
      }
    
      if (ecrans[ecran_index].first_train_received == 0)
        ecrans[ecran_index].first_train_received = 1;

  }
  
}

static boolean callback_get_trains(EventBase* evt)
{
    EventTrains* e = (EventTrains*) evt;

    print_debug("free memory:" + String(ESP.getFreeHeap()));

    if (WiFi.status() == WL_CONNECTED) {

        print_debug("get horaires ecran:" + String(e->index_ecran));
        get_horaires_train(e->index_ecran);
        print_debug("fin get horaires ecran:" + String(e->index_ecran));

    }

    return false;
}

static boolean callback_refresh_screen(EventBase* evt) {

  if (ecran_courant < nbr_ecrans) {

    if (ecrans[ecran_courant].first_train_received == 1) {

          display.clear();
          display.setTextAlignment(TEXT_ALIGN_LEFT);
          display.setFont(ArialMT_Plain_16);

          for (int i = 0; i < ecrans[ecran_courant].nbr_lignes; i++)
              display.drawString(0, 16*i, ecrans[ecran_courant].buffer[i]);

          display.display();
    }
    
  }

  return false;
  
}



void initialise_ecran_physique(){
  // Initialising the UI will init the display too.
  display.init();
  display.flipScreenVertically();
  display.clear();
  display.drawXbm(32,0, logo_train_width, logo_train_height, logo_train_bits);
  display.setTextAlignment(TEXT_ALIGN_LEFT);
  display.setFont(ArialMT_Plain_10);
  display.drawString(10, 52, "Chargement en cours...");
  display.display();
}


void configModeCallback (WiFiManager *myWiFiManager) {
  display.clear();
  /*display.drawXbm(25,0, wifi_cross_width, wifi_cross_height, wifi_cross_bits);
  display.setTextAlignment(TEXT_ALIGN_LEFT);
  display.setFont(ArialMT_Plain_10);
  display.drawString(76, 0, "Pas de");
  display.drawString(66, 10, "connection");
  display.drawString(74, 20, "internet");

  
  display.drawString(0, 32, "Connectez vous au réseau");
  display.drawString(12, 42, "Wifi TCHOUTCHOUC");
  display.drawString(10, 52, "pour configurer le Wifi");*/

  display.drawXbm(38,0, wifi_cross_big_width, wifi_cross_big_height, wifi_cross_big_bits);
  display.setTextAlignment(TEXT_ALIGN_LEFT);
  display.setFont(ArialMT_Plain_10);
  display.drawString(20, 52, "Pas de réseau Wifi");
  
  

  
  
  display.display();
}

void connect_wifi() {

  WiFiManager wifiManager;
  wifiManager.setAPCallback(configModeCallback);
  wifiManager.autoConnect("TCHOUTCHOUC");
  
}

void initialise_events_timer() {

  events_trains = (EventTrains*) malloc(nbr_ecrans*sizeof(EventTrains));
  for (int i=0;i<nbr_ecrans;i++){

    (events_trains+i)->period = TIME_BETWEEN_TRAINS_SCRAP;
    (events_trains+i)->repeatCount = -1; // forever
    (events_trains+i)->nextTriggerTime = OFFSET_BETWEEN_TRAINS_SCRAP*i; // if 0, means now
    (events_trains+i)->callback = &callback_get_trains;
    (events_trains+i)->index_ecran = i;
    timer.addEvent(events_trains+i);
  }

  timer.every(TIME_BETWEEN_SCREEN_UPDATE, callback_refresh_screen);
  
}



void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println();
  Serial.println();

  Serial.print(" ESP8266 Chip id = ");
  Serial.println(ESP.getChipId());

  initialise_ecran_physique();
  connect_wifi();
  fetch_ecrans_configuration();


  httpclient_transilien_server.setHttpResponseTimeout(3000);

  initialise_events_timer();
  
}

void loop() {

  timer.update();

}

