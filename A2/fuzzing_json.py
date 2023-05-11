import random
import json 
import orjson
import msgspec

from tqdm import tqdm

letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


class dict_node:
    def __init__(self,parent):
        self.content = {}
        self.parent = parent

    def add_content(self,node):
        #select 5 random letters
        key = ''.join(random.choice(letters) for i in range(5))
        self.content[key] = node
    
    def get_content(self):
        return self.content
    
    def get_type(self):
        return dict

class list_node:
    def __init__(self,parent):
        self.content = []
        self.parent = parent
    
    def add_content(self,node):
        self.content.append(node)
    
    def get_content(self):
        return self.content
    
    def get_type(self):
        return list

class int_node:
    def __init__(self):
        self.content = random.randint(0,100)
    
    def get_type(self):
        return int

    def get_content(self):
        return self.content

class json_tree:
    def __init__(self,size=1000):
        self.root = dict_node(None)
        self.scope = self.root
        starting_size = size

        while size > 0:
            amount = random.randint(2,4)
            for i in range(amount):
                if self.coin() == 0:
                    self.scope.add_content(dict_node(self.scope))
                else:
                    self.scope.add_content(list_node(self.scope))
            size -= amount
            amount = 8-amount
            for i in range(amount):
                self.scope.add_content(int_node())

            new_scope_id = random.randint(0,starting_size-size)
            self.new_scope(new_scope_id)
            
    def new_scope(self,id):
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            if node.get_type() == dict:
                for key in node.get_content():
                    queue.append(node.get_content()[key])
            elif node.get_type() == list:
                for item in node.get_content():
                    queue.append(item)
            if len(queue) > id:
                #remove last index if it is an int
                while queue[-1].get_type() == int:
                    queue.pop(-1)
                self.scope = queue[-1]

    def convert(self):
        result = self.convert_node(self.root)
        return result

    @staticmethod
    def convert_node(node):
        if isinstance(node, dict_node):
            result = "{"
            content = node.get_content()
            for key in content:
                result += f'"{key}": {json_tree.convert_node(content[key])}, '
            if len(content) > 0:
                result = result[:-2]  # Remove the trailing comma and space
            result += "}"
            return result
        elif isinstance(node, list_node):
            result = "["
            content = node.get_content()
            for item in content:
                result += f'{json_tree.convert_node(item)}, '
            if len(content) > 0:
                result = result[:-2]  # Remove the trailing comma and space
            result += "]"
            return result
        elif isinstance(node, int_node):
            return str(node.get_content())

    @staticmethod
    def coin():
        return random.randint(0,1)


def random_data_generator():
    while True:
        j = json_tree(400)
        yield j.convert()


def main():
    random.seed(9001)
    data_generator = random_data_generator()
    exeptions = []
    mismatches = []
    for _ in tqdm(range(1000)):
        data = next(data_generator)
        try:
            output_json = json.dumps(data, indent=None, separators=(',', ':'), ensure_ascii=False).encode('utf8')
            output_orjson = orjson.dumps(data)
            output_mesgspec = msgspec.json.encode(data)
        except Exception as exception:
            exeptions += [(exception, data)]
        else:
            if not output_json == output_orjson == output_mesgspec:
                print(output_json, output_orjson, output_mesgspec)
                mismatches += [data]
    print(f'{len(exeptions)} exceptions and {len(mismatches)} mismatches found')


if __name__ == '__main__':
    main()
