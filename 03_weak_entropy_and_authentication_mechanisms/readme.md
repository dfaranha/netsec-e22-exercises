# Exercises: Weak Entropy and Authentication Mechanisms

## Exercise 1: Authentication Mechanisms

We will classify authentication mechanisms described in a set of printed slides according to the taxonomy we saw on class, and rank from the least secure to the most secure. The class will be split in at most 8 groups, each with its own set of slides. There will be two activities in the exercise:

1. First, classify all different authentication solutions into the 4 types given. Use the diagram below as a reference example. Consider that a user is authenticating against some service provider, and the classification should be performed from the point of view of the service provider and what authentication factors must be managed by it.

<p align="center">
  <img src="https://user-images.githubusercontent.com/5369810/134070931-a702ac64-8d96-45e1-a1fb-bc8846e572b9.png" />
</p>

2. After all solutions are classified, organize each column from **least** secure (on bottom) to **most** secure (on top).

**Observation:** _There is no single correct solution, the point is exactly to discuss the trade-offs. Assume a realistic implementation (not horrible or perfect) working in realistic conditions._

## Exercise 2: Weak Entropy

I have a big problem: When preparing this exercise last Monday, I encrypted a
very important file.  Unfortunately, I forgot to save the key, and now I cannot
access the data anymore.  Can you help me decrypt it?

This is the command that I used:
```
$ python encrypt.py plain.txt ciphertext.bin
```


### Solution

See [`decrypt.py`](decrypt.py) for a brute force attack over possible keys.
Use it like this:
```
$ python decrypt.py 2021-09-20 ciphertext.bin decrypted.txt
```
