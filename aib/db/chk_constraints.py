from json import loads
from ast import literal_eval
import operator
import re

from errors import AibError

def chk_constraint(ctx, constraint, value=None, errmsg=None):
    # can be a column constraint (col_chk) or a table constraint (upd_chk or del_chk)
    try:
        db_obj = ctx.db_obj  # this is a column constraint
        fld = ctx
        descr = ctx.col_defn.short_descr
    except AttributeError:
        db_obj = ctx  # this is a table constraint
        fld = None
        descr = db_obj.db_table.short_descr
    new_check = []
    for test, lbr, src, chk, tgt, rbr in constraint:
        if test in ('and', 'or'):
            new_check.append(test)
        if lbr == '(':
            new_check.append(lbr)
        if src == '$value':
            src_val = value
        else:
            src_val = db_obj.getval(src)
        if tgt == '':
            tgt_val = None
        else:
            tgt_val = literal_eval(tgt)
        chk, err = CHKS[chk]
        try:
            result = chk(src_val, tgt_val)
        except ValueError as e:
            result = False
            err = e.args[0]
        if result is False:
            if not errmsg:  # if exists, use errmsg supplied
                errmsg = err
                if '$src' in errmsg:
                    errmsg = errmsg.split('$src')
                    errmsg.insert(1, '{}'.format(db_obj.getfld(src).col_name))
                    errmsg = ''.join(errmsg)
                if '$tgt' in errmsg:
                    errmsg = errmsg.split('$tgt')
                    errmsg.insert(1, tgt)
                    errmsg = ''.join(errmsg)
        new_check.append(str(result))  # literal 'True' or 'False'
        if rbr == ')':
            new_check.append(rbr)

    try:
        result = eval(' '.join(new_check))
        if result is False:
            raise AibError(head=descr, body=errmsg)
    except SyntaxError:  # e.g. unmatched brackets
        errmsg = 'constraint {} is invalid'.format(constraint)
        raise AibError(head=descr, body=errmsg)

def enum(value, args):
    # [['enum', ['aaa', 'bbb', 'ccc']]
    return value in args

def pattern(value, args):
    return bool(re.match(args+'$', value))  #  $ means end of string

def cdv(value, args):
    # this cannot work as is - is value a string or an int?
    # it will be easy to get working when needed, so leave for now
    weights, cdv_mod = args
    base, chkdig = value[:-1], value[-1]
#   tot = sum(operator.mul(b, w) for b, w in zip(base, weights))
    tot = sum((b * w) for b, w in zip(base, weights))
    mod = tot % cdv_mod
    return mod == chkdig

def nospace(value, args):
    return value.isalnum()

def nexist(value, args):
    table_name, where = args

    where_clause = 'WHERE'
    params = []
    for test, lbr, col, op, expr, rbr in where:
        col = 'a.{}'.format(col)

        if expr is None:
            expr = 'null'

        if not isinstance(expr, str):  # must be int, dec, date
            params.append(expr)
            expr = '?'
        elif expr.lower() == 'null':
            pass  # don't parameterise 'null'
        elif expr.lower() == '$value':
            params.append(value)
            expr = '?'
        elif expr.startswith("c'"):  # expr is a column name
            expr = expr[2:-1]  # strip leading "c'" and trailing "'"
            expr = 'a.{}'.format(expr)
        elif expr.startswith('('):  # expression
            # could be a tuple - WHERE title IN ('Mr', 'Mrs')
            raise NotImplementedError  # does this ever happen
        elif expr.startswith('_'):  # parameter
            raise NotImplementedError  # does this ever happen
        elif expr.startswith('?'):  # get user input
            raise NotImplementedError  # does this ever happen
        else:  # must be literal string
            params.append(expr)
            col = 'LOWER({})'.format(col)
            expr = 'LOWER(?)'

        where_clause += ' {} {}{} {} {}{}'.format(
            test, lbr, col, op, expr, rbr)

    where_clause = where_clause.replace('?', self.param_style)

    if chk_val == '$value':
        chk_val = value
    with db_obj.db_session as conn:
        conn.cur.execute(
            'SELECT COUNT(*) FROM {}.{} WHERE {} = {}'
            .format(company, db_obj.data_table, fld.col_name,
            conn.param_style) , chk_val)
    return conn.cur.fetchone()[0] == 0

CHKS = {
    '=': (operator.eq, '$src must equal $tgt'),
    '!=': (operator.ne, '$src must not equal $tgt'),
    '<': (operator.lt, '$src must be less than $tgt'),
    '>': (operator.gt, '$src must be greater than $tgt'),
    '<=': (operator.le, '$src must be less than or equal to $tgt'),
    '>=': (operator.ge, '$src must greater than or equal to $tgt'),
    'is': (operator.is_, '$src must be $tgt'),
    'is not': (operator.is_not, '$src must not be $tgt'),
    'in': (lambda x,y: x in y, '$src must be one of $tgt'),
#   'in': (enum,  'must be one of $tgt'),
    'not in': (lambda x,y: x not in y, '$src must not be one of $tgt'),
    'matches': (lambda x,y: bool(re.match(y+'$', x)),  'Value must match the pattern $tgt'),
#   'matches': (pattern,  'Value must match the pattern $tgt'),
    'cdv': (cdv,  '$src fails the check digit test $tgt'),
    'nospace': (nospace,  '$src may not contain spaces'),
#   'is xml': (is_xml, ''),
    'nexist': (nexist, '$src must not exist on $tgt')
    }

#--------------------------------------------------------------------
"""
import operator
ops = {
  'in':lambda x,y: x in y,  # operator.contains has the args backwards
  '==':operator.eq, # or use '=' for more SQL-like syntax
  '<':operator.lt,
  '>':operator.gt,
}

op, value = 'in', "('abc', 'xyz')"
x = 'abc'

if ops[op](x,ast.literal_eval(value)):
  print("Constraint passed")
else:
  print("Ignore this one")

ChrisA
"""

#--------------------------------------------------------------------
"""
import operator
OPERATORS = {
    '=': operator.eq,
    'is': operator.is_,
    '<': operator.lt,
    # etc.
    }

def eval_op(column_name, op, literal):
    value = lookup(column_name)  # whatever...
    return OPERATORS[op](value, literal)

result = False
# first row has bool_op = 'or'

for (bool_op, column_name, comparison_op, literal) in sequence:
    flag = eval_op(column_name, comparison_op, literal)
    if bool_op == 'and':
        result = result and flag
    else: 
        assert bool_op == 'or'
        result = result or flag
    # Lazy processing?
    if result:
        break

"""
