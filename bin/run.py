import uvicorn
import sys

sys.path.append("./")

if __name__ == "__main__":
    uvicorn.run("dolphin.main:app", host="0.0.0.0")
