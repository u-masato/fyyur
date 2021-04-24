from enum import Enum


class Genre(Enum):
    Alternative = 'Alternative'
    Blues = 'Blues'
    Classical = 'Classical'
    Country = 'Country'
    Electronic = 'Electronic'
    Folk = 'Folk'
    Funk = 'Funk'
    HipHop = 'Hip-Hop'
    HeavyMetal = 'Heavy Metal'
    Instrumental = 'Instrumental'
    Jazz = 'Jazz'
    MusicalTheatre = 'Musical Theatre'
    Pop = 'Pop'
    Punk = 'Punk'
    RB = 'R&B'
    Reggae = 'Reggae'
    RockNRoll = 'Rock n Roll'
    Soul = 'Soul'
    Other = 'Other'

    @classmethod
    def choices(cls):
        return [(choice.value, choice.value) for choice in cls]

    @classmethod
    def coerce(cls, item):
        return cls(item) if not isinstance(item, cls) else item
