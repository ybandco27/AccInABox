# table definition
table = {
    'table_name'    : 'cb_ledger_params',
    'module_id'     : 'cb',
    'short_descr'   : 'Cb bank accounts',
    'long_descr'    : 'Cb bank accounts with parameters',
    'sub_types'     : None,
    'sub_trans'     : None,
    'sequence'      : None,
    'tree_params'   : None,
    'roll_params'   : None,
    'indexes'       : None,
    'ledger_col'    : None,
    'defn_company'  : None,
    'data_company'  : None,
    'read_only'     : False,
    }

# column definitions
cols = []
cols.append ({
    'col_name'   : 'row_id',
    'data_type'  : 'AUTO',
    'short_descr': 'Row id',
    'long_descr' : 'Row id',
    'col_head'   : 'Row',
    'key_field'  : 'Y',
    'calculated' : True,
    'allow_null' : False,
    'allow_amend': False,
    'max_len'    : 0,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : None,
    'dflt_rule'  : None,
    'col_checks' : None,
    'fkey'       : None,
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'created_id',
    'data_type'  : 'INT',
    'short_descr': 'Created id',
    'long_descr' : 'Created row id',
    'col_head'   : 'Created',
    'key_field'  : 'N',
    'calculated' : False,
    'allow_null' : False,
    'allow_amend': False,
    'max_len'    : 0,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : '0',
    'dflt_rule'  : None,
    'col_checks' : None,
    'fkey'       : None,
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'deleted_id',
    'data_type'  : 'INT',
    'short_descr': 'Deleted id',
    'long_descr' : 'Deleted row id',
    'col_head'   : 'Deleted',
    'key_field'  : 'N',
    'calculated' : False,
    'allow_null' : False,
    'allow_amend': False,
    'max_len'    : 0,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : '0',
    'dflt_rule'  : None,
    'col_checks' : None,
    'fkey'       : None,
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'ledger_id',
    'data_type'  : 'TEXT',
#   'short_descr': 'Ledger id',
#   'long_descr' : 'Ledger id',
#   'col_head'   : 'Ledger',
    'short_descr': 'Account code',
    'long_descr' : 'Account code',
    'col_head'   : 'Acc code',
    'key_field'  : 'A',
    'calculated' : False,
    'allow_null' : False,
    'allow_amend': False,
    'max_len'    : 20,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : None,
    'dflt_rule'  : None,
    'col_checks' : None,
    'fkey'       : None,
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'descr',
    'data_type'  : 'TEXT',
#   'short_descr': 'Description',
#   'long_descr' : 'Description',
#   'col_head'   : 'Description',
    'short_descr': 'Account name',
    'long_descr' : 'Account name',
    'col_head'   : 'Acc name',
    'key_field'  : 'N',
    'calculated' : False,
    'allow_null' : False,
    'allow_amend': True,
    'max_len'    : 30,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : None,
    'dflt_rule'  : None,
    'col_checks' : None,
    'fkey'       : None,
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'gl_ctrl_id',
    'data_type'  : 'INT',
    'short_descr': 'Gl control a/c',
    'long_descr' : 'Gl control a/c',
    'col_head'   : 'Gl ctrl',
    'key_field'  : 'N',
    'calculated' : False,
    'allow_null' : True,  # null means 'not integrated to g/l'
#   'allow_amend': True,  # can change from null to not-null to start integration
    'allow_amend': [['where', '', '$value', 'is', '$None', '']],
    'max_len'    : 0,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : None,
    'dflt_rule'  : None,
    'col_checks' : None,
    'fkey'       : ['gl_codes', 'row_id', 'ctrl_acc', 'gl_code', False, 'gl_codes'],
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'currency_id',
    'data_type'  : 'INT',
    'short_descr': 'Currency id',
    'long_descr' : 'Currency id',
    'col_head'   : 'Curr',
    'key_field'  : 'N',
    'calculated' : [['where', '', '_param.currency_id', 'is_not', '$None', '']],
    'allow_null' : False,
    'allow_amend': False,
    'max_len'    : 0,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : '{_param.currency_id}',
    'dflt_rule'  : None,
    'col_checks' : None,
    'fkey'       : ['adm_currencies', 'row_id', 'currency', 'currency', False, 'curr'],
    'choices'    : None,
    })
