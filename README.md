# DIY PyArmor RFT Mode

DIY PyArmor RFT Mode is an AST-based obfuscation tool that mimics the renaming functionality of PyArmor’s RFT mode. It systematically renames function names, class names, global and local variables, builtin references, and import aliases—while preserving function argument names, keyword argument names, any identifier that starts with `__`, strings in the module attribute `__all__`, and any names you choose to exclude.

The tool runs interactively:
- It scans the current working directory for Python (`.py`) files.
- It prompts you to select the file to transform.
- It asks for a custom alias prefix (default is `BwE_`).
- It allows you to enter a comma-separated list of identifiers to exclude from renaming.
- It outputs the transformed code as `<filename>_rft.py` and writes a detailed rename log as `<filename>_tracelog.log`.

## Features

- **AST-based Renaming**:
  - Renames **function names**, **class names**, **global and local variables**, **builtin references**, and **import aliases**.
- **Exclusions**:
  - Skips renaming for:
    - Function arguments in definitions.
    - Keyword argument names in calls.
    - Any identifier that starts with `__` (e.g. `__init__`, `__all__`, `__name__`).
    - Strings in the module attribute `__all__`.
    - Any names provided in the exclude list.
- **Interactive File Selection**:
  - Automatically lists all `.py` files in the current directory for you to choose from.
- **Custom Alias Prefix**:
  - Allows you to specify a custom prefix for generated aliases (default is `BwE_`).
- **Rename Log**:
  - Outputs a log file named `<filename>_tracelog.log` that lists each renaming event with its corresponding line number.

## Requirements

- **Python 3.6+** (Python 3.9+ is recommended if you want to use `ast.unparse` instead of `astunparse`).
- The **`astunparse`** package (if using Python versions older than 3.9):
  ```bash
  pip install astunparse

## Example

Given an original `hello.py`

```#!/usr/bin/env python3

import random
import base64
import string
import secrets
import binascii
from Crypto.Cipher import AES
import hashlib
from math import log2

def pointless_banner():
    banner = r"""
__________          ___________
\______   \___  _  _\_   _____/
 |    |  _/\  \/ \/ /|   __)_ 
 |    |   \ \      //        \
 |______  /  \_/\_//_______  /
        \/                 \/
"""
    print(banner)

def scramble_text(txt):
    arr = list(txt)
    random.shuffle(arr)
    return ''.join(arr)

def calculate_entropy(data):
    prob = {char: data.count(char) / len(data) for char in set(data)}
    return -sum(p * log2(p) for p in prob.values())

def rot18(text):
    table = str.maketrans(
        string.ascii_uppercase + string.ascii_lowercase + string.digits,
        string.ascii_uppercase[13:] + string.ascii_uppercase[:13] +
        string.ascii_lowercase[13:] + string.ascii_lowercase[:13] +
        string.digits[5:] + string.digits[:5]
    )
    return text.translate(table)

def to_binary(data):
    return ''.join(format(ord(c), '08b') for c in data)

def reverse_bytes(data):
    hex_data = binascii.hexlify(data.encode()).decode()
    return ''.join([hex_data[i:i+2] for i in range(0, len(hex_data), 2)][::-1])

def aes_encrypt(data, key):
    key = hashlib.sha256(key.encode()).digest()
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

def main():
    pointless_banner()
    u = input("Type something: ")
    print("Base64:", base64.b64encode(u.encode()).decode())
    print("Entropy:", calculate_entropy(u))
    print("ROT18:", rot18(u))
    print("Binary:", to_binary(u))
    print("Byte Reversed:", reverse_bytes(u))
    print("AES Encrypted:", aes_encrypt(u, 'pyarmoriscool'))
    input("Press Enter to quit...")

if __name__ == "__main__":
    main()
```

### Post Obfuscation

```import base64
import builtins
BwE_78142 = getattr(builtins, base64.b64decode("cHJpbnQ=").decode())
BwE_79432 = getattr(builtins, base64.b64decode("bGlzdA==").decode())
BwE_59119 = getattr(builtins, base64.b64decode("c2V0").decode())
BwE_83485 = getattr(builtins, base64.b64decode("bGVu").decode())
BwE_30150 = getattr(builtins, base64.b64decode("c3Vt").decode())
BwE_23312 = getattr(builtins, base64.b64decode("c3Ry").decode())
BwE_43630 = getattr(builtins, base64.b64decode("Zm9ybWF0").decode())
BwE_11014 = getattr(builtins, base64.b64decode("b3Jk").decode())
BwE_68792 = getattr(builtins, base64.b64decode("cmFuZ2U=").decode())
BwE_80301 = getattr(builtins, base64.b64decode("aW5wdXQ=").decode())

import random as BwE_60249
import base64 as BwE_56370
import string as BwE_21763
import secrets as BwE_19661
import binascii as BwE_78577
from Crypto.Cipher import AES as BwE_80065
import hashlib as BwE_05887
from math import log2 as BwE_75993

