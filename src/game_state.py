from enum import Enum


# defines the different states of the game, these values should be regarded as final
class GameState(Enum):
    HAS_NOT_CONCLUDED = 0
    PLAYER_ONE_WIN = 1
    PLAYER_TWO_WIN = -1
    DRAW = 2