# cols.append ({
#     'col_name'   : 'alt_curr',
#     'data_type'  : 'BOOL',
#     'short_descr': 'Allow alternative currency?',
#     'long_descr' : 'Allow transactions in different currency?',
#     'col_head'   : 'Alt curr?',
#     'key_field'  : 'N',
#     'calculated' : False,
#     'allow_null' : False,
#     'allow_amend': True,
#     'max_len'    : 0,
#     'db_scale'   : 0,
#     'scale_ptr'  : None,
#     'dflt_val'   : 'false',
#     'dflt_rule'  : None,
#     'col_checks' : None,
#     'fkey'       : None,
#     'choices'    : None,
#     })
cols.append ({
    'col_name'   : 'auto_temp_no',
    'data_type'  : 'JSON',
    'short_descr': 'Auto-generate temp no?',
    'long_descr' : 'Parameters to generate number for unposted transaction. If blank, use auto tran no',
    'col_head'   : 'Auto inv no?',
    'key_field'  : 'N',
    'calculated' : False,
    'allow_null' : True,
    'allow_amend': True,
    'max_len'    : 0,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : None,
    'dflt_rule'  : None,
    'col_checks' : None,
    'fkey'       : None,
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'auto_rec_no',
    'data_type'  : 'JSON',
    'short_descr': 'Auto-generate receipt no?',
    'long_descr' : 'Parameters to generate receipt number. If blank, manual input',
    'col_head'   : 'Auto rec no?',
    'key_field'  : 'N',
    'calculated' : False,
    'allow_null' : True,
    'allow_amend': True,
    'max_len'    : 0,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : None,
    'dflt_rule'  : None,
    'col_checks' : None,
    'fkey'       : None,
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'auto_pmt_no',
    'data_type'  : 'JSON',
    'short_descr': 'Auto-generate payment no?',
    'long_descr' : 'Parameters to generate payment number. If blank, manual input',
    'col_head'   : 'Auto pmt no?',
    'key_field'  : 'N',
    'calculated' : False,
    'allow_null' : True,
    'allow_amend': True,
    'max_len'    : 0,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : None,
    'dflt_rule'  : None,
    'col_checks' : None,
    'fkey'       : None,
    'choices'    : None,
    })

# bank code/name
# branch code/name
# account number

# virtual column definitions
virt = []
virt.append ({
    'col_name'   : 'module_id',
    'data_type'  : 'TEXT',
    'short_descr': 'Module',
    'long_descr' : 'Module id',
    'col_head'   : '',
    'sql'        : "'cb'",
    })
virt.append ({
    'col_name'   : 'module_row_id',
    'data_type'  : 'INT',
    'short_descr': 'Module row id',
    'long_descr' : 'Module row id',
    'col_head'   : '',
    'sql'        : "SELECT b.row_id FROM {company}.db_modules b WHERE b.module_id = 'cb'",
    })

# cursor definitions
cursors = []
"""
cursors.append({
    'cursor_name': 'cb_ledg',
    'descr': 'Bank accounts',
    'columns': [
        ['ledger_id', 100, False, False, False, False, None, None, None, None],
        ['descr', 260, True, True, False, False, None, None, None, None],
        ],
    'filter': [],
    'sequence': [['ledger_id', False]],
    })
"""
cursors.append ({
    'cursor_name': 'cash_books',
    'title': 'Maintain cash book params',
    'columns': [
        ['ledger_id', 80, False, False, False, False, None, None, None, None],
        ['descr', 160, True, False, False, False, None, None, None, None],
        ],
    'filter': [],
    'sequence': [['ledger_id', False]],
    'formview_name': 'cb_params',
    })

# actions
actions = []
actions.append([
    'after_insert', '<pyfunc name="db.cache.ledger_inserted"/>'
    ])
actions.append([
    'after_commit', '<pyfunc name="db.cache.ledger_updated"/>'
    ])