def BwE_71821():
    BwE_96432 = '\n__________          ___________\n\\______   \\___  _  _\\_   _____/\n |    |  _/\\  \\/ \\/ /|   __)_ \n |    |   \\ \\      //        \\\n |______  /  \\_/\\_//_______  /\n        \\/                 \\/\n'
    BwE_78142(BwE_96432)

def BwE_55875(txt):
    BwE_62684 = BwE_79432(txt)
    BwE_60249.shuffle(BwE_62684)
    return ''.join(BwE_62684)

def BwE_86601(data):
    BwE_08559 = {BwE_16840: (data.count(BwE_16840) / BwE_83485(data)) for BwE_16840 in BwE_59119(data)}
    return (- BwE_30150(((BwE_47176 * BwE_75993(BwE_47176)) for BwE_47176 in BwE_08559.values())))

def BwE_99230(text):
    BwE_26962 = BwE_23312.maketrans(((BwE_21763.ascii_uppercase + BwE_21763.ascii_lowercase) + BwE_21763.digits), (((((BwE_21763.ascii_uppercase[13:] + BwE_21763.ascii_uppercase[:13]) + BwE_21763.ascii_lowercase[13:]) + BwE_21763.ascii_lowercase[:13]) + BwE_21763.digits[5:]) + BwE_21763.digits[:5]))
    return text.translate(BwE_26962)

def BwE_73833(data):
    return ''.join((BwE_43630(BwE_11014(BwE_71590), '08b') for BwE_71590 in data))

def BwE_99644(data):
    BwE_03204 = BwE_78577.hexlify(data.encode()).decode()
    return ''.join([BwE_03204[BwE_28021:(BwE_28021 + 2)] for BwE_28021 in BwE_68792(0, BwE_83485(BwE_03204), 2)][::(- 1)])

def BwE_19451(data, key):
    key = BwE_05887.sha256(key.encode()).digest()
    BwE_87340 = BwE_80065.new(key, BwE_80065.MODE_EAX)
    (BwE_32200, BwE_79708) = BwE_87340.encrypt_and_digest(data.encode())
    return BwE_56370.b64encode(((BwE_87340.nonce + BwE_79708) + BwE_32200)).decode()

def BwE_17395():
    BwE_71821()
    BwE_21786 = BwE_80301('Type something: ')
    BwE_78142('Base64:', BwE_56370.b64encode(BwE_21786.encode()).decode())
    BwE_78142('Entropy:', BwE_86601(BwE_21786))
    BwE_78142('ROT18:', BwE_99230(BwE_21786))
    BwE_78142('Binary:', BwE_73833(BwE_21786))
    BwE_78142('Byte Reversed:', BwE_99644(BwE_21786))
    BwE_78142('AES Encrypted:', BwE_19451(BwE_21786, 'pyarmoriscool'))
    BwE_80301('Press Enter to quit...')
if (__name__ == '__main__'):
    BwE_17395()
```

### PyArmor's RFT Mode

```
#!/usr/bin/env python3
import base64
import builtins
import random as pyarmor__9
import base64 as pyarmor__10
import string as pyarmor__11
import secrets as pyarmor__12
import binascii as pyarmor__13
from Crypto.Cipher import AES as pyarmor__14
import hashlib as pyarmor__15
from math import log2 as pyarmor__16

def pyarmor__1():
    pyarmor__17 = r"""
__________          ___________
\______   \___  _  _\_   _____/
 |    |  _/\  \/ \/ /|   __)_ 
 |    |   \ \      //        \
 |______  /  \_/\_//_______  /
        \/                 \/
"""
    pyarmor__18(pyarmor__17)

def pyarmor__2(txt):
    pyarmor__19 = pyarmor__20(txt)
    pyarmor__9.shuffle(pyarmor__19)
    return ''.join(pyarmor__19)

def pyarmor__3(data):
    pyarmor__21 = {pyarmor__22: data.count(pyarmor__22) / pyarmor__23(data) for pyarmor__22 in pyarmor__24(data)}
    return -pyarmor__25(pyarmor__26 * pyarmor__16(pyarmor__26) for pyarmor__26 in pyarmor__21.values())

def pyarmor__4(text):
    pyarmor__27 = pyarmor__28.maketrans(
        pyarmor__11.ascii_uppercase + pyarmor__11.ascii_lowercase + pyarmor__11.digits,
        pyarmor__11.ascii_uppercase[13:] + pyarmor__11.ascii_uppercase[:13] +
        pyarmor__11.ascii_lowercase[13:] + pyarmor__11.ascii_lowercase[:13] +
        pyarmor__11.digits[5:] + pyarmor__11.digits[:5]
    )
    return text.translate(pyarmor__27)

def pyarmor__5(data):
    return ''.join(pyarmor__29(pyarmor__30(pyarmor__31), '08b') for pyarmor__31 in data)

