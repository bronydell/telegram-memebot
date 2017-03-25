import shelve

filename = "settings"

def savePref(user,key,value):
    d = shelve.open(filename)
    d[str(user)+'.'+str(key)] = value
    d.close()

def openPref(user, key, default):
    d = shelve.open(filename)
    if (str(user)+'.'+str(key)) in d:
        return d[str(user)+'.'+str(key)]
    else:
        return default

def getUsers():
    d = shelve.open(filename)
    users = set()
    for key in list(d.keys()):
        users.add(int(key.split('.')[0]))
    return users

def getAdmins():
    d = shelve.open(filename)
    admins = set()
    for key in list(d.keys()):
        if key.split('.')[1] == 'is_admin':
            if d['{}.is_admin'.format(key.split('.')[0])] == True:
                admins.add(int(key.split('.')[0]))
    return admins
