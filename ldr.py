class LDR: 
    """This class calibrates and converts a binary number of the LDR to a percentage for prac 4 of ESII """
    minimumLight = 0
    maximumLight = 0
    debug = False

    def read(ten_bit_val):
        nonlocal minimumLight
        nonlocal maximumLight
        c = -(minimumLight)/(maximumLight-minimumLight)
        m = 1/(maximumLight-minimumLight)
        return m*int(ten_bit_val)+c

    def calibrateMin(ten_bit_val):
        nonlocal minimumLight
        minimumLight = int(ten_bit_val)
        print("Minimum calibrated as: " + str(minimumLight)
        return minimumLight

    def calibrateMax(ten_bit_val):
        nonlocal maximumLight
        maximumLight = int(ten_bit_val)
        print("Minimum calibrated as: " + str(maximumLight)
        return maximumLight