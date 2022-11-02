
# Import libraries
import enum;



# --- Defining Constants ---

# The corresponding ciphertext letters on the outside of the rotor; The index of each letter correspond
# to its position on the rotor (E is at port 0 - the top, S is at port 6 - the bottom letter, etc.)
ALPHABETS = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'U']

# Fixed reflector wires that connect which inside port goes to which other inside port.
# Note that it is bidirectional
REFLECTOR_DICT = {0: 10, 1: 6, 2: 4, 3: 9, 4: 2, 5: 8, 6: 1, 7: 11, 8: 5, 9: 3, 10: 0, 11: 7}

# The default rotor channels that connect the inside reflector to the outer rotor letters. Aka the rotor wires
# For example, rotor channel [0, 0] connects the inside port at location 0 to the outside letter at location 0.
# ^ be more clear about this
# [4, 6] maps the inside port at location 4 to the outside port at location 6.
# The rotor is "turned" by incrementing these values. [inside, outside]
rotor_wires = [[0, 0], [1, 2], [2, 1], [3, 3], [4, 6], [5, 4], [6, 5], [7, 7], [8, 10], [9, 8], [10, 11], [11, 9]]
# ^ change to wires?


# Creating an array of the wire mapping for the plug board. Default with each keyboard outside port mapping
# to same corresponding inside port. After the plugboard input, these never change value. [inside, outside]
plugboard_wires = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9], [10, 10], [11, 11]]


# TODO - add decrypt functionality in enigma
# TODO - add header


# use enumeration constant?
class Direction(enum.Enum):
    IN = 0;
    OUT = 1;
    CLOCKWISE = 2;
    COUNTERCLOCKWISE = 3;


def get_plugboard_input():
    """ Function gets user input of where plugboards are throughout rotor (according to the project instructions).
    Updates plugboard_wires accordingly.

    ASSUMING GOOD INPUT FOR NOW

    """

    # Getting inputs
    pair1 = input("\nInput first pair of letters of the plugboard (letter_1 letter_2)\n>");
    pair2 = input("\nInput second pair of letters of the plugboard (letter_1 letter_2)\n>");
    pair3 = input("\nInput third pair of letters of the plugboard (letter_1 letter_2)\n>");

    # Unpacking , getting plugboard pairs
    pair1a, pair1b = pair1[0], pair1[2];
    pair2a, pair2b = pair2[0], pair2[2];
    pair3a, pair3b = pair3[0], pair3[2];

    # Not checking for now if the given pairs are actually adjacent ports
    pair1Ind = [ALPHABETS.index(pair1a), ALPHABETS.index(pair1b)]
    pair2Ind = [ALPHABETS.index(pair2a), ALPHABETS.index(pair2b)]
    pair3Ind = [ALPHABETS.index(pair3a), ALPHABETS.index(pair3b)]

    # write inefficiently for now

    # note, the indices of the plugboard_wires right now will be the same as their index in the array
    port1 = plugboard_wires[pair1Ind[0]];
    port2 = plugboard_wires[pair1Ind[1]];

    dummy_inside_port = port1[0];

    # Switching the wiring
    plugboard_wires[pair1Ind[0]][0] = port2[0];
    plugboard_wires[pair1Ind[1]][0] = dummy_inside_port;




    port1 = plugboard_wires[pair2Ind[0]];
    port2 = plugboard_wires[pair2Ind[1]];

    dummy_inside_port = port1[0];

    # Switching the wiring
    plugboard_wires[pair2Ind[0]][0] = port2[0];
    plugboard_wires[pair2Ind[1]][0] = dummy_inside_port;




    port1 = plugboard_wires[pair3Ind[0]];
    port2 = plugboard_wires[pair3Ind[1]];

    dummy_inside_port = port1[0];

    # Switching the wiring
    plugboard_wires[pair3Ind[0]][0] = port2[0];
    plugboard_wires[pair3Ind[1]][0] = dummy_inside_port;



    # debug print out statement
    print(plugboard_wires);



