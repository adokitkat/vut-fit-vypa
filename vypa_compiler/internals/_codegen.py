from vypa_compiler.internals._utils import eprint, ExitCode

#'expression-cast', 'expression-list', 'next-expression'

def classify_expression(expression):
    for expr in expression:
        if expr == 'expression-arithmetic-binary':
            return Expr_Arithmetic(expression)
        elif expr == 'expression-function-call': 
            return Expr_Function_Call(expression)
        elif expr == 'expression-value':
            return Expr_Value(expression)
        elif expr == 'expression-arithmetic-unary':
            pass # Expr Arithmetic?
        elif expr == 'expression-relational':
            return Expr_Relational(expression)
        elif expr == 'expression-logical-unary':
            return Expr_Logical_Unary(expression)
        elif expr == 'expression-logical-binary':
            return Expr_Logical_Binary(expression)
        elif expr == 'expression-class-new':
            return Expr_Class_New(expression)

# Unary???
class Expr_Value:
    def __init__(self, value):
        self.output = value[1]

# Unary???
class Expr_Arithmetic:
    def __init__(self, expr):
        self.expr = expr
        self.output = []
        self.process(expr)
    
    def process(self,expression):
        previous = None
        for arg_expr in expression:
            if isinstance(arg_expr, (list, tuple)):
                self.process(arg_expr)
            if previous == 'expression-arithmetic-binary':
                self.output.append(arg_expr)
            elif previous == 'expression-value':
                self.output.append(arg_expr)
            previous = arg_expr 


class Expr_Class_Operation:
    def __init__(self, expr):
        self.expr = expr
        self.output = []

class Expr_Function_Call:
    def __init__(self, expr):
        self.expr = expr
        self.output = []

class Expr_Class_New:
    def __init__(self, expr):
        self.expr = expr
        self.output = []

class Expr_Logical_Unary:
    def __init__(self, expr):
        self.expr = expr
        self.output = []

class Expr_Logical_Binary:
    def __init__(self, expr):
        self.expr = expr
        self.output = []

class Expr_Relational:
    def __init__(self, expr):
        self.expr = expr
        self.output = []


