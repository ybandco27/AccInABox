import os.path
import __main__
schema_path = os.path.join(os.path.dirname(__main__.__file__), 'schemas')

from copy import deepcopy
from lxml import etree
import gzip
from decimal import Decimal as D, ROUND_HALF_UP, Context, DecimalException, Inexact
from datetime import date as dt, datetime as dtm, timedelta as td
import weakref
from weakref import WeakKeyDictionary as WKD
from json import loads, dumps
from hashlib import pbkdf2_hmac as kdf
from secrets import token_bytes
import operator

import logging
logger = logging.getLogger(__name__)

import db.objects
from db.chk_constraints import chk_constraint, eval_expr
import db.cache
import db.dflt_xml
import ht
from ht.validation_xml import check_vld

from common import AibError, AibDenied

# db_fkeys columns
(FK_TARGET_TABLE
,FK_TARGET_COLUMN
,FK_ALT_SOURCE
,FK_ALT_TARGET
,FK_CHILD
,FK_CURSOR
,FK_IS_ALT
) = range(7)

blank = object()  # placeholder in value_changed() - None is a valid argument

#-----------------------------------------------------------------------------

class ComplexFkey(list):
    """
    ComplexFkey is a 2-part list
    The first element is the column name that determines which fkey to use
    The second element is a dictionary keyed on the possible column values
    Each 'value' of the dictionary is another dictionary representing the actual fkey
    If the dictionary is empty, the fkey has not been set up, else it has
    We subclass 'list' and over-ride __bool__() to provide the correct response to
            if foreign_key:
    """
    def __bool__(self):
        col_name, vals_fkeys = self
        for val in vals_fkeys:
            if vals_fkeys[val]:
                return True  # at least one foreign_key has been set up
        return False  # no foreign keys have been set up

#-----------------------------------------------------------------------------

