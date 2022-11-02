
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


# the indices of the plugboard_wires, and the value at each index is the corresponding inside port mapped to it
# Creating an array of the wire mapping for the plug board. Default with each keyboard outside port mapping
# to same corresponding inside port. After the plugboard input, these never change value. [inside, outside]
plugboard_wires = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9], [10, 10], [11, 11]]



# TODO - add header


# use enumeration constant?
class Direction(enum.Enum):
    IN = 0;
    OUT = 1;
    CLOCKWISE = 2;
    COUNTERCLOCKWISE = 3;


def get_rotation_direction():
    """ Function prompts user for direction input. If "D" inputted, direction returned is CLOCKWISE.
    If "O" inputted, direction returned is COUNTERCLOCKWISE. """

    # ASSUMING GOOD INPUT FOR NOW

    this_input = input("Type in direction character (D or O): \n>").upper();

    if this_input == 'D':
        return Direction.CLOCKWISE;
    elif this_input == 'O':
        return Direction.COUNTERCLOCKWISE;
    else:
        print("lol invalid input.");



def get_plugboard_input():
    """ Function gets user input of where plugboards are throughout rotor
    (according to the project instructions). Updates plugboard_wires accordingly.
    """

    # LET US ASSUME NO BAD INPUT FOR NOW

    # Loop through to get three plugboard configurations
    for i in range(3):

        # Getting the input first
        input_letters = input(f"\nInput pair {i + 1} of the plugboard configuration (ie: >O I)\n>").upper();

        # Unpacking input to get the letters of the plugboard
        letterA, letterB = input_letters[0], input_letters[2];

        # Getting the corresponding indices of the input letters in ALPHABETS - their locations around the keyboard
        indexA, indexB = ALPHABETS.index(letterA), ALPHABETS.index(letterB);

        # Retrieving the corresponding wire of the inputted letters
        wireA, wireB = plugboard_wires[indexA], plugboard_wires[indexB];   # Get copy of the letter's wires
        wireA_in_temp = wireA[0]; # Creating dummy var for the switch
        plugboard_wires[indexA][0] = wireB[0];
        plugboard_wires[indexB][0] = wireA_in_temp;


    # debug print out statement
    print(plugboard_wires);


def pass_thru_plugboard(port_a, direction):
    """ Function responsible for getting corresponding output of an input <port_a>
    according to the set plugboard configuration.

    I guess we'll say this works just like pass_thru_rotor()

    #todo fill in docstring properly later """

    # Default port_b to be -1 for error case
    port_b = -1;

    # If the direction is keyboard -> inside...
    if direction == Direction.IN:

        # Return the corresponding inside port
        port_b = plugboard_wires[port_a][0];

    # If the direction is inside -> keyboard...
    elif direction == Direction.OUT:

        # Find the inside port port_a and return the corresponding outside port
        for this_wire in plugboard_wires:

            inside_port = this_wire[0];

            if port_a == inside_port:
                port_b = this_wire[1];


    # Handling error case
    if port_b < 0:
        raise TypeError("Invalid port_a input - no corresponding port_b found.");
    else:
        return port_b;



# port_a:int - the port you're starting at in the rotor
# direction : Direction - IN, OUT
# returns: port_b:int - the other side of the wire, connected to port_a
def pass_thru_rotor(port_a, direction):
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



def reflector(i):
    """ Returns the corresponding reflected output port depending on the passed in <i>, the input port. """ # Fix
    return REFLECTOR_DICT[i]


# main enigma code
def enigma(plaintext_input,  rot_direction, rotor_start = 0):
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

        # Pass the letter position inwards through plugboard first
        plugboard_in_output = pass_thru_plugboard(letter_position, Direction.IN);

        # Pass the plaintext through rotor inwards
        rotor_in_output = pass_thru_rotor(plugboard_in_output, Direction.IN);

        # "Reflect" the input through reflector
        reflector_output = reflector(rotor_in_output)

        # Pass the reflected output through rotor outwards - results in its ciphertext
        rotor_out_output = pass_thru_rotor(reflector_output, Direction.OUT);

        # Pass the rotor_out_output through plugboard outwards
        plugboard_out_output = pass_thru_plugboard(rotor_out_output, Direction.OUT);

        # Add enciphered letter to ciphertext string
        ciphertext_output += ALPHABETS[plugboard_out_output];

        # Finally, turn rotor clockwise/counterclockwise once depending on rot_direction
        offset = 0;
        if rot_direction == Direction.COUNTERCLOCKWISE:
            offset = -1;
        elif rot_direction == Direction.CLOCKWISE:
            offset = 1;
        turn_rotor(offset);

    # Return final ciphertext
    return ciphertext_output


# main
if __name__ == "__main__":

    # Get plugboard input first
    get_plugboard_input();

    # Get rotation direction
    rotation = get_rotation_direction();

    # Get plaintext input
    plaintext = input("Enter enigma machine input:\n")

    # Get initial position - if input invalid, raises error
    try:
        initial_position: int = ALPHABETS.index \
            (input("Enter the initial position - the letter on the dashed line:\n").upper())

    except ValueError:
        print("Invalid initial position, good bye")
        exit(1)

    # Get ciphertext
    ciphertext = enigma(plaintext, rotation, initial_position);

    # Print ciphertext
    print("\nPlaintext: " + plaintext.upper() + "\nCiphertext: " + ciphertext);



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
