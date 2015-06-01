import guru.ttslib.*;
import processing.sound.*;
import com.temboo.core.*;

TTS tts;
SoundFile s;
PImage lower3rd;
PFont reg;
PFont bold;

String title;
String price;
String description = "";
String [] voiceover = new String[5];

ArrayList<PImage> images = new ArrayList<PImage>();
int startingTime = 0;
int speakTimer = 0;

PImage currentImage;
int w;
int x, y;

void setup() {
  size(1280, 720);
  loadData();
  
  reg = createFont("Proxima Nova-Regular.otf", 72);
  bold = createFont("Proxima Nova-Extrabold.otf", 30);
  
  tts = new TTS();
  lower3rd = loadImage("strobe-lower3rds.png");
  // s = new SoundFile(this, "elevator.wav");
  
  voiceover[0] = description;
  voiceover[1] = "Buy now";
  voiceover[2] = "Text the number on the screen to buy";
  voiceover[3] = "Limited time offer";
  voiceover[4] = "Something like this doesn't come along every day";
}

void draw() {
  
  background(0);
  // s.loop();
  timer();
  voice();
  
  currentImage = images.get(0);
  currentImage.resize(0, 720);
  if (images.size() > 0) {
    imageMode(CENTER);
    image(currentImage, x, y);
  }
  
  imageMode(CORNER);
  image(lower3rd, 0, 0);
  
  move();
  
  fill(100);
  textFont(bold, 30);
  text(title, 40, 100, 210, 250);
  
  fill(255);
  textFont(bold, 72);
  text("$" + price, 50, 450);
  
  fill(100);
  textFont(reg, 43);
  text("Text \"BUY\" to 12345 to make an offer", 170, 615);
}

void loadData() {
  
  String[] data = loadStrings("data.txt");
  title = data[0];
  price = data[1];
  
  for (int i = 2; i < data.length; i++) {
    description = description + " " + data[i];
    
  } 
  
  addPhotos();
  println(title);
  println(description);
  
  x = 0;
  y = height/2;
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
      println(l);
      PImage i = loadImage(l);
      images.add(i);
    }
  } 
  println(images);  
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
    speakTimer = millis();
  } else {
    println(currentTime - speakTimer);
  }
  
}

void move() {
  x +=1;
}

void speak() {
  tts.speak(description);
  
}