class Field:
    async def _ainit_(self, db_obj, col_defn):

        # print(f'init {col_defn.table_name}.{col_defn.col_name}')

        self.db_obj = db_obj
        self.col_defn = col_defn
        self.table_id = col_defn.table_id
        self.table_name = col_defn.table_name
        self.col_name = col_defn.col_name
        # self.gui_obj = weakref.WeakSet()  # []  # gui_objects to be notified of changes
        self.gui_obj = ()  # gui_objects to be notified of changes
        self.gui_subtype = WKD()  # if set by form, notify gui on change
        self.flds_to_recalc = ()  # change to WeakSet if any exist
        self.sequence = False  # if over-ridden in db.objects._ainit(), display as seq+1
        self.fkey_parent = None

        self.ledger_col = (self.col_name == db_obj.db_table.ledger_col)
        self.ledger_vld = (db_obj.db_table.ledger_col is not None and
            self.col_name == db_obj.db_table.ledger_col.split('>')[0])

        self.must_be_evaluated = False  # if set to True, recalc on getval, then reset to False

        self.children = []  # list of xrefs to child fkey fields
        self.table_keys = []  # populated if this is a key field
        self.constant = None  # can be over-ridden in db.objects after fields set up

        if col_defn.calculated in (True, False):
            self._calculated = col_defn.calculated
        else:
            self._calculated = None  # will be evaluated in self.calculated()

        self.getval = self._getval  # on getval(), call _getval() which returns value immediately
                                    # but see next block - can be over-ridden

        if col_defn.fkey is None:
            self.foreign_key = None
        else:
            self.foreign_key = {}  # un-initialised foreign key
            if db_obj.parent is None:
                child_obj = False
            elif db_obj.parent[0] != self.col_name:  # e.g. dir_users_companies.company_id
                child_obj = False
            else:
                child_obj = True
            # if not child_obj:  # else fkey will be set up in db.objects()
            if col_defn.fkey[FK_IS_ALT]:
                self.getval = self._getval_fkey  # on getval(), set up fkey before calling _getval()

        self._value_ = None  # used by 'property' for '_value' - see at end
        self._value = await self.get_dflt(from_init=True)  # eval dflt_val, but not dflt_rule
        self._orig = self._value
        self._prev = None

        """
        Add attributes for 'auth_userid' and 'auth_datetime'.
        For every 'setval', compare 'userid' with 'orig_userid'.
        If different, supervisor has overridden permissions,
        so these attributes must be updated.
        Still have to decide where to store this info in database.
        Must be reset on every init(), restore(), etc.
        Also reset if second 'setval' passes without permission problem.

        Maybe, maybe not.
        If a task definition has a 'business rule' which, on failure,
        invokes an 'authorisation' task, the above attributes
        become 'task data', not 'field data' (or something ...).

        If it is decided that this must be stored in the database for
        future retrieval, then the first paragraph above applies.
        If it is decided that the data should be stored as part of the
        'task instance' only, then the second paragraph applies.

        [26/03/2013]
        Assume we need to store it in the database.
        Possible solution - 
        
        CREATE TABLE {table_name}_audit_override
            row_id SERIAL
            data_row_id INT REFERENCES {table_name}
            data_col_name TEXT
            data_col_value TEXT {string value?}
            user_row_id INT
            user_role_id INT (possibly)
            date_time {)
        """

    async def setup_foreign_key(self):
        fkey = self.col_defn.fkey
        if fkey is None:
            # errmsg = '{}.{}: foreign key does not exist'.format(
            #     self.table_name, self.col_name)
            errmsg = f'{self.table_name}.{self.col_name}: foreign key does not exist'
            raise AibError(head=self.table_name, body=errmsg)

        tgt_table_name = fkey[FK_TARGET_TABLE]
        tgt_col_name = fkey[FK_TARGET_COLUMN]
        altsrc_name = fkey[FK_ALT_SOURCE]
        alttgt_name = fkey[FK_ALT_TARGET]
        is_alt = fkey[FK_IS_ALT]

        if isinstance(tgt_table_name, str):
            self.foreign_key = await self.setup_fkey(
                tgt_table_name, tgt_col_name, altsrc_name, alttgt_name, is_alt)
        else:
            # e.g. ar_openitems has the following tgt_table_name -
            #   ['tran_type', [
            #       ['ar_inv', 'ar_tran_inv'],
            #       ['ar_crn', 'ar_tran_crn'],
            #       ['ar_rec', 'ar_tran_rec'],
            #       ]]
            # create foreign_key like this -
            #   ['tran_type', {
            #       'ar_inv': {'tgt_field': ar_tran_inv.row_id, 'alt_src': None, 'true_src': None},
            #       'ar_crn': {'tgt_field': ar_tran_crn.row_id, 'alt_src': None, 'true_src': None},
            #       'ar_rec': {'tgt_field': ar_tran_rec.row_id, 'alt_src': None, 'true_src': None},
            #       }]
            col_name, vals_tblnames = tgt_table_name
            self.foreign_key = ComplexFkey()
            self.foreign_key.append(col_name)
            fkeys = {}
            self.foreign_key.append(fkeys)
            for val, tbl_name in vals_tblnames:
                fkeys[val] = {}
        # self.getval = self._getval

    async def setup_fkey(self, tgt_table_name, tgt_col_name, altsrc_name, alttgt_name, is_alt):
        foreign_key = {}

        if is_alt:
            true_src = self.db_obj.fields[altsrc_name]
            # if true_src.foreign_key == {}:
            #     await true_src.setup_foreign_key()

            true_foreign_key = await self.db_obj.get_foreign_key(true_src)

            # tgt_obj = true_src.foreign_key['tgt_field'].db_obj
            tgt_obj = true_foreign_key['tgt_field'].db_obj

            tgt_val = await true_src.getval()
            if tgt_val is not None:
                # true_tgt = true_src.foreign_key['tgt_field']
                true_tgt = true_foreign_key['tgt_field']
                await true_tgt.setval(tgt_val, validate=False)

            tgt_field = tgt_obj.fields[tgt_col_name]
            foreign_key['tgt_field'] = tgt_field
            foreign_key['true_src'] = true_src
            foreign_key['alt_src'] = []  # only used if this *has* an alt
            # true_src.foreign_key['alt_src'].append(self)
            true_foreign_key['alt_src'].append(self)
            self._value = await tgt_field.getval()
            return foreign_key

        if '>' in tgt_table_name:
            # in setup_form, we create and populate two in-memory tables, obj_names
            #   and col_names - col_names is a child of obj_names
            # in setup_form_body, we have two fields - obj_name and col_name
            # obj_name has fkey of ['{mem}.obj_names', 'name', None, None, False, None]
            # col_name has fkey of ['obj_name>{mem}.col_names', 'name', None, None, False, None]
            # if user calls a lkup on col_names, we need a way to tell it that its parent
            #   is obj_names, so that it only displays col_names belonging to that obj_name
            # this is a rather complicated way of achieving that
            parent_name, tgt_table_name = tgt_table_name.split('>')
            parent_fld = await self.db_obj.getfld(parent_name)
            # if parent_fld.foreign_key == {}:
            #     await parent_fld.setup_foreign_key()
            parent_foreign_key = await parent_fld.db_obj.get_foreign_key(parent_fld)
            # parent_obj = parent_fld.foreign_key['tgt_field'].db_obj
            parent_obj = parent_foreign_key['tgt_field'].db_obj
        else:
            parent_obj = None

        if self.fkey_parent is not None:
            tgt_field = self.fkey_parent  # already set up - just use it
        else:
            if '.' in tgt_table_name:  # target table is in another company
                tgt_company, tgt_table_name = tgt_table_name.split('.')
            else:
                tgt_company = self.db_obj.company
            if tgt_company == '{mem}':
                tgt_object = await db.objects.get_mem_object(self.db_obj.context,
                    self.db_obj.company, tgt_table_name, parent=parent_obj)
            else:

                # check if tgt_object is a child of this object [added 2018-11-05]
                #   e.g. ar_tran_disc_det.subtran_row_id > pch_npch_subtran.tran_det_row_id
                # this example no longer applies [2019-01-23] - any other examples?

                tgt_table = await db.objects.get_db_table(self.db_obj.context,
                    tgt_company, tgt_table_name)
                if tgt_table.parent_params:

                    parent_obj = None
                    for parent_name, parent_pkey, child_fkey in tgt_table.parent_params:
                        if isinstance(parent_name, str):  # normal fkey
                            if '.' in parent_name:
                                parent_name = parent_name.split('.')[1]
                            if parent_name == self.table_name:
                                parent_obj = self.db_obj
                                break
                        else:
                            # e.g. this is the tgt_table part of the fkey for ar_openitems.tran_row_id
                            #  ['tran_type', [['ar_inv', 'ar_tran_inv'], ['ar_rec', 'ar_tran_rec']]]
                            col_name, vals_tgts = parent_name
                            for val, tgt in vals_tgts:
                                if tgt == self.table_name:
                                    parent_obj = self.db_obj
                                    break

                tgt_object = await db.objects.get_db_object(self.db_obj.context,
                    tgt_company, tgt_table_name, parent=parent_obj)

            tgt_field = await tgt_object.getfld(tgt_col_name)

        foreign_key['tgt_field'] = tgt_field
        foreign_key['true_src'] = None  # only used if this *is* an alt
        foreign_key['alt_src'] = []  # only used if this *has* an alt

        return foreign_key

    async def get_fk_object(self):
        if self.foreign_key == {}:  # not yet set up
            await self.setup_foreign_key()
        foreign_key = await self.db_obj.get_foreign_key(self)
        tgt_fld = foreign_key['tgt_field']
        # if await self.getval() is not None:
        value = await self.getval()
        if value is not None:
            if value != tgt_fld._value:  # set up fk object if applicable
                # await tgt_fld.db_obj.init()  # added 2017-10-08
                # await tgt_fld.setval(self._value)  # added 2016-11-08 - monitor
                await tgt_fld.db_obj.select_row(keys={tgt_fld.col_name: value}, display=False)
        return tgt_fld.db_obj

        # if isinstance(self.foreign_key, dict):
        #     return self.foreign_key['tgt_field'].db_obj
        # col_name, vals_fkeys = self.foreign_key
        # try:
        #     foreign_key = await vals_fkeys[self.db_obj.getval(col_name)]
        # except KeyError:
        #     errmsg = '{} not a valid value for {}'.format(
        #         await self.db_obj.getval(col_name), col_name)
        #     raise AibError(head=self.col_defn.short_descr, body=errmsg)
        # return foreign_key['tgt_field'].db_obj

    def notify_recalc(self, fld):
        # print('recalc {}.{} if {}.{} changes'.format(
        #     fld.table_name, fld.col_name,
        #     self.table_name,self.col_name))
        if self.flds_to_recalc == ():
            self.flds_to_recalc = weakref.WeakSet()
        self.flds_to_recalc.add(fld)

    async def recalc_orig(self):
        # called from db.objects.add_virtual()
        # used to set up _orig when initialising a virtual field

        if self.col_defn.dflt_rule is not None:
            orig_value = await db.dflt_xml.get_db_dflt(self, orig=True)
            # print('{}.{} {} -> {}'.format(self.table_name, self.col_name, self._value, dflt_value))
            if orig_value is not None:  # added 2016-04-17 - to be tested
                if orig_value != self._orig:
                    orig_value = await self.get_val_from_sql(orig_value)
                    self._orig = orig_value
                    for child in self.children:  # probably not required
                        child._orig = orig_value  # but does no harm

    async def recalc(self, display=False):
        if self.col_defn.dflt_val is not None:
            if self.col_defn.dflt_val.startswith('{'):  # get value from another field
                if self._value is None or await self.calculated():  # else do not
                    dflt_value = await self.db_obj.getval(self.col_defn.dflt_val[1:-1])
                    if dflt_value is not None:
                        if dflt_value != self._value:
                            await self.setval(dflt_value, display=display, validate=False)
                            # # must test for foreign_key [20018-11-03]
                            # # either set 'validate' to True, or set 'validate' to False and test separately
                            # await self.setval(dflt_value, display=display, validate=False)
                            # if self.foreign_key is not None:
                            #     if self.foreign_key == {}:  # not yet set up
                            #         await self.setup_foreign_key()
                            #     foreign_key = await self.db_obj.get_foreign_key(self)
                            #     tgt_field = foreign_key['tgt_field']
                            #     if tgt_field._value != self._value:
                            #         if self._value is None:
                            #             await tgt_field.db_obj.init()
                            #         else:
                            #             await tgt_field.read_row(self._value, display)
                            #     alt_src = foreign_key['alt_src']
                            #     for alt_src_fld in alt_src:
                            #         alt_src_fld._value = (
                            #             alt_src_fld.foreign_key['tgt_field']._value)
                            #         if display:
                            #             for obj in alt_src_fld.gui_obj:
                            #                 await obj._redisplay()

                return
            # else: pass  # do not recalc literal dflt_val - that is for init only (messy)

        if self.col_defn.dflt_rule is not None:
            dflt_value = await self.check_val(
                await db.dflt_xml.get_db_dflt(self)
                )
            if dflt_value is not None:  # added 2016-04-17 - to be tested
                if dflt_value != await self.getval():
                    await self.setval(dflt_value, display=display, validate=False)
            return

        # print(f'recalc {self.table_name}.{self.col_name}')

        sql = self.col_defn.sql.replace('{company}', self.db_obj.company)

        # if sql.startswith('['):
        #     end_join = sql.find(']')
        #     join = sql[1:end_join]
        #     sql = sql[end_join+1:]

        #     if join.startswith('('):
        #         lbr = rbr = 0  # find first lbr and matching rbr
        #         for pos, ch in enumerate(join):
        #             if ch == '(':
        #                 if not lbr:  # must be the first lbr
        #                     lbr = pos
        #                 rbr += 1
        #             elif ch == ')':
        #                 rbr -= 1
        #                 if not rbr:  # must be the matching rbr
        #                     rbr = pos
        #                     break

        #         prefix = join[:lbr]  # LEFT JOIN
        #         select = join[lbr:rbr+1]  # (SELECT ...)
        #         suffix = join[rbr+1:]  # alias ON ... = ...

        #     else:
 
        #         prefix = join[:10]  # LEFT JOIN
        #         select = ' (SELECT * FROM '
        #         suffix = join[10:] + ') ' + sql.split('.')[0] # alias ON ... = ...
        #         sql = sql.split('.')[1]  # extract col_name from table_name.col_name

        #     sql = 'SELECT {} FROM {} {}'.format(
        #         sql,
        #         select,
        #         suffix.replace(' ON ', ' WHERE ')
        #         )

        param_style = self.db_obj.db_table.constants.param_style
        param_pos = []
        params = []
        for dep in self.col_defn.sql_a_cols:
            fld = await self.db_obj.getfld(dep)
            col = 'a.{}'.format(dep)
            pos = sql.find(col)
            value = await fld.get_val_for_sql()
            if value is None:
                if sql[pos-2] == '=':  # assumes exactly one space - s/b ok, but no guarantee
                    if sql[pos-3] == '!':
                        sql = sql[:pos-3] + 'IS NOT NULL' + sql[pos+len(col):]
                    else:
                        sql = sql[:pos-2] + 'IS NULL' + sql[pos+len(col):]
                    continue
            sql = sql.replace(col, param_style, 1)
            pos_to_insert = len([x for x in param_pos if x < pos])  # can use 'bisect' here
            params.insert(pos_to_insert, value)
            param_pos.insert(pos_to_insert, pos)

        if self.col_defn.data_type == 'DEC':
            # # force sqlite3 to return Decimal type
            # pos = sql.find(' FROM')
            # if pos == -1:
            #     sql += ' AS "x [REAL]"'
            # else:
            #     sql = '{} AS "x [REAL]" {}'.format(sql[:pos], sql[pos:])
            # sql += ' AS "x [REAL]"'
            pass
        elif self.col_defn.data_type == 'BOOL':
            # # force sqlite3 to return Bool type
            # pos = sql.find(' FROM')
            # if pos == -1:
            #     sql += ' AS "x [BOOLTEXT]"'
            # else:
            #     sql = '{} AS "x [BOOLTEXT]" {}'.format(sql[:pos], sql[pos:])
            sql += ' AS "x [BOOLTEXT]"'

        if sql[:7].upper() != 'SELECT ':
            sql = 'SELECT ' + sql

        async with self.db_obj.context.db_session.get_connection() as db_mem_conn:
            if self.db_obj.mem_obj:
                conn = db_mem_conn.mem
            else:
                conn = db_mem_conn.db

            # conn.tablenames = None
            # conn.joins = {}
            # col_text = await conn.get_col_text(self.db_obj, [], self.col_name)

            # if 'LEFT JOIN' in conn.tablenames:
            #     sql = 'SELECT {} FROM {}'.format(col_text, conn.tablenames)
            # else:
            #     sql = 'SELECT ' + col_text

            # param_style = self.db_obj.db_table.constants.param_style
            # param_pos = []
            # params = []
            # for dep in self.deps:
            #     fld = await self.db_obj.getfld(dep)
            #     dep = 'a.{}'.format(dep)
            #     pos = sql.find(dep)
            #     sql = sql.replace(dep, param_style, 1)
            #     pos_to_insert = len([x for x in param_pos if x < pos])
            #     params.insert(pos_to_insert, await fld.get_val_for_sql())
            #     param_pos.insert(pos_to_insert, pos)

            # # works for now, but not thought through! [2018-04-23]
            # if 'LEFT JOIN' in conn.tablenames:
            #     sql += ' WHERE a.row_id = {}'.format(param_style)
            #     params.append(await self.db_obj.getval('row_id'))

            # print(f'{self.table_name}.{self.col_name}')
            # print(sql, params)
            # input()

            cur = await conn.exec_sql(sql, params, context=self.db_obj.context)
            try:
                row = await cur.__anext__()
            except StopAsyncIteration:  # no rows selected
                value = None
            else:
                try:
                    next_row = await cur.__anext__()
                except StopAsyncIteration:  # exactly one row selected
                    value = row[0]
                else:
                    raise RuntimeError('More than one row found')

        value = await self.check_val(value)

        # print('-'*20)
        # print('{}.{}'.format(self.table_name, self.col_name))
        # print(sql)
        # print(params)
        # print('value = "{}"'.format(value))
        # print('='*20)
        # print()

        await self.setval(value, display=display, validate=False)

    def notify_form(self, obj):  # called from form when gui_obj created
        if self.gui_obj == ():
            self.gui_obj = weakref.WeakSet()
        self.gui_obj.add(obj)  # reference to object, for redisplay

    async def read_row(self, value, display, debug=False):
        cols_vals = {}
        for fld in self.table_keys:
            if fld is self:
                val = value
            else:
                val = fld._value
            cols_vals[fld.col_name] = val
        await self.db_obj.select_row(cols_vals, display, debug=debug)

    async def setval(self, value, display=True, validate=True, from_init=False,
            from_sql=False, form_vlds=[]):

        db_obj = self.db_obj
        col_defn = self.col_defn
        col_name = self.col_name

        # print(f'setval {self.table_name}.{col_name}: "{self._value_}" -> "{value}"')

        if from_sql:
            value = await self.get_val_from_sql(value)
        else:
            # check that value is of the correct type - do a bit of type-casting
            value = await self.check_val(value)  # will raise AibError on error

        if not from_init and (value is None or value == ''):
            if not col_defn.allow_null:
                # if from_sql, check if fld in flds_to_update - ignore if not active subtype
                if not from_sql or self in db_obj.get_flds_to_update():
                    errmsg = f'{self.table_name}.{col_name} - a value is required'
                    raise AibError(head=col_defn.short_descr, body=errmsg)

        if not from_init:
            if self.ledger_vld:  # added 2018-07-11 - if ok, don't need col_checks
                ctx_mod_id, ctx_ledg_id = getattr(db_obj.context, 'mod_ledg_id', (None, None))
                if ctx_mod_id == db_obj.db_table.module_row_id:
                    if ctx_ledg_id != await db_obj.getval(db_obj.db_table.ledger_col):
                        raise AibError(head=self.table_name,
                            body='Sub-ledger must be ' +
                                (await db.cache.get_mod_ledg_name(
                                    db_obj.company, (ctx_mod_id, ctx_ledg_id)))[2])

        changed = await self.value_changed(value)

        if changed and validate:  # check for allow_amend
            try:
                await db_obj.check_perms('amend', self, value)
            except AibDenied:
                raise AibDenied(head=f'Amend {self.table_name}.{col_name}',
                    body='Permission denied')
            allow_amend = col_defn.allow_amend
            if allow_amend not in (False, True):
                # allow_amend = await eval_expr(deepcopy(allow_amend), db_obj, self)
                allow_amend = await eval_expr(allow_amend, db_obj, self)
            if not db_obj.exists and col_defn.key_field != 'N':
                pass  # trying to select
            elif db_obj.db_table.read_only:
                raise AibError(head=f'Amend {self.table_name}.{col_name}',
                    body='Table is read only - no amendments allowed')
            elif (
                col_defn.col_type != 'virt'  # e.g. ar_openitems.alloc_cust is ok
                    and 'posted' in db_obj.db_table.col_dict
                    # next line added 2019-08-20
                    # in ar_alloc_item.xml we add the virtual column 'alloc_cust'
                    #   to the grid where db_obj is ar_openitems
                    # without the next line, it fails because ar_openitems is 'posted',
                    #   but that is ok because we use it to update ar_tran_alloc_det
                    # any implications?
                    and db_obj.db_table.col_dict['posted'].col_type != 'virt'
                    and await db_obj.getval('posted')
                    and await db_obj.get_orig('posted')
                    ):
                raise AibError(head=f'Amend {self.table_name}.{col_name}',
                    body='Transaction posted - no amendments allowed')
            elif allow_amend:
                pass  # note - all virtual fields have allow_amend=True
            elif col_name in db_obj.sub_trans and self._value is not None and value != self._value:
                # added 2019-09-21 - I think it is appropriate for *all* sub_trans
                raise AibError(head=f'Amend {self.table_name}.{col_name}',
                    body='Cannot amend sub_trans - cancel current sub_trans first')
            elif await self.calculated():
                errmsg = (
                    f'{self.table_name}.{col_name}: Calculated field - '
                    f'amendment not allowed {self._value_} -> {value}'
                    )
                raise AibError(head=self.table_name, body=errmsg)
            elif not db_obj.exists:
                pass  # does not apply to new objects
            elif self._value is None:
                pass  # to cater for new 'user' column - allow first-time value
            else:
                errmsg = '{}.{}: amendment not allowed {} -> {}'.format(
                    self.table_name, col_name, self._value, value)
                raise AibError(head=self.table_name, body=errmsg)

        if self.table_keys and value is not None and not from_sql and not self.db_obj.exists:
            # 1. if value is None, do not trigger read_row
            # 2. if from_sql, we have just selected the row and are
            #      populating the fields - do not trigger another read_row!
            # 3. if db_obj.exists, assume that we are changing an alt_key
            #      e.g. on posting transaction, change temp tran_number to
            #      actual tran_number - IMPLICATIONS??
            # 4. must read row before other validations, because
            #      other validations may use contents of db_obj
            await self.read_row(value, display)
            if db_obj.exists:
                value = self._value  # to change (eg) 'a001' to 'A001'
                changed = False
                if display:  # on_read checks for 'repos' - don't if not 'display'
                    for caller_ref in list(db_obj.on_read_func.keyrefs()):
                        caller = caller_ref()
                        if caller is not None:
                            if not caller.form.closed:
                                method = db_obj.on_read_func[caller]
                                try:
                                    await ht.form_xml.exec_xml(caller, method)
                                except AibError:  # can fail in ht.gui_grid.repos_row()
                                    await db_obj.init()  # re-initialise
                                    raise

        if self.foreign_key is not None:
            if validate or changed:
                # check that value exists as key on foreign table, read fk_object
                # if self.foreign_key == {}:  # not yet set up
                #     await self.setup_foreign_key()
                foreign_key = await db_obj.get_foreign_key(self)
                tgt_field = foreign_key['tgt_field']
                true_src = foreign_key['true_src']
                alt_src = foreign_key['alt_src']
                if true_src:  # this is an alt_src
                    alt_srcnames = [
                        s.strip() for s in true_src.col_defn.fkey[FK_ALT_SOURCE].split(',')
                        ]
                if value is None:
                    if self._value is not None:  # added 2018-03-15
                        await tgt_field.db_obj.init()
                elif value == tgt_field._value and (
                        tgt_field.db_obj.exists or not tgt_field.db_obj.dirty):
                    # if not exists and not dirty, has just been saved [2018-03-26]
                    # if this is ok, might as well just test for 'dirty' (?)
                    if true_src:  # don't re-read, but if true_src, set value
                        true_foreign_key = await true_src.db_obj.get_foreign_key(true_src)
                        if col_name == alt_srcnames[-1]:  # if multi-part key, all parts are present
                            # must validate true_src - db_obj might exist because we have
                            #   performed a lookup, but true_src might have col_checks
                            await true_src.setval(true_foreign_key['tgt_field']._value)
                elif self.db_obj.parent and tgt_field == self.db_obj.parent[1]:
                    pass  # e.g. ap_tran_inv_tax.tran_det_row_id -> ap_tran_inv_det.row_id
                else:
                    if true_src:  # this is an alt_src
                        if col_name == alt_srcnames[0]:  # if multi-part key, only init on first part
                            await tgt_field.db_obj.init()
                        await tgt_field.setval(value, display, validate=False)
                        if col_name == alt_srcnames[-1]:  # if multi-part key, all parts are present
                            if not tgt_field.db_obj.exists:
                                await tgt_field.db_obj.init()
                                if len(alt_srcnames) > 1:  # build meaningful error message
                                    where = []
                                    for altsrc_name in alt_srcnames:
                                        if altsrc_name == col_name:
                                            altsrc_val = value
                                        else:
                                            altsrc_val = await db_obj.getval(altsrc_name)
                                        where.append('{}={}'.format(altsrc_name, altsrc_val))
                                    errmsg = '{} not found where {}'.format(
                                        tgt_field.table_name, ' and '.join(where))
                                else:
                                    errmsg = '{} not found on {}'.format(
                                        value, tgt_field.table_name)
                                raise AibError(head=col_defn.short_descr, body=errmsg)
                            value = tgt_field._value  # to change (eg) 'a001' to 'A001'
                            # must call setval, in case validation required
                            # i.e. there could be a col_check on the true_src, but not on the alt_src
                            true_foreign_key = await true_src.db_obj.get_foreign_key(true_src)
                            await true_src.setval(true_foreign_key['tgt_field']._value, display=display)
                            # next line unnecessary? already checked in setval
                            # if display:
                            #     for obj in true_src.gui_obj:
                            #         await obj._redisplay()
                    else:
                        await tgt_field.read_row(value, display)
                        if not tgt_field.db_obj.exists:
                            await tgt_field.db_obj.init()
                            errmsg = '{} not found on {}'.format(
                                value, tgt_field.table_name)
                            raise AibError(head=col_defn.short_descr, body=errmsg)
                        value = tgt_field._value  # to change (eg) 'a001' to 'A001'

        if validate:
            # check for constant
            if self.constant is not None:
                if value != self.constant:
                    errmsg = 'Value must be {}'.format(self.constant)
                    raise AibError(head=self.table_name, body=errmsg)
            # check for fkey_parent
            if self.fkey_parent is not None:
                if value != self.fkey_parent._value:
                    errmsg = f'Parent value is {self.fkey_parent._value}'
                    raise AibError(head=self.table_name, body=errmsg)
            # check for choices
            if col_defn.choices is not None:
                if value is not None and value not in col_defn.choices:
                    errmsg = (
                        f'{self.table_name}.{col_name} - '
                        f'value must be one of {", ".join(str(_) for _ in col_defn.choices.keys())}'
                        )
                    raise AibError(head=col_defn.short_descr, body=errmsg)
            # check for col_checks
            for descr, errmsg, col_chk in col_defn.col_checks:
                await chk_constraint(self, col_chk, value=value, errmsg=errmsg)  # can raise AibError

            # check for form_vlds
            for ctx, vld in form_vlds:
                await check_vld(self, ctx, vld, value)

        # if we get here, all validations have passed

        if not changed:
            # if self.must_be_evaluated:
            #     # do we get here? if not, no need to reset
            #     print(f'{self.table_name}.{col_name} {value} no change but must be evaluated??')
            self.must_be_evaluated = False  # reset in case it was True
            return

        self._value = value

        # update any child fields with the same value
        # if the child has table_keys, this means that there is a one-to-one relationship
        #   with the parent e.g. db_tables -> db_actions, or any sub_tran table
        # in this case, automatically read the child row to keep the two in sync
        # slight downside - if there are sub_tran tables, only one of them can be active
        #   at a time, but we try to read all of them
        #     for the active one, SELECT succeeds and 'exists' is set to True
        #     for the inactive ones, SELECT fails and 'exists' is set to False
        #   we could get clever and achieve the latter locally if warranted
        for child in self.children:
            child._value = value
            if value is not None:  # could be if from_init
                if child.table_keys:
                    await child.read_row(value, display)

        # if foreign key has changed, re-read foreign object
        if self.foreign_key:
            foreign_key = await db_obj.get_foreign_key(self)

            if not validate:  # else already executed above
                tgt_field = foreign_key['tgt_field']
                if tgt_field._value != value:
                    if value is None:
                        await tgt_field.db_obj.init()
                    else:
                        await tgt_field.read_row(value, display)

            alt_src = foreign_key['alt_src']
            # if this is a true source, change alt source
            for alt_src_fld in alt_src:
                alt_foreign_key = await alt_src_fld.db_obj.get_foreign_key(alt_src_fld)
                # alt_src_fld._value = alt_src_fld.foreign_key['tgt_field']._value
                alt_src_fld._value = alt_foreign_key['tgt_field']._value
                if display:
                    for obj in alt_src_fld.gui_obj:
                        await obj._redisplay()

        if value is not None:  # could be if from_init
            if col_name in db_obj.sub_types:
                if db_obj.active_subtypes.get(col_name) != value:
                    db_obj.active_subtypes[col_name] = value
                    subtype_flds = db_obj.sub_types[col_name][value]
                    db_obj.active_subtype_flds[col_name] = subtype_flds
                    for fld in subtype_flds:
                        if fld._value is None:  # added 2019-03-11
                            if fld.col_defn.dflt_val is not None:
                                fld._value = await fld.get_dflt(from_init=True)

            if col_name in db_obj.sub_trans:
                if db_obj.sub_trans[col_name][value] is None:  # not set up
                    subtran_tblname = db_obj.db_table.sub_trans[col_name][value][0]
                    await db.objects.get_db_object(db_obj.context, db_obj.company,
                        subtran_tblname, parent=db_obj)

        if from_init:
            return  # the rest are all gui-related - n/a if not changed or from_init

        for caller_ref in list(self.gui_subtype.keyrefs()):
            caller = caller_ref()
            if caller is not None and not caller.form.closed:  # e.g. select_date_range.xml
                sub_colname = self.gui_subtype[caller]
                await caller.set_subtype(sub_colname, value)

        if not db_obj.dirty:
            if validate or col_defn.col_type != 'virt':  # added [2018-11-12]
                # assumptions -
                #   1. if 'virt' field is changed, do not set db_obj to 'dirty'
                #   2. unless 'validate' is True, in which case field was probably
                #        changed by user - do set db_obj to 'dirty'
                #      e.g. acc.roles.expandable
                #   3. 'probably' is not rigorous - monitor and try to tighten up
                db_obj.dirty = True
                if display:
                    for caller_ref in list(db_obj.on_amend_func.keyrefs()):
                        caller = caller_ref()
                        if caller is not None:
                            if not caller.form.closed:
                                method = db_obj.on_amend_func[caller]
                                await ht.form_xml.exec_xml(caller, method)

                if db_obj.subtran_parent is not None:
                    subtran_parent, return_vals = db_obj.subtran_parent
                    if not subtran_parent.dirty:
                        subtran_parent.dirty = True
                        if display:
                            for caller_ref in list(subtran_parent.on_amend_func.keyrefs()):
                                caller = caller_ref()
                                if caller is not None:
                                    if not caller.form.closed:
                                        method = subtran_parent.on_amend_func[caller]
                                        await ht.form_xml.exec_xml(caller, method)

                if not from_sql:
                    if db_obj.mem_obj:
                        memobj = db_obj
                        while memobj.mem_parent is not None:
                            if not memobj.mem_parent.dirty:
                                memobj.mem_parent.dirty = True
                                if display:
                                    for caller_ref in list(memobj.mem_parent.on_amend_func.keyrefs()):
                                        caller = caller_ref()
                                        if caller is not None:
                                            if not caller.form.closed:
                                                method = memobj.mem_parent.on_amend_func[caller]
                                                await ht.form_xml.exec_xml(caller, method)
                            memobj = memobj.mem_parent

        if display:
            for obj in self.gui_obj:
                await obj._redisplay()

    def set_readonly(self, state):
        for obj in self.gui_obj:
            obj.set_readonly(state)

    async def _getval(self):
        if self.must_be_evaluated:
            self.must_be_evaluated = False  # reset first, to avoid recursion in some situations
            await self.recalc(display=True)
        return self._value

    async def _getval_fkey(self):
        # await self.setup_foreign_key()
        # return await self._getval()

        foreign_key = await self.db_obj.get_foreign_key(self)

        # if self.foreign_key == {}:
        #     await self.setup_foreign_key()
        # true_src = self.foreign_key['true_src']
        true_src = foreign_key['true_src']
        await true_src.get_fk_object()  # what does this do?
        # return await self.foreign_key['tgt_field'].getval()
        return await foreign_key['tgt_field'].getval()

    async def get_orig(self):
        return self._orig

    async def get_prev(self):
        return self._prev

    async def get_val_from_sql(self, value):
        return value

    async def get_val_for_sql(self):
        # used for insert/update - return value suitable for storing in database
        if self.must_be_evaluated:
            self.must_be_evaluated = False
            await self.recalc()
        return self._value

    async def get_val_from_xml(self, value):
        # at present [2015-03-15]] this is only used for in-memory
        #   objects in form definitions
        # form definitions are stored as xml
        # for maintenance, we unpack it into several in-memory db tables
        # this method accepts a value from the xml file, converts it
        #   if necessary, and returns it
        if value is None:
            value = self.col_defn.dflt_val
        return value

    async def get_val_for_xml(self):
        # see above
        # this method does the opposite
        # it returns a value to be used when re-creating the xml file
        if self._value is None:
            return None
        if self._value == self.col_defn.dflt_val:
            return None
        return self._value

    async def get_dflt(self, from_init=False):
        if self.constant is not None:
            return self.constant  # e.g. tran_type in ar_openitems
        if self.ledger_col:
            ctx_mod_id, ctx_ledg_id = getattr(self.db_obj.context, 'mod_ledg_id', (None, None))
            if ctx_mod_id == self.db_obj.db_table.module_row_id:
                # if ctx_ledg_id is None:
                #     raise AibError(head=self.table_name, body='Ledger not set up')
                # return ctx_ledg_id
                # changed [2019-11-27]
                # when setting up new ledger, we now prompt for 'first financial period'
                # <mod>_ledger_periods has a ledger_col, but ledger is not yet set up
                # without this change, an error is raised; with it, user can proceed
                # ledger_col is a mandatory field, so no danger of it being omitted in error
                if ctx_ledg_id is not None:
                    return ctx_ledg_id
        if not from_init and self.col_defn.dflt_rule is not None:
            return await db.dflt_xml.get_db_dflt(self)
        dflt_val = self.col_defn.dflt_val
        if dflt_val is not None:
            if dflt_val.startswith('{'):
                # if = '{}', empty dict, else contents of '{}' is a column name
                if dflt_val == '{}':
                    return '{}'  # assumes data_type is JSON
                # reason why next line is necessary [2018-03-18] -
                #
                #   if '>' in dflt_val, it follows path using fkey
                #   if from_init, foreign key has not been set up, therefore
                #     setup.fkey() will be triggered
                #   in the case of acc_roles.module_row_id, the dflt_val is
                #     {parent_id>module_row_id}, and parent_id is an fkey
                #     pointing to itself, so we go into a loop creating an
                #     infinite number of parents until we hit a recursion limit
                #   therefore it is better *not* to calculate the default value
                #     if from_init and '>' in dflt_val
                #
                #   on the other hand, in the case of ap_tran_inv_det>tran_date, this
                #     is a virt field with a dflt_val of {tran_row_id>tran_date}
                #   on init, we want to recreate the value from the parent - ap_tran_inv
                #
                #   therefore, we disallow if from_init and '>' in dflt_val *unless*
                #     this is a child table
                #
                # it works for now, but there may be cases where if fails - monitor
                #
                # a possible alternative test is "and self.col_defn.col_type != 'virt'"
                # it would work just as well here, and may succeed where the other
                #   one fails
                #
                if from_init and '>' in dflt_val:
                    return None
                else:
                    return await self.db_obj.getval(dflt_val[1:-1])
            else:
                return dflt_val
        # if we get here, None is returned

    async def calculated(self):

        if self._calculated is None:  # first time
            # don't understand the reason for the following lines [2018-07-16]
            # remove for now, explain properly if it turns out that they are needed
            # allow_amend = self.col_defn.allow_amend
            # if allow_amend not in (False, True):
            #     allow_amend = await eval_expr(deepcopy(allow_amend), self.db_obj, self)
            # if self.db_obj.exists and not allow_amend:
            #     self._calculated = False
            # else:
                src_obj, op, tgt_val = self.col_defn.calculated
                if '.' in src_obj:
                    obj_name, col_name = src_obj.split('.')
                    if obj_name == '_param':
                        db_obj = await db.cache.get_adm_params(self.db_obj.company)
                    elif obj_name == '_ledger':
                        module_row_id = self.db_obj.db_table.module_row_id
                        ctx_mod_id, ctx_ledg_id = getattr(
                            self.db_obj.context, 'mod_ledg_id', (None, None))
                        if ctx_mod_id == module_row_id:  # get ledger_row_id from 'context'
                            ledger_row_id = ctx_ledg_id
                        else:  # get ledger_row_id from db_table.ledger_col - could be None
                            ledger_col = self.db_obj.db_table.ledger_col
                            if ledger_col is None:
                                raise AibError(
                                head='Checking calculated',
                                body=f'No ledger col defined for {self.db_obj.table_name}'
                                )
                            ledger_row_id = await self.db_obj.getval(ledger_col)
                        db_obj = await db.cache.get_ledger_params(
                            self.db_obj.company, module_row_id, ledger_row_id)
                    elif obj_name in self.db_obj.context.data_objects:
                        db_obj = self.db_obj.context.data_objects[obj_name]
                    else:
                        db_obj = await db.objects.get_db_object(
                            self.db_obj.context, self.db_obj.company, obj_name)
                    src_val = await db_obj.getval(col_name)
                else:
                    col_name = src_obj
                    src_val = await self.db_obj.getval(col_name)
                self._calculated = getattr(operator, op)(src_val, tgt_val)
        return self._calculated

    async def value_changed(self, value=blank):
        if value is blank:
            value = self._orig
        # return await self.getval() != value
        return self._value_ != value

    def concurrency_check(self):  # self._curr_val has just been read in from database
        if self._curr_val == self._orig:  # value has not been changed - ok
            return True
        if self._curr_val == self._value:  # value changed to the same as ours - ok
            return True
        return False  # value changed to a different value from ours - not ok

    #-------------------------------------------------------------------------

    def _get_value(self):
        assert not self.must_be_evaluated, f'{self.table_name}.{self.col_name} must be evaluated'
        return self._value_
    def _set_value(self, value):
        if value != self._value_:
            # next block works 99% of the time, but ...
            #   if self is db_tables.row_id, and child is db_actions.table_id,
            #     we want db_actions to call select_row()
            # it will if we use 'await setval()', but cannot mix @property and async :-(
            # fixed by -
            #   removing block below
            #   adding
            #       for child in self.children:
            #           child._value = value
            #           if child.table_keys:
            #               await child.read_row(vaue, display)
            #     to setval()
            #   adding
            #       for child in self.children:
            #           child._value = None
            #     to db.objects.init()
            #   adding
            #       for child in self.children:
            #           child._value = value
            #     to conn.mssql/pgsql/sqlite3
            #   any other places? don't know
            # tried to add 'assert child._value == value' here,
            #   but hit recursion limit if child has a table_key/fkey
            # Monitor
            # for child in self.children:
            #     child._value = value
            for fld in self.flds_to_recalc:
                fld.must_be_evaluated = True
            self._value_ = value
        self.must_be_evaluated = False
    _value = property(_get_value, _set_value)

