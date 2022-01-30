import os

lines = open('./POST/INPUT/POST1.IN').readlines()

villages = int(lines[0].split(' ')[0])
print('villages =', villages)

post_offices = int(lines[0].split(' ')[1])
print('post offices =', post_offices)

assert villages >= post_offices

village_positions = list(map(int, lines[1].split(' ')))
print('village positions =', village_positions)
