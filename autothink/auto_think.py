from py4j.java_gateway import JavaGateway, CallbackServerParameters, GatewayParameters, launch_gateway
from pai.pai_think_helper import PaiSpeechTagging
from pai.pai_think_helper import PaiSentenceHelper
from pai.create_chat_files import PaiChatFiles
from pai.pai_think_helper import PaiWordNet
from textblob import TextBlob
import random


class BagOfWords:
    @staticmethod
    def get_good_attributes():
        good_attributes = ["good", "great", "cool", "amazing", "perfect", "fun", "great", "fantastic"]
        return good_attributes

    @staticmethod
    def get_bad_attributes():
        bad_attributes = ["bad", "trash", "horrible", "not cool", "not good", "not great"]
        return bad_attributes


class AutoThinkSystems:
    @staticmethod
    def sentiment_of_noun(noun, messages):
        noun_sentences = []
        sentiment = 0.0

        for item in messages:
            if noun in item:
                noun_sentences.append(item)

        for item in noun_sentences:
            print(item)
            text = TextBlob(item)
            sentiment = sentiment + text.sentiment.polarity

        return sentiment


    @staticmethod
    def get_attributes(noun, all_sent):
        attributes = []

        for item in all_sent:
            if noun in item:
                att = PaiSpeechTagging().find_adj(item)
                for attribute in att:
                    if len(list(attribute)) < 1:
                        del att[att.index(attribute)]

                if len(att) > 0:
                    for x in att:
                        attributes.append(x)

        return attributes

    @staticmethod
    def complete_thought(noun, attributes):
        thoughts = []
        finished_thought = []

        for item in attributes:
            thoughts.append(str(item).replace("]", "").replace("[", "").replace("'", ""))
        # generate sentence

        return PaiSentenceHelper().sentence_generator_desc(noun, thoughts)


    @staticmethod
    def start_server():
        java = JavaGateway(gateway_parameters=GatewayParameters(port=1002))
        noun_list = PaiSpeechTagging().find_nouns_all(java.jvm.kai.paibrain.PaiServer.AutoThinkServer().getAllMessages())

        given_noun = random.choice(noun_list)

        if AutoThinkSystems.sentiment_of_noun(given_noun, java.jvm.kai.paibrain.PaiServer.AutoThinkServer().getAllMessages()) > 0:
            list_of_att = [random.choice(BagOfWords.get_good_attributes()),random.choice(BagOfWords.get_good_attributes())]
            print(list_of_att)
            print(AutoThinkSystems().complete_thought(given_noun, list_of_att))
        else:
            list_of_att = [random.choice(BagOfWords.get_bad_attributes()),random.choice(BagOfWords.get_bad_attributes())]
            print(list_of_att)
            print(AutoThinkSystems().complete_thought(given_noun,list_of_att))

        """
        # connection to kai
        java = JavaGateway(gateway_parameters=GatewayParameters(port=1002))

        # all nouns in messages
        noun_list = PaiSpeechTagging().find_nouns_all(java.jvm.kai.paibrain.PaiServer.AutoThinkServer().getAllMessages())

        # attributes of noun
        chosen_noun = random.choice(noun_list)
        print(chosen_noun)
        print(AutoThinkSystems.sentiment_of_noun(chosen_noun, java.jvm.kai.paibrain.PaiServer.AutoThinkServer().getAllMessages()))

        att = AutoThinkSystems().get_attributes(chosen_noun, java.jvm.kai.paibrain.PaiServer.AutoThinkServer().getAllMessages())

        # complete thoughts
        if len(att) > 0:
            PaiChatFiles().create_json(chosen_noun, AutoThinkSystems().complete_thought(chosen_noun, att), "Desc")
            PaiChatFiles.create_chat_file("C:/Users/corie/OneDrive/Documents/kai/KaiCompanion/documents/autogen/1.json")
        """


AutoThinkSystems().start_server()