#-----------------------------------------------------------------------------

class Text(Field):
    async def check_val(self, value):
        if value in (None, ''):
            return None
        if isinstance(value, str):
            pass
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            value = str(value)
        else:
            errmsg = '{}.{} - type is {}, must be str'.format(
                self.table_name, self.col_name, str(type(value)).split("'")[1])
            raise AibError(head=self.col_defn.short_descr, body=errmsg)
        max_len = self.col_defn.max_len  # 0 means no maximum
        if max_len and len(value) > max_len:
            errmsg = '{}.{} - maximum length is {}'.format(
                self.table_name, self.col_name, max_len)
            raise AibError(head=self.col_defn.short_descr, body=errmsg)
        return value

    async def str_to_val(self, value):
        if value in (None, ''):
            return None
        return value

    async def val_to_str(self, value=blank):
        try:
            await self.db_obj.check_perms('view', self)
        except AibDenied:
            return '*'
        if value is blank:
            value = await self.getval()
        if value is None:
            return ''
        return value

    async def prev_to_str(self):
        try:
            await self.db_obj.check_perms('view', self)
        except AibDenied:
            return '*'
        if self._prev is None:
            return ''
        return self._prev

    def get_val_for_where(self):
        return None if self._value is None else repr(self._value)

class Password(Text):
    async def check_val(self, value):
        # called from setval() - generate and return pwd_hash to store in database
        if value is None:
            value = ''
        hash_name = 'sha256'
        salt = token_bytes(16)
        iterations = 100000
        dk = kdf(hash_name, value.encode('utf-8'), salt, iterations)
        return dumps([hash_name, salt.hex(), iterations, dk.hex()])

    async def chk_password(self, value):
        # check that password in 'value' matches password on database
        pwd_hash = self._value
        if pwd_hash is None:
            print('Password is None - can this ever happen?')
            return value is None
        if value is None:
            value = ''
        hash_name, salt, iterations, dk = loads(pwd_hash)
        return (kdf(hash_name, value.encode('utf-8'), bytes.fromhex(salt), iterations)
            == bytes.fromhex(dk))

