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

### Part A Run 3 rows below.
# rockyou_data = np.genfromtxt("rockyou.txt", delimiter=None, dtype='U')
# table = dictionary_attack(rockyou_data)
# write_table_to_csv(table)
# Attack table is done. Wrote into attack_table.csv

# Part B
def find_passwords():
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

find_passwords()
# Name, Password
# Alice maganda
# Bob gangsta
# Charlie claire
# Harry grenade

# Part E
def part_e():
    salty_digitalcorp_data = np.genfromtxt("salty-digitalcorp.txt", delimiter=",", dtype='U', skip_header=1)
    rockyou_data = np.genfromtxt("rockyou.txt", delimiter=None, dtype='U')

    names = salty_digitalcorp_data[:,0]
    salts = salty_digitalcorp_data[:,1]
    hashes = salty_digitalcorp_data[:,2]

    # Hashes = H(Salts + passwords)
    table = {}

    for salt in salts:
        salted_pass = [salt + rockyou_data[k] for k in range(len(rockyou_data))]
        i = 0
        for password in salted_pass:
            hashed_string = hl.sha512(str(password).encode('utf-8')).hexdigest()
            if table:
                if rockyou_data[i] in table:
                    table[rockyou_data[i]].append(hashed_string)
                else:
                    table[rockyou_data[i]] = [hashed_string]
            else:
                table[rockyou_data[i]] = [hashed_string]
            i += 1

    passwords = []
    for hash in hashes:
        for key, entry in table.items():
            for element in entry:
                if element == hash:
                    passwords.append(key)

    print("Name, Password")
    for i in range(len(names)):
        print(names[i], passwords[i])

part_e()
# Name, Password
# Dave kitten
# Karen karen
# Faith bowwow
# Harrison pomegranate