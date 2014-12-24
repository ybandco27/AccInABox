import asyncio
from lxml import etree
parser = etree.XMLParser(remove_comments=True, remove_blank_text=True)

import db.api
import ht.form_xml
from db.validation_xml import check_rule
from errors import AibError
from start import log, debug

#----------------------------------------------------------------------------

NEG_DISPLAY = 'r'  # d=default, r=minus sign on right, b=angle brackets
                   # how about an option for 'red'?

DATE_INPUT = '%d-%m-%Y'
DATE_DISPLAY = '%a %d %b %Y'

#----------------------------------------------------------------------------

class GuiCtrl:
    def __init__(self, parent, fld, readonly):

#       self.frame = frame
#       self.form = frame.form
        self.parent = parent
        self.fld = fld
#       self.root_id = form.root_id
#       self.form_id = form.form_id
        self.readonly = readonly
        self.col_name = fld.col_defn.col_name
        self.descr = fld.col_defn.short_descr
        self.must_validate = True
        self.hidden = False  # for 'subtype' gui objects
        self.after_input = None
        self.pwd = ''  # over-ridden with 'seed' if type is pwd
#       self.choices = None  # over-ridden if type is GuiChoice
#       fld.notify_form(self)
#       if fld._value:
#           self._redisplay()
        ref, pos = parent.form.add_obj(parent, self)
        self.ref = ref
        self.pos = pos

    def __str__(self):
        return '{}.{}'.format(self.fld.db_obj.table_name, self.col_name)

    @asyncio.coroutine
    def validate(self, temp_data):
        if debug:
            log.write('validate {} {}\n\n'.format(
                self.col_name, temp_data))
        if self.hidden:  # unused subtype fields
            return

        """
        if self.ref in temp_data:
#           self.fld.setval(self.fld.str_to_val(
#               temp_data[self.ref]))  # can raise AibError
#           del temp_data[self.ref]  # only delete if previous line passes
            value = temp_data[self.ref]
            del temp_data[self.ref]
            yield from self.fld.setval_async(self.fld.str_to_val(value))  # can raise AibError
#       else:  # not in temp_data - get current value, or if None, default value
##          value = self.fld.getval()
##          if value is None:
##              if self.fld.col_defn.dflt_val is not None:
##                  value = self.fld.get_dflt(self.fld.col_defn.dflt_val)
##              else:
##                  value = self.fld.str_to_val('')
#           value = self.fld.get_dflt()
#           self.fld.setval(value)  # can raise AibError
        else:  # not in temp_data - use current value
            yield from self.fld.setval_async(self.fld.getval())  # can raise AibError
        """

        if self.ref in temp_data:  # user has entered a value
            value = self.fld.str_to_val(temp_data[self.ref])
            del temp_data[self.ref]
        else:  # not in temp_data - get current value, or if None, default value
            value = self.fld.getval()
            if value is None:
                value = self.fld.get_dflt()
        prev_value = self.fld.getval()
        yield from self.fld.setval_async(value)  # can raise AibError

#       if self.after_input is not None:  # steps to perform after input
#           self.fld._prev_value = prev_value
#           yield from ht.form_xml.after_input(self)

    def _redisplay(self):  # must only be called from db module
        if self.pwd:
            return  # do not send password back to client
        value = self.fld.val_to_str()  # prepare value for display
        if hasattr(self.parent, 'current_row'):  # grid object
            if self.parent.current_row is None:
                return  # entered in grid, then repos to existing row!
            value = (self.parent.current_row, value)
        self.parent.session.request.obj_to_redisplay.append((self.ref, value))

    def set_readonly(self, state):
        if state != self.readonly:
            self.parent.session.request.obj_to_set_readonly.append((self.ref, state))
            self.readonly = state

    def enable(self, state):
        self.parent.session.request.send_enable(self.ref, state)

    def show(self, state):
        self.parent.session.request.send_show(self.ref, state)

