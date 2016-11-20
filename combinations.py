from itertools import permutations, combinations
import string

__author__ = "Christoph Rist"
__copyright__ = "Copyright 2016, Christoph Rist"
__license__ = "MIT"

ALPHABET = list(string.ascii_uppercase)
NUMBER_RANGE = list(range(26))


def generate_plug_settings(nb_plugs, unused_alpha=set()):
    def generate_pairs_from_set(l, p_comb):
        if not bool(set(l) - unused_alpha):
            yield p_comb
            return
        for i in range(1, len(l)):
            rn = p_comb + l[0] + l[i] + " "
            ln = [l[j] for j in range(1, len(l)) if j is not i]
            if ln:
                yield from generate_pairs_from_set(ln, rn)
            else:
                yield rn

    # <-- 230230 iterations -->
    for comb in combinations(reversed(ALPHABET), nb_plugs):
        plug = ""
        ll = list(comb)
        c = len(ll) - 1
        for u in unused_alpha:
            for i in range(0, c + 1):
                if ll[i] == u:
                    ll[i], ll[c] = ll[c], ll[i]
                    c -= 1
                    break

        yield from generate_pairs_from_set(ll, plug)


def gen_setting(ciphertext, plaintext):
    unused_alpha = set(ALPHABET) - set(ciphertext) - set(plaintext)

    def generate_ring_settings():
        for r1 in NUMBER_RANGE:
            for r2 in NUMBER_RANGE:
                for r3 in NUMBER_RANGE:
                    yield [r1, r2, r3]

    rotors = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']
    reflectors = ['B', 'C']

    # <-- 2 iterations -->
    for refl in reflectors:
        # <-- 17576 iterations -->
        for r in generate_ring_settings():
            # <-- 336 iterations -->
            for rot_perm in permutations(rotors, 3):
                for plug_perm in generate_plug_settings(10, unused_alpha):
                    yield {"rotor": rot_perm, "ref": refl, "ring": r, "plug": plug_perm}
