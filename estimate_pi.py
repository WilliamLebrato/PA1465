import argparse
from pathlib import Path
import random


def estimate_pi(n):
    count = 0
    for i in range(n):
        x, y = random.uniform(-1, 1), random.uniform(-1, 1)
        if x**2 + y**2 <= 1:
            count += 1
    return 4 * count / n


class PiFileWriter:
    @staticmethod
    def write(content: str, file_path: Path):
        with open(file_path, 'w', encoding='utf8') as file:
            file.write(content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='PI Maker', description='Computes pi and stores the result to a file')
    parser.add_argument('-i', '--iterations', default=1000000)
    parser.add_argument('-o', '--out_file', type=Path, default=None)
    args = parser.parse_args()

    if args.out_file:
        args.out_file.parent.mkdir(parents=True, exist_ok=True)

    pi = estimate_pi(args.iterations)

    if args.out_file:
        PiFileWriter.write(str(pi), args.out_file)
    else:
        print(pi)
