#!/usr/bin/env python3
import re

raw_flag = input("Enter the raw data: ")

raw_flag = raw_flag.split()[::-1]

for i in range(len(raw_flag)):
	raw_flag[i] = re.findall('..', raw_flag[i])

flag = []
for chars in raw_flag:
	word = ""
	for char in chars[::-1]:
		if char != '0x':
			word += chr(int(char, 16))
	flag.append(word)

flag.reverse()
print(''.join(flag))
