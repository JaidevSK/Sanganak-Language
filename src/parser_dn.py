from src.astDefiner import *
from src.lexer_dn import *

class Parser:
    def __init__(self, tokens, args=[]):
        # आम्ही प्रथम टोकनची यादी, वर्तमान निर्देशांक आणि रिक्त स्टॅकसह पार्सरची सुरुवात करतो.
        self.tokens = tokens
        self.i = 0
        self.stack = []
        self.args = args

    def parse(self):
        # टोकन पार्स करण्यासाठी ही फंक्शन वापरली जाते.
        try:
            while self.i < len(self.tokens):  # टोकनवर लूप करा
                token = self.tokens[self.i]  # वर्तमान टोकन मिळवा
                if isinstance(token, StringToken):  # जर टोकन स्ट्रिंग असेल
                    self.stack.append(token.v)
                elif isinstance(token, NumberToken):
                    self.stack.append(int(token.v))
                elif isinstance(token, NegNumberToken):
                    self.stack.append(-int(token.v))
                elif isinstance(token, DecimalNumberToken):
                    self.stack.append(float(token.v))
                elif isinstance(token, NegDecimalNumberToken):
                    self.stack.append(-float(token.v))
                elif isinstance(token, BoolToken):
                    if token.v in ["true", "खरे"]:
                        self.stack.append(True)
                    else:
                        self.stack.append(False)
                elif isinstance(token, SymbolToken):
                    self.stack.append(token)
                elif isinstance(token, WordToken):
                    if token.v == '[':
                        openingctr = 1
                        tokens_list = []
                        self.i += 1
                        while self.i < len(self.tokens):
                            if self.tokens[self.i] == WordToken("]"):
                                openingctr -= 1
                            elif self.tokens[self.i] == WordToken("["):
                                openingctr += 1
                            if openingctr == 0:
                                p = Parser(tokens_list)
                                p.parse()
                                stk = p.stack
                                self.stack.append(stk)
                                break
                            else:
                                tokens_list.append(self.tokens[self.i])
                                self.i += 1

                    elif token.v == '+':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        num1 = self.stack.pop()
                        num2 = self.stack.pop()
                        assert isinstance(num1, (int, float)), "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(num2, (int, float)), "अवैध ऑपरेन्ड प्रकार"
                        self.stack.append(num1 + num2)
                    elif token.v == '-':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        num1 = self.stack.pop()
                        num2 = self.stack.pop()
                        assert isinstance(num1, (int, float)), "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(num2, (int, float)), "अवैध ऑपरेन्ड प्रकार"
                        self.stack.append(num2 - num1)
                    elif token.v == '*':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        num1 = self.stack.pop()
                        num2 = self.stack.pop()
                        assert isinstance(num1, (int, float)), "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(num2, (int, float)), "अवैध ऑपरेन्ड प्रकार"
                        self.stack.append(num1 * num2)
                    elif token.v == '/':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        num1 = self.stack.pop()
                        num2 = self.stack.pop()
                        assert isinstance(num1, (int, float)), "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(num2, (int, float)), "अवैध ऑपरेन्ड प्रकार"
                        assert num1 != 0, "शून्यावर विभागणी"
                        self.stack.append(num2 / num1)
                    elif token.v == '^':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        num1 = self.stack.pop()
                        num2 = self.stack.pop()
                        assert isinstance(num1, (int, float)), "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(num2, (int, float)), "अवैध ऑपरेन्ड प्रकार"
                        assert not (num1 <= 0 and num2 == 0), "शून्यावर विभागणी"
                        self.stack.append(num2 ** num1)
                    elif token.v == 'वाचा':
                        inp_val = input()
                        if inp_val in ["true", "खरे"]:
                            self.stack.append(True)
                        elif inp_val in ["false", "खोटे"]:
                            self.stack.append(False)
                        elif inp_val[0] != '"':
                            if inp_val[0] == "-":
                                inp_val_wo_neg = inp_val[1:]
                                if inp_val_wo_neg.isdigit():
                                    self.stack.append(int(inp_val))
                                elif inp_val_wo_neg.replace('.', '', 1).isdigit():
                                    self.stack.append(float(inp_val))
                                else:
                                    raise Exception(f"अवैध प्रकार इनपुट: {inp_val}")
                            elif inp_val.isdigit():
                                self.stack.append(int(inp_val))
                            elif inp_val.replace('.', '', 1).isdigit():
                                self.stack.append(float(inp_val))
                            else:
                                raise Exception(f"अवैध प्रकार इनपुट: {inp_val}")
                        else:
                            if inp_val[-1] == '"':
                                for j in range(1, len(inp_val) - 1):
                                    if inp_val[j] == '"' and inp_val[j - 1] != '\\':
                                        raise Exception(f"अवैध स्ट्रिंग: {inp_val}")
                                self.stack.append(inp_val[1:-1])
                            else:
                                raise Exception(f"अवैध स्ट्रिंग: {inp_val}")
                    elif token.v == 'दाखवा':
                        assert len(self.stack) > 0, "रिक्त स्टॅक"
                        def format_value(value):
                            if isinstance(value, bool):
                                return "खरे" if value else "खोटे"
                            elif isinstance(value, list):
                                formatted_list = " ".join(format_value(v) for v in value)
                                return f"[ {formatted_list} ]"
                            elif isinstance(value, str):
                                return '"' + value + '"'
                            elif isinstance(value, SymbolToken):
                                return "'" + value.v
                            else:
                                return str(value)
                        print(format_value(self.stack[-1]))
                        self.stack.pop()
                    elif token.v == 'छापा':
                        assert len(self.stack) > 0, "रिक्त स्टॅक"
                        if isinstance(self.stack[-1], str):
                            to_print = self.stack[-1]
                            to_print = to_print.replace('\\n', '\n').replace('\\t', '\t').replace('\\\\', '\\').replace('\\"', '"')
                            print(to_print)
                            self.stack.pop()
                        else:
                            print(self.stack[-1])
                            self.stack.pop()
                    elif token.v == 'काढा':
                        assert len(self.stack) > 0, "रिक्त स्टॅक"
                        self.stack.pop()
                    elif token.v == 'नक्कल':
                        assert len(self.stack) > 0, "रिक्त स्टॅक"
                        self.stack.append(self.stack[-1])
                    elif token.v == 'फिरवा':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        num1 = self.stack.pop()
                        num2 = self.stack.pop()
                        self.stack.append(num1)
                        self.stack.append(num2)
                    elif token.v == 'जोडा':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        assert isinstance(self.stack[-1], str), "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(self.stack[-2], str), "अवैध ऑपरेन्ड प्रकार"
                        str1 = self.stack.pop()
                        str2 = self.stack.pop()
                        self.stack.append(str2 + str1)
                    elif token.v == "नकार":
                        assert len(self.stack) > 0, "रिक्त स्टॅक"
                        assert isinstance(self.stack[-1], bool), "अवैध ऑपरेन्ड प्रकार"
                        b1 = self.stack.pop()
                        self.stack.append(not b1)
                    elif token.v == "किंवा":
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        assert isinstance(self.stack[-1], bool), "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(self.stack[-2], bool), "अवैध ऑपरेन्ड प्रकार"
                        b1 = self.stack.pop()
                        b2 = self.stack.pop()
                        self.stack.append(b1 or b2)
                    elif token.v == "आणि":
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        assert isinstance(self.stack[-1], bool), "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(self.stack[-2], bool), "अवैध ऑपरेन्ड प्रकार"
                        b1 = self.stack.pop()
                        b2 = self.stack.pop()
                        self.stack.append(b1 and b2)
                    elif token.v == "एक्सओआर":
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        assert isinstance(self.stack[-1], bool), "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(self.stack[-2], bool), "अवैध ऑपरेन्ड प्रकार"
                        b1 = self.stack.pop()
                        b2 = self.stack.pop()
                        self.stack.append(b1 ^ b2)
                    elif token.v == '=':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        num1 = self.stack.pop()
                        num2 = self.stack.pop()
                        assert isinstance(num1, (int, float)), "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(num2, (int, float)), "अवैध ऑपरेन्ड प्रकार"
                        self.stack.append(num1 == num2)
                    elif token.v == '<':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        num1 = self.stack.pop()
                        num2 = self.stack.pop()
                        assert isinstance(num1, (int, float)), "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(num2, (int, float)), "अवैध ऑपरेन्ड प्रकार"
                        self.stack.append(num1 > num2)
                    elif token.v == '>':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        num1 = self.stack.pop()
                        num2 = self.stack.pop()
                        assert isinstance(num1, (int, float)), "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(num2, (int, float)), "अवैध ऑपरेन्ड प्रकार"
                        self.stack.append(num1 < num2)
                    elif token.v == '>=':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        num1 = self.stack.pop()
                        num2 = self.stack.pop()
                        assert isinstance(num1, (int, float)), "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(num2, (int, float)), "अवैध ऑपरेन्ड प्रकार"
                        self.stack.append(num1 <= num2)
                    elif token.v == '<=':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        num1 = self.stack.pop()
                        num2 = self.stack.pop()
                        assert isinstance(num1, (int, float)), "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(num2, (int, float)), "अवैध ऑपरेन्ड प्रकार"
                        self.stack.append(num1 >= num2)
                    elif token.v == '!=':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        num1 = self.stack.pop()
                        num2 = self.stack.pop()
                        assert isinstance(num1, (int, float)), "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(num2, (int, float)), "अवैध ऑपरेन्ड प्रकार"
                        self.stack.append(num1 != num2)
                    elif token.v == 'न_?':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        idx = self.stack.pop()
                        lst = self.stack.pop()
                        assert isinstance(idx, int), "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(lst, list), "अवैध ऑपरेन्ड प्रकार"
                        self.stack.append(lst[idx])
                    elif token.v == "अतिरिक्त_तर्क":
                        print(self.stack)
                        self.stack.append(self.args)
                        print(self.stack)
                    elif token.v == 'फैलवा':
                        assert len(self.stack) > 0, "रिक्त स्टॅक"
                        lst = self.stack.pop()
                        assert isinstance(lst, list), "अवैध ऑपरेन्ड प्रकार"
                        for elt in lst:
                            self.stack.append(elt)
                    elif token.v == 'बूल_समान':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        b1 = self.stack.pop()
                        b2 = self.stack.pop()
                        assert isinstance(b1, bool), "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(b2, bool), "अवैध ऑपरेन्ड प्रकार"
                        self.stack.append(b1 == b2)
                    elif token.v == 'बूल_वेगळे':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        b1 = self.stack.pop()
                        b2 = self.stack.pop()
                        assert isinstance(b1, bool), "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(b2, bool), "अवैध ऑपरेन्ड प्रकार"
                        self.stack.append(b1 != b2)
                    elif token.v == 'स्ट्रिंग_समान':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        s1 = self.stack.pop()
                        s2 = self.stack.pop()
                        assert isinstance(s1, str), "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(s2, str), "अवैध ऑपरेन्ड प्रकार"
                        self.stack.append(s1 == s2)
                    elif token.v == 'स्ट्रिंग_वेगळे':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        s1 = self.stack.pop()
                        s2 = self.stack.pop()
                        assert isinstance(s1, str), "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(s2, str), "अवैध ऑपरेन्ड प्रकार"
                        self.stack.append(s1 != s2)
                    elif token.v == 'लेक्स_जास्त':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        s1 = self.stack.pop()
                        s2 = self.stack.pop()
                        assert isinstance(s1, str), "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(s2, str), "अवैध ऑपरेन्ड प्रकार"
                        self.stack.append(s1 < s2)
                    elif token.v == 'लेक्स_कमी':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        s1 = self.stack.pop()
                        s2 = self.stack.pop()
                        assert isinstance(s1, str), "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(s2, str), "अवैध ऑपरेन्ड प्रकार"
                        self.stack.append(s1 > s2)
                    elif token.v == 'लेक्स_जास्त_किंवा_बरोबर':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        s1 = self.stack.pop()
                        s2 = self.stack.pop()
                        assert isinstance(s1, str), "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(s2, str), "अवैध ऑपरेन्ड प्रकार"
                        self.stack.append(s1 <= s2)
                    elif token.v == 'लेक्स_कमी_किंवा_बरोबर':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        s1 = self.stack.pop()
                        s2 = self.stack.pop()
                        assert isinstance(s1, str), "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(s2, str), "अवैध ऑपरेन्ड प्रकार"
                        self.stack.append(s1 >= s2)
                    elif token.v == 'लिस्ट':
                        assert len(self.stack) > 0, "रिक्त स्टॅक"
                        lst = self.stack.pop()
                        assert isinstance(lst, list), "अवैध ऑपरेन्ड प्रकार"
                        self.stack.append(len(lst))
                    elif token.v == 'लिस्ट':
                        self.stack = list([self.stack])
                    elif token.v == 'लिस्ट_न':
                        assert len(self.stack) > 0, "रिक्त स्टॅक"
                        n = self.stack.pop()
                        assert isinstance(n, int), "अवैध ऑपरेन्ड प्रकार"
                        dummy = []
                        for _ in range(n):
                            dummy.append(self.stack.pop())
                        dummy.reverse()
                        self.stack.append(dummy)
                    elif token.v == '{':
                        opening_ctr = 1
                        tokens_list = []
                        self.i += 1
                        while self.i < len(self.tokens):
                            if self.tokens[self.i] == WordToken("}"):
                                opening_ctr -= 1
                            elif self.tokens[self.i] == WordToken("{"):
                                opening_ctr += 1
                            if opening_ctr == 0:
                                self.stack.append(tokens_list)
                                break
                            else:
                                tokens_list.append(self.tokens[self.i])
                                self.i += 1
                    elif token.v == 'चला':
                        assert len(self.stack) > 0, "रिक्त स्टॅक"
                        procedure = self.stack.pop()
                        assert isinstance(procedure, list), "अवैध ऑपरेन्ड प्रकार"
                        p = Parser(procedure)
                        p.parse()
                        self.stack.extend(p.stack)
                    elif token.v == 'जर':
                        assert len(self.stack) > 2, "रिक्त स्टॅक"
                        else_proc = self.stack.pop()
                        then_proc = self.stack.pop()
                        condition = self.stack.pop()
                        assert isinstance(condition, bool), "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(then_proc, list) and isinstance(else_proc, list), "अवैध ऑपरेन्ड प्रकार"
                        p = Parser(then_proc if condition else else_proc)
                        p.functions = self.functions
                        p.variables = self.variables
                        p.stack = self.stack
                        p.args = self.args
                        p.parse()
                        self.stack.extend(p.stack)
                        self.functions.update(p.functions)
                        self.variables.update(p.variables)
                    elif token.v == 'पुन्हा':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        procedure = self.stack.pop()
                        n = self.stack.pop()
                        assert isinstance(n, int) and n >= 0, "अवैध ऑपरेन्ड प्रकार"
                        assert isinstance(procedure, list), "अवैध ऑपरेन्ड प्रकार"
                        for _ in range(n):
                            p = Parser(procedure)
                            p.functions = self.functions
                            p.variables = self.variables
                            p.stack = self.stack
                            p.parse()
                            self.stack.extend(p.stack)
                            self.functions.update(p.functions)
                            self.variables.update(p.variables)
                    elif token.v == 'जेव्हा':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        body_proc = self.stack.pop()
                        condition_proc = self.stack.pop()
                        assert isinstance(condition_proc, list) and isinstance(body_proc, list), "अवैध ऑपरेन्ड प्रकार"
                        stack_copy = self.stack.copy()
                        while True:
                            cp = Parser(condition_proc)
                            cp.stack.extend(self.stack)
                            cp.parse()
                            condition = cp.stack.pop()
                            assert isinstance(condition, bool), "अवैध ऑपरेन्ड प्रकार"
                            if not condition:
                                break
                            bp = Parser(body_proc)
                            bp.stack.extend(self.stack)
                            bp.parse()
                            self.stack = bp.stack.copy()
                    elif token.v == 'वाढवा':
                        assert len(self.stack) > 0, "रिक्त स्टॅक"
                        num = self.stack.pop()
                        assert isinstance(num, int), "अवैध ऑपरेन्ड प्रकार"
                        self.stack.append(num + 1)
                    elif token.v == 'घटवा':
                        assert len(self.stack) > 0, "रिक्त स्टॅक"
                        num = self.stack.pop()
                        assert isinstance(num, int), "अवैध ऑपरेन्ड प्रकार"
                        self.stack.append(num - 1)
                    elif token.v == 'नंबर_आहे_का':
                        assert len(self.stack) > 0, "रिक्त स्टॅक"
                        num = self.stack.pop()
                        self.stack.append(isinstance(num, (int, float)))
                    elif token.v == 'लिस्ट_आहे_का':
                        assert len(self.stack) > 0, "रिक्त स्टॅक"
                        num = self.stack.pop()
                        self.stack.append(isinstance(num, list))
                    elif token.v == 'स्ट्रिंग_आहे_का':
                        assert len(self.stack) > 0, "रिक्त स्टॅक"
                        num = self.stack.pop()
                        self.stack.append(isinstance(num, str))
                    elif token.v == 'बूल_आहे_का':
                        assert len(self.stack) > 0, "रिक्त स्टॅक"
                        num = self.stack.pop()
                        self.stack.append(isinstance(num, bool))
                    elif token.v == 'सदैव':
                        assert len(self.stack) > 0, "रिक्त स्टॅक"
                        body_proc = self.stack.pop()
                        assert isinstance(body_proc, list), "अवैध ऑपरेन्ड प्रकार"
                        while True:
                            bp = Parser(body_proc)
                            bp.stack.extend(self.stack)
                            bp.parse()
                            self.stack = bp.stack.copy()
                    elif token.v == 'प्रत्येक':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        list_on = self.stack.pop()
                        body_on = self.stack.pop()
                        assert isinstance(body_on, list) and isinstance(list_on, list), "अवैध ऑपरेन्ड प्रकार"
                        for elt in list_on:
                            bp = Parser(body_on)
                            bp.stack.append(elt)
                            bp.parse()
                    elif token.v == 'चिन्ह_आहे_का':
                        assert len(self.stack) > 0, "रिक्त स्टॅक"
                        item = self.stack.pop()
                        self.stack.append(isinstance(item, SymbolToken))
                    elif token.v == 'चिन्ह_समान':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        sym1 = self.stack.pop()
                        sym2 = self.stack.pop()
                        assert isinstance(sym1, SymbolToken), "अवैध ऑपरेन्ड प्रकार: चिन्ह अपेक्षित"
                        assert isinstance(sym2, SymbolToken), "अवैध ऑपरेन्ड प्रकार: चिन्ह अपेक्षित"
                        self.stack.append(sym1 == sym2)
                    elif token.v == 'व्याख्या':
                        assert len(self.stack) > 1, "रिक्त स्टॅक"
                        symbol = self.stack.pop()
                        procedure = self.stack.pop()
                        assert isinstance(symbol, SymbolToken), "अवैध ऑपरेन्ड प्रकार: चिन्ह अपेक्षित"
                        assert isinstance(procedure, list), "अवैध ऑपरेन्ड प्रकार: प्रक्रिया अपेक्षित"
                        if not symbol.v:
                            raise Exception("रिक्त चिन्ह परवानगी दिलेले नाही")
                        self.functions[symbol.v] = procedure
                    else:
                        if token.v in self.functions:
                            procedure = self.functions[token.v]
                            p = Parser(procedure, self.args)
                            p.functions = self.functions
                            p.variables = self.variables
                            p.stack = self.stack
                            p.parse()
                            self.stack = p.stack
                        elif token.v in self.variables:
                            self.stack.append(self.variables[token.v])
                        else:
                            raise Exception(f"अज्ञात टोकन किंवा फंक्शन: {token.v}")
                self.i += 1
        except Exception as e:
            print(e)

    functions = {}
    variables = {}