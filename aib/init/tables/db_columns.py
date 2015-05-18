from lxml import etree

# table definition
table = {
    'table_name'    : 'db_columns',
    'group_code'    : 'db',
    'short_descr'   : 'Db columns',
    'long_descr'    : 'Database column definitions',
    'audit_trail'   : True,
    'table_created' : True,
    'default_cursor': None,
    'setup_form'    : None,
    'upd_chks'      : None,
    'del_chks'      : None,
    'table_hooks'   : etree.fromstring(
        '<hooks>'
            '<hook type="after_save"><setup_disp_name/></hook>'
            '<hook type="after_insert">'
                '<case>'
                    '<compare src="col_type" op="eq" tgt="user">'
                        '<add_column/>'
                    '</compare>'
                '</case>'
            '</hook>'
        '</hooks>'
        ),
    'sequence'      : ['seq', ['table_id', 'col_type'], None],
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
    'generated'  : True,
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
    'col_name'   : 'created_id',
    'data_type'  : 'INT',
    'short_descr': 'Created id',
    'long_descr' : 'Created row id',
    'col_head'   : 'Created',
    'key_field'  : 'N',
    'generated'  : True,
    'allow_null' : False,
    'allow_amend': True,
    'max_len'    : 0,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : '0',
    'col_chks'   : None,
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
    'generated'  : True,
    'allow_null' : False,
    'allow_amend': True,
    'max_len'    : 0,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : '0',
    'col_chks'   : None,
    'fkey'       : None,
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'table_id',
    'data_type'  : 'INT',
    'short_descr': 'Table id',
    'long_descr' : 'Table id',
    'col_head'   : 'Table',
    'key_field'  : 'A',
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
    'col_name'   : 'col_name',
    'data_type'  : 'TEXT',
    'short_descr': 'Column name',
    'long_descr' : 'Column name',
    'col_head'   : 'Column',
    'key_field'  : 'A',
    'generated'  : False,
    'allow_null' : False,
    'allow_amend': False,
    'max_len'    : 15,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : None,
    'col_chks'   : None,
    'fkey'       : None,
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'col_type',
    'data_type'  : 'TEXT',
    'short_descr': 'Column type',
    'long_descr' : 'Column type',
    'col_head'   : 'Col type',
    'key_field'  : 'N',
    'generated'  : False,
    'allow_null' : False,
    'allow_amend': False,
    'max_len'    : 5,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : None,
    'col_chks'   : None,
    'fkey'       : None,
    'choices'    : [
        False,  # use sub_types?
        False,  # use display_names?
        [
            ['sys', 'System column', [], []],
            ['virt', 'Virtual column', [], []],
            ['user', 'User-defined column', [], []],
            ]
        ],
    })
cols.append ({
    'col_name'   : 'seq',
    'data_type'  : 'INT',
    'short_descr': 'Seq',
    'long_descr' : 'Position for display',
    'col_head'   : 'Seq',
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
    'col_name'   : 'data_type',
    'data_type'  : 'TEXT',
    'short_descr': 'Data type',
    'long_descr' : 'Data type',
    'col_head'   : 'Type',
    'key_field'  : 'N',
    'generated'  : False,
    'allow_null' : False,
    'allow_amend': False,
    'max_len'    : 5,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : None,
    'col_chks'   : None,
    'fkey'       : None,
    'choices'    : [
        False,   # use sub_types?
        False,  # use display_names?
        [
            ['TEXT', 'Text', [], []],
            ['INT', 'Integer', [], []],
            ['DEC', 'Decimal', [], []],
            ['DTE', 'Date', [], []],
            ['DTM', 'Date-time', [], []],
            ['BOOL', 'True/False', [], []],
            ['AUTO', 'Auto-generated key', [], []],
            ['JSON', 'Json', [], []],
            ['XML', 'Xml', [], []],
            ['FXML', 'Form definition', [], []],
            ['PXML', 'Process definition', [], []],
            ]
        ],
    })
