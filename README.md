# Padding Oracle

## Intro
This Python script is one of the many solutions to solve the Padding Oracle challenge from PentesterLab, available here:
https://pentesterlab.com/exercises/padding_oracle

## Details
Pad.py is used in order to detect a Padding Oracle vulnerability. It only rotates the last byte of the second last block and writes the results in a text file.
This text file can then be used with Burp Intruder.

Padding Oracle.py is the script that will exploit the vulnerability. You need to update the parameters at the end according to your needs, more specifically "URL", "COOKIES" and "cookie".
