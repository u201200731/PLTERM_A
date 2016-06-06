# -*- coding: utf-8 -*-
from string import letters, digits
import copy
class CuteType:
    INT=1
    ID=4
    MINUS=2
    PLUS=3
    L_PAREN=5
    R_PAREN=6
    TRUE=8
    FALSE=9
    TIMES=10
    DIV=11
    LT=12
    GT=13
    EQ=14
    APOSTROPHE=15
    DEFINE=20
    LAMBDA=21
    COND=22
    QUOTE=23
    NOT=24
    CAR=25
    CDR=26
    CONS=27
    ATOM_Q=28
    NULL_Q=29
    EQ_Q=30

    KEYWORD_LIST=('define', 'lambda', 'cond','quote', 'not', 'car', 'cdr', 'cons', 'atom?', 'null?', 'eq?' )
    BINARYOP_LIST=(DIV, TIMES, MINUS, PLUS, LT, GT, EQ)
    BOOLEAN_LIST=(TRUE, FALSE)

def check_keyword(token):
    """
    :type token:str
    :param token:
    :return:
    """
    if token.lower() in CuteType.KEYWORD_LIST:
        return True
    return False

def is_type_keyword(token):
    if 20 <= token.type <= 30 :
        return True
    return False




def _get_keyword_type(token):
    return {
        'define':CuteType.DEFINE,
        'lambda':CuteType.LAMBDA,
        'cond':CuteType.COND,
        'quote':CuteType.QUOTE,
        'not':CuteType.NOT,
        'car':CuteType.CAR,
        'cdr':CuteType.CDR,
        'cons':CuteType.CONS,
        'atom?':CuteType.ATOM_Q,
        'null?':CuteType.NULL_Q,
        'eq?':CuteType.EQ_Q
    }[token]

CUTETYPE_NAMES=dict((eval(attr, globals(), CuteType.__dict__), attr) for attr in dir(CuteType()) if not callable(attr) and not attr.startswith("__"))


def is_type_binaryOp(token):
    """
    :type token:Token
    :param token:
    :return:
    """
    if token.type in CuteType.BINARYOP_LIST:
        return True
    return False
def is_type_boolean(token):
    """
    :type token:Token
    :param token:
    :return:
    """
    if token.type in CuteType.BOOLEAN_LIST:
        return True
    return False



class Token(object):
    def __init__(self, type, lexeme):
        """
        :type type:CuteType
        :type lexeme: str
        :param type:
        :param lexeme:
        :return:
        """
        self.type=type
        self.lexeme=lexeme
        #print type

    def __str__(self):
        #return self.lexeme
        if self is None: return None
        return "[" + CUTETYPE_NAMES[self.type] + ": " + self.lexeme + "]"
    def __repr__(self):
        return str(self)


class CuteScanner(object):
    """
    :type token_iter:iter
    """

    transM={}
    def __init__(self, source):
        """
        :type source:str
        :param source:
        :return:
        """
        source=source.strip()
        token_list=source.split(" ")
        self.token_iter=iter(token_list)


    def get_state(self, old_state, trans_char):
        if trans_char in digits+letters+'?':
            return {
                0: {k: 1 if k in digits else 4 for k in digits+letters},
                1: {k: 1 for k in digits},
                2: {k: 1 for k in digits},
                3: {k: 1 for k in digits},
                4: {k: 4 if k is not '?' else 16 for k in digits+letters+'?'},
                7: {k: 8 if k is 'T' else 9 for k in ['T', 'F']}
            }[old_state][trans_char]
        if old_state is 0:
            return {
                '(': 5, ')': 6,
                '+': 3, '-': 2,
                '*': 10, '/': 11,
                '<': 12, '=': 14,
                '>': 13, "'": 15,
                '#': 7
            }[trans_char]


    def next_token(self):
        state_old=0
        temp_token=next(self.token_iter, None)
        """:type :str"""
        if temp_token is None : return None
        for temp_char in temp_token:
            state_old=self.get_state(state_old, temp_char)

        if check_keyword(temp_token):
            result = Token(_get_keyword_type(temp_token), temp_token)
        else:
            result=Token(state_old, temp_token)
        return result

    def tokenize(self):
        tokens=[]
        while True:
            t=self.next_token()
            if t is None :break
            tokens.append(t)
        return tokens

