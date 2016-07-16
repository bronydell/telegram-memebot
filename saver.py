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