cols.append ({
    'col_name'   : 'short_descr',
    'data_type'  : 'TEXT',
    'short_descr': 'Short description',
    'long_descr' : 'Column description',
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
    'col_name'   : 'long_descr',
    'data_type'  : 'TEXT',
    'short_descr': 'Long description',
    'long_descr' : 'Full description for user manual, tool-tip, etc',
    'col_head'   : 'Long description',
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
    'col_name'   : 'col_head',
    'data_type'  : 'TEXT',
    'short_descr': 'Column heading',
    'long_descr' : 'Column heading for reports and grids',
    'col_head'   : 'Col head',
    'key_field'  : 'N',
    'generated'  : False,
    'allow_null' : True,
    'allow_amend': True,
    'max_len'    : 15,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : None,
    'col_chks'   : None,
    'fkey'       : None,
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'key_field',
    'data_type'  : 'TEXT',
    'short_descr': 'Key field',
    'long_descr' : 'Yes=primary key, Alt=alternate key, No=not key field',
    'col_head'   : 'Key?',
    'key_field'  : 'N',
    'generated'  : False,
    'allow_null' : False,
    'allow_amend': False,
    'max_len'    : 1,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : None,
    'col_chks'   : None,
    'fkey'       : None,
    'choices'    : [
        False,  # use sub_types?
        False,  # use display_names?
        [
            ['N', 'No', [], []],
            ['Y', 'Yes', [], []],
            ['A', 'Alt', [], []],
            ]
        ],
    })
cols.append ({
    'col_name'   : 'generated',
    'data_type'  : 'BOOL',
    'short_descr': 'Ganerated?',
    'long_descr' : 'Is value generated programatically?',
    'col_head'   : 'Generated?',
    'key_field'  : 'N',
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
    'col_name'   : 'allow_null',
    'data_type'  : 'BOOL',
    'short_descr': 'Allow null?',
    'long_descr' : 'Allow column to contain null?',
    'col_head'   : 'Null?',
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
    'col_name'   : 'allow_amend',
    'data_type'  : 'BOOL',
    'short_descr': 'Allow amendment?',
    'long_descr' : 'Allow column to be amended?',
    'col_head'   : 'Amend?',
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
    'col_name'   : 'max_len',
    'data_type'  : 'INT',
    'short_descr': 'Maximum length',
    'long_descr' : 'Maximum length for text field',
    'col_head'   : 'Max len',
    'key_field'  : 'N',
    'generated'  : False,
    'allow_null' : False,
    'allow_amend': True,
    'max_len'    : 0,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : '0',
    'col_chks'   : None,
    'fkey'       : None,
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'db_scale',
    'data_type'  : 'INT',
    'short_descr': 'Decimal places in database',
    'long_descr' : 'Number of decimal places as defined in database',
    'col_head'   : 'Db scale',
    'key_field'  : 'N',
    'generated'  : False,
    'allow_null' : False,
    'allow_amend': False,
    'max_len'    : 0,
    'db_scale'   : 0,
    'scale_ptr'  : None,
    'dflt_val'   : '0',
    'col_chks'   : None,
    'fkey'       : None,
    'choices'    : None,
    })
cols.append ({
    'col_name'   : 'scale_ptr',
    'data_type'  : 'TEXT',
    'short_descr': 'Parameter for number of decimals',
    'long_descr' : 'Virtual column to return number of decimals allowed',
    'col_head'   : 'Scale ptr',
    'key_field'  : 'N',
    'generated'  : False,
    'allow_null' : True,
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
    'col_name'   : 'dflt_val',
    'data_type'  : 'TEXT',
    'short_descr': 'Default deinition',
    'long_descr' : 'Default definition',
    'col_head'   : 'Default',
    'key_field'  : 'N',
    'generated'  : False,
    'allow_null' : True,
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
    'col_name'   : 'col_chks',
    'data_type'  : 'JSON',
    'short_descr': 'Column checks',
    'long_descr' : 'Column checks',
    'col_head'   : 'Checks',
    'key_field'  : 'N',
    'generated'  : False,
    'allow_null' : True,
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
    'col_name'   : 'fkey',
    'data_type'  : 'JSON',
    'short_descr': 'Foreign key',
    'long_descr' : 'Foreign key',
    'col_head'   : 'Fkey',
    'key_field'  : 'N',
    'generated'  : False,
    'allow_null' : True,
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
    'col_name'   : 'choices',
    'data_type'  : 'JSON',
    'short_descr': 'Choices',
    'long_descr' : 'List of valid choices',
    'col_head'   : 'Choices',
    'key_field'  : 'N',
    'generated'  : False,
    'allow_null' : True,
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
    'col_name'   : 'sql',
    'data_type'  : 'TEXT',
    'short_descr': 'Sql statement',
    'long_descr' : 'Sql statement to return value',
    'col_head'   : 'Sql',
    'key_field'  : 'N',
    'generated'  : False,
    'allow_null' : True,
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
