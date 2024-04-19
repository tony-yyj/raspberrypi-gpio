from car_motor import CarMotor

class CarControl:
    
    MOVEMENT_STATE_STOP = 'stop'
    MOVEMENT_STATE_FORWARD = 'forward'
    MOVEMENT_STATE_BACKWARD = 'backward'
    DIRECTION_STATE_LEFT = 'left'
    DIRECTION_STATE_RIGHT = 'right'
    DIRECTION_STATE_STRAIGHT = 'straight'

    def __init__(self) -> None:
        
        # stop straight left right
        self.direction = self.DIRECTION_STATE_STRAIGHT
        # stop forward backword
        self.movement = self.MOVEMENT_STATE_STOP
        self.carMotor = CarMotor()

    def move_forward(self):
        if self.movement != self.MOVEMENT_STATE_FORWARD:
            speed = self.carMotor.getSpeed()
            if speed > 10:
                self.carMotor.accelerate(self.movement, self.direction, True, 2)
                return
            if self.movement == self.MOVEMENT_STATE_FORWARD:
                return

            self.movement = self.MOVEMENT_STATE_FORWARD
            self.carMotor.forwoard()
    
    def move_backword(self):
        if self.movement != self.MOVEMENT_STATE_BACKWARD:
            speed = self.carMotor.getSpeed()
            if speed > 10:
                self.carMotor.accelerate(self.movement, self.direction, True, 2)
                return
            if self.movement == self.MOVEMENT_STATE_BACKWARD:
                return

            self.movement = self.MOVEMENT_STATE_BACKWARD
            self.carMotor.backward()

    def turn_left(self):
        self.direction = self.DIRECTION_STATE_LEFT
    
    def turn_right(self):
        self.direction = self.DIRECTION_STATE_RIGHT

    def straight_ahead(self):
        self.direction = self.DIRECTION_STATE_STRAIGHT

    def change_speed(self, dec = False):
        if self.movement == self.MOVEMENT_STATE_STOP:
            self.carMotor.stop()
            return

        self.carMotor.accelerate(self.movement, self.direction, dec)
    
    def stop(self):
        self.movement = self.MOVEMENT_STATE_STOP
        self.direction = self.DIRECTION_STATE_STRAIGHT
        self.carMotor.stop()