def pyarmor__6(data):
    pyarmor__32 = pyarmor__13.hexlify(data.encode()).decode()
    return ''.join([pyarmor__32[pyarmor__33:pyarmor__33+2] for pyarmor__33 in pyarmor__34(0, pyarmor__23(pyarmor__32), 2)][::-1])

def pyarmor__7(data, key):
    key = pyarmor__15.sha256(key.encode()).digest()
    pyarmor__35 = pyarmor__14.new(key, pyarmor__14.MODE_EAX)
    pyarmor__36, pyarmor__37 = pyarmor__35.encrypt_and_digest(data.encode())
    return pyarmor__10.b64encode(pyarmor__35.nonce + pyarmor__37 + pyarmor__36).decode()

def pyarmor__8():
    pyarmor__1()
    pyarmor__38 = pyarmor__39("Type something: ")
    pyarmor__18("Base64:", pyarmor__10.b64encode(pyarmor__38.encode()).decode())
    pyarmor__18("Entropy:", pyarmor__3(pyarmor__38))
    pyarmor__18("ROT18:", pyarmor__4(pyarmor__38))
    pyarmor__18("Binary:", pyarmor__5(pyarmor__38))
    pyarmor__18("Byte Reversed:", pyarmor__6(pyarmor__38))
    pyarmor__18("AES Encrypted:", pyarmor__7(pyarmor__38, 'pyarmoriscool'))
    pyarmor__39("Press Enter to quit...")

if __name__ == "__main__":
    pyarmor__8()

```

As you can see the functionality is identical to that of PyArmor!

## My Trace Log Example (Truncated)

```Line 3: random -> BwE_60249
Line 4: base64 -> BwE_56370
Line 5: string -> BwE_21763
Line 6: secrets -> BwE_19661
Line 7: binascii -> BwE_78577
Line 8: AES -> BwE_80065
Line 9: hashlib -> BwE_05887
Line 10: log2 -> BwE_75993
Line 12: pointless_banner -> BwE_71821
Line 13: banner -> BwE_96432
Line 21: print -> BwE_78142
Line 21: banner -> BwE_96432
Line 23: scramble_text -> BwE_55875
Line 24: arr -> BwE_62684
Line 24: list -> BwE_79432
Line 25: random -> BwE_60249
Line 25: arr -> BwE_62684
Line 26: arr -> BwE_62684
Line 28: calculate_entropy -> BwE_86601
Line 29: prob -> BwE_08559
Line 29: char -> BwE_16840
Line 29: set -> BwE_59119
Line 29: char -> BwE_16840
Line 29: char -> BwE_16840
Line 29: len -> BwE_83485
Line 30: sum -> BwE_30150
Line 30: p -> BwE_47176
Line 30: prob -> BwE_08559
Line 30: p -> BwE_47176
Line 30: log2 -> BwE_75993
Line 30: p -> BwE_47176
```

## PyArmor's Trace Log Example (Truncated)

```trace.rft            hello:3 (import random as pyarmor__9)
trace.rft            hello:4 (import base64 as pyarmor__10)
trace.rft            hello:5 (import string as pyarmor__11)
trace.rft            hello:6 (import secrets as pyarmor__12)
trace.rft            hello:7 (import binascii as pyarmor__13)
trace.rft            hello:8 (from Crypto.Cipher import AES as pyarmor__14)
trace.rft            hello:9 (import hashlib as pyarmor__15)
trace.rft            hello:10 (from math import log2 as pyarmor__16)
trace.rft            hello:12 (pointless_banner->pyarmor__1)
trace.rft            hello:13 (banner->pyarmor__17)
trace.rft            hello:21 (print->pyarmor__18)
trace.rft            hello:21 (banner->pyarmor__17)
trace.rft            hello:23 (scramble_text->pyarmor__2)
trace.rft            hello:24 (arr->pyarmor__19)
trace.rft            hello:24 (list->pyarmor__20)
trace.rft            hello:25 (random->pyarmor__9)
trace.rft            hello:25 (arr->pyarmor__19)
trace.rft            hello:26 (arr->pyarmor__19)
trace.rft            hello:28 (calculate_entropy->pyarmor__3)
trace.rft            hello:29 (prob->pyarmor__21)
trace.rft            hello:29 (char->pyarmor__22)
trace.rft            hello:29 (char->pyarmor__22)
trace.rft            hello:29 (len->pyarmor__23)
trace.rft            hello:29 (char->pyarmor__22)
trace.rft            hello:29 (set->pyarmor__24)
trace.rft            hello:30 (sum->pyarmor__25)
trace.rft            hello:30 (p->pyarmor__26)
trace.rft            hello:30 (log2->pyarmor__16)
trace.rft            hello:30 (p->pyarmor__26)
trace.rft            hello:30 (p->pyarmor__26)
trace.rft            hello:30 (prob->pyarmor__21)
```

Functionally identical!