class TokenType():
    INT=1
    ID=4
    MINUS=2
    PLUS=3
    LIST=5
    TRUE=8
    FALSE=9
    TIMES=10
    DIV=11
    LT=12
    GT=13
    EQ=14
    APOSTROPHE=15
    DEFINE=20
    LAMBDA=21
    COND=22
    QUOTE=23
    NOT=24
    CAR=25
    CDR=26
    CONS=27
    ATOM_Q=28
    NULL_Q=29
    EQ_Q=30

NODETYPE_NAMES = dict((eval(attr, globals(), TokenType.__dict__), attr) for attr in dir(TokenType()) if not callable(attr) and not attr.startswith("__"))

class Node (object):

    def __init__(self, type, value=None):
        self.next  = None
        self.value = value
        self.type  = type

    def set_last_next(self, next_node):
        if self.next is not None:
            self.next.set_last_next(next_node)

        else : self.next=next_node

    def get_tail(self):
        def get_list_tail(node):
            """
            :type node: Node
            """
            if node.type is TokenType.LIST:
                return get_list_tail(node.value)
            else:
                if node.next is None:
                    return node
                return get_list_tail(node.next)
        if self.type is TokenType.LIST:
            return get_list_tail(self)
        return self


    def __str__(self):
        result = ""

        if   self.type is TokenType.ID:
            result = "["+self.value+"]"
        elif self.type is TokenType.INT:
            result = str(self.value)
        elif self.type is TokenType.LIST:
            if self.value is not None and self.value.type is TokenType.QUOTE:
                result = str(self.value)
            else:
                result = "("+str(self.value)+")"
        elif self.type is TokenType.QUOTE:
            result = "'"
        else:
            result = "["+NODETYPE_NAMES[self.type]+"]"

        if self.next is None:
            return result
        else: return result+" "+str(self.next)

class BasicPaser(object):

    def __init__(self, token_list):
        """
        :type token_list:list
        :param token_list:
        :return:
        """
        self.token_iter=iter(token_list)

    def _get_next_token(self):
        """
        :rtype: Token
        :return:
        """
        next_token=next(self.token_iter, None)
        if next_token is None: return None
        return next_token

    def parse_expr(self):
        """
        :rtype : Node
        :return:
        """
        token =self._get_next_token()
        """:type :Token"""
        if token==None: return None
        result = self._create_node(token)
        return result


    def _create_node(self, token):
        if token is None: return None

        if   token.type is CuteType.INT:     return Node(TokenType.INT,  token.lexeme)
        elif token.type is CuteType.ID:      return Node(TokenType.ID,   token.lexeme)
        elif token.type is CuteType.L_PAREN: return Node(TokenType.LIST, self._parse_expr_list())
        elif token.type is CuteType.R_PAREN: return None
        elif token.type is CuteType.APOSTROPHE:
            q_node = Node(TokenType.QUOTE)
            q_node.next=self.parse_expr()
            new_list_node = Node(TokenType.LIST, q_node)
            return new_list_node

        elif token.type is CuteType.QUOTE:
            q_node = Node(TokenType.QUOTE)
            return q_node

        elif is_type_binaryOp(token) or \
            is_type_keyword(token)   or \
            is_type_boolean(token):
            return Node(token.type)

        else:
            return None

    def _parse_expr_list(self):
        head = self.parse_expr()
        """:type :Node"""
        if head is not None:
            head.next = self._parse_expr_list()
        return head

