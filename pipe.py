import os

"""
-------------------
more objects here
-------------------
"""

pin, pout = os.pipe()
os.write(pout, b"obj")
print(os.read(pin,2))
