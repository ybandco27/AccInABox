dbcols_sys = """
<form name="">
  <db_objects>
    <db_obj name="db_table" table_name="db_tables" fkey="db_obj.table_id"/>
  </db_objects>
  <mem_objects/>
  <input_params/>
  <output_params/>
  <rules/>
  <frame main_object="db_obj">
    <toolbar/>
    <body>
      <block/>
      <panel/>
      <row/>
      <col/>
      <label value="Table name:"/>
      <col/>
      <display fld="db_table.table_name" lng="120"/>
      <col/>
      <label value="Description:"/>
      <col/>
      <display fld="db_table.short_descr" lng="160"/>
      <row/>
      <col/>
      <label value="Column name:"/>
      <col/>
      <input fld="db_obj.col_name" lng="120"/>
      <col/>
      <label value="Description:"/>
      <col/>
      <input fld="db_obj.short_descr" lng="150"/>
      <row/>
      <col/>
      <label value="Data type:"/>
      <col/>
      <input fld="db_obj.data_type" lng="160"/>
      <col/>
      <label value="Col heading:"/>
      <col/>
      <input fld="db_obj.col_head" lng="120"/>
      <row/>
      <col/>
      <label value="Long description:"/>
      <col rowspan="3" colspan="3"/>
      <input fld="db_obj.long_descr" lng="300" height="3"/>
      <block/>
      <panel/>
      <row/>
      <col/>
      <label value="Key field?"/>
      <input fld="db_obj.key_field" lng="100"/>
      <col/>
      <label value="Generated?"/>
      <input fld="db_obj.generated"/>
      <col/>
      <label value="Allow null?"/>
      <input fld="db_obj.allow_null"/>
      <col/>
      <label value="Allow amend?"/>
      <input fld="db_obj.allow_amend"/>
      <row/>
      <col/>
      <label value="Max length"/>
      <input fld="db_obj.max_len" lng="40"/>
      <col/>
      <label value="Scale"/>
      <input fld="db_obj.db_scale" lng="40"/>
      <col/>
      <label value="Scale param"/>
      <input fld="db_obj.scale_ptr" lng="60"/>
      <col/>
      <label value="Default value"/>
      <input fld="db_obj.dflt_val" lng="60"/>
      <row/>
      <col/>
      <button lng="100" btn_id="chk" btn_label="Col checks"
          btn_enabled="true" btn_validate="true" btn_action="
        <<action>>
          <<sub_form form_name=`col_checks`>>
            <<call_params>>
              <<call_param name=`col_chks` type=`data_attr`
                source=`db_obj.col_chks`/>>
            <</call_params>>
            <<return_params>>
              <<return_param name=`col_chks` type=`data_attr`
                target=`db_obj.col_chks`/>>
            <</return_params>>
            <<on_return>>
              <<return state=`completed`/>>
              <<return state=`cancelled`/>>
            <</on_return>>
          <</sub_form>>
        <</action>>
      "/>
      <col/>
      <button lng="100" btn_id="fkey" btn_label="Foreign key"
          btn_enabled="true" btn_validate="true" btn_action="
        <<action>>
          <<sub_form form_name=`foreign_key`>>
            <<call_params>>
              <<call_param name=`fkey` type=`data_attr` source=`db_obj.fkey`/>>
            <</call_params>>
            <<return_params>>
              <<return_param name=`fkey` type=`data_attr` target=`db_obj.fkey`/>>
            <</return_params>>
            <<on_return>>
              <<return state=`completed`/>>
              <<return state=`cancelled`/>>
            <</on_return>>
          <</sub_form>>
        <</action>>
      "/>
      <col/>
      <button lng="100" btn_id="sub" btn_label="Choices"
          btn_enabled="true" btn_validate="true" btn_action="
        <<action>>
          <<sub_form form_name=`choices`>>
            <<call_params>>
              <<call_param name=`table_name` type=`data_attr` source=`db_table.table_name`/>>
              <<call_param name=`col_name` type=`data_attr` source=`db_obj.col_name`/>>
              <<call_param name=`choices` type=`data_attr` source=`db_obj.choices`/>>
            <</call_params>>
            <<return_params>>
              <<return_param name=`choices` type=`data_attr` target=`db_obj.choices`/>>
            <</return_params>>
            <<on_return>>
              <<return state=`completed`/>>
              <<return state=`cancelled`/>>
            <</on_return>>
          <</sub_form>>
        <</action>>
      "/>
      <col/>
      <button lng="100" btn_id="sql" btn_label="SQL"
          btn_enabled="true" btn_validate="true" btn_action="
        <<action>>
          <<sub_form form_name=`sql`>>
            <<call_params/>>
            <<return_params/>>
            <<on_return/>>
          <</sub_form>>
        <</action>>
      "/>
    </body>
    <button_row validate="true" template="Setup_Form"/>
    <frame_methods template="Setup_Form">
      <method name="do_save" action="
        <<action>>
          <<assign>>
            <<source>>sys<</source>>
            <<target>>db_obj.col_type<</target>>
          <</assign>>
          <<assign>>
            <<source>>$current_row<</source>>
            <<target>>db_obj.seq<</target>>
          <</assign>>
          <<save_obj obj_name=`db_obj`/>>
        <</action>>
      "/>
    </frame_methods>
  </frame>

</form>
"""
