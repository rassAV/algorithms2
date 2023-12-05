class SpecialHashMap(dict):
    def __init__(self):
        self.iloc = iloc(self)
        self.ploc = ploc(self)

class iloc:
    def __init__(self, data):
        self.data = data

    def __getitem__(self, index):
        sort_data = sorted(self.data)
        if 0 <= index < len(sort_data):
            return self.data[sort_data[index]]
        else:
            raise ValueError("Index out of range!")

class ploc:
    def __init__(self, data):
        self.data = data

    def parse_dict(self, keys, values):
        result = [[], []]
        num = 0
        for i, key in enumerate(keys):
            resKey = []
            digits = True
            for ch in key:
                if ch.isdigit():
                    num += int(ch)
                    num *= 10
                elif ch == ",":
                    resKey.append(int(num / 10))
                    num = 0
                elif ch in ["(", " ", ")"]:
                    pass
                else:
                    digits = False
                    break
            if digits:
                resKey.append(int(num / 10))
                num = 0
                result[0].append(resKey)
                result[1].append(list(values)[i])
        return result
    
    def parse_index(self, index):
        conditions = [[], []]
        op = ""
        num = 0
        for ch in index:
            if len(conditions[0]) >= len(conditions[1]):
                if ch in ["=", "<", ">"]:
                    if num != 0:
                        raise SyntaxError("Invalid indexes syntax")
                    op += str(ch)
                elif ch.isdigit():
                    if len(op) > 0:
                        conditions[0].append(op)
                        op = ""
                    num += int(ch)
                    num *= 10
                elif ch == ",":
                    conditions[1].append(int(num / 10))
                    num = 0
                elif ch == " ":
                    pass
                else:
                    raise SyntaxError("Invalid condition")
            else:
                raise SyntaxError("Invalid indexes syntax")
        conditions[1].append(int(num / 10))
        return conditions

    def compare(self, op, num, key):
        match op: 
            case '=':
                return key == num
            case '<>':
                return key != num
            case '>':
                return key > num
            case '<':
                return key < num
            case '>=':
                return key >= num
            case '<=':
                return key <= num

    def answer(self, conditions, data):
        result = []
        ops = conditions[0]
        nums = conditions[1]
        keys = data[0]
        values = data[1]
        for k, key in enumerate(keys):
            if len(nums) == len(key):
                if all([self.compare(ops[i], num, key[i]) for i, num in enumerate(nums)]):
                    result.append([key, values[k]])
        return result
    
    def answer_to_dict(self, answer):
        result = {}
        for ans in answer:
            if len(ans[0]) == 1:
                result[ans[0][0]] = ans[1]
            else:
                result[tuple(ans[0])] = ans[1]
        return result

    def __getitem__(self, index):
        conditions = self.parse_index(index)
        data_parsed = self.parse_dict(self.data.keys(), self.data.values())
        return self.answer_to_dict(self.answer(conditions, data_parsed))
