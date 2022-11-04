"""

    Description:

    This is the Paper Enigma project submission for the course MAE234. This python program models the functioning of the
    specific paper enigma model given to the class as the assignment. The model includes the plugboard, rotor,
    reflector, and keyboard layout.

    The program prompts the user for the appropriate inputs, including the plugboard configuration, initial position
    of the rotor, direction the rotor is to rotate, and of course the plaintext to encipher through the enigma machine.

    NOTE: THIS VERSION OF THE CODE ASSUMES THAT THERE WILL ALWAYS BE GOOD INPUT - in the best interest of time,
    no bad input filters have been implemented.

    Notes:

        1 - The ALPHABETS array contains the 12 corresponding letters surrounding the circular keyboard. Each of
        their indices represent their designated "keyboard port", ie. 'E' is associated with keyboard port 0,
        which is at the 12 o'clock position of the machine. It follows that 'O' is with keyboard port 3, and is
        at the 3 o'clock position of the machine. Likewise, 'S' of port 6 is at 6 o'clock, and 'D' of port 9
        is at the 9o'clock position. THIS MAPPING NEVER CHANGES.


        2 - The REFLECTOR_DICT is a dictionary which essentially maps out the inside reflector part of the given
        enigma machine. For example, we see that the first element in the dictionary maps the reflector port 0 at the
        12 o'clock position with the reflector port 10 at the 10 o'clock position. All 12 reflector ports of the
        machine are modeled in the code exactly how the paper enigma was given. THIS MAPPING NEVER CHANGES.

        It follows that the reflector ports are bidirectional - we see that reflector port 10 also reflects to port 0.


        3 - The rotor_wires 2D array models the channels/rotors found in the wire. They were designed to change in value
        in order to model the rotor rotating when plaintext is being enciphered.

        Unlike REFLECTOR_DICT, each element in the rotor_wires represents the mapping of given INSIDE port of the rotor
        to a specific OUTSIDE port:

        [[inside_0, outside_0], [inside_1, outside_1], ..., [inside_11, outside_11]]

        Using the default rotor_wires array values as an example, we see that the inside rotor port 0 (12 o'clock)
        is connected to the outside rotor port 0 (12 o'clock), and that inside rotor port 1 (1 o'clock) maps to the
        outside rotor port 2 (2 o'clock). In other wires in the default array we see that inside port 4 maps to
        outside port 6, and more varied wirings.

        As previously noted, the rotor is simulated to rotate one port clockwise/counterclockwise by
        incrementing/decrementing (in % 12) all the port values in the rotor_wires array.

        For example, if we were to rotate the default array counterclockwise once, the first element [0, 0] would
        change to [11, 11], essentially resulting in the direction correction which was originally at the 12 o'clock
        position to now be at the 11 o'clock position. Using the [4, 6] example, the rotation would change its
        values to [3, 5], mapping the inside rotor port 3 to outside rotor port 5.  In other words, the specific wire,
        and in fact all the wires in the rotor, would be shifted one port down counterclockwise. Hence, the entire
        rotor itself would be rotated once clockwise.


        4 - The plugboard_wires functions similarly to rotor_wires, such as how the elements in the 2D array
        map the inside ports and outside ports of the plugboard (on the outside is where the keyboard is):

        [[inside_0, outside_0], [inside_1, outside_1], ..., [inside_11, outside_11]]

        This however only changes once when the user configures the plugboard of the enigma machine at the beginning
        of the program. Modeling the paper enigma machine given in the project, these configurations solely consist
        of the switching of the inside ports of adjacent ports.

        For example, if we were to set up the plugboard between the two ports with keys O and I which are at ports
        3 and 4 respectively, the values of the plugboard wires would change like this:

        [..., [3, 3], [4, 4], ...] --> [..., [4, 3], [3, 4], ...]

        The change has resulted in the outside keyboard port of O now being connected to inside port 4, and
        outside keyboard port of I now being connected to inside port 3.

        Hence, this models the plugboard exactly given in the paper enigma project.



    Collaborators:
        - OCdt Al-Ansar Mohammed
        - NCdt Eric Cho
        - OCdt Liethan Velasco

    Completed on: November 3rd, 2022


"""


# --- Importing Libraries ---
import enum;


