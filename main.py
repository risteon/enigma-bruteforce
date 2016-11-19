#!/usr/bin/python3

from itertools import permutations, combinations
import string

from multiprocessing import cpu_count, Event, Queue, Pool
import time
import argparse

from enigma.machine import EnigmaMachine


__author__ = "Christoph Rist"
__copyright__ = "Copyright 2016, Christoph Rist"
__license__ = "MIT"

CIPHERTEXT = ''
PLAINTEXT = ''

ALPHABET = list(string.ascii_uppercase)
NUMBER_RANGE = list(range(26))

stop_event = Event()
max_queue_size = 4*cpu_count()
data_queue = Queue(max_queue_size)
solution_queue = Queue(cpu_count())


def gen_setting():
    def generate_plug_settings():

        def generate_pairs_from_set(l, p_comb):
            for i in range(1, len(l)):
                rn = p_comb + l[0] + l[i] + " "
                ln = [l[j] for j in range(1, len(l)) if j is not i]
                if ln:
                    yield from generate_pairs_from_set(ln, rn)
                else:
                    yield rn

        for comb in combinations(ALPHABET, 20):
            plug = ""
            yield from generate_pairs_from_set(comb, plug)

    def generate_ring_settings():
        for r1 in NUMBER_RANGE:
            for r2 in NUMBER_RANGE:
                for r3 in NUMBER_RANGE:
                    yield [r1, r2, r3]

    rotors = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']
    reflectors = ['B', 'C']

    for r in generate_ring_settings():
        for refl in reflectors:
            for rot_perm in permutations(rotors, 3):
                for plug_perm in generate_plug_settings():
                    yield {"rotor": rot_perm, "ref": refl, "ring": r, "plug": plug_perm}


def combinations_task():
    for setting in gen_setting():
        while data_queue.qsize() >= max_queue_size:
            time.sleep(0.2)
            if stop_event.is_set():
                break
        data_queue.put(setting)

        if stop_event.is_set():
            break


def run_enigma_task(num):
    print("Started worker #{}".format(num))
    while not stop_event.is_set():
        while data_queue.empty():
            if stop_event.is_set():
                return
            time.sleep(0.05)
        d = data_queue.get()

        def generate_rotor_positions():
            for s1 in ALPHABET:
                for s2 in ALPHABET:
                    for s3 in ALPHABET:
                        yield s1 + s2 + s3

        machine = EnigmaMachine.from_key_sheet(
            rotors=d["rotor"],
            reflector=d["ref"],
            ring_settings=d["ring"],
            plugboard_settings=d["plug"])

        print("Created enigma from settings: ")
        print(d)

        for r in generate_rotor_positions():
            machine.set_display(r)

            for cipher, char in zip(CIPHERTEXT, PLAINTEXT):
                output = machine.process_text(cipher)
                if output != char:
                    break
            else:
                d["display"] = r
                solution_queue.put(d)
                stop_event.set()
                return


def main():
    parser = argparse.ArgumentParser("Try to find enigma settings when cipher and plain text are known.")
    parser.add_argument('--ciphertext', metavar='STRING', required=True)
    parser.add_argument('--plaintext', metavar='STRING', required=True)
    args = parser.parse_args()

    global CIPHERTEXT
    global PLAINTEXT
    CIPHERTEXT = args.ciphertext.upper()
    PLAINTEXT = args.plaintext.upper()
    # sanity check ciphertext and plaintext
    if not CIPHERTEXT.isalpha():
        print("Error: Ciphertext can only contain letters.")
        return
    if not PLAINTEXT.isalpha():
        print("Error: Plaintext can only contain letters.")
        return
    if len(CIPHERTEXT) != len(PLAINTEXT):
        print("Error: Ciphertext and plaintext have to be equal in length.")
        return
    for a, b in zip(PLAINTEXT, CIPHERTEXT):
        if a == b:
            print("Error: No letter is encrypted to itself. There will be no solution.")
            return

    num_cores = cpu_count()
    pool = Pool(num_cores)
    r = pool.map_async(run_enigma_task, [i for i in range(num_cores)])
    # generate combinations
    combinations_task()

    pool.close()
    pool.join()

    if stop_event.is_set():
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("Solution found! Encrypt {} to {}".format(PLAINTEXT, CIPHERTEXT))
        while not solution_queue.empty():
            print(solution_queue.get())
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    else:
        print("No solution found")


if __name__ == "__main__":
    main()