class CuteInterpreter(object):

    TRUE_NODE = Node(TokenType.TRUE)
    FALSE_NODE = Node(TokenType.FALSE)
    dic = {}
    lambda_temp =""
    op_temp=""
    def run_arith(self, arith_node):
        pass

    def run_func(self, func_node):
        rhs1 = func_node.next
        rhs2 = rhs1.next if rhs1.next is not None else None
        func_node_temp=""
        def create_quote_node(node, list_flag = False):
            """
            "Quote 노드를 생성한 뒤, node를 next로 하여 반환"
            "list_flag가 True일 경우, list node를 생성한 뒤, list의 value를 입력받은 node로 연결하고"
            "Quote의 next를 여기서 생상한 list로 연결함"
            "최종 리턴은 여기서 생성한 quote노드를 value로 갖는 List"
            """
            q_node = Node(TokenType.QUOTE)
            if list_flag:
                inner_l_node = Node(TokenType.LIST, node)
                q_node.next = inner_l_node
            else:
                q_node.next = node
            l_node = Node(TokenType.LIST, q_node)
            return l_node

        def is_quote_list(node):
            "Quote의 next가 list인지 확인"
            if node.type is TokenType.LIST:
                if node.value.type is TokenType.QUOTE:
                    if node.value.next.type is TokenType.LIST:
                        return True
            return False

        def pop_node_from_quote_list(node):
            "Quote list에서 quote에 연결되어 있는 list노드의 value를 꺼내줌"
            if not is_quote_list(node):
                return node
            return node.value.next.value

        def list_is_null(node):
            "입력받은 node가 null list인지 확인함"
            node = pop_node_from_quote_list(node)
            if node is None:return True
            return False

        if func_node.type is TokenType.PLUS:
            expr_rhs1 = self.run_expr(rhs1)
            expr_rhs2 = self.run_expr(rhs2)
            if self.dic.has_key(expr_rhs1.value) is True:
                expr_rhs1= self.dic.__getitem__(expr_rhs1.value)
            if self.dic.has_key(expr_rhs2.value)  is True:
                expr_rhs2= self.dic.__getitem__(expr_rhs2.value)
            return Node(TokenType.INT, int(expr_rhs1.value) + int(expr_rhs2.value))

        elif func_node.type is TokenType.MINUS:
            expr_rhs1 = self.run_expr(rhs1)
            expr_rhs2 = self.run_expr(rhs2)
            if self.dic.has_key(expr_rhs1.value) is True:
                expr_rhs1= self.dic.__getitem__(expr_rhs1.value)
            if self.dic.has_key(expr_rhs2.value)  is True:
                expr_rhs2= self.dic.__getitem__(expr_rhs2.value)
            return Node(TokenType.INT, int(expr_rhs1.value) - int(expr_rhs2.value))

        elif func_node.type is TokenType.TIMES:
            expr_rhs1 = self.run_expr(rhs1)
            expr_rhs2 = self.run_expr(rhs2)
            if self.dic.has_key(expr_rhs1.value) is True:
                expr_rhs1= self.dic.__getitem__(expr_rhs1.value)
            if self.dic.has_key(expr_rhs2.value)  is True:
                expr_rhs2= self.dic.__getitem__(expr_rhs2.value)
            return Node(TokenType.INT, int(expr_rhs1.value) * int(expr_rhs2.value))

        elif func_node.type is TokenType.DIV:
            expr_rhs1 = self.run_expr(rhs1)
            expr_rhs2 = self.run_expr(rhs2)
            if self.dic.has_key(expr_rhs1.value) is True:
                expr_rhs1= self.dic.__getitem__(expr_rhs1.value)
            if self.dic.has_key(expr_rhs2.value)  is True:
                expr_rhs2= self.dic.__getitem__(expr_rhs2.value)
            return Node(TokenType.INT, int(expr_rhs1.value) / int(expr_rhs2.value))

        elif func_node.type is TokenType.LT :
            expr_rhs1 = self.run_expr(rhs1)
            expr_rhs2 = self.run_expr(rhs2)
            if self.dic.has_key(expr_rhs1.value) is True:
                expr_rhs1= self.dic.__getitem__(expr_rhs1.value)
            if self.dic.has_key(expr_rhs2.value)  is True:
                expr_rhs2= self.dic.__getitem__(expr_rhs2.value)
            if (int(expr_rhs1.value) < int(expr_rhs2.value)):
                return self.TRUE_NODE
            else: return self.FALSE_NODE

        elif func_node.type is TokenType.GT:
           expr_rhs1 = self.run_expr(rhs1)
           expr_rhs2 = self.run_expr(rhs2)
           if self.dic.has_key(expr_rhs1.value) is True:
                expr_rhs1= self.dic.__getitem__(expr_rhs1.value)
           if self.dic.has_key(expr_rhs2.value)  is True:
                expr_rhs2= self.dic.__getitem__(expr_rhs2.value)
           if (int(expr_rhs1.value) > int(expr_rhs2.value)):
                return self.TRUE_NODE
           else: return self.FALSE_NODE

        elif func_node.type is TokenType.EQ:
            expr_rhs1 = self.run_expr(rhs1)
            expr_rhs2 = self.run_expr(rhs2)
            if self.dic.has_key(expr_rhs1.value) is True:
                expr_rhs1= self.dic.__getitem__(expr_rhs1.value)
            if self.dic.has_key(expr_rhs2.value)  is True:
                expr_rhs2= self.dic.__getitem__(expr_rhs2.value)
            if (int(expr_rhs1.value) == int(expr_rhs2.value)):
                return self.TRUE_NODE
            else: return self.FALSE_NODE

        elif func_node.type is TokenType.NOT:
            expr_rhs1 = self.run_expr(rhs1)
            if self.dic.has_key(expr_rhs1.value) is True:
                expr_rhs1= self.dic.__getitem__(expr_rhs1.value)
            if expr_rhs1.type is TokenType.TRUE:
                return self.FALSE_NODE
            else: return self.TRUE_NODE

        elif func_node.type is TokenType.COND:
            a = rhs1
            while(rhs1!=None):
                if self.dic.has_key(rhs1.value.value) is True:

                    temp=rhs1.value.next
                    rhs1.value= self.dic.__getitem__(rhs1.value.value)
                    rhs1.value.next=temp
                if self.run_expr(rhs1.value).type is TokenType.TRUE:
	                return rhs1.value.next
                rhs1 = rhs1.next


        elif func_node.type is TokenType.CAR:
            rhs1 = self.run_expr(rhs1)

            if self.dic.has_key(rhs1.value) is True:
                rhs1= self.dic.__getitem__(rhs1.value)
            if not is_quote_list(rhs1):
                print ("car error!")
            result = pop_node_from_quote_list(rhs1)
            if result.type is not TokenType.LIST:
                return result
            return create_quote_node(result)

        elif func_node.type is TokenType.CDR:
            rhs1 = self.run_expr(rhs1)

            if self.dic.has_key(rhs1.value) is True:
                rhs1= self.dic.__getitem__(rhs1.value)
            if not is_quote_list(rhs1):
                print ("car error!")
            rhs1_pop= pop_node_from_quote_list(rhs1)
            r = create_quote_node(rhs1_pop.next, list_flag = True)
            return r
            #작성

        elif func_node.type is TokenType.CONS:
            expr_rhs1 = self.run_expr(rhs1)
            expr_rhs2 = self.run_expr(rhs2)

            if self.dic.has_key(expr_rhs1.value) is True:
                expr_rhs1= self.dic.__getitem__(expr_rhs1.value)
            if self.dic.has_key(expr_rhs2.value)  is True:
                expr_rhs2= self.dic.__getitem__(expr_rhs2.value)
            expr_rhs1.next =None
            if expr_rhs1.type is not TokenType.LIST: result = expr_rhs1
            else: result =expr_rhs1.value.next

            temp = expr_rhs2.value.next.value
            result.next = temp
            r = create_quote_node(result, list_flag = True)

            return r
            #작성
            #rhs2는 무조건 list라고 가정



        elif func_node.type is TokenType.ATOM_Q:
            if self.dic.has_key(rhs1.value) is True:
                rhs1= self.dic.__getitem__(rhs1.value)

            #if rhs1 is None:
            #   return self.TRUE_NODE
            if list_is_null(rhs1): return self.TRUE_NODE
            if rhs1.type is not TokenType.LIST: return self.TRUE_NODE
            if rhs1.type is TokenType.LIST:
                if rhs1.value.type is TokenType.QUOTE:
                    if rhs1.value.next.type is not TokenType.LIST:
                        return self.TRUE_NODE
            return self.FALSE_NODE


        elif func_node.type is TokenType.EQ_Q:
            expr_rhs1 = self.run_expr(rhs1)
            expr_rhs2 = self.run_expr(rhs2)

            if self.dic.has_key(expr_rhs1.value) is True:
                expr_rhs1= self.dic.__getitem__(expr_rhs1.value)
            if self.dic.has_key(expr_rhs2.value)  is True:
                expr_rhs2= self.dic.__getitem__(expr_rhs2.value)
            if expr_rhs1.type is TokenType.INT:
                if expr_rhs2.type is TokenType.INT:
                    result1 = expr_rhs1.value
                    result2 = expr_rhs2.value
                    if(result1==result2):
                        return self.TRUE_NODE
                    else:
                        return self.FALSE_NODE
                return self.FALSE_NODE
            else:
                return self.FALSE_NODE
                        #작성

        elif func_node.type is TokenType.NULL_Q:
            if self.dic.has_key(rhs1.value) is True:
                rhs1= self.dic.__getitem__(rhs1.value)
            if list_is_null(rhs1): return self.TRUE_NODE
            return self.FALSE_NODE

        elif func_node.type is TokenType.DEFINE:
            expr_rhs1 = self.run_expr(rhs1)
            expr_rhs2 = self.run_expr(rhs2)

            expr_rhs1.next = None
            self.insertTable(expr_rhs1.value, expr_rhs2)


        elif func_node.type is TokenType.LAMBDA:
            #func_node_temp = copy.deepcopy(func_node) #deep copy 개쩔었다
            a = func_node.next.next.next
            if a is not None : # 람다에 값을 넣었을 때
                val = a.value
                inja = func_node.next.value.value
                func_node.next.next.next= None
                lamb_tem = copy.deepcopy(func_node.next.next)
                lamb = func_node.next.next.value

                while(lamb.next!=None): # 인자를 바인딩을 한다.
                    if lamb.next.value is inja:
                        lamb.next.value = val
                    if self.dic.has_key(lamb.next.value) is True:
                        lamb.next.value = self.dic.__getitem__(lamb.next.value).value
                    #if self.dic.has_key(lamb.next.value.value) is True:
                    #    lamb.next.value = self.dic.__getitem__(lamb.next.value).value
                    lamb = lamb.next
                cal = self.run_expr(func_node.next.next) # 변수 바인딩 한 것을 계산한다.


                 #바인딩 한 부분을 제거한다.
                rhs2 = rhs2.value
                lamb_tem = lamb_tem.value
                while(rhs2.next!=None):
                    if rhs2.next.value is not lamb_tem.next.value:
                        rhs2.next.value = lamb_tem.next.value
                    rhs2 = rhs2.next
                    lamb_tem = lamb_tem.next


                return cal

            if a is None : # define 할 때
                 return func_node

        elif func_node.type is TokenType.LIST:
            if func_node.value.type is TokenType.LAMBDA:
                return


        else:
            return None
    def insertTable(self, id, value):
        self.dic[id]= value
        print self.dic[id]

    def run_expr(self, root_node):
        """
        :type root_node: Node
        """
        if root_node is None:
            return None
        if root_node.type is TokenType.ID:
            return root_node
        elif root_node.type is TokenType.INT:
            return root_node
        elif root_node.type is TokenType.TRUE:
            return root_node
        elif root_node.type is TokenType.FALSE:
            return root_node
        elif root_node.type is TokenType.LIST:
            return self.run_list(root_node)
        else:
            print "Run Expr Error"
        return None

    def run_list(self, l_node):
        """
        :type l_node:Node
        """
        op_code = l_node.value

        if op_code is None:
            return l_node
        if self.dic.has_key(op_code.value) is True:
            lambda_temp = op_code.next
            op_code = self.dic.__getitem__(op_code.value)
            op_temp = op_code
            while(op_code.next!=None):
                op_code = op_code.next
            op_code.next = lambda_temp
            return self.run_func(op_temp)

        if op_code.type in \
                [TokenType.CAR, TokenType.CDR, TokenType.CONS, TokenType.ATOM_Q,TokenType.PLUS,
                 TokenType.MINUS, TokenType.TIMES, TokenType.DIV, TokenType.LT, TokenType.LAMBDA,
                 TokenType.GT,TokenType.EQ, TokenType.NOT, TokenType.COND, TokenType.DEFINE,
                                    \
                 TokenType.EQ_Q, TokenType.NULL_Q]:
            return self.run_func(op_code)
        if op_code.type is TokenType.QUOTE:
            return l_node
        if op_code.type is TokenType.LIST:
            if op_code.value.type is TokenType.LAMBDA:
                return self.run_func(op_code)
        else:
            print "application: not a procedure;"
            print "expected a procedure that can be applied to arguments"
            print "Token Type is "+ op_code.value
            return None



