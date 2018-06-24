import shelve

filename = "settings"


def save_pref(user, key, value):
    d = shelve.open(filename)
    d[str(user) + '.' + str(key)] = value
    d.close()


def open_pref(user, key, default):
    d = shelve.open(filename)
    if (str(user) + '.' + str(key)) in d:
        return d[str(user) + '.' + str(key)]
    else:
        return default


def get_users():
    d = shelve.open(filename)
    users = set()
    for key in list(d.keys()):
        users.add(int(key.split('.')[0]))
    return users


def get_admins():
    d = shelve.open(filename)
    admins = set()
    for key in list(d.keys()):
        if key.split('.')[1] == 'is_admin':
            if d['{}.is_admin'.format(key.split('.')[0])]:
                admins.add(int(key.split('.')[0]))
    return admins
