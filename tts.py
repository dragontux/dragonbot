# TODO: extend this with TTS-specific classes, this just writes to a file
#       which is assumed to be a fifo
class TextToSpeach:
    def __init__(self, output="./tts-pipe"):
        self.output = open(output, "w")

    def say(self, text):
        self.output.write(text)
        self.output.write("\n")
        self.output.flush()