class Json(Text):
    async def _getval(self):
        # must return deepcopy because value is mutable, so
        #   we would not be able to detect if it was changed
        return deepcopy(self._value)

    def serialise(self, value):
        # simple serialiser to handle date objects
        # if any are found, they will be converted into a string using repr -
        #   'datetime.date(y, m, d)'
        # ditto for Decimal objects
        return dumps(value, default=repr)

    def deserialise(self, value):
        # simple deserialiser to handle date objects
        # assumes that any string starting with 'datetime.date(' is a date object
        # also handles Decimal objects - string starting with 'Decimal('
        def deserialise_list(value):
            for pos, val in enumerate(value):
                if isinstance(val, str):
                    if val.startswith('datetime.date('):
                        value[pos] = dt(*map(int, val[14:-1].split(',')))
                    elif val.startswith('Decimal('):
                        value[pos] = D(val[9:-2])
                elif isinstance(val, list):
                    deserialise_list(val)
                elif isinstance(val, dict):
                    deserialise_dict(val)
        def deserialise_dict(value):
            for key, val in value.items():
                if isinstance(val, str):
                    if val.startswith('datetime.date('):
                        value[key] = dt(*map(int, val[14:-1].split(',')))
                    elif val.startswith('Decimal('):
                        value[key] = D(val[9:-2])
                elif isinstance(val, list):
                    deserialise_list(val)
                elif isinstance(val, dict):
                    deserialise_dict(val)
        value = loads(value)
        if isinstance(value, list):
            deserialise_list(value)
        elif isinstance(value, dict):
            deserialise_dict(value)
        return value

    async def get_dflt(self, from_init=False):
        dflt_val = await Field.get_dflt(self, from_init)
        if dflt_val is None:
            return None
        return self.deserialise(dflt_val)

    async def check_val(self, value):
        if value is None:
            return None
        if isinstance(value, (list, dict, bool, tuple)):
            return value
        # 'str' is valid for JSON, but not for AIB - just use TEXT!
        errmsg = '{}.{} - type is {}, not valid for JSON'.format(
            self.table_name, self.col_name, str(type(value)).split("'")[1])
        raise AibError(head=self.col_defn.short_descr, body=errmsg)

    async def str_to_val(self, value):
        if value in (None, ''):
            return None
        else:
            try:
                return self.deserialise(value)
            except ValueError:
                errmsg = '{}.{} - {} not a valid Json string'.format(
                    self.table_name, self.col_name, value)
                raise AibError(head=self.col_defn.short_descr, body=errmsg)

    async def val_to_str(self, value=blank):
        try:
            await self.db_obj.check_perms('view', self)
        except AibDenied:
            return '*'
        if value is blank:
            value = await self.getval()
        if value is None:
            return ''
        return self.serialise(value)

    async def get_val_for_sql(self):
        return None if self._value is None else self.serialise(self._value)

    async def get_val_for_xml(self):
        if self._value is None:
            return None
        value = self.serialise(self._value)
        if value == self.col_defn.dflt_val:
            return None
        return value

    async def get_val_from_sql(self, value):
        return None if value is None else self.deserialise(value)

    async def get_val_from_xml(self, value):
        if value is None:
            value = self.col_defn.dflt_val
        return None if value is None else self.deserialise(value)

    def concurrency_check(self):
        if self._curr_val is None:
            return self._orig is None
        return self.deserialise(self._curr_val) == self._orig

