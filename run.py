import logging
import sys

from tg import tg_run

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-release':
        logging.basicConfig(level=logging.ERROR,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    tg_run.run()