class GuiTextCtrl(GuiCtrl):
    def __init__(self, parent, fld, reverse, readonly, choices, lkup,
            pwd, lng, height, gui):
        GuiCtrl.__init__(self, parent, fld, readonly)
        self.pwd = pwd

        if lng != 0:  # if not, do not create a gui object
            value = fld.val_to_str()  #fld.get_dflt())
            if choices is not None:
                type = 'choice'
                if value == '':
                    value = choices[1][0][0]
            else:
                type = 'text'
            input = {'type': type, 'lng': lng,
                'maxlen': fld.col_defn.max_len, 'ref': self.ref,
                'help_msg': fld.col_defn.long_descr,
                'head': fld.col_defn.col_head, 'allow_amend': fld.col_defn.allow_amend,
                'password': self.pwd, 'readonly': readonly, 'lkup': lkup,
                'choices': choices, 'height': height, 'value': value}
            gui.append(('input', input))
        else:
            self.readonly = True

    @asyncio.coroutine
    def on_req_lookup(self, value):  # user selected 'lookup'
        # TO DO - block if db_obj exists and fld not amendable
        tgt_obj = self.fld.foreign_key['tgt_field'].db_obj
        form_name = 'grid_lookup'
        data_inputs = {'start_val': value}
        sub_form = ht.form.Form(self.parent.form.company, form_name,
            parent=self.parent, data_inputs=data_inputs,
            callback=(self.on_selected,))
        yield from sub_form.start_form(self.parent.session,
            db_obj=tgt_obj, cursor=tgt_obj.db_table.default_cursor,
            formdefn_company='_sys')

    @asyncio.coroutine
    def on_selected(self, caller, state, output_params):
        if state == 'completed':
            tgt_fld = self.fld.foreign_key['tgt_field']
            if tgt_fld.db_obj.exists:
                yield from self.fld.setval_async(tgt_fld.getval())

    @asyncio.coroutine
    def on_req_lookdown(self):  # user selected 'lookdown'
        tgt_obj = self.fld.foreign_key['tgt_field'].db_obj
        if tgt_obj.exists:
#           form_name = 'setup_form'
            form_name = tgt_obj.db_table.setup_form
            data_inputs = {}  # input parameters to be passed to sub-form
            data_inputs['db_obj'] = tgt_obj
            sub_form = ht.form.Form(self.parent.form.company,
                form_name, parent=self.parent, data_inputs=data_inputs)
            yield from sub_form.start_form(self.parent.session)

class GuiNumCtrl(GuiCtrl):
    def __init__(self, parent, fld, reverse, readonly, choices, fkey,
            pwd, lng, height, gui):
        GuiCtrl.__init__(self, parent, fld, readonly)
        if lng != 0:
            value = fld.val_to_str()  #fld.get_dflt())
            input = {'type': 'num', 'lng': lng, 'ref': self.ref,
                'help_msg': fld.col_defn.long_descr,
                'head': fld.col_defn.col_head, 'allow_amend': fld.col_defn.allow_amend,
                'readonly': readonly, 'reverse': reverse, 'value': value,
                'integer': (fld.col_defn.data_type == 'INT'),
                'max_decimals': fld.col_defn.db_scale, 'neg_display': NEG_DISPLAY}
            gui.append(('input', input))
        else:
            self.readonly = True

class GuiDateCtrl(GuiCtrl):
    def __init__(self, parent, fld, reverse, readonly, choices, fkey,
            pwd, lng, height, gui):
        GuiCtrl.__init__(self, parent, fld, readonly)
        if lng != 0:
            value = fld.val_to_str()  #fld.get_dflt())
            input = {'type': 'date', 'lng': lng, 'ref': self.ref,
                'help_msg': fld.col_defn.long_descr,
                'head': fld.col_defn.col_head, 'allow_amend': fld.col_defn.allow_amend,
                'readonly': readonly, 'value': value,
                'input_format': DATE_INPUT, 'display_format': DATE_DISPLAY}
            gui.append(('input', input))
        else:
            self.readonly = True

