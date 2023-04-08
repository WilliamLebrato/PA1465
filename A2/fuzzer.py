import random

import json
import orjson
import msgspec

from tqdm import tqdm


def random_data_generator():
    while True:
        yield {'field_1': random.randint(0, 100),
               'field_2': random.randint(100, 200)}  # maybe you have a better idea


def main():
    random.seed(9001)
    data_generator = random_data_generator()
    exeptions = []
    mismatches = []
    for _ in tqdm(range(1000)):
        data = next(data_generator)
        try:
            output_json = json.dumps(data, indent=None, separators=(',', ':'))
            output_orjson = orjson.dumps(data)
            output_mesgspec = msgspec.json.encode(data)
        except Exception as exception:
            exeptions += [(exception, data)]
        else:
            if not output_json.encode() == output_orjson == output_mesgspec:
                print(output_json.encode(), output_orjson, output_mesgspec)
                mismatches += [data]
    print(f'{len(exeptions)} exceptions and {len(mismatches)} mismatches found')


if __name__ == '__main__':
    main()