# --- Defining Constants ---

class Direction(enum.Enum):

    # Enumerated constants that specify direction of input -> output
    IN = 0;
    OUT = 1;

    # Enumerated constants that specify rotation direction of rotor
    CLOCKWISE = 2;
    COUNTERCLOCKWISE = 3;


# Refer to Notes 1
ALPHABETS = ['E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'U']

# Refer to Notes 2
REFLECTOR_DICT = {0: 10, 1: 6, 2: 4, 3: 9, 4: 2, 5: 8, 6: 1, 7: 11, 8: 5, 9: 3, 10: 0, 11: 7}

# Refer to Notes 3
rotor_wires = [[0, 0], [1, 2], [2, 1], [3, 3], [4, 6], [5, 4], [6, 5], [7, 7], [8, 10], [9, 8], [10, 11], [11, 9]]

# Refer to Notes 4
plugboard_wires = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9], [10, 10], [11, 11]]


# ------ Defining Functions ------

def get_rotation_direction():
    """ Function prompts user for direction input.

    If "D" inputted, direction returned is CLOCKWISE.
    If "O" inputted, direction returned is COUNTERCLOCKWISE. """

    this_input = input("\nType in direction character (D or O): \n>").strip().upper();

    if this_input == 'D':
        return Direction.CLOCKWISE;
    elif this_input == 'O':
        return Direction.COUNTERCLOCKWISE;
    else:
        print("Invalid input.");



def get_plugboard_input():
    """ Function prompts user for the plugboard configurations.

    Update values in plugboard_wires accordingly in order to model the configurations.
    """

    # Loop through to get three plugboard configurations
    for i in range(3):

        # Getting the input first
        input_letters = input(f"\nInput pair {i + 1} of the plugboard configuration "
                              f"(one space in between letters):\n>").strip().upper();

        # Unpacking input to get the letters of the plugboard
        letterA, letterB = input_letters[0], input_letters[2];

        # Getting keyboard port numbers of inputted letters.
        indexA, indexB = ALPHABETS.index(letterA), ALPHABETS.index(letterB);

        # Create dummy vars first to help the switch
        wireA, wireB = plugboard_wires[indexA], plugboard_wires[indexB];
        wireA_inside = wireA[0];

        # Switching inside ports of the inputted letter's ports.
        plugboard_wires[indexA][0] = wireB[0];
        plugboard_wires[indexB][0] = wireA_inside;



def get_initial_pos():
    """ Function prompts user to enter the letter of the initial position to set up the enigma rotor before enciphering.
    Returns the associated port number of the inputted letter. """

    user_input = input("\nEnter the initial position - the letter on the dashed line:\n>").strip().upper();
    return ALPHABETS.index(user_input);



def pass_thru_plugboard(port_a, direction):
    """ Function returns the corresponding plugboard output port of the inputted <port_a : int> input plugboard port.

    If <direction : Direction> is IN, <port_a> resembles an input port on the outside of the plugboard, and the returned
    corresponding output port is from the inside of the plugboard.
    Conversely, if <direction : Direction> is OUT, <port_a> resembles an input port on the inside, and the
    returned corresponding output port is from the outside.
    according to the set plugboard configuration.
    """

    # Default port_b to be -1 for error case
    port_b = -1;

    # If the direction is keyboard -> inside...
    if direction == Direction.IN:

        # Simply set the corresponding inside port
        port_b = plugboard_wires[port_a][0];

    # If the direction is inside -> keyboard...
    elif direction == Direction.OUT:

        # Find the inside port of port_a and return the corresponding outside port
        for this_wire in plugboard_wires:

            inside_port = this_wire[0];

            # If found, set outside port and break from loop
            if port_a == inside_port:
                port_b = this_wire[1];
                break;


    # Handling error case (if port_a not found) - return if no error
    if port_b < 0:
        raise TypeError("Invalid port_a input - no corresponding port_b found.");
    else:
        return port_b;



