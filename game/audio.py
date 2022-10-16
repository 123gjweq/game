import pyglet


class Audio:
    MONKEYSOUND = pyglet.resource.media("sounds/MONKEY.mp3")
    PEWSOUND = pyglet.resource.media("sounds/PEW.mp3")
    PAPSOUND = pyglet.resource.media("sounds/PAP.mp3")

    dict_of_sounds = {False: PEWSOUND, True: PAPSOUND}

    def __init__(self):
        self.audioPlayers = [pyglet.media.Player() for i in range(0, 10, 1)]

    def GetAvailablePlayer(self):
        for audioPlayer in self.audioPlayers:
            if not audioPlayer.playing:
                return audioPlayer
        return False