# table definition
table = {
    'table_name'    : 'ar_ledger_params',
    'module_id'     : 'ar',
    'short_descr'   : 'Ar ledgers',
    'long_descr'    : 'Ar ledgers with parameters',
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
    'short_descr': 'Ledger id',
    'long_descr' : 'Ledger id',
    'col_head'   : 'Ledger',
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
    'short_descr': 'Description',
    'long_descr' : 'Description',
    'col_head'   : 'Description',
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
    'col_name'   : 'location_id',
    'data_type'  : 'INT',
    'short_descr': 'Location id',
    'long_descr' : 'Location id - if specified, all customers will share this location',
    'col_head'   : 'Loc',
    'key_field'  : 'N',
    'calculated' : ['_param.location_id', 'is_not', None],
    'allow_null' : True,  # null means customers can have any location
    'allow_amend': True,  # if change from null to not-null, must check existing data
    'max_len'    : 0,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : '{_param.location_id}',
    'dflt_rule'  : None,
    'col_checks' : None,
    'fkey'       : ['adm_locations', 'row_id', 'location', 'location', False, 'locs'],
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'currency_id',
    'data_type'  : 'INT',
    'short_descr': 'Currency id',
    'long_descr' : 'Currency id - if specified, all customers will share this currency',
    'col_head'   : 'Curr',
    'key_field'  : 'N',
    'calculated' : ['_param.currency_id', 'is_not', None],
    'allow_null' : True,  # null means customers can have any currency
    'allow_amend': True,  # if change from null to not-null, must check existing data
    'max_len'    : 0,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : '{_param.currency_id}',
    'dflt_rule'  : None,
    'col_checks' : None,
    'fkey'       : ['adm_currencies', 'row_id', 'currency', 'currency', False, 'curr'],
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'alt_curr',
    'data_type'  : 'BOOL',
    'short_descr': 'Allow alternative currency?',
    'long_descr' : 'Allow transactions in different currency from customers?',
    'col_head'   : 'Alt curr?',
    'key_field'  : 'N',
    'calculated' : False,
    'allow_null' : False,
    'allow_amend': True,
    'max_len'    : 0,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : 'false',
    'dflt_rule'  : None,
    'col_checks' : None,
    'fkey'       : None,
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'alt_rec_override',
    'data_type'  : 'BOOL',
    'short_descr': 'Allow receipt override?',
    'long_descr' : 'Allow receipt in different currency to be overridden? Can control % with alt_rec_perc.',
    'col_head'   : 'Alt rec oride?',
    'key_field'  : 'N',
    'calculated' : False,
    'allow_null' : False,
    'allow_amend': True,
    'max_len'    : 0,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : 'false',
    'dflt_rule'  : None,
    'col_checks' : None,
    'fkey'       : None,
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'alt_rec_perc',
    'data_type'  : 'DEC',
    'short_descr': 'Max percent receipt override',
    'long_descr' : 'Maximum percent alt receipt override compared with system exchange rate - 0 means no check',
    'col_head'   : 'Alt rec perc',
    'key_field'  : 'N',
    'calculated' : False,
    'allow_null' : False,
    'allow_amend': True,
    'max_len'    : 0,
    'db_scale'   : 2,
    'scale_ptr'  : None,
    'dflt_val'   : '0',
    'dflt_rule'  : None,
    'col_checks' : None,
    'fkey'       : None,
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'auto_temp_no',
    'data_type'  : 'JSON',
    'short_descr': 'Auto-generate temp no?',
    'long_descr' : 'Parameters to generate number for unposted transaction. If blank, use auto tran no',
    'col_head'   : 'Auto temp no?',
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
    'col_name'   : 'auto_inv_no',
    'data_type'  : 'JSON',
    'short_descr': 'Auto-generate invoice no?',
    'long_descr' : 'Parameters to generate invoice number. If blank, manual input',
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
    'col_name'   : 'auto_crn_no',
    'data_type'  : 'JSON',
    'short_descr': 'Auto-generate cr note no?',
    'long_descr' : 'Parameters to generate credit note number. If blank, manual input',
    'col_head'   : 'Auto crn no?',
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
    'col_name'   : 'auto_jnl_no',
    'data_type'  : 'JSON',
    'short_descr': 'Auto-generate journal no?',
    'long_descr' : 'Parameters to generate journal number. If blank, manual input',
    'col_head'   : 'Auto jnl no?',
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
    'col_name'   : 'discount_code_id',
    'data_type'  : 'INT',
    'short_descr': 'Discount code row id',
    'long_descr' : 'Discount code row id. If blank, no discount allowed',
    'col_head'   : 'Disc code',
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
    'fkey'       : ['sls_nsls_codes', 'row_id', 'discount_code', 'nsls_code', False, 'nsls_codes'],
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'auto_disc_no',
    'data_type'  : 'JSON',
    'short_descr': 'Auto-generate discount no',
    'long_descr' : 'Parameters to generate discount c/note number. If blank, no discount allowed',
    'col_head'   : 'Auto disc no',
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
    'col_name'   : 'separate_stat_close',
    'data_type'  : 'BOOL',
    'short_descr': 'Separate date for statements?',
    'long_descr' : 'Separate closing dates for statements and period end?',
    'col_head'   : 'Stmt close',
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
    # 1=last day of month [1, None]
    # 2=fixed day per month [2, dd] check dd <= 28
    # 3=last weekday of month [3, 0-6, min_days_to_end]
    # 4=manual input [4, None]
    'col_name'   : 'stmt_date',
    'data_type'  : 'JSON',
    'short_descr': 'Statement date parameter',
    'long_descr' : 'Statement date parameter. Only applies if separate_stat_close is True',
    'col_head'   : 'Stmt date',
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
    'col_name'   : 'separate_stat_cust',
    'data_type'  : 'BOOL',
    'short_descr': 'Statement date per customer?',
    'long_descr' : 'Separate statement date per customer? Only applies if separate_stat_close is True',
    'col_head'   : 'Stmt cust',
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

# virtual column definitions
virt = []
virt.append ({
    'col_name'   : 'module_id',
    'data_type'  : 'TEXT',
    'short_descr': 'Module',
    'long_descr' : 'Module id',
    'col_head'   : '',
    'sql'        : "'ar'",
    })
virt.append ({
    'col_name'   : 'module_row_id',
    'data_type'  : 'INT',
    'short_descr': 'Module row id',
    'long_descr' : 'Module row id',
    'col_head'   : '',
    'sql'        : "SELECT b.row_id FROM {company}.db_modules b WHERE b.module_id = 'ar'",
    })

# cursor definitions
cursors = []
cursors.append({
    'cursor_name': 'ar_ledg',
    'title': 'Maintain ar ledger params',
    'columns': [
        ['ledger_id', 100, False, False, False, False, None, None, None, None],
        ['descr', 260, True, False, False, False, None, None, None, None],
        ],
    'filter': [],
    'sequence': [['ledger_id', False]],
    'formview_name': 'ar_params',
    })

# actions
actions = []
actions.append([
    'upd_checks', [
        [
            'disc_params',
            'Must set up auto discount number',
            [
                ['check', '', 'discount_code_id', 'is', '$None', ''],
                ['or', '', 'auto_disc_no', 'is not', '$None', ''],
                ],
            ],
        ],
    ])
actions.append([
    'after_insert', '<pyfunc name="db.cache.ledger_inserted"/>'
    ])
actions.append([
    'after_commit', '<pyfunc name="db.cache.ledger_updated"/>'
    ])