# port_a:int - the port you're starting at in the rotor
# direction : Direction - IN, OUT
# returns: port_b:int - the other side of the wire, connected to port_a
def get_corresponding_output(port_a, direction):
    """ Finds the corresponding output port with the provided <port_a> input port, depending on current
    rotor_wires value. 
    
    <port_a> could be a port from the reflector side of the rotor, or the keyboard side, depending
    on <direction> argument: if is Direction.IN, <port_a> is an outside keyboard port and function
    returns corresponding output port from reflector side, if is Direction.OUT, <port_a> is an inside
    keyboard port and function returns corresponding output port from keyboard side. 
    
    port_a : int - input port of the rotor to get the corresponding output port of
    direction : Direction - specifies direction of input to output signal (IN or OUT)
    returns: port_b : int - the corresponding output port of port_a.
    """

    # Default port_b to -1 value to handle error case -> port_a value not found in rotor_wires.
    port_b = -1

    # If direction is inwards (board -> reflector)...
    if direction == Direction.IN:

        # Loop through all wires in rotor_wires to find one of port_a, and its corresponding output
        for inside_wire, outside_wire in rotor_wires:

            if inside_wire == port_a:
                port_b = outside_wire;
                break;

    # If direction is outwards (reflector -> board)...
    elif direction == Direction.OUT:

        # Loop through all wires in rotor_wires to find one of port_a, and its corresponding output
        for inside_wire, outside_wire in rotor_wires:

            if outside_wire == port_a:
                port_b = inside_wire;
                break;


    # Handle error case
    if port_b < 0:
        raise TypeError("Invalid port_a input - no corresponding port_b found.");
    else:
        return port_b




def turn_rotor(offset):
    """ Function "turns the rotor" by adding the <offset> value passed through args
    to the rotor channel elements in the rotor_val array. """

    # Get length of rotor_wires list
    list_len = len(rotor_wires);

    # iterate through the indices of the rotor_wires list
    for channel_ind in range(list_len):

        # Store current rotor in dummy var
        this_rotor = rotor_wires[channel_ind];

        # Add offset to the elements of each rotor.
        # Ensure we stay in mod 12 (since only 12 letters on each rotor)
        for element in range(len(this_rotor)):
            this_rotor[element] += offset
            this_rotor[element] %= 12;



# reflects
def reflector(i):
    """ Returns the corresponding reflected output port depending on the passed in <i>, the input port. """ # Fix
    return REFLECTOR_DICT[i]


# main enigma code
def enigma(plaintext_input,  rotation, rotor_start = 0):
    """ Enciphers <plaintext_input> string through enigma machine, with the initial rotor
    position at <rotor_start := default 0>.

    Rotates clockwise if <rotation> is "D", rotates counter-clockwise if is "O".

    Returns ciphertext. """


    # First capitalize input
    plaintext_input = plaintext_input.upper()

    # Setting up ciphertext output
    ciphertext_output = ""

    # Set up the rotor to initial position
    turn_rotor(rotor_start)

    # For each letter in the plaintext input...
    for letter in plaintext_input:

        # Find the corresponding keyboard of the letter around the torotr
        letter_position = ALPHABETS.index(letter)

        # TODO - plugboard here

        # Pass the plaintext through rotor inwards
        rotor_in_output = get_corresponding_output(letter_position, Direction.IN);

        # "Reflect" the input through reflector
        reflector_output = reflector(rotor_in_output)

        # Pass the reflected output through rotor outwards - results in its ciphertext
        rotor_out_output = get_corresponding_output(reflector_output, Direction.OUT);

        # Add enciphered letter to ciphertext string
        ciphertext_output += ALPHABETS[rotor_out_output]

        # Finally, turn rotor clockwise/counterclockwise once depending on input
        # TODO - GET INPUT FOR THIS
        offset = 0;
        if rotation == "O":
            offset = -1;
        elif rotation == "D":
            offset = 1;
        turn_rotor(offset);

    # Return final ciphertext
    return ciphertext_output


# main
if __name__ == "__main__":

    # Get plugboard input first
    get_plugboard_input();


    plaintext = input("Enter enigma machine input:\n")  # can replace by just text for testing

    try:

        initial_position: int = ALPHABETS.index \
            (input("Enter the initial position - the letter on the dashed line:\n").upper())  # can replace by offset
        # for testing
    except ValueError:
        print("Invalid initial position, good bye")
        exit(1)

    print(plaintext.upper() + "\n" + enigma(plaintext, "D", initial_position))

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
