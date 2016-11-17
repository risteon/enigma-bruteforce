#!/usr/bin/python3

from itertools import permutations
from joblib import Parallel, delayed
from multiprocessing import cpu_count


from enigma.machine import EnigmaMachine


__author__ = "Christoph Rist"
__copyright__ = "Copyright 2016, Christoph Rist"
__license__ = "MIT"

CIPHERTEXT = 'HOOJILEQKCYJN'
plugboard = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y', 'Z']


def get_plug_string(l):
    ret = ''
    for i in range(0, 20, 2):
        ret += l[i]
        ret += l[i+1]
        ret += " "

    return ret


def run_enigma(d):
    counter = 0
    for plug_perm in permutations(plugboard, 20):
        counter += 1
        if counter % 100000 == 0:
            print(counter)

        machine = EnigmaMachine.from_key_sheet(
            rotors=d["rotor"],
            reflector=d["ref"],
            ring_settings=d["ring"],
            plugboard_settings=get_plug_string(plug_perm))

        output = machine.process_text(CIPHERTEXT)
        if output == "BLETCHLEYPARK":
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            print(d)
            print("PLUGS: ", plug_perm)
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            raise RuntimeError("Solution found.")


def gen_setting():
    rotors = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']
    reflectors = ['B'] #, 'C'] this is known to be reflector B!
    ring_setting = list(range(26))

    for r1 in ring_setting:
        for r2 in ring_setting:
            for r3 in ring_setting:
                for refl in reflectors:
                    for rot_perm in permutations(rotors, 3):
                        yield {"rotor": rot_perm, "ref": refl, "ring": [r1, r2, r3]}
                        print("Checking rotor:", rot_perm)


def main():

    assert(len(plugboard) == 26)

    num_cores = cpu_count()

    Parallel(n_jobs=num_cores)(delayed(run_enigma)(i) for i in gen_setting())


    # set machine initial starting position
    #machine.set_display('WXC')

    # decrypt the message key
    #msg_key = machine.process_text('KCH')

    # decrypt the cipher text with the unencrypted message key
    #machine.set_display(msg_key)

    #ciphertext = 'NIBLFMYMLLUFWCASCSSNVHAZ'
    #plaintext = machine.process_text(ciphertext)

    #print(plaintext)


if __name__ == "__main__":
    main()