def pass_thru_rotor(port_a, direction):
    """ Returns the corresponding output rotor port with the provided <port_a : int> input rotor port.

    If <direction : Direction> is IN, <port_a> resembles an input port on the outside side of the rotor, and the returned
    corresponding output port is from the inside of the rotor.
    Conversely, if <direction : Direction> is OUT, <port_a> resembles an input port on the inside, and the
    returned corresponding output port is from the outside of the rotor.
    according to the set plugboard configuration.
    """

    # Default port_b to -1 value to handle error case
    port_b = -1

    # If direction is inwards (board -> reflector)...
    if direction == Direction.IN:

        # Loop through all wires in rotor_wires to find which one is of port_a.
        # If found, set corresponding outside output port.
        for inside_port, outside_port in rotor_wires:

            if inside_port == port_a:
                port_b = outside_port;
                break;

    # If direction is outwards (reflector -> board)...
    elif direction == Direction.OUT:

        # Loop through all wires in rotor_wires to find which one is of port_a.
        # If found, set corresponding inside output port.
        for inside_port, outside_port in rotor_wires:

            if outside_port == port_a:
                port_b = inside_port;
                break;


    # Handle error case (if port_a not found) - return otherwise
    if port_b < 0:
        raise TypeError("Invalid port_a input - no corresponding port_b found.");
    else:
        return port_b



def turn_rotor(offset):
    """ Function "turns the rotor" by adding the <offset : int> value passed through args
    to the rotor channel elements in the rotor_val array. """

    # Get length of rotor_wires list
    list_len = len(rotor_wires);

    # iterate through the indices of the rotor_wires list
    for channel_ind in range(list_len):

        # Store current rotor in dummy var
        this_rotor = rotor_wires[channel_ind];

        # Add offset to the elements of each rotor (stay in mod 12).
        for element in range(len(this_rotor)):
            this_rotor[element] += offset
            this_rotor[element] %= 12;



def reflector(port_a):
    """ Returns the corresponding reflector output port of reflector input port <port_a : int>. """
    return REFLECTOR_DICT[port_a]



def enigma(plaintext_input,  rot_direction, rotor_start = 0):
    """ Enciphers <plaintext_input : str> string through enigma machine, with the initial rotor
    position at <rotor_start : int, default = 0>.

    Rotates rotor clockwise if <rot_direction : Direction> is CLOCKWISE, rotates counter-clockwise
    if is COUNTERCLOCKWISE.

    Returns corresponding ciphertext.
    """

    # First capitalize input
    plaintext_input = plaintext_input.upper()

    # Setting up ciphertext output
    ciphertext_output = ""

    # Set up the rotor to initial position
    turn_rotor(rotor_start)

    # For each letter in the plaintext input...
    for letter in plaintext_input:

        # Find the corresponding keyboard of the letter around the rotor
        letter_position = ALPHABETS.index(letter)

        # Pass the letter position inwards through plugboard first
        plugboard_in_output = pass_thru_plugboard(letter_position, Direction.IN);

        # Pass the plaintext through rotor inwards
        rotor_in_output = pass_thru_rotor(plugboard_in_output, Direction.IN);

        # "Reflect" the input through reflector
        reflector_output = reflector(rotor_in_output)

        # Pass the reflected output through rotor outwards
        rotor_out_output = pass_thru_rotor(reflector_output, Direction.OUT);

        # Pass the rotor_out_output through plugboard outwards - gives ciphertext
        plugboard_out_output = pass_thru_plugboard(rotor_out_output, Direction.OUT);

        # Add enciphered letter to ciphertext string
        ciphertext_output += ALPHABETS[plugboard_out_output];

        # Finally, turn rotor clockwise/counterclockwise once depending on rot_direction
        if rot_direction == Direction.COUNTERCLOCKWISE:
            turn_rotor(-1);
        elif rot_direction == Direction.CLOCKWISE:
            turn_rotor(1);

    # Return final ciphertext
    return ciphertext_output



# --- Entry Point ---

if __name__ == "__main__":

    # Get plugboard input first
    get_plugboard_input();

    # Getting initial position of rotor
    ini_pos = get_initial_pos();

    # Get rotation direction
    rotation = get_rotation_direction();

    # Get plaintext input - assuming getting good input
    plaintext = input("\nEnter enigma machine input: ")

    # Get ciphertext
    ciphertext = enigma(plaintext, rotation, ini_pos);

    # Print ciphertext
    print("\nPlaintext: " + plaintext.upper() + "\nCiphertext: " + ciphertext);


# End of code