class GuiBoolCtrl(GuiCtrl):
    def __init__(self, parent, fld, reverse, readonly, choices, fkey,
            pwd, lng, height, gui):
        GuiCtrl.__init__(self, parent, fld, readonly)
        if lng != 0:
            value = fld.val_to_str()  #fld.get_dflt())
            input = {'type': 'bool', 'lng': lng, 'ref': self.ref, 'value': value,
                'help_msg': fld.col_defn.long_descr, 'head': fld.col_defn.col_head,
                'allow_amend': fld.col_defn.allow_amend, 'readonly': readonly}
            gui.append(('input', input))
        else:
            self.readonly = True

class GuiSxmlCtrl(GuiCtrl):
    def __init__(self, parent, fld, reverse, readonly, choices, fkey,
            pwd, lng, height, gui):
        GuiCtrl.__init__(self, parent, fld, readonly)
        if lng != 0:
            value = fld.val_to_str()  #fld.get_dflt())
            input = {'type': 'sxml', 'lng': lng, 'ref': self.ref, 'value': value,
                'help_msg': fld.col_defn.long_descr, 'head': fld.col_defn.col_head,
                'allow_amend': fld.col_defn.allow_amend, 'readonly': readonly}
            gui.append(('input', input))
        else:
            self.readonly = True

class GuiDisplay:
    def __init__(self, parent, fld):
#       self.request = form.request
#       self.root_id = form.root_id
#       self.form_id = form.form_id
#       self.frame = frame
#       self.form = frame.form
        self.parent = parent
        self.fld = fld
        self.col_name = fld.col_defn.col_name
        self.must_validate = True
        self.hidden = False  # for 'subtype' gui objects
        self.after_input = None
#       fld.notify_form(self)
#       if fld._value:
#           self._redisplay(fld._value)
        ref, pos = parent.form.add_obj(parent, self)
        self.ref = ref
        self.pos = pos

    def __str__(self):
        return '{}.{}'.format(self.fld.db_obj.table_name, self.col_name)

    @asyncio.coroutine
    def validate(self, temp_data, tab=False):
        pass

    def set_readonly(self, state):
        pass

    def _redisplay(self):
        if self.hidden:
            return  # do not send hidden objects back to client
        value = self.fld.val_to_str()  # prepare value for display
        if hasattr(self.parent, 'current_row'):  # grid object
            value = (self.parent.current_row, value)
        self.parent.session.request.obj_to_redisplay.append((self.ref, value))

    def show(self, state):
        self.parent.session.request.sendShow(self.ref, state)

class GuiDummy:  # dummy field to force validation of last real field
    def __init__(self, parent, gui):
        self.parent = parent
        self.pwd = ''
        self.choices = None
        self.must_validate = True
        self.vld_rules = []
        self.after_input = None
        self.col_name = 'dummy'
        ref, pos = parent.form.add_obj(parent, self)
        self.ref = ref
        self.pos = pos
        gui.append(('dummy', {'type': 'dummy', 'ref': self.ref,
            'lng': None, 'help_msg': '', 'value': ''}))

    def __str__(self):
        return 'dummy'

    @asyncio.coroutine
    def validate(self, temp_data, tab=False):
#       if self.vld_rules is not None:  # validations to perform after input
#           try:
#               check_rules(self, 'Dummy field', None)
#           except AibError:
#               self.parent.session.request.send_set_focus(self.ref)
#               raise

        for rule in self.vld_rules:  # 'rule' is a tuple of (ctx, xml)
            yield from check_rule(self, 'Dummy', rule, None)

#       if self.after_input is not None:  # steps to perform after input
#           yield from ht.form_xml.after_input(self)