class Instruction:

    # Chunk manipulation
    @staticmethod
    def _create(dst, size):
        '''dst (reg), size (stack/reg/imm)'''
        if size >= 0:
            return f"CREATE {dst}, {size}"
        else:
            exit(ExitCode.ERR_TARGET_CODE_GEN) # Should not happen

    @staticmethod
    def _copy(dst, id):
        '''Shallow copy

        dst (reg), id (stack/reg/imm)'''
        return f"COPY {dst}, {id}"

    @staticmethod
    def _get_size(dst, id):
        '''dst (reg), id (stack/reg/imm)'''
        return f"GETSIZE {dst}, {id}"

    @staticmethod
    def _get_word(dst, id, index):    
        '''dst (reg), id (stack/reg/imm), index (stack/reg/imm)'''
        return f"GETWORD {dst}, {id}, {index}"

    @staticmethod
    def _resize(dst, newsize):
        '''id (stack/reg/imm), newsize (stack/reg/imm)'''
        return f"RESIZE {dst}, {newsize}"

    @staticmethod
    def _set_word(id, index, value):
        '''id (stack/reg/imm), '''
        return f"SETWORD {id}, {index}, {value}"

    @staticmethod
    def _destroy(id):
        '''id (stack/reg/imm)'''
        return f"DESTROY {id}"   

    # Control flow
    @staticmethod
    def _call(pc, where):
        '''pc (stack), where (stack/reg/imm)'''
        return f"CALL {pc}, {where}"

    @staticmethod
    def _return(pc):
        '''restore PC from `pc`
        
        pc (stack/reg/imm)'''
        return f"RETURN {pc}"
    
    @staticmethod
    def _set(dst, value):
        '''copy `value` into `dst`
        
        dst (reg/stack), value (stack/reg/imm)'''
        return f"SET {dst}, {value}"

    @staticmethod
    def _jump(label):
        '''label (literal)'''
        return f"JUMP {label}"

    @staticmethod
    def _jumpz(label, src):
        '''if `src` is zero value, then jump to `label`
        
        label (literal), sec (stack/reg/imm)'''
        return f"JUMPZ {label}, {src}"

    @staticmethod
    def _jumpnz(label, src):
        '''if `src` is non-zero value, then jump to `label`
        
        label (literal), sec (stack/reg/imm)'''
        return f"JUMPNZ {label}, {src}"

    # Input and output
    @staticmethod
    def _reads(dst):
        '''dst (reg)'''
        return f"READS {dst}"

    @staticmethod
    def _writes(id):
        '''id (stack/reg/imm)'''
        return f"WRITES {id}"

    @staticmethod
    def _readi(dst):
        '''dst (reg)'''
        return f"READI {dst}"

    @staticmethod
    def _writei(id):
        '''id (stack/reg/imm)'''
        return f"WRITEI {id}"
    
    # Arithmetic, Relation, Logic, and Conversions
    @staticmethod
    def _addi(dst, src1, src2):
        '''dst (reg), src1 (stack/reg/imm), src2 (stack/reg/imm)'''
        return f"ADDI {dst}, {src1}, {src2}"

    @staticmethod
    def _subi(dst, src1, src2):
        '''dst (reg), src1 (stack/reg/imm), src2 (stack/reg/imm)'''
        return f"SUBI {dst}, {src1}, {src2}"

    @staticmethod
    def _muli(dst, src1, src2):
        '''dst (reg), src1 (stack/reg/imm), src2 (stack/reg/imm)'''
        return f"MULI {dst}, {src1}, {src2}"

    @staticmethod
    def _divi(dst, src1, src2):
        '''dst (reg), src1 (stack/reg/imm), src2 (stack/reg/imm)'''
        return f"DIVI {dst}, {src1}, {src2}"

    @staticmethod
    def _lti(dst, src1, src2):
        '''dst (reg), src1 (stack/reg/imm), src2 (stack/reg/imm)'''
        return f"LTI {dst}, {src1}, {src2}"

    @staticmethod
    def _gti(dst, src1, src2):
        '''dst (reg), src1 (stack/reg/imm), src2 (stack/reg/imm)'''
        return f"GTI {dst}, {src1}, {src2}"

    @staticmethod
    def _eqi(dst, src1, src2):
        '''dst (reg), src1 (stack/reg/imm), src2 (stack/reg/imm)'''
        return f"EQI {dst}, {src1}, {src2}"

    @staticmethod
    def _lts(dst, src1, src2):
        '''dst (reg), src1 (stack/reg/imm), src2 (stack/reg/imm)'''
        return f"LTS {dst}, {src1}, {src2}"

    @staticmethod
    def _gts(dst, src1, src2):
        '''dst (reg), src1 (stack/reg/imm), src2 (stack/reg/imm)'''
        return f"GTS {dst}, {src1}, {src2}"

    @staticmethod
    def _eqs(dst, src1, src2):
        '''dst (reg), src1 (stack/reg/imm), src2 (stack/reg/imm)'''
        return f"EQS {dst}, {src1}, {src2}"
    
    @staticmethod
    def _and(dst, src1, src2):
        '''dst (reg), src1 (stack/reg/imm), src2 (stack/reg/imm)'''
        return f"AND {dst}, {src1}, {src2}"

    @staticmethod
    def _or(dst, src1, src2):
        '''dst (reg), src1 (stack/reg/imm), src2 (stack/reg/imm)'''
        return f"OR {dst}, {src1}, {src2}"

    @staticmethod
    def _not(dst, src):
        '''dst (reg), src (stack/reg/imm)'''
        return f"NOT {dst}, {src}"

    ### INT2FLOAT/FLOAT2INT - nemame float

    @staticmethod
    def _int_to_string(dst, src):
        '''dst ?, src ?'''
        return f"INT2STRING {dst}, {src}"

    # Debugging
    @staticmethod
    def _dprinti(src):
        '''stderr
        
        src (stack/reg/imm)'''
        return f"DPRINTI {src}"

    @staticmethod
    def _dprints(id):
        '''stderr
        
        id (stack/reg/imm)'''
        return f"DPRINTS {id}"

    @staticmethod
    def _dumpregs():
        '''stderr'''
        return "DUMPREGS"

    @staticmethod
    def _dumpstack():
        '''stderr'''
        return "DUMPSTACK"

    @staticmethod
    def _dumpheap():
        '''stderr'''
        return "DUMPHEAP"

    @staticmethod
    def _dumpchunk(id):
        '''stderr
        
        id (stack/reg/imm)'''
        return f"DUMPCHUNK {id}"

if __name__ == "__main__":
    i = Instruction
    print(i._writes("yolo"))