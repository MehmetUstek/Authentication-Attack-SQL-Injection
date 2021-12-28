import hashlib as hl
import numpy as np

def dictionary_attack(rockyou_data):
    table = {}
    for i in rockyou_data:
        hashed_string = hl.sha512(str(i).encode('utf-8')).hexdigest()
        table[i] = hashed_string
    return table

def write_table_to_csv(table):
    keys = list(table.keys())
    vals = list(table.values())
    stack = np.stack((keys, vals), axis=1)
    np.savetxt("attack_table.csv", stack, delimiter=",", fmt="%s")

# rockyou_data = np.genfromtxt("rockyou.txt", delimiter=None, dtype='U')
# table = dictionary_attack(rockyou_data)
# write_table_to_csv(table)
# Attack table is done. Wrote into attack_table.csv

# Part B
digitalcorp_data = np.genfromtxt("digitalcorp.txt", delimiter=",", dtype='U', skip_header=1)
attack_table = np.genfromtxt("attack_table.csv", delimiter=",", dtype='U')

names = digitalcorp_data[:,0]
hashes = digitalcorp_data[:,1]
attack_table_passwords = attack_table[:,0]
attack_table_hashes:np.ndarray = attack_table[:,1]
passwords = []
for i in hashes:
    index = np.where(attack_table_hashes == i)
    password = attack_table_passwords[index][0]
    passwords.append(password)

print("Name, Password")
for i in range(len(names)):
    print(names[i], passwords[i])


