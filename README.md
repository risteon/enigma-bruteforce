# enigma-bruteforce

This small script tries to find a enigma setting encrypting known plaintext into known ciphertext.

Brian Neal's Py-Enigma library is used to simulate the enigma. All possible combinations are bruteforced. Note that is unlikely to find a working combination using this strategy if the plaintext and ciphertext are somewhat longer than five characters each.

Example:
```
$ python3 main.py --plaintext=GITHUB --ciphertext=PYJAMA
```
This outputs (after a while of searching):
```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Solution found! Encrypt GITHUB to PYJAMA
{'ref': 'B', 'plug': 'AB CD EF GL HJ IN KO MP QT RS ', 'rotor': ('I', 'II', 'III'), 'ring': [0, 0, 0], 'display': 'HLR'}
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
```

## Dependencies

```
Py-Enigma
```
