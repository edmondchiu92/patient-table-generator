DOB_list = []
with open('../data/dob.txt', 'r') as a:
    DOB_list = a.read().splitlines()
    
print(DOB_list)