class Xml(Text):
    parser = etree.XMLParser(remove_comments=True, remove_blank_text=True)
    schema = None
    root = None

    async def _getval(self):
        # must return deepcopy because value is mutable, so
        #   we would not be able to detect if it was changed
        return deepcopy(self._value)

    async def check_val(self, value):
        if value is None:
            return None
        if isinstance(value, etree._Element):
            return value
        return self.parse_xml(value)

    async def get_val_for_sql(self):
        return (None if self._value is None else
            gzip.compress(etree.tostring(self._value)))

    async def get_val_for_xml(self):
        if self._value is None:
            return None
        value = gzip.compress(etree.tostring(self._value))
        if value == self.col_defn.dflt_val:
            return None
        return value

    def parse_xml(self, value):
        if value is None:
            return None
        try:
            xml = etree.fromstring(value, parser=self.parser)
        except etree.XMLSyntaxError as e:
            raise AibError(head='Xml error', body=str(e))
        if self.schema is not None:
            try:
                if self.root is None:
                    self.schema.assertValid(xml)
                else:
                    self.schema.assertValid(xml.find(self.root))
            except etree.DocumentInvalid as e:
                raise AibError(head='Xml error', body=str(e))
        return xml

    async def get_val_from_sql(self, value):
        value = gzip.decompress(value)
        return self.parse_xml(value)

    async def get_val_from_xml(self, value):
        if value is None:
            value = self.col_defn.dflt_val
        return self.parse_xml(value)

    def concurrency_check(self):
        if self._curr_val is None:
            return self._orig is None
        curr_val = gzip.decompress(self._curr_val)
        curr_val = self.parse_xml(curr_val)
        return self._equal(curr_val, self._orig)

    async def value_changed(self, value=blank):
        if value is blank:
            value = self._orig
        return not self._equal(self._value, value)

    def _equal(self, a, b):
        if a is None:
            return b is None  # can be True or False
        if b is None:
            return False
        if a.tag != b.tag or a.attrib != b.attrib:
            return False
        if a.text != b.text or a.tail != b.tail:
            return False
        if len(a) != len(b):
            return False
        if any(not self._equal(a, b) for a, b in zip(a, b)):
            return False
        return True

