import pyttsx3
from py4j.java_gateway import JavaGateway, CallbackServerParameters, GatewayParameters, launch_gateway
import speech_recognition as sr     # import the library

def start_server():
    java = JavaGateway(gateway_parameters=GatewayParameters(port=1003))

    r = sr.Recognizer()                 # initialize recognizer
    with sr.Microphone() as source:     # mention source it will be either Microphone or audio files.
        print("Speak Anything :")
        audio = r.listen(source)        # listen to the source
        try:
            text = r.recognize_google(audio)    # use recognizer to convert our audio into text part.
            print("You said : {}".format(text))

            java.jvm.kai.paibrain.PaiServer.ListenServer().getReturnedSpeak(format(text))

        except:
            print("Sorry could not recognize your voice")    # In case of voice not recognized


start_server()