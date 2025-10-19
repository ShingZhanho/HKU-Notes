import sys
from page_gen_tools import start

def main():
    targets_list = sys.argv[1].split(" ")
    start(targets_list)

if __name__ == "__main__":
    main()
