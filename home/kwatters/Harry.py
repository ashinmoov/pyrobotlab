from java.lang import String

#############################################################
# This is the Harry script
# Harry is an InMooved powered by a Ras PI2
# Initially we'll start simple
# It will use ProgramAB & Webkit for all interactions with
# the bot.
#############################################################
# All bot specific hardware configuration goes here.
leftPort = "COM21"
rightPort = "COM31"
headPort = leftPort

gesturesPath = "c:/dev/workspace.kmw/pyrobotlab/home/kwatters/harry/gestures"

aimlPath = "c:/dev/workspace.kmw/pyrobotlab/home/kwatters/harry"
aimlBotName = "harry"
aimlUserName = "Kevin"
botVoice = "Rod"

######################################################################
# helper function help debug the recognized text from webkit/sphinx
######################################################################
def heard(data):
  print "Speech Recognition Data:"+str(data)

######################################################################
#
# MAIN ENTRY POINT  - Start and wire together all the services.
#
######################################################################

######################################################################
# Create ProgramAB chat bot ( This is the inmoov "brain" )
######################################################################
harry = Runtime.createAndStart("harry", "ProgramAB")
harry.setPath(aimlPath)
harry.startSession(aimlUserName, aimlBotName)

######################################################################
# Html filter to clean the output from programab.  (just in case)
htmlfilter = Runtime.createAndStart("htmlfilter", "HtmlFilter")

######################################################################
# mouth service, speech synthesis
mouth = Runtime.createAndStart("i01.mouth", "AcapelaSpeech")
mouth.setVoice(botVoice)

######################################################################
# the "ear" of the inmoov TODO: replace this with just base inmoov ear?
ear = Runtime.createAndStart("i01.ear", "WebkitSpeechRecognition")
ear.addListener("publishText", python.name, "heard");
ear.addMouth(mouth)

######################################################################
# MRL Routing webkitspeechrecognition/ear -> program ab -> htmlfilter -> mouth
######################################################################
ear.addTextListener(harry)
harry.addTextListener(htmlfilter)
htmlfilter.addTextListener(mouth)

######################################################################
# Start up the inmoov and attach stuff.
######################################################################
i01 = Runtime.createAndStart("i01", "InMoov")
i01.startAll(leftPort, rightPort)

######################################################################
# Launch the web gui and create the webkit speech recognition gui
# This service works in Google Chrome only with the WebGui
#################################################################
webgui = Runtime.createAndStart("webgui","WebGui")

######################################################################
# END MAIN SERVICE SETUP SECTION
######################################################################


######################################################################
# Helper functions and various gesture definitions
######################################################################
i01.loadGestures(gesturesPath)


