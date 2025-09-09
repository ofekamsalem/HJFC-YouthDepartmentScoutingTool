from dataclasses import dataclass, field
from typing import Optional


FULL_GAME_MINUTES = 90

@dataclass
class Involvement:
    game_ID: str
    date: str
    minutes: int = field(init=False, default=0)
    in_squad: bool
    started: bool
    subbed_in: bool
    subbed_out: bool
    subbed_in_min: Optional[int] = None
    subbed_out_min: Optional[int] = None
    goals: int = 0

    def __post_init__(self):
        self.minutes = self._compute_minutes()

    def _compute_minutes(self):
        # not in squad -> minutes = 0
        if not self.in_squad:
            return 0
        else:    
            # on bench and didn't play at all -> minutes = 0
            if self.in_squad and not self.started and not self.subbed_in and not self.subbed_out:
                return 0 
            # subbed in and subbed -> minutes = in - out
            if self.subbed_in and self.subbed_out and not self.started:
                return (self.subbed_out_min - self.subbed_in_min)
            
            # subbed in and played till the end -> minutes = 90 - in
            if self.subbed_in and not self.subbed_out:
                return (FULL_GAME_MINUTES - self.subbed_in_min)
            
            # started and then subbed out in the game -> minutes = out
            if not self.subbed_in and self.subbed_out and self.started:
                return self.subbed_out_min
            
            # played the full game -> minutes = 90
            if self.started and not self.subbed_out:
                return FULL_GAME_MINUTES
            
            # in squad but did'nt played at all -> minutes = 0
            if self.in_squad and not self.started and not self.subbed_in:
                return 0
            
        return 0
            
