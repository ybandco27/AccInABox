# table definition
table = {
    'table_name'    : 'pch_npch_crntax',
    'module_id'     : 'pch',
    'short_descr'   : 'Pch tax on non_inv crn items',
    'long_descr'    : 'Purchase tax on non-inventory credit note items',
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
    'col_name'   : 'npch_row_id',
    'data_type'  : 'INT',
    'short_descr': 'Npch row id',
    'long_descr' : 'Npch row id',
    'col_head'   : 'Npch row id',
    'key_field'  : 'A',
    'calculated' : False,
    'allow_null' : False,
    'allow_amend': False,
    'max_len'    : 0,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : None,
    'dflt_rule'  : None,
    'col_checks' : None,
    'fkey'       : ['pch_npch_subcrn', 'row_id', None, None, True, None],
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'tax_code_id',
    'data_type'  : 'INT',
    'short_descr': 'Tax code id',
    'long_descr' : 'Tax code id',
    'col_head'   : 'Tax code',
    'key_field'  : 'A',
    'calculated' : False,
    'allow_null' : False,
    'allow_amend': False,
    'max_len'    : 0,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : None,
    'dflt_rule'  : None,
    'col_checks' : None,
    'fkey'       : ['adm_tax_codes', 'row_id', 'tax_cat, tax_code', 'tax_cat, tax_code', False, None],
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'tax_rate',
    'data_type'  : 'DEC',
    'short_descr': 'Tax rate',
    'long_descr' : 'Tax rate as at transaction date',
    'col_head'   : 'Tax rate',
    'key_field'  : 'N',
    'calculated' : False,
    'allow_null' : False,
    'allow_amend': False,
    'max_len'    : 0,
    'db_scale'   : 2,
    'scale_ptr'  : 'tax_code_id>scale',
    'dflt_val'   : None,
    'dflt_rule'  : None,
    'col_checks' : None,
    'fkey'       : None,
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'tax_amt',
    'data_type'  : 'DEC',
    'short_descr': 'Tax amount',
    'long_descr' : 'Tax amount in transaction currency',
    'col_head'   : 'Tax amt',
    'key_field'  : 'N',
    'calculated' : False,
    'allow_null' : False,
    'allow_amend': False,
    'max_len'    : 0,
    'db_scale'   : 2,
    'scale_ptr'  : 'npch_row_id>tran_det_row_id>tran_row_id>currency_id>scale',
    'dflt_val'   : '0',
    'dflt_rule'  : None,
    'col_checks' : None,
    'fkey'       : None,
    'choices'    : None,
    })

# virtual column definitions
virt = []
virt.append ({
    'col_name'   : 'posted',
    'data_type'  : 'BOOL',
    'short_descr': 'Posted?',
    'long_descr' : 'Has transaction been posted?',
    'col_head'   : 'Posted?',
    'dflt_val'   : '{npch_row_id>tran_det_row_id>tran_row_id>posted}',
    'sql'        : "a.npch_row_id>tran_det_row_id>tran_row_id>posted"
    })
virt.append ({
    'col_name'   : 'tax_local',
    'data_type'  : 'DEC',
    'short_descr': 'Tax local',
    'long_descr' : 'Tax amount in local currency',
    'col_head'   : 'Tax local',
    'db_scale'   : 2,
    'scale_ptr'  : '_param.local_curr_id>scale',
    'dflt_val'   : '0',
    'dflt_rule'  : (
        '<expr>'
          '<fld_val name="tax_amt"/>'
          '<op type="/"/>'
          '<fld_val name="npch_row_id>tran_det_row_id>tran_row_id>tran_exch_rate"/>'
        '</expr>'
        ),
    'sql'        : (
        "a.tax_amt / a.npch_row_id>tran_det_row_id>tran_row_id>tran_exch_rate"
        ),
    })

# cursor definitions
cursors = []

# actions
actions = []
actions.append([
    'upd_on_post', [
        [
            'pch_tax_totals',  # table name
            None,  # condition
            False,  # split source?
            [  # key fields
                ['tax_code_id', 'tax_code_id'],  # tgt_col, src_col
                ['tran_date', 'npch_row_id>tran_det_row_id>tran_row_id>tran_date'],
                ],
            [  # aggregation
                ['npch_crn_net_day', '-', 'npch_row_id>net_local'],
                ['npch_crn_tax_day', '-', 'tax_local'],
                ['npch_crn_net_tot', '-', 'npch_row_id>net_local'],
                ['npch_crn_tax_tot', '-', 'tax_local'],
                ],
            [],  # on post
            [],  # on unpost
            ],
        ],
    ])
