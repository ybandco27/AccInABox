table_formview = """
<form name="">
  <db_objects>
    <db_obj name="db_col_sys" table_name="db_columns" parent="db_obj"/>
    <db_obj name="db_col_user" table_name="db_columns" parent="db_obj"/>
    <db_obj name="db_col_virt" table_name="db_columns" parent="db_obj"/>
    <db_obj name="db_cur" table_name="db_cursors" parent="db_obj"/>
  </db_objects>
  <mem_objects/>
  <input_params/>
  <output_params/>
  <rules/>
  <frame>
    <toolbar/>
    <body>
      <block/>
      <panel/>
      <row/>
      <col/>
      <label value="Table name:"/>
      <col colspan="3"/>
      <input fld="db_obj.table_name" lng="150"/>
      <row/>
      <col/>
      <label value="Short description:"/>
      <col colspan="3"/>
      <input fld="db_obj.short_descr" lng="200"/>
      <row/>
      <col/>
      <label value="Long description:"/>
      <col colspan="3"/>
      <input fld="db_obj.long_descr" lng="300" height="5"/>
      <row/>
      <col/>
      <label value="Keep audit trail?"/>
      <input fld="db_obj.audit_trail"/>
      <row/>
      <col/>
      <label value="Definition company:"/>
      <col/>
      <input fld="db_obj.defn_company" lng="120"/>
      <row/>
      <col/>
      <label value="Data company:"/>
      <col/>
      <input fld="db_obj.data_company" lng="120"/>
      <label value="Read only?"/>
      <input fld="db_obj.read_only"/>
      <row/>
      <col/>
      <col/>
      <col/>
      <button btn_id="pre_save" btn_label="Save header"
        help_msg = "Save header before proceeding"
        btn_enabled="true" btn_validate="true" btn_action="
          <<action>>
            <<save_obj obj_name=`db_obj`/>>
            <<change_button>>
              <<btn_dflt btn_id=`btn_rgt`/>>
            <</change_button>>
            <<change_button>>
              <<btn_show btn_id=`pre_save` state=`false`/>>
            <</change_button>>
            <<case>>
              <<compare src=`db_obj.audit_trail` op=`eq` tgt=`$True`>>
                <<pyfunc name=`db.db_xml.setup_audit_cols`/>>
              <</compare>>
            <</case>>
            <<case>>
              <<compare src=`db_obj.defn_company` op=`is_` tgt=`$None`>>
                <<change_button>>
                  <<btn_enabled btn_id=`upd_chk` state=`true`/>>
                <</change_button>>
                <<change_button>>
                  <<btn_enabled btn_id=`del_chk` state=`true`/>>
                <</change_button>>
                <<change_button>>
                  <<btn_enabled btn_id=`db_col` state=`true`/>>
                <</change_button>>
                <<change_button>>
                  <<btn_enabled btn_id=`db_cur` state=`true`/>>
                <</change_button>>
                <<change_button>>
                  <<btn_enabled btn_id=`db_hook` state=`true`/>>
                <</change_button>>
                <<change_button>>
                  <<btn_enabled btn_id=`form_defn` state=`true`/>>
                <</change_button>>
              <</compare>>
            <</case>>
          <</action>>
        "/>

      <dummy
        validation="
          <<validations>>
            <<validation>>
              <<case>>
                <<obj_exists obj_name=`db_obj`/>>
                <<default>>
                  <<error head=`Error` body=`Header not saved`/>>
                <</default>>
              <</case>>
            <</validation>>
          <</validations>>
        "/>

      <block/>
      <panel/>
      <row/>
      <col/>
      <button lng="150" btn_id="upd_chk" btn_label="Update checks"
        btn_enabled="true" btn_validate="true" btn_action="
          <<action>>
          <</action>>
        "/>
      <col/>
      <button lng="150" btn_id="del_chk" btn_label="Delete checks"
        btn_enabled="true" btn_validate="true" btn_action="
          <<action>>
          <</action>>
        "/>
      <row/>
      <col/>
      <button lng="150" btn_id="db_col" btn_label="Db columns"
        btn_enabled="true" btn_validate="true" btn_action="
          <<action>>
            <<inline_form form_name=`Db columns`/>>
          <</action>>
        "/>
      <col/>
      <button lng="150" btn_id="db_cur" btn_label="Db cursors"
        btn_enabled="true" btn_validate="true" btn_action="
          <<action>>
            <<sub_form form_name=`cursor_grid`>>
              <<call_params>>
                <<call_param name=`db_table` type=`data_obj` source=`db_obj`/>>
              <</call_params>>
              <<return_params/>>
              <<on_return>>
                <<return state=`cancelled`/>>
                <<return state=`completed`/>>
              <</on_return>>
           <</sub_form>>
          <</action>>
        "/>
      <row/>
      <col/>
      <button lng="150" btn_id="db_hook" btn_label="Table hooks"
        btn_enabled="true" btn_validate="true" btn_action="
          <<action>>
          <</action>>
        "/>
      <col/>
      <button lng="150" btn_id="form_defn" btn_label="Form definition"
        btn_enabled="true" btn_validate="true" btn_action="
          <<action>>
            <<inline_form form_name=`Form setup`/>>
          <</action>>
        "/>
    </body>
    <button_row validate="true">
      <button btn_id="create_table" btn_label="Create table" btn_enabled="true"
        btn_validate="true" btn_default="false" btn_action="
          <<action>>
            <<pyfunc name=`db.db_xml.create_table`/>>
            <<assign>>
              <<source>>$True<</source>>
              <<target>>db_obj.table_created<</target>>
            <</assign>>
            <<save_obj obj_name=`db_obj`/>>
            <<change_button>>
              <<btn_enabled btn_id=`create_table` state=`false`/>>
            <</change_button>>
          <</action>>
        " help_msg="Set up table in database"/>
      </button_row>
      <frame_methods>
        <method name="on_start_form" action="
          <<action>>
            <<case>>
              <<obj_exists obj_name=`db_obj`>>
                <<change_button>>
                  <<btn_dflt btn_id=`btn_rgt`/>>
                <</change_button>>
                <<change_button>>
                  <<btn_show btn_id=`pre_save` state=`false`/>>
                <</change_button>>
                <<case>>
                  <<compare src=`db_obj.defn_company` op=`is_` tgt=`$None`>>
                    <<change_button>>
                      <<btn_enabled btn_id=`upd_chk` state=`true`/>>
                    <</change_button>>
                    <<change_button>>
                      <<btn_enabled btn_id=`del_chk` state=`true`/>>
                    <</change_button>>
                    <<change_button>>
                      <<btn_enabled btn_id=`db_col` state=`true`/>>
                    <</change_button>>
                    <<change_button>>
                      <<btn_enabled btn_id=`db_cur` state=`true`/>>
                    <</change_button>>
                    <<change_button>>
                      <<btn_enabled btn_id=`db_hook` state=`true`/>>
                    <</change_button>>
                    <<change_button>>
                      <<btn_enabled btn_id=`form_defn` state=`true`/>>
                    <</change_button>>
                  <</compare>>
                  <<default>>
                    <<change_button>>
                      <<btn_enabled btn_id=`upd_chk` state=`false`/>>
                    <</change_button>>
                    <<change_button>>
                      <<btn_enabled btn_id=`del_chk` state=`false`/>>
                    <</change_button>>
                    <<change_button>>
                      <<btn_enabled btn_id=`db_col` state=`false`/>>
                    <</change_button>>
                    <<change_button>>
                      <<btn_enabled btn_id=`db_cur` state=`false`/>>
                    <</change_button>>
                    <<change_button>>
                      <<btn_enabled btn_id=`db_hook` state=`false`/>>
                    <</change_button>>
                    <<change_button>>
                      <<btn_enabled btn_id=`form_defn` state=`false`/>>
                    <</change_button>>
                  <</default>>
                <</case>>
              <</obj_exists>>
              <<default>>
                <<change_button>>
                  <<btn_show btn_id=`pre_save` state=`true`/>>
                <</change_button>>
                <<change_button>>
                  <<btn_dflt btn_id=`pre_save`/>>
                <</change_button>>
                <<change_button>>
                  <<btn_enabled btn_id=`upd_chk` state=`false`/>>
                <</change_button>>
                <<change_button>>
                  <<btn_enabled btn_id=`del_chk` state=`false`/>>
                <</change_button>>
                <<change_button>>
                  <<btn_enabled btn_id=`db_col` state=`false`/>>
                <</change_button>>
                <<change_button>>
                  <<btn_enabled btn_id=`db_cur` state=`false`/>>
                <</change_button>>
                <<change_button>>
                  <<btn_enabled btn_id=`db_hook` state=`false`/>>
                <</change_button>>
                <<change_button>>
                  <<btn_enabled btn_id=`form_defn` state=`false`/>>
                <</change_button>>
              <</default>>
            <</case>>
            <<case>>
              <<compare src=`db_obj.table_created` op=`eq` tgt=`$True`>>
                <<change_button>>
                  <<btn_enabled btn_id=`create_table` state=`false`/>>
                <</change_button>>
              <</compare>>
              <<default>>
                <<change_button>>
                  <<btn_enabled btn_id=`create_table` state=`true`/>>
                <</change_button>>
              <</default>>
            <</case>>
          <</action>>
        "/>
      </frame_methods>
  </frame>

  <inline_form form_name="Db columns">
    <frame main_object="db_obj">
      <toolbar/>
      <body>
        <block/>
        <panel/>
        <row/>
        <col/>
        <text value="Table:"/>
        <col/>
        <display fld="db_obj.table_name" lng="160"/>
        <col/>
        <text value="Description:"/>
        <col/>
        <display fld="db_obj.short_descr" lng="250"/>
        <block/>
        <nb_start/>
        <nb_page label="System Columns"/>
        <block/>
        <grid data_object="db_col_sys" growable="true"
            num_grid_rows="10" form_name="dbcols_sys">
          <toolbar template="Setup_Grid"/>
          <cur_columns>
            <cur_col col_name="col_name" lng="120"/>
            <cur_col col_name="short_descr" lng="200" expand="true"/>
          </cur_columns>
          <cur_filter>
            <cur_fil test="where" lbr="" col_name="col_type" op="=" expr="sys" rbr=""/>
          </cur_filter>
          <cur_sequence>
            <cur_seq col_name="seq" desc="false"/>
          </cur_sequence>
          <grid_methods template="Setup_Grid"/>
        </grid>
        <nb_page label="User Columns"/>
        <block/>
        <grid data_object="db_col_user" growable="true"
            num_grid_rows="10" form_name="dbcols_user">
          <toolbar template="Setup_Grid"/>
          <cur_columns>
            <cur_col col_name="col_name" lng="120"/>
            <cur_col col_name="short_descr" lng="200" expand="true"/>
          </cur_columns>
          <cur_filter>
            <cur_fil test="where" lbr="" col_name="col_type" op="=" expr="user" rbr=""/>
          </cur_filter>
          <cur_sequence>
            <cur_seq col_name="seq" desc="false"/>
          </cur_sequence>
          <grid_methods template="Setup_Grid"/>
        </grid>
        <nb_page label="Virtual Columns"/>
        <block/>
        <grid data_object="db_col_virt" growable="true"
            num_grid_rows="10" form_name="dbcols_virt">
          <toolbar template="Setup_Grid"/>
          <cur_columns>
            <cur_col col_name="col_name" lng="120"/>
            <cur_col col_name="short_descr" lng="200" expand="true"/>
          </cur_columns>
          <cur_filter>
            <cur_fil test="where" lbr="" col_name="col_type" op="=" expr="virt" rbr=""/>
          </cur_filter>
          <cur_sequence>
            <cur_seq col_name="seq" desc="false"/>
          </cur_sequence>
          <grid_methods template="Setup_Grid"/>
        </grid>
        <nb_end/>
      </body>
      <button_row validate="true">
        <button btn_id="btn_close" btn_label="Close" btn_enabled="true"
            btn_validate="true" btn_default="true" lng="60" btn_action="
          <<action>>
            <<call method=`on_req_cancel`/>>
          <</action>>
        "/>
      </button_row>
      <frame_methods>
        <method name="on_req_cancel" action="
          <<action>>
            <<end_form state=`completed`/>>
          <</action>>
        "/>
        <method name="on_req_close" action="
          <<action>>
            <<end_form state=`completed`/>>
          <</action>>
        "/>
      </frame_methods>
    </frame>
  </inline_form>
<!--
  <inline_form form_name="Db cursors">
    <frame main_object="db_obj">
      <toolbar/>
      <body>
        <block/>
        <panel/>
        <row/>
        <col/>
        <text value="Table:"/>
        <col/>
        <display fld="db_obj.table_name" lng="160"/>
        <col/>
        <text value="Description:"/>
        <col/>
        <display fld="db_obj.short_descr" lng="250"/>
        <block/>
        <grid data_object="db_cur" growable="true" num_grid_rows="3"
            form_name="db_cursor">
          <toolbar template="Setup_Form"/>
          <cur_columns>
            <cur_col col_name="cursor_name" lng="120"/>
            <cur_col col_name="descr" lng="200" expand="true"/>
          </cur_columns>
          <cur_filter/>
          <cur_sequence>
            <cur_seq col_name="cursor_name" desc="false"/>
          </cur_sequence>
          <grid_methods template="Setup_Grid"/>
        </grid>
        <block/>
        <grid_frame main_object="db_cur">
          <toolbar template="Setup_Form"/>
          <body>
            <block/>
            <panel/>
            <row/>
            <col/>
            <label value="Cursor name:"/>
            <col/>
            <input fld="db_cur.cursor_name" lng="120"/>
            <row/>
            <col/>
            <label value="Description:"/>
            <col/>
            <input fld="db_cur.descr" lng="250"/>
            <block/>
            <panel/>
            <row/>
            <col/>
            <button lng="150" btn_id="cur_cols" btn_label="Columns"
              btn_enabled="true" btn_validate="true" btn_action="
                <<action>>
                  <<inline_form form_name=`cur_cols`/>>
                <</action>>
              "/>
            <row/>
            <col/>
            <button lng="150" btn_id="cur_filt" btn_label="Filter"
              btn_enabled="true" btn_validate="true" btn_action="
                <<action>>
                <</action>>
              "/>
            <row/>
            <col/>
            <button lng="150" btn_id="cur_seq" btn_label="Sequence"
              btn_enabled="true" btn_validate="true" btn_action="
                <<action>>
                <</action>>
              "/>
          </body>
          <button_row validate="true" template="Grid_Frame"/>
          <frame_methods/>
        </grid_frame>
      </body>
      <button_row validate="true">
        <button btn_id="btn_close" btn_label="Close" btn_enabled="true"
            btn_validate="true" btn_default="true" lng="60" btn_action="
          <<action>>
            <<call method=`on_req_cancel`/>>
          <</action>>
        "/>
      </button_row>
      <frame_methods>
        <method name="on_req_cancel" action="
          <<action>>
            <<end_form state=`completed`/>>
          <</action>>
        "/>
        <method name="on_req_close" action="
          <<action>>
            <<end_form state=`completed`/>>
          <</action>>
        "/>
      </frame_methods>
    </frame>
  </inline_form>
-->
<!--
  <inline_form form_name="cur_cols">
    <frame main_object="db_cur">
      <toolbar/>
      <body>
        <block/>
        <panel/>
        <row/>
        <col/>
        <text value="Table:"/>
        <col/>
        <display fld="db_cur.cursor_name" lng="160"/>
        <col/>
        <text value="Description:"/>
        <col/>
        <display fld="db_cur.descr" lng="250"/>
      </body>
      <frame_methods/>
    </frame>
  </inline_form>
-->
  <inline_form form_name="Form setup">

    <frame main_object="db_obj">
      <toolbar/>
      <body>
        <block/>
        <panel/>
        <row/>
        <col/>
        <label value="Table name:"/>
        <col/>
        <input fld="db_obj.table_name" lng="160"/>
        <row/>
        <col/>
        <label value="Description:"/>
        <col/>
        <input fld="db_obj.short_descr" lng="250"/>

        <block/>
        <panel/>
        <row/>
        <col/>
        <button lng="150" btn_id="dbobj" btn_label="Db objects"
            btn_enabled="true" btn_validate="true" btn_action="
          <<action>>
            <<sub_form form_name=`form_setup_dbobj`>>
              <<call_params>>
                <<call_param name=`form_name` type=`data_attr` source=`db_obj.table_name`/>>
                <<call_param name=`title` type=`data_attr` source=`Form view`/>>
                <<call_param name=`form_xml` type=`data_attr` source=`db_obj.form_xml`/>>
              <</call_params>>
              <<return_params>>
                <<return_param name=`form_xml` type=`data_attr` target=`db_obj.form_xml`/>>
              <</return_params>>
              <<on_return>>
                <<return state=`completed`/>>
                <<return state=`cancelled`/>>
              <</on_return>>
            <</sub_form>>
          <</action>>
        "/>
        <col/>
        <button lng="150" btn_id="memobj" btn_label="Memory objects"
            btn_enabled="true" btn_validate="true" btn_action="
          <<action>>
            <<sub_form form_name=`form_setup_memobj`>>
              <<call_params>>
                <<call_param name=`form_name` type=`data_attr` source=`db_obj.table_name`/>>
                <<call_param name=`title` type=`data_attr` source=`Form view`/>>
                <<call_param name=`form_xml` type=`data_attr` source=`db_obj.form_xml`/>>
              <</call_params>>
              <<return_params>>
                <<return_param name=`form_xml` type=`data_attr` target=`db_obj.form_xml`/>>
              <</return_params>>
              <<on_return>>
                <<return state=`completed`/>>
                <<return state=`cancelled`/>>
              <</on_return>>
            <</sub_form>>
          <</action>>
        "/>
        <row/>
        <col/>
        <button lng="150" btn_id="inputs" btn_label="Input parameters"
            btn_enabled="true" btn_validate="true" btn_action="
          <<action>>
            <<sub_form form_name=`form_setup_inputs`>>
              <<call_params>>
                <<call_param name=`form_name` type=`data_attr` source=`db_obj.table_name`/>>
                <<call_param name=`title` type=`data_attr` source=`Form view`/>>
                <<call_param name=`form_xml` type=`data_attr` source=`db_obj.form_xml`/>>
              <</call_params>>
              <<return_params>>
                <<return_param name=`form_xml` type=`data_attr` target=`db_obj.form_xml`/>>
              <</return_params>>
              <<on_return>>
                <<return state=`completed`/>>
                <<return state=`cancelled`/>>
              <</on_return>>
            <</sub_form>>
          <</action>>
        "/>
        <col/>
        <button lng="150" btn_id="outputs" btn_label="Output parameters"
            btn_enabled="true" btn_validate="true" btn_action="
          <<action>>
            <<sub_form form_name=`form_setup_outputs`>>
              <<call_params>>
                <<call_param name=`form_name` type=`data_attr` source=`db_obj.table_name`/>>
                <<call_param name=`title` type=`data_attr` source=`Form view`/>>
                <<call_param name=`form_xml` type=`data_attr` source=`db_obj.form_xml`/>>
              <</call_params>>
              <<return_params>>
                <<return_param name=`form_xml` type=`data_attr` target=`db_obj.form_xml`/>>
              <</return_params>>
              <<on_return>>
                <<return state=`completed`/>>
                <<return state=`cancelled`/>>
              <</on_return>>
            <</sub_form>>
          <</action>>
        "/>
        <row/>
        <col/>
        <button lng="150" btn_id="rules" btn_label="Rules"
            btn_enabled="true" btn_validate="true" btn_action="
          <<action>>
            <<sub_form form_name=`form_setup_rules`>>
              <<call_params>>
                <<call_param name=`form_name` type=`data_attr` source=`db_obj.table_name`/>>
                <<call_param name=`title` type=`data_attr` source=`Form view`/>>
                <<call_param name=`form_xml` type=`data_attr` source=`db_obj.form_xml`/>>
              <</call_params>>
              <<return_params>>
                <<return_param name=`form_xml` type=`data_attr` target=`db_obj.form_xml`/>>
              <</return_params>>
              <<on_return>>
                <<return state=`completed`/>>
                <<return state=`cancelled`/>>
              <</on_return>>
            <</sub_form>>
          <</action>>
        "/>
        <col/>
        <button lng="150" btn_id="frame" btn_label="Gui objects"
            btn_enabled="true" btn_validate="true" btn_action="
          <<action>>
            <<sub_form form_name=`form_setup_gui`>>
              <<call_params>>
                <<call_param name=`form_name` type=`data_attr` source=`db_obj.table_name`/>>
                <<call_param name=`title` type=`data_attr` source=`Form view`/>>
                <<call_param name=`form_xml` type=`data_attr` source=`db_obj.form_xml`/>>
              <</call_params>>
              <<return_params>>
                <<return_param name=`form_xml` type=`data_attr` target=`db_obj.form_xml`/>>
              <</return_params>>
              <<on_return>>
                <<return state=`completed`/>>
                <<return state=`cancelled`/>>
              <</on_return>>
            <</sub_form>>
          <</action>>
        "/>

      </body>
      <button_row validate="true" template="Setup_Form"/>
      <frame_methods template="Setup_Form"/>
    </frame>
  </inline_form>

</form>
"""
