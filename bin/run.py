import uvicorn
import sys

sys.path.append("./")

if __name__ == "__main__":
    from bin.env import set_env

    set_env()

    uvicorn.run("dolphin.main:app", host="0.0.0.0")
