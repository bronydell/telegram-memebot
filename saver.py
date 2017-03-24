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
        users.add(key.split('.')[0])
    return users