def print_node(node):
    """
    "Evaluation 후 결과를 출력하기 위한 함수"
    "입력은 List Node 또는 atom"
    :type node: Node
    """
    def print_list(node):
        """
        "List노드의 value에 대해서 출력"
        "( 2 3 )이 입력이면 2와 3에 대해서 모두 출력함"
        :type node: Node
        """
        def print_list_val(node):
            if node.next is not None:
                return print_node(node)+" "+print_list_val(node.next)
            return print_node(node)

        if node.type is TokenType.LIST:
            if node.value.type is TokenType.QUOTE:
                return print_node(node.value)
            return "("+print_list_val(node.value)+")"

    if node is None:
        return ""
    if node.type in [TokenType.ID, TokenType.INT]:
        return node.value
    if node.type is TokenType.TRUE:
        return "#T"
    if node.type is TokenType.FALSE:
        return "#F"
    if node.type is TokenType.PLUS:
        return "+"
    if node.type is TokenType.MINUS:
        return "-"
    if node.type is TokenType.TIMES:
        return "*"
    if node.type is TokenType.DIV:
        return "/"
    if node.type is TokenType.GT:
        return ">"
    if node.type is TokenType.LT:
        return "<"
    if node.type is TokenType.EQ:
        return "="
    if node.type is TokenType.LIST:
        return print_list(node)
    if node.type is TokenType.ATOM_Q:
        return "atom?"
    if node.type is TokenType.CAR:
        return "car"
    if node.type is TokenType.CDR:
        return "cdr"
    if node.type is TokenType.COND:
        return "cond"
    if node.type is TokenType.CONS:
        return "cons"
    if node.type is TokenType.LAMBDA:
        return "lambda"
    if node.type is TokenType.NULL_Q:
        return "null?"
    if node.type is TokenType.EQ_Q:
        return "eq?"
    if node.type is TokenType.NOT:
        return "not"
    if node.type is TokenType.QUOTE:
        return "'"+print_node(node.next)

