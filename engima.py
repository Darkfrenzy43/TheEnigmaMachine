# CONSTANTS
ALPHABETS = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'U']
REFLECTOR_DICT = {0: 10, 1: 6, 2: 4, 3: 9, 4: 2, 5: 8, 6: 1, 7: 11, 8: 5, 9: 3, 10: 0, 11: 7}

# [outside, inside]
rotor_val = [[0, 0], [1, 2], [2, 1], [3, 3], [4, 6], [5, 4], [6, 5], [7, 7], [8, 10], [9, 8], [10, 11], [11, 9]]


# TODO - add plugboard
# TODO - add decrypt functionality in enigma
# TODO - add header

# turns rotor by adding the offset to every element of the rotor_val array
def turn_rotor(offset):
    for pair in range(len(rotor_val)):
        for element in range(len(rotor_val[pair])):
            rotor_val[pair][element] += offset
            if rotor_val[pair][element] >= 12:
                rotor_val[pair][element] -= 12


# port_a:int - the port you're starting at in the rotor
# direction:str - ("in","out")
# returns: port_b:int - the other side of the wire, connected to port_a
def rotor(port_a, direction):
    port_b = -1
    if direction == "in":  # from board to reflector
        for wire in rotor_val:
            if wire[0] == port_a:
                port_b = wire[1]
                break
    else:  # direction is out => from reflector to board
        for wire in rotor_val:
            if wire[1] == port_a:
                port_b = wire[0]
                break
        turn_rotor(1)

    if port_b < 0:
        raise TypeError("invalid rotor configuration")
    else:
        return port_b


# reflects
def reflector(i):
    return REFLECTOR_DICT[i]


# main enigma code
def enigma(enigma_input, rotor_start=0):
    enigma_input = enigma_input.upper()
    enigma_output = ""

    turn_rotor(rotor_start)

    for letter in enigma_input:
        letter_position = ALPHABETS.index(letter)
        rotor_output = rotor(letter_position, "in")
        reflector_output = reflector(rotor_output)
        rotor_output2 = rotor(reflector_output, "out")
        enigma_output += ALPHABETS[rotor_output2]
        # print(enigma_output)
    return enigma_output


# main
if __name__ == "__main__":
    plaintext = input("Enter enigma machine input:\n")  # can replace by just text for testing

    try:
        initial_position: int = ALPHABETS.index \
            (input("Enter the initial position - the letter on the dashed line:\n").upper())  # can replace by offset
        # for testing
    except ValueError:
        print("Invalid initial position, good bye")
        exit(1)

    print(plaintext.upper() + "\n" + enigma(plaintext, initial_position))

# dead code :
########################################################################################################################
# #outer, inner
# # all outers should be just enumerated
# rotor_list = [[0, 0], [1, 2], [2, 1], [3, 3], [4, 6], [5, 4], [6, 5], [7, 7], [8, 10], [9, 10], [10, 11], [11, 8]]
#
#
# def rotor(rotor_in, rotor_list):
#     rotor_out = 0
#     for wire in rotor_list:
#         if wire[0] == rotor_in:
#             rotor_out = wire[1]
#             break
#     print("invalid input:", rotor_in, "for the rotor function")
#
#     for pair in rotor_list:
#         for element in pair:
#             element += 1
#             if element>=12:
#                 element -= 12
#
# print(rotor(2, rotor_list))

# def decrypt(cipher_text):
#     cipher_text = plain_text.upper()
#     plain_text = ""
#
#         for letter in plain_text:
#             letter_position = ALPHABETS.index(letter)
#             rotor_output = rotor(letter_position, "in")
#             reflector_output = reflector(rotor_output)
#             rotor_output2 = rotor(reflector_output, "out")
#             cipher_text += ALPHABETS[rotor_output2]
#             print(cipher_text)
#         return cipher_text
