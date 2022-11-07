from sys import *
from interpreter import *

if __name__ == "__main__":
    content = parser(argv[1])
    print(content)

# python main.py "test.storm"