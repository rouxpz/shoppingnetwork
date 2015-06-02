import guru.ttslib.*;
import processing.sound.*;
import com.temboo.core.*;
import com.temboo.Library.Twilio.SMSMessages.*;
import java.io.IOException;

TTS tts;
SoundFile s;
PImage lower3rd;
PFont reg, bold;

String title, price, serial;
String tembooName, tembooProject, tembooKey, accountSID, authToken;
TembooSession session;
String description = "";
String [] voiceover = new String[5];

ArrayList<PImage> images = new ArrayList<PImage>();
int startingTime = 0;
int speakTimer = 0;

int imageCounter = 0;
int voiceCounter = 1;
PImage currentImage;
int w;
float x, y;
int scale;

int totalResponses;
JSONArray results;

public void init(){
  frame.removeNotify();
  frame.setUndecorated(true);
  super.init();
}

void setup() {
  size(1280, 720);
  frame.setAlwaysOnTop(true);
  frame.setLocation(1280,0);
  
  //load temboo info and start session
  String[] tembooInfo = loadStrings("temboo-info.txt");
  tembooName = tembooInfo[0];
  tembooProject = tembooInfo[1];
  tembooKey = tembooInfo[2];
  session = new TembooSession(tembooName, tembooProject, tembooKey);
  
  String[] apiInfo = loadStrings("api-info.txt");
  authToken = apiInfo[0];
  accountSID = apiInfo[1];
  
  //load initial craigslist data from running python app
  loadData();
  
  reg = createFont("Proxima Nova-Regular.otf", 72);
  bold = createFont("Proxima Nova-Extrabold.otf", 30);
  
  tts = new TTS();
  lower3rd = loadImage("strobe-lower3rds.png");
  s = new SoundFile(this, "elevator02.wav");
  
  voiceover[0] = description;
  voiceover[1] = "Buy now";
  voiceover[2] = "Text the number on the screen to buy";
  voiceover[3] = "Limited time offer";
  voiceover[4] = "Something like this doesn't come along every day";
  
  voiceCounter = 1;
  
  totalResponses = getTotalMessages();
  println(totalResponses);
  
  s.loop();
}

void draw() {
  
  background(0);
  timer();
  voice();
  
  currentImage = images.get(imageCounter);
  currentImage.resize(1320, 0);
  
  if (images.size() > 0) {
    imageMode(CENTER);
    image(currentImage, x, y);
  }
  
  imageMode(CORNER);
  image(lower3rd, 0, 0);
  
  move();
  // increaseScale();
  
  fill(100);
  textFont(reg, 30);
  text(serial, 40, 70);
  textFont(bold, 30);
  text(title, 40, 100, 210, 250);
  
  fill(255);
  textFont(bold, 72);
  text("$" + price, 50, 450);
  
  fill(100);
  textFont(reg, 50);
  text("Text \"BUY\" to (917) 789-1004", 210, 620);
  
  if (millis() % 10000 == 0) {
    receiveSMS(title, description);
    
  }
}

void loadData() {
  
  String[] data = loadStrings("data.txt");
  title = data[0];
  price = data[1];
  
  for (int i = 2; i < data.length; i++) {
    description = description + " " + data[i];
    
  } 
  
  addPhotos();
  // println(title);
  // println(description);
  
  int itemNumber = round(random(9999));
  serial = "CSN-" + nf(itemNumber, 4, 0);
  println("serial number: " + serial);
  
  x = 620;
  y = height/2;
  scale = 720;
}

void addPhotos() {
  
  for (int i = 0; i < images.size(); i++) {
    images.remove(i);
  }
  File dir = new File(dataPath(""));
  String[] list = dir.list();
  
  for (String l : list) {
    String [] m = match(l, ".jpg");
    if (m != null) {
      // println(l);
      PImage i = loadImage(l);
      images.add(i);
    }
  } 
  // println(images);  
}

void timer() {
  int currentTime = millis();
  
  if (currentTime - startingTime >= 300000) {
    loadData(); 
    startingTime = millis();
  } else {
    // println("no reload yet");
  }
  
}

void voice() {
  int currentTime = millis();
  
  if (currentTime - speakTimer >= 45000) {
    thread("speak");
    
    if (voiceCounter >= voiceover.length - 1) {
      voiceCounter = 0;
    } else {
      voiceCounter += 1;
    }
    
    speakTimer = millis();
  } else {
    // println(currentTime - speakTimer);
  }
  
}

void move() {
  x += 0.5;
  
  if (x >= 660) {
    if (images.size() > 1) {
    if (imageCounter < images.size() - 1) {
      imageCounter++;
    } else {
      imageCounter = 0;
    }
    x = 620;
    }
  }
}

void increaseScale() {
  x = width/2;
  scale += 1;
  
}

void speak() {
  // tts.speak(description);
  
  try {
      Runtime.getRuntime().exec(new String[] {"say", voiceover[voiceCounter]});
    }
    catch (IOException e) {
      System.err.println("IOException");
    }
  
}

void receiveSMS(String address, String title) {
  
  //check twilio JSON for new entries
  int newResponses = getTotalMessages();
  
  if (newResponses > totalResponses) {
    int diff = newResponses - totalResponses;
    
    for (int i = 0; i < diff; i++) { //for all new entries:
    
      //1 - collect phone number
      JSONObject r = results.getJSONObject(i);
      String phone = r.getString("from");
      println(phone);
    }
    
    totalResponses = newResponses;
  } else {
    println("no new inquiries");
  }
  
  //2 - craft email to address in ad with phone number & ad title as subject
  //3 - send email
  //4 - save total number of JSON entries in totalResponses
  
}

int getTotalMessages() {
  // Create the Choreo object using your Temboo session
  GetMessagesThatContain getMessagesThatContainChoreo = new GetMessagesThatContain(session);

  // Set inputs
  getMessagesThatContainChoreo.setAuthToken("b11d0672a5ff9e9e3b5353df7f5f6134");
  getMessagesThatContainChoreo.setFilter("BUY");
  getMessagesThatContainChoreo.setAccountSID("AC7966a6197cb5f3fd07720e411910c908");
  getMessagesThatContainChoreo.setResponseMode("verbose");

  // Run the Choreo and store the results
  GetMessagesThatContainResultSet getMessagesThatContainResults = getMessagesThatContainChoreo.run();
  
  results = JSONArray.parse(getMessagesThatContainResults.getResponse());
  return results.size();

}
