import os


def set_env():
    print("Setting ENV")
    f = open(".env", "r")
    flines = f.readlines()

    for line in flines:
        try:
            n = line.split("=")[0]
            v = line.split("=")[1]
            n = n.strip()
            v = v.strip()
            os.environ[n] = v
        except:
            continue
