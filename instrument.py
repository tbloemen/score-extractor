class Instrument:
    def __init__(self, name: str, synonyms: list[str] = None, number: int = None):
        self.name = name
        self.synonyms = synonyms if synonyms is not None else []
        self.number = number

    def __str__(self):
        if self.number is None:
            return self.name
        return f"{self.name} {self.number}"

    def representation(self) -> list[str]:
        names = []
        if self.number is not None:
            names.append(f"{self.name} {self.number}")
            for synonym in self.synonyms:
                names.append(f"{synonym} {self.number}")
        if self.number is None:
            names.append(f"{self.name}")
            for synonym in self.synonyms:
                names.append(f"{synonym}")

        return names


def create_instruments() -> list[Instrument]:
    instruments = []
    # Saxen
    sax_alt_1 = Instrument("Alt Saxofoon",
                           ["alto", "alto sax", "sax alt", "saxo alt", "alt", "alto saxophone", "alt saxophone",
                            "saxophone alto", "saxophone alt"], 1)
    sax_alt_2 = Instrument("Alt Saxofoon",
                           ["alto", "alto sax", "sax alt", "saxo alt", "alt", "alto saxophone", "alt saxophone",
                            "saxophone alto", "saxophone alt"], 2)
    sax_tenor_1 = Instrument("Tenor Saxofoon",
                             ["tenor", "tenor sax", "sax tenor", "saxo tenor", "tenor saxophone", "saxophone tenor"], 1)
    sax_tenor_2 = Instrument("Tenor Saxofoon",
                             ["tenor", "tenor sax", "sax tenor", "saxo tenor", "tenor saxophone", "saxophone tenor"], 2)
    sax_bari = Instrument("Baritone Saxofoon",
                          ["baritone", "bari sax", "sax bari", "saxo bari", "baritone saxophone", "saxophone bari"])

    instruments.extend([sax_alt_1, sax_alt_2, sax_tenor_1, sax_tenor_2, sax_bari])
    # Trombones
    trombone_1 = Instrument("Trombone", ["Tromb", "tb"], 1)
    trombone_2 = Instrument("Trombone", ["Tromb", "tb"], 2)
    trombone_3 = Instrument("Trombone", ["Tromb", "tb"], 3)
    trombone_4 = Instrument("Trombone", ["Tromb", "tb"], 4)

    instruments.extend([trombone_1, trombone_2, trombone_3, trombone_4])

    # Trompetten
    trumpet_1 = Instrument("Trompet", ["tpt", "trumpet", "tromp", "trump", "tp"], 1)
    trumpet_2 = Instrument("Trompet", ["tpt", "trumpet", "tromp", "trump", "tp"], 2)
    trumpet_3 = Instrument("Trompet", ["tpt", "trumpet", "tromp", "trump", "tp"], 3)
    trumpet_4 = Instrument("Trompet", ["tpt", "trumpet", "tromp", "trump", "tp"], 4)

    instruments.extend([trumpet_1, trumpet_2, trumpet_3, trumpet_4])

    # Ritme
    piano = Instrument("Piano", ["pno", "keys"])
    drums = Instrument("Drums", ["drum", "perc", "percussion", "percussie"])
    bass = Instrument("Bass",
                      ["electric bass", "elec bass", "upright", "upright bass", "double", "double bass", "contrabas",
                       "contrabass", "contra"])
    guitar = Instrument("Gitaar", ["guitar", "electric guitar", "elec guitar", "acoustic guitar", "acou guitar"])
    singer = Instrument("Voice", ["sing", "vocal", "singer"])

    instruments.extend([piano, drums, bass, guitar, singer])

    return instruments
