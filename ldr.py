class LDR: 
    """This class calibrates and converts a binary number of the LDR to a percentage for prac 4 of ESII """
    minimumLight = 0
    maximumLight = 0
    debug = False

    def read(ten_bit_val, test):
        global minimumLight
        global maximumLight
        c = -(float(minimumLight))/(maximumLight-minimumLight)
        m = 1/(float(maximumLight-minimumLight))
        return m*float(test)+c

    def calibrateMin(ten_bit_val, test):
        global minimumLight
        minimumLight = int(test) - 10
        print("Minimum calibrated as: " + str(minimumLight))
        return minimumLight

    def calibrateMax(ten_bit_val, test):
        global maximumLight
        maximumLight = int(test) + 10
        print("Maximum calibrated as: " + str(maximumLight))
        return maximumLight