class GuiButton:
#   def __init__(self, parent, gui, element):
    def __init__(self, parent, gui, btn_label, lng, enabled,
            must_validate, default, help_msg, btn_action):
#       self.root_id = form.root_id
#       self.form_id = form.form_id
        self.parent = parent
#       self.xml = element
#       self.xml = etree.fromstring(element.get('btn_action'), parser=parser)
        self.xml = btn_action
        ref, pos = parent.form.add_obj(parent, self)
        self.ref = ref
        self.pos = pos

#       self.enabled = (element.get('btn_enabled') == 'true')
#       self.must_validate = (element.get('btn_validate') == 'true')
#       self.default = (element.get('btn_default') == 'true')
#       self.label = element.get('btn_label')
#       help_msg = element.get('help_msg', '')
        self.after_input = None
        self.enabled = enabled
        self.must_validate = must_validate
        self.default = default
        self.label = btn_label
        self.show = True
        gui.append(('button', {'label':self.label, 'lng':lng, 'ref':self.ref,
            'enabled':self.enabled, 'default':self.default, 'help_msg':help_msg}))

    def __str__(self):
        return "Button: '{}'".format(self.label)

    @asyncio.coroutine
    def validate(self, temp_data, tab=False):
        pass

    def change_button(self, attr, value):
        # attr can be enabled/default/label/show
        setattr(self, attr, value)
        self.parent.session.request.obj_to_redisplay.append((self.ref, (attr, value)))

"""
class GuiToolBar:
    def __init__(self, task, ref):
        self.task = task
        self.ref = ref
        self.obj_list = []

    def validate(self, temp_data):
        pass
"""

"""
class GuiNbButton:  # Notebook button (prev/next page)
    # there is no click() event associated with these buttons
    # they are required so that, if they get focus, they trigger
    #   validations of all controls up to that point
    def __init__(self, parent, element):
#       self.root_id = form.root_id
#       self.form_id = form.form_id
#       self.frame = frame
        self.xml = element
        self.must_validate = False
        ref, pos = parent.form.add_obj(parent, self)
        self.ref = ref
        self.pos = pos

    def __str__(self):
        return 'Notebook button'

    def validate(self, temp_data, tab=False):
        pass
"""

class GuiTbButton:  # Toolbar button
    def __init__(self, parent, element):
#       self.root_id = form.root_id
#       self.form_id = form.form_id
#       self.frame = frame
        self.parent = parent
        self.xml = element
        ref, pos = parent.form.add_obj(parent, self, add_to_list=False)
        self.ref = ref
        #self.pos = pos

    def validate(self, temp_data):
        pass

class GuiTbText:
    def __init__(self, formRef, ref, task):
        self.formRef = formRef
        self.ref = ref
    def setValue(self, value):
        self.parent.obj_to_redisplay.append((self.formRef, self.ref, value))

#class GuiTree:
#   def __init__(self, task, ref):
#       self.task = task
#       self.ref = ref
#       self.root_id = task.root.root_id
#       self.treeData = {}
#       self.must_validate = False
#       self.descr = 'Tree'

#   def validate(self, temp_data):
#       pass

class GuiTree:
    def __init__(self, formRef, ref, task):
        self.formRef = formRef
        self.ref = ref
        self.task = task
        self.root_id = task.root_id
        self.form_id = task.task_id
        self.treeData = {}
        self.must_validate = False
        self.descr = 'Tree'

    def validate(self, temp_data):
        pass

#----------------------------------------------------------------------------

gui_ctrls = {
    'TEXT'  : (GuiTextCtrl),
    'INT'   : (GuiNumCtrl),
    'DEC'   : (GuiNumCtrl),
    'DTE'   : (GuiDateCtrl),
    'DTM'   : (GuiDateCtrl),
    'BOOL'  : (GuiBoolCtrl),
    'JSON'  : (GuiTextCtrl),
    'SXML'  : (GuiSxmlCtrl)
    }
