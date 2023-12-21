from PONG import Pong
import numpy as np
import Neural


class PongIA(Pong):
    def __init__(self):
        super().__init__(self)
        
    def get_data_for_IA(self):
        data = []
        if self.boll.x > self.window_width/2:
            self.ia_direction = 0.5
            return
        
        if self.boll.y < self.player1.y:
            self.ia_direction = 1
            return
            
        if self.boll.y > self.player1.y:
            self.ia_direction = 0
        
        data.append((np.array(self.player1.x, self.player1.y, self.player2.x, self.player2.y, self.boll.x, self.boll.y), np.array(self.ia_direction)))
        