class ProcessXml(Xml):
    schema = etree.XMLSchema(file=os.path.join(schema_path, 'bpmn20', 'BPMN20.xsd'))
    root = '{http://www.omg.org/spec/BPMN/20100524/MODEL}definitions'

class FormXml(Xml):
    schema = etree.XMLSchema(file=os.path.join(schema_path, 'form.xsd'))

class StringXml(Xml):
    parser = etree.XMLParser(remove_blank_text=True)

    async def str_to_val(self, value):
        if value in (None, ''):
            return None
        else:
            try:
                return self.from_string(value, from_gui=True)
            except (etree.XMLSyntaxError, ValueError) as e:
                raise AibError(head=self.col_defn.short_descr,
                    body='Xml error - {}'.format(e.args[0]))

    async def val_to_str(self, value=blank):
        try:
            await self.db_obj.check_perms('view', self)
        except AibDenied:
            return '*'
        if value is blank:
            value = await self.getval()
        if value is None:
            return ''
        return self.to_string(value, for_gui=True)

    async def get_val_for_sql(self):
        return None if self._value is None else self.to_string(self._value)

    async def get_val_for_xml(self):
        if self._value is None:
            return None
        value = self.to_string(self._value)
        if value == self.col_defn.dflt_val:
            return None
        return value

    async def get_val_from_sql(self, value):
        return None if value is None else self.from_string(value)

    async def get_val_from_xml(self, value):
        if value is None:
            value = self.col_defn.dflt_val
        return None if value is None else self.from_string(value)

    def concurrency_check(self):
        if self._curr_val is None:
            return self._orig is None
        curr_val = self.from_string(self._curr_val)
        return self._equal(curr_val, self._orig)

    def from_string(self, string, from_gui=False):
        if from_gui:
            lines = string.split('"')  # split on attributes
            for pos, line in enumerate(lines):
                if pos%2:  # every 2nd line is an attribute
                    lines[pos] = line.replace(
                        '&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            string = '"'.join(lines)
        return etree.fromstring(string, parser=self.parser)

    def to_string(self, xml, for_gui=False):
        if not for_gui:  # for storing in database
            return etree.tostring(xml, encoding=str)
        else:  # for gui
            string = etree.tostring(xml, encoding=str, pretty_print=True)
            lines = string.split('"')  # split on attributes
            for pos, line in enumerate(lines):
                if pos%2:  # every 2nd line is an attribute
                    lines[pos] = line.replace(
                        '&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
            return '"'.join(lines)

class Integer(Field):
    async def get_dflt(self, from_init=False):
        dflt_val = await Field.get_dflt(self, from_init)
        if dflt_val is None:
            return None
        return int(dflt_val)

    async def check_val(self, value):
        if value is None:
            return None
        try:
            return int(value)
        except ValueError:
            errmsg = '{}.{} - "{}" is not an integer'.format(
                self.table_name, self.col_name, value)
            raise AibError(head=self.col_defn.short_descr, body=errmsg)

    async def str_to_val(self, value):
        if value in (None, ''):
            return None
        try:
            if self.sequence:
                if int(value) < 0:
                    errmsg = '{}.{} - "{}" cannot be negative'.format(
                        self.table_name, self.col_name, value)
                    raise AibError(head=self.col_defn.short_descr, body=errmsg)
                return int(value) - 1
            else:
                return int(value)
        except (ValueError, TypeError):
            errmsg = '{}.{} - "{}" is not an integer'.format(
                self.table_name, self.col_name, value)
            raise AibError(head=self.col_defn.short_descr, body=errmsg)

    async def val_to_str(self, value=blank):
        try:
            await self.db_obj.check_perms('view', self)
        except AibDenied:
            return '*'
        if value is blank:
            value = await self.getval()
        if value is None:
            return ''
        if self.sequence:
            return str(value + 1)
        else:
            return str(value)

    async def prev_to_str(self):
        try:
            await self.db_obj.check_perms('view', self)
        except AibDenied:
            return '*'
        if self._prev is None:
            return ''
        return str(self._prev)

    async def get_val_for_xml(self):
        if self._value is None:
            return None
        value = str(self._value)
        if value == self.col_defn.dflt_val:
            return None
        return value

    async def get_val_from_xml(self, value):
        if value is None:
            value = self.col_defn.dflt_val
        return None if value is None else int(value)

    def get_val_for_where(self):
        return self._value

class Decimal(Field):
    async def get_dflt(self, from_init=False):
        dflt_val = await Field.get_dflt(self, from_init)
        if dflt_val is None:
            return None
        dflt_val = D(dflt_val)
        if from_init:
            return dflt_val
        if dflt_val == int(dflt_val):  # if dflt_val is an integer, no need to check scale
            return dflt_val
        scale = await self.get_scale()
        quant = D(str(10**-scale))
        return dflt_val.quantize(quant, rounding=ROUND_HALF_UP)

    async def check_val(self, value):
        if value is None:
            return None
        try:
            value = D(value)
        except DecimalException:
            errmsg = '{}.{} - {} not a valid Decimal type'.format(
                self.table_name, self.col_name, value)
            raise AibError(head=self.col_defn.short_descr, body=errmsg)
        if value == int(value):  # if value is an integer, no need to check scale
            return value.quantize(0)
        scale = await self.get_scale()
        quant = D(str(10**-scale))
        return value.quantize(quant, rounding=ROUND_HALF_UP)

    async def str_to_val(self, value):
        if value in (None, ''):
            return None
        try:
            value = D(value)
        except DecimalException:
            errmsg = '{}.{} - {} not a valid Decimal type'.format(
                self.table_name, self.col_name, value)
            raise AibError(head=self.col_defn.short_descr, body=errmsg)
        scale = await self.get_scale()
        quant = D(str(10**-scale))
        try:
            return D(value).quantize(
                quant, context=Context(traps=[Inexact]))
        except Inexact:
            if scale:
                errmsg = f'{self.table_name}.{self.col_name} - cannot exceed {scale} decimals'
            else:
                errmsg = f'{self.table_name}.{self.col_name} - no decimals allowed'
            raise AibError(head=self.col_defn.short_descr, body=errmsg)

    async def val_to_str(self, value=blank, scale=None):
        try:
            await self.db_obj.check_perms('view', self)
        except AibDenied:
            return '*'
        if value is blank:
            value = await self.getval()
        if value is None:
            return ''
        if scale is None:
            scale = await self.get_scale()
        # output = '{{:.{}f}}'.format(scale)
        output = f'{{:.{scale}f}}'
        return output.format(value)

    async def prev_to_str(self, value=blank):
        try:
            await self.db_obj.check_perms('view', self)
        except AibDenied:
            return '*'
        if value is blank:
            value = self._prev
        if value is None:
            return ''
        output = '{{:.{}f}}'.format(await self.get_scale())
        # output = f'{{:.{await self.get_scale()}f}}'  # does not work in Python 3.6 - try in 3.7
        return output.format(value)

    async def get_val_from_sql(self, value):
        return await self.check_val(value)

    async def get_val_from_xml(self, value):
        if value is None:
            value = self.col_defn.dflt_val
        if value is None:
            return None
        value = D(value)  # could be integer
        scale = await self.get_scale()
        quant = D(str(10**-scale))
        return value.quantize(quant, rounding=ROUND_HALF_UP)

    async def get_scale(self):
        col_defn = self.col_defn
        if col_defn.scale_ptr is None:
            scale = col_defn.db_scale
        else:
            scale_ptr = await self.db_obj.getfld(col_defn.scale_ptr)
            scale = await scale_ptr.getval()
        return scale

    def get_val_for_where(self):
        return self._value  # not tested

class Date(Field):
    async def check_val(self, value):
        if value is None:
            return None
        if isinstance(value, dt):
            return value
        try:
            # assumes value is 'yyyy-mm-dd'
            return dt(*map(int, value.split('-')))
        except ValueError:
            raise AibError(head=self.col_defn.short_descr,
                body='{}.{} - "{}" is not a valid date'.format(
                    self.table_name, self.col_name, value))

    async def get_dflt(self, from_init=False):
        dflt_val = await Field.get_dflt(self, from_init)
        if isinstance(dflt_val, str):
            if dflt_val.lower() == 'today':
                return dt.today()
        return dflt_val

    async def str_to_val(self, value):
        if value in (None, ''):
            return None
        try:
            # value must be 'yyyy-mm-dd'
            return dt(*map(int, value.split('-')))
        except ValueError:
            raise AibError(head=self.col_defn.short_descr,
                body='{}.{} - "{}" is not a valid date'.format(
                    self.table_name, self.col_name, value))

    async def val_to_str(self, value=blank):
        try:
            await self.db_obj.check_perms('view', self)
        except AibDenied:
            return '*'
        if value is blank:
            value = await self.getval()
        if value is None:
            return ''
        return '{:%Y-%m-%d}'.format(value)  # 'yyyy-mm-dd' - works for dt and dtm

    async def prev_to_str(self):
        try:
            await self.db_obj.check_perms('view', self)
        except AibDenied:
            return '*'
        if self._prev is None:
            return ''
        return '{:%Y-%m-%d}'.format(self._prev)  # 'yyyy-mm-dd' - works for dt and dtm

    async def get_val_from_sql(self, value):
        return await self.check_val(value)
        # if value is None:
        #     return None
        # if isinstance(value, dtm):  # Sql Server returns a datetime object
        #     return dt(value.year, value.month, value.day)
        # if isinstance(value, str):  # sqlite3 can return a string
        #     try:  # value must be 'yyyy-mm-dd'
        #         return dt(*map(int, value.split('-')))
        #     except ValueError:
        #         raise AibError(head=self.col_defn.short_descr,
        #             body='{}.{} - "{}" is not a valid date'.format(
        #                 self.table_name, self.col_name, value))
        # return value

    async def get_val_for_sql(self):
        """
        MS Sql Server only accepts datetime objects, not date objects.
        [Actually ceODBC does, but pyodbc does not].
        It *does* accept a string of 'yyyy-mm-dd'.
        Luckily, PostgreSQL and sqlite3 accept this as well.
        """
        return None if self._value is None else str(self._value)  # 'yyyy-mm-dd'

    def get_val_for_where(self):
        return None if self._value is None else repr(str(self._value))  # "'yyyy-mm-dd'"

class DateTime(Field):
    async def get_dflt(self, from_init=False):
        dflt_val = await Field.get_dflt(self, from_init)
        if dflt_val is not None:
            if dflt_val.lower() == 'now':
                return dtm.now()
        return dflt_val

    async def check_val(self, value):
        if value is None:
            return None
        if not isinstance(value, dtm):
            errmsg = '{}.{} - not a valid datetime object'.format(
                self.table_name, self.col_name)
            raise AibError(head=self.col_defn.short_descr, body=errmsg)
        return value

    async def str_to_val(self, value):
        if value in (None, ''):
            return None
        else:
            raise NotImplementedError

    async def val_to_str(self, value=blank):
        try:
            await self.db_obj.check_perms('view', self)
        except AibDenied:
            return '*'
        if value is blank:
            value = await self.getval()
        if value is None:
            return ''
        return '{:%Y-%m-%d %H:%M:%S}'.format(value)

    async def prev_to_str(self):
        try:
            await self.db_obj.check_perms('view', self)
        except AibDenied:
            return '*'
        if self._prev is None:
            return ''
        return '{:%Y-%m-%d %H:%M:%S}'.format(self._prev)

    def get_val_for_where(self):
        raise NotImplementedError

class Boolean(Field):
    async def get_dflt(self, from_init=False):
        dflt_val = await Field.get_dflt(self, from_init)
        if dflt_val is None:
            if self.col_defn.allow_null:  # don't know if this is correct
                return None
            else:
                return False
        if isinstance(dflt_val, bool):  # can happen if dflt_val is {table_name.col_name}
            return dflt_val
        if isinstance(dflt_val, str):
            if dflt_val.lower() == 'true':
                return True
            if dflt_val.lower() == 'false':
                return False
        errmsg = f'{self.table_name}.{self.col_name} {dflt_val!r} - not a valid boolean value'
        raise AibError(head=self.col_defn.short_descr, body=errmsg)

    async def check_val(self, value):
        if value in (0, 1):
            return bool(value)
        if value in (None, True, False):
            return value
        if value in ('0', '1'):
            return bool(int(value))
        errmsg = f'{self.table_name}.{self.col_name} {value!r} - not a valid boolean value'
        raise AibError(head=self.col_defn.short_descr, body=errmsg)

    async def str_to_val(self, value):
        if value in (None, ''):
            return False  # None (any implications? 14/12/2012)
        else:
            return bool(int(value))

    async def val_to_str(self, value=blank):
        try:
            await self.db_obj.check_perms('view', self)
        except AibDenied:
            return '*'
        if value is blank:
            value = await self.getval()
        if value is None:
            return ''
        return str(int(value))

    async def prev_to_str(self):
        try:
            await self.db_obj.check_perms('view', self)
        except AibDenied:
            return '*'
        if self._prev is None:
            return ''
        return str(int(self._prev))

    async def get_val_for_sql(self):
        return '1' if self._value else '0'

    async def get_val_for_xml(self):
        if self._value is None:
            return None
        if self._value:
            value = 'true'
        else:
            value = 'false'
        if value == self.col_defn.dflt_val:
            return None
        return value

    async def get_val_from_xml(self, value):
        if value is None:
            value = self.col_defn.dflt_val
        if value is None:
            return None
        elif value == 'true':
            return True
        else:
            return False

    def get_val_for_where(self):
        return None if self._value is None else str(int(self._value)) # '1' or '0'

#-----------------------------------------------------------------------------

# map of data_types to class definitions
DATA_TYPES = {
    'TEXT' :Text,
    'PWD'  :Password,
    'INT'  :Integer,
    'DEC'  :Decimal,
    'DTE'  :Date,
    'DTM'  :DateTime,
    'BOOL' :Boolean,
    'JSON' :Json,
    'FXML' :FormXml,
    'PXML' :ProcessXml,
    'SXML' :StringXml,
    'AUTO' :Integer,
    }
