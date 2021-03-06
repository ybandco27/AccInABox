# table definition
table = {
    'table_name'    : 'adm_params',
    'module_id'     : 'adm',
    'short_descr'   : 'Company parameters',
    'long_descr'    : 'Company parameters',
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
    'col_name'   : 'company_id',
    'data_type'  : 'TEXT',
    'short_descr': 'Company id',
    'long_descr' : 'Company id',
    'col_head'   : 'Company',
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
    'fkey'       : None,
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'company_name',
    'data_type'  : 'TEXT',
    'short_descr': 'Company name',
    'long_descr' : 'Company name',
    'col_head'   : 'Name',
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
    'col_name'   : 'local_curr_id',
    'data_type'  : 'INT',
    'short_descr': 'Local currency id',
    'long_descr' : 'Local currency id',
    'col_head'   : 'Local currency',
    'key_field'  : 'N',
    'calculated' : False,
    'allow_null' : True,
    'allow_amend': True,  # should be False, but need to set up - ask for local curr on creation??
    'max_len'    : 0,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : None,
    'dflt_rule'  : None,
    'col_checks' : None,
    'fkey'       : ['adm_currencies', 'row_id', 'local_currency', 'currency', False, 'curr'],
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'use_locations',
    'data_type'  : 'BOOL',
    'short_descr': 'Allow use of locations?',
    'long_descr' : 'Allow use of locations?',
    'col_head'   : 'Use locations?',
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
    'col_name'   : 'loc_levels',
    'data_type'  : 'JSON',
    'short_descr': 'Fixed levels for locations',
    'long_descr' : 'Fixed levels for locations. List of (code, descr, allow_split). If blank, free format.',
    'col_head'   : 'Loc levels',
    'key_field'  : 'N',
    'calculated' : [['where', '', 'use_locations', 'is', '$False', '']],
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
    'col_name'   : 'use_functions',
    'data_type'  : 'BOOL',
    'short_descr': 'Allow use of functions?',
    'long_descr' : 'Allow use of functions?',
    'col_head'   : 'Use functions?',
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
    'col_name'   : 'fun_levels',
    'data_type'  : 'JSON',
    'short_descr': 'Fixed levels for functions',
    'long_descr' : 'Fixed levels for functions. List of (code, descr, allow_split). If blank, free format.',
    'col_head'   : 'Fun levels',
    'key_field'  : 'N',
    'calculated' : [['where', '', 'use_functions', 'is', '$False', '']],
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
    'col_name'   : 'auto_party_id',
    'data_type'  : 'JSON',
    'short_descr': 'Auto-generate party id?',
    'long_descr' : 'Parameters to generate party id. If blank, manual input',
    'col_head'   : 'Auto party id?',
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
# 1=last day of month [1, None]
# 2=fixed day per month [2, dd] check dd <= 28
# 3=last weekday of month [3, 0-6, min_days_to_end]
cols.append ({
    'col_name'   : 'period_end_gl',
    'data_type'  : 'JSON',
    'short_descr': 'Period end parameter - gl',
    'long_descr' : 'Period end parameter - gl module',
    'col_head'   : 'Per end gl',
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
    'col_name'   : 'eff_date_nsls',
    'data_type'  : 'BOOL',
    'short_descr': 'Change effective date - nsls?',
    'long_descr' : 'Allow change of effective date - non-inventory sales?',
    'col_head'   : 'Eff date nsls',
    'key_field'  : 'N',
    'calculated' : False,
    'allow_null' : True,
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
    'col_name'   : 'eff_date_npch',
    'data_type'  : 'BOOL',
    'short_descr': 'Change effective date - npch?',
    'long_descr' : 'Allow change of effective date - non-inventory purchases?',
    'col_head'   : 'Eff date npch',
    'key_field'  : 'N',
    'calculated' : False,
    'allow_null' : True,
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
    'col_name'   : 'allow_alloc_rec',
    'data_type'  : 'BOOL',
    'short_descr': 'Allow receipt allocation?',
    'long_descr' : 'Allow receipt allocation while entering receipt?',
    'col_head'   : 'Allow alloc?',
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

# virtual column definitions
virt = []
virt.append ({
    'col_name'   : 'location_row_id',
    'data_type'  : 'INT',
    'short_descr': 'Location',
    'long_descr' : 'Return location row id if there is only one, else None',
    'col_head'   : 'Loc',
    'sql'        : (
        "CASE "
            "WHEN (SELECT COUNT(*) FROM {company}.adm_locations "
                "WHERE deleted_id = 0) = 1 THEN "
                "(SELECT row_id FROM {company}.adm_locations WHERE deleted_id = 0) "
        "END"
        ),
    })
virt.append ({
    'col_name'   : 'loc_root_row_id',
    'data_type'  : 'INT',
    'short_descr': 'Row id of loc root element',
    'long_descr' : 'Row id of root element for adm_locations',
    'col_head'   : '',
    'sql'        : (
        "SELECT row_id FROM {company}.adm_locations "
        "WHERE parent_id IS NULL AND deleted_id = 0"
        ),
    })
virt.append ({
    'col_name'   : 'function_row_id',
    'data_type'  : 'INT',
    'short_descr': 'Function',
    'long_descr' : 'Return function row id if there is only one, else None',
    'col_head'   : 'Fun',
    'sql'        : (
        "CASE "
            "WHEN (SELECT COUNT(*) FROM {company}.adm_functions "
                "WHERE deleted_id = 0) = 1 THEN "
                "(SELECT row_id FROM {company}.adm_functions WHERE deleted_id = 0) "
        "END"
        ),
    })
virt.append ({
    'col_name'   : 'fun_root_row_id',
    'data_type'  : 'INT',
    'short_descr': 'Row id of fun root element',
    'long_descr' : 'Row id of root element for adm_functions',
    'col_head'   : '',
    'sql'        : (
        "SELECT row_id FROM {company}.adm_functions "
        "WHERE parent_id IS NULL AND deleted_id = 0"
        ),
    })
virt.append ({
    'col_name'   : 'currency_id',
    'data_type'  : 'INT',
    'short_descr': 'Currency',
    'long_descr' : 'Return currency id if there is only one, else None',
    'col_head'   : 'Curr',
    'sql'        : (
        "CASE "
            "WHEN (SELECT COUNT(*) FROM {company}.adm_currencies "
                "WHERE deleted_id = 0) = 1 THEN "
                "(SELECT row_id FROM {company}.adm_currencies WHERE deleted_id = 0) "
        "END"
        ),
    })
virt.append ({
    'col_name'   : 'ar_ledger_id',
    'data_type'  : 'INT',
    'short_descr': 'Ar ledger',
    'long_descr' : 'Return ar ledger id if there is only one, else None',
    'col_head'   : 'Ar ledger',
    'sql'        : (
        "CASE "
            "WHEN (SELECT COUNT(*) FROM {company}.ar_ledger_params "
                "WHERE deleted_id = 0) = 1 THEN "
                "(SELECT row_id FROM {company}.ar_ledger_params WHERE deleted_id = 0) "
        "END"
        ),
    })
virt.append ({
    'col_name'   : 'ap_ledger_id',
    'data_type'  : 'INT',
    'short_descr': 'Ap ledger',
    'long_descr' : 'Return ap ledger id if there is only one, else None',
    'col_head'   : 'Ap ledger',
    'sql'        : (
        "CASE "
            "WHEN (SELECT COUNT(*) FROM {company}.ap_ledger_params "
                "WHERE deleted_id = 0) = 1 THEN "
                "(SELECT row_id FROM {company}.ap_ledger_params WHERE deleted_id = 0) "
        "END"
        ),
    })
virt.append ({
    'col_name'   : 'in_ledger_id',
    'data_type'  : 'INT',
    'short_descr': 'In ledger',
    'long_descr' : 'Return in ledger id if there is only one, else None',
    'col_head'   : 'In ledger',
    'sql'        : (
        "CASE "
            "WHEN (SELECT COUNT(*) FROM {company}.in_ledger_params "
                "WHERE deleted_id = 0) = 1 THEN "
                "(SELECT row_id FROM {company}.in_ledger_params WHERE deleted_id = 0) "
        "END"
        ),
    })
virt.append ({
    'col_name'   : 'cb_ledger_id',
    'data_type'  : 'INT',
    'short_descr': 'Cb ledger',
    'long_descr' : 'Return cb ledger id if there is only one, else None',
    'col_head'   : 'Cb ledger',
    'sql'        : (
        "CASE "
            "WHEN (SELECT COUNT(*) FROM {company}.cb_ledger_params "
                "WHERE deleted_id = 0) = 1 THEN "
                "(SELECT row_id FROM {company}.cb_ledger_params WHERE deleted_id = 0) "
        "END"
        ),
    })
virt.append ({
    'col_name'   : 'tax_cat_id',
    'data_type'  : 'INT',
    'short_descr': 'Tax category',
    'long_descr' : 'Return sales tax category id if there is only one, else None',
    'col_head'   : 'Tax cat',
    'sql'        : (
        "CASE "
            "WHEN (SELECT COUNT(*) FROM {company}.adm_tax_cats "
                "WHERE deleted_id = 0) = 1 THEN "
                "(SELECT row_id FROM {company}.adm_tax_cats WHERE deleted_id = 0) "
        "END"
        ),
    })

# cursor definitions
cursors = []

# actions
actions = []
actions.append([
    'after_commit', '<pyfunc name="db.cache.param_updated"/>'
    ])
