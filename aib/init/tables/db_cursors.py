from lxml import etree

# table definition
table = {
    'table_name'    : 'db_cursors',
    'group_code'    : 'db',
    'short_descr'   : 'Cursor definitions',
    'long_descr'    : 'Database cursor definitions',
    'audit_trail'   : False,
    'table_created' : True,
    'default_cursor': None,
    'setup_form'    : None,
    'upd_chks'      : None,
    'del_chks'      : None,
    'table_hooks'   : None,
    'defn_company'  : None,
    'data_company'  : None,
    'read_only'     : False,
    }

# column definitions
cols = []
cols.append ({
    'col_name'   : 'table_id',
    'data_type'  : 'INT',
    'short_descr': 'Table id',
    'long_descr' : 'Table id',
    'col_head'   : 'Table',
    'key_field'  : 'Y',
    'generated'  : False,
    'allow_null' : False,
    'allow_amend': False,
    'max_len'    : 0,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : None,
    'col_chks'   : None,
    'fkey'       : ['db_tables', 'row_id', 'table_name', 'table_name', True],
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'cursor_name',
    'data_type'  : 'TEXT',
    'short_descr': 'Cursor name',
    'long_descr' : 'Cursor name',
    'col_head'   : 'Cursor',
    'key_field'  : 'Y',
    'generated'  : False,
    'allow_null' : False,
    'allow_amend': False,
    'max_len'    : 0,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : None,
    'col_chks'   : None,
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
    'generated'  : False,
    'allow_null' : False,
    'allow_amend': True,
    'max_len'    : 30,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : None,
    'col_chks'   : None,
    'fkey'       : None,
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'columns',
    'data_type'  : 'JSON',
    'short_descr': 'Columns',
    'long_descr' : 'Columns',
    'col_head'   : 'Columns',
    'key_field'  : 'N',
    'generated'  : False,
    'allow_null' : False,
    'allow_amend': True,
    'max_len'    : 0,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : None,
    'col_chks'   : None,
    'fkey'       : None,
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'filter',
    'data_type'  : 'JSON',
    'short_descr': 'Filter',
    'long_descr' : 'Filter',
    'col_head'   : 'Filter',
    'key_field'  : 'N',
    'generated'  : False,
    'allow_null' : False,
    'allow_amend': True,
    'max_len'    : 0,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : None,
    'col_chks'   : None,
    'fkey'       : None,
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'sequence',
    'data_type'  : 'JSON',
    'short_descr': 'Sequence',
    'long_descr' : 'Sequence',
    'col_head'   : 'Sequence',
    'key_field'  : 'N',
    'generated'  : False,
    'allow_null' : False,
    'allow_amend': True,
    'max_len'    : 0,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : None,
    'col_chks'   : None,
    'fkey'       : None,
    'choices'    : None,
    })

# virtual column definitions
virt = []

# cursor definitions
cursors = []
