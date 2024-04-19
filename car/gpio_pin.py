
class GPIOPIN:
    # --- TB6612FNG ----
    @staticmethod
    def STBY():
        return 27
    @staticmethod
    def AIN1():
        return 16
    @staticmethod
    def AIN2():
        return 20 
    @staticmethod
    def PWMA():
        return 18

    @staticmethod
    def BIN1():
        return 23
    @staticmethod
    def BIN2():
        return 24

    @staticmethod
    def PWMB():
        return 19
    #--------------


    # --- SG90s ---

    # vertical axis Y
    @staticmethod
    def VER_SERVO_PIN():
        return 25

    # horizontal axis X
    @staticmethod
    def HOR_SERVO_PIN():
        return 17
    #----------------

