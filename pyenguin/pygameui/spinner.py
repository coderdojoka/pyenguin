from . import flipbook


class SpinnerView(flipbook.FlipbookView):
    size = 24

    def __init__(self, frame):
        frame.size = (SpinnerView.size, SpinnerView.size)
        from pyenguin import BildSpeicher
        BildSpeicher.lade_aus_paket("spinner", "pygameui/spinner.png")
        image = BildSpeicher.gib_pygame_bild('spinner')
        flipbook.FlipbookView.__init__(self, frame, image)