def Test_method(input):
    test_cute = CuteScanner(input)
    test_tokens=test_cute.tokenize()
    test_basic_paser = BasicPaser(test_tokens)
    node = test_basic_paser.parse_expr()
    cute_inter = CuteInterpreter()
    result = cute_inter.run_expr(node)
    print print_node(result)

def Test_All():

    #Test_method("( define a #T )")
    #Test_method("( car ' ( 1 2 3 ) )")
    #Test_method("( define b ' ( 1 2 3 ) )")
    #Test_method("( define b ( + 2 3 ) )")
    #Test_method("( define b ( + 2 6 ) )")
    #Test_method("( + a 3 )")
    #Test_method("( car b )")
    #Test_method("( + b 3 )")
    #Test_method("( define plus1 ( lambda ( x ) ( + x 1 ) ) )")
    #Test_method("( plus1 2 )")
    #Test_method("( ( lambda ( x ) ( + x 1 ) ) 2 )")
    #Test_method("( cond ( a 3 ) ( #T 7 ) )")

    i = True
    while(i):
        cal = raw_input("> ")
        print "...",
        Test_method(cal)

    #Test_method("( define x 9 )")
    #Test_method("( define add2 ( lambda ( x ) ( + x 2 ) ) )")
    #Test_method("( add2 3 )")
    #Test_method("( add2 x )")
    #Test_method("( define plus1 ( lambda ( x ) ( + x 1 ) ) )")
    #Test_method("( plus1 2 )")
    #Test_method("( define plus1 ( lambda ( x ) ( + x 1 ) ) )")
    ##Test_method("( define plus2 ( lambda ( x ) ( + ( plus1 x ) 1 ) ) )")
    #Test_method("( plus1 2 )")
    #Test_method("( plus2 2 )")
       # answer = raw_input("계속 하시겠습니까?(y,n) : ")
       # if(answer =="n"):
       #     i = False
       #     print "goodbye"


Test_All()
