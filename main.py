#!/usr/bin/python3

from itertools import permutations, combinations
from joblib import Parallel, delayed
from multiprocessing import cpu_count
from difflib import SequenceMatcher


from enigma.machine import EnigmaMachine


__author__ = "Christoph Rist"
__copyright__ = "Copyright 2016, Christoph Rist"
__license__ = "MIT"

CIPHERTEXT = 'HOOJILEQKCYJN'

ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBER_RANGE = list(range(26))

COUNTER = 0

def similar(a, b):
    return sum(1 for i, j in zip(a, b) if i == j)


def generate_plug_settings():

    def generate_pairs_from_set(l, r):
        for i in range(1, len(l)):
            rn = r + l[0] + l[i] + " "
            ln = [l[j] for j in range(1, len(l)) if j is not i]
            if ln:
                yield from generate_pairs_from_set(ln, rn)
            else:
                yield rn

    for comb in combinations(ALPHABET, 20):
        plug = ""
        yield from generate_pairs_from_set(comb, plug)


def generate_rotor_positions():
    for s1 in ALPHABET:
        for s2 in ALPHABET:
            for s3 in ALPHABET:
                yield s1 + s2 + s3


def generate_ring_settings():
    for r1 in NUMBER_RANGE[:14]:
        for r2 in NUMBER_RANGE[:1]:
            #for r3 in NUMBER_RANGE:
            yield [r1, r2, 0]#, r3]


def run_enigma(d):
    f = open('out.txt', 'a')
    machine = EnigmaMachine.from_key_sheet(
        rotors=d["rotor"],
        reflector=d["ref"],
        ring_settings=d["ring"])
        #plugboard_settings=d["plug"])


    for r in generate_rotor_positions():
        global COUNTER
        machine.set_display(r)
        output = machine.process_text(CIPHERTEXT)
        if similar(output, "BLETCHLEYPARK") == 3 and output[1:2] == output[6:7]:
            f.write(str(d)+" "+str(r)+" ---> "+str(output)+"\n")
            print(str(d)+" "+str(r)+" ---> "+str(output))
        COUNTER += 1
        print(COUNTER*100/18396504.0)
        #if output == "BLETCHLEYPARK":
        #    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        #    print(d)
        #    print("ROTOR POSITION: ", r)
        #    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        #    raise RuntimeError("Solution found.")


def gen_setting():
    rotors = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']
    reflectors = ['B'] #, 'C'] this is known to be reflector B!

    for r in generate_ring_settings():
        for refl in reflectors:
            for rot_perm in permutations(rotors, 3):
                #for plug_perm in generate_plug_settings():
                yield {"rotor": rot_perm, "ref": refl, "ring": r}#, "plug": plug_perm}


def main():

    assert(len(ALPHABET) == 26)
    num_cores = cpu_count()
    Parallel(n_jobs=num_cores)(delayed(run_enigma)(i) for i in gen_setting())


if __name__ == "__main__":
    main()



