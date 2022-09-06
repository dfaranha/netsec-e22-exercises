# Exercises: Symmetric Encryption


## Preliminaries

Install Python, the PyCryptodome library, and ImageMagick.

### Ubuntu 21.04 / Debian 11

```
sudo apt install python3 python3-pip imagemagick
pip3 install --user pycryptodome
```

### Arch Linux

```
sudo pacman -S python python-pycryptodome imagemagick
```

## PPM -- A Simple Image File Format

Since looking at hex dumps can be a bit tiring, we are going to encrypt
pictures in the next exercises.

To this end, we use the Portable Pixel Map (PPM) format, which is a very simple
file format.
It starts with a human-readable header containing the dimensions of the image
(and the maximum value in each channel which is 255 in our case).
```
P6
<width> <height>
# The header can also contain comments which start with a # and continue until the end of the line.
255
```
This header is followed by n = 3 * width * height bytes.  Each pixel is stored
in three consecutive bytes which contain its red, green, and blue values.  The
pixels themselves are stored row by row.

PPM is quite inefficient and uncompressed.  Therefore, you probably don't have
any files in this format.  Some example files are included, but you can also
use other pictures, and convert it as follows (provided you have ImageMagick
installed):
```
$ convert image.png -depth 8 image.ppm
```

To work with these PPM files, we provide you with a Python class `PPMImage`
that can read and write PPM images and gives you easy access to the raw pixel
data.  You can find this class in the file `ppmcrypt.py`.

You can load/modify/store an image as follows:
```python
image = PPMImage.load_from_file(open('image.ppm', 'rb'))
print(f'image width: {image.width} px')
print(f'image height: {image.height} px')
print(f'first 16 bytes of that data: {image.data[:16].hex()}')
# make the first 1000 pixel blue
image.data[:3 * 1000] = bytes.fromhex('0000FF') * 1000
image.write_to_file(open('new_image.ppm', 'wb'))
```

PPM specification: http://netpbm.sourceforge.net/doc/ppm.html


## Exercise 1: Electronic Code Book (ECB)

Implement ECB encryption and decryption functionality in the `PPMImage` class
using the PyCryptodome library.  Take a look at the
[examples](https://pycryptodome.readthedocs.io/en/latest/src/examples.html#encrypt-data-with-aes)
and [the relevant API
documentation](https://pycryptodome.readthedocs.io/en/latest/src/cipher/classic.html).

Take some arbitrary image file and use the Python code to load your image,
encrypt it, and write the encrypted image back into a file:
```python
image = PPMImage.load_from_file(open('image.ppm', 'rb'))
image.encrypt(key, 'ecb')
image.write_to_file(open('image_encrypted.ppm', 'wb'))
```

Now open the encrypted image. What do you observe?

Try to modify encrypted pictures, and observe how the picture has changed after decryption.
For this you can use a hex editor, or you just access the `.data` property of
an `PPMImage` instance:
```python
image.data[42] = 0x42  # set the byte at position 42 to the value 0x42
```

Think about if you can make (somewhat) controlled changes to the picture.


## Exercise 2: Cipher-Block-Chaining (CBC) and Counter Mode (CTR)

Implement encryption and decryption with CBC and CTR modes analogously to ECB.

Note that both modes require an additional value:
- CBC takes an Initialization Vector (IV) (use the `iv` parameter to pass a bytes-object of 16 B)
- CTR takes a nonce (use the `nonce` paraemeter to pass a bytes-object of 8 B)
Since these are required for decryption, we store them in comments in the PPM
header.

What is different compared to ECB?
- Take a look at encrypted images containing different patterns.
- Modify the ciphertext and observe what happens to the plaintext?


## Exercise 3: Tampering with Counter Mode

While we cannot any obvious patterns in the ciphertexts generated by CBC and
CTR, an adversary can still tamper with ciphertext.

To demonstrate this problem with CTR mode, implement the following evil plan:

1. Take the image of the Danish flag `dk.ppm` and encrypt it using CTR mode.
2. Modify the encrypted image *without using the key* such that when decrypted,
   an image of the Swedish flag appears.

NB: You are given an image of the Swedish flag `se.ppm` that has the same
dimensions as `dk.ppm`.


## Exercise 4: Authenticated Encryption

We have seen that the modes of operation discussed above (ECB, CBC, CTR) allow
an adversary to modify the plaintext by performing operations on the
ciphertext.

To prevent tampering, we want to use *authenticated encryption*.  Modes of
operations providing this level of security create an authentication tag in
addition to the ciphertext.  When decrypting, this tag can be used to verify
the integrity of a given ciphertext.

- Implement the encryption and decryption with Galois-Counter Mode (GCM).
- Encrypt an image, modify the ciphertext, and try to decrypt the modified
  image. Observe what happens.


## Exercise 5: Are we done yet?

Now that we use authenticated encryption, it should be impossible to tamper
with encrypted images, right?

The file `security.ppm` contains a simple message.
Since we do not believe in the statement:

- Encrypt the file using GCM.
- Try to modify the encrypted file (without using the key) such that decryption
  succeeds, but the resulting image shows a different/modified message

What have you learned by this?



# Solution

To be posted after the lecture.