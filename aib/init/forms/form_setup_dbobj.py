form_setup_dbobj = """
<form name="form_setup_dbobj">

  <db_objects/>
  <mem_objects>

    <mem_obj name="form" descr="Variables used in form">
      <mem_col col_name="form_name" data_type="TEXT" short_descr="Form name"
        long_descr="Form name" col_head="Name" key_field="N" allow_null="false"
        allow_amend="false" max_len="0" db_scale="0"/>
      <mem_col col_name="title" data_type="TEXT" short_descr="Title"
        long_descr="Form title" col_head="Title" key_field="N" allow_null="false"
        allow_amend="false" max_len="0" db_scale="0"/>
      <mem_col col_name="form_xml" data_type="FXML" short_descr="Form definition"
        long_descr="Form definition (xml)" col_head="Defn" key_field="N" allow_null="false"
        allow_amend="true" max_len="0" db_scale="0"/>
    </mem_obj>

    <mem_obj name="dbobj" descr="Db objects used in form" parent="form">
      <mem_col col_name="form_name" data_type="TEXT" short_descr="Form name"
        long_descr="Form name" col_head="Form name" key_field="A" allow_null="false"
        allow_amend="false" max_len="20" db_scale="0"
        fkey="[`form`, `form_name`, null, null, true]"/>
      <mem_col col_name="name" data_type="TEXT" short_descr="Object name"
        long_descr="Object name" col_head="Object" key_field="A" allow_null="false"
        allow_amend="false" max_len="20" db_scale="0"/>
      <mem_col col_name="table_name" data_type="TEXT" short_descr="Table name"
        long_descr="Table name" col_head="Table" key_field="N" allow_null="false"
        allow_amend="false" max_len="0" db_scale="0"
        fkey="[`db_tables`, `table_name`, null, null, false]"/>
    </mem_obj>

    <mem_obj name="dbhooks" descr="Table hooks for db objects" parent="dbobj">
      <mem_col col_name="dbobj_name" data_type="TEXT" short_descr="Dbobj name"
        long_descr="Dbobj name" col_head="" key_field="N" allow_null="false"
        allow_amend="false" max_len="0" db_scale="0"
        fkey="[`dbobj`, `name`, null, null, true]"/>
      <mem_col col_name="type" data_type="TEXT" short_descr="Hook type"
        long_descr="Hook type" col_head="Hook type" key_field="N" allow_null="false"
        allow_amend="false" max_len="15" db_scale="0"
        choices="[false, false, [
          [`on_setup`, `On setting up object`, [], []],
          [`after_read`, `After row selected`, [], []],
          [`after_init`, `After row initialised`, [], []],
          [`after_restore`, `After row restored`, [], []],
          [`before_save`, `Before row saved`, [], []],
          [`after_save`, `After row saved and committed`, [], []],
          [`before_insert`, `Before insert`, [], []],
          [`after_insert`, `After insert, before commit`, [], []],
          [`before_update`, `Before update`, [], []],
          [`after_update`, `After update, before commit`, [], []],
          [`before_delete`, `Before delete`, [], []],
          [`after_delete`, `After delete, before commit`, [], []]
          ]]"
        />
      <mem_col col_name="action" data_type="SXML" short_descr="Hook action"
        long_descr="Action to be performed" col_head="Action" key_field="N" allow_null="false"
        allow_amend="true" max_len="0" db_scale="0"/>
    </mem_obj>
  </mem_objects>


  <input_params>
    <input_param name="form_name" type="data_attr" target="form.form_name" required="true"/>
    <input_param name="title" type="data_attr" target="form.title" required="true"/>
    <input_param name="form_xml" type="data_attr" target="form.form_xml" required="true"/>
  </input_params>

  <output_params>
    <output_param name="form_xml" type="data_attr" source="form.form_xml"/>
  </output_params>

  <rules/>

  <frame main_object="form">
    <toolbar/>
    <body>
      <block/>
      <panel/>
      <row/>
      <col/>
      <text value="Form name:"/>
      <col/>
      <display fld="form.form_name" lng="160"/>
      <col/>
      <text value="Title:"/>
      <col/>
      <display fld="form.title" lng="250"/>
      <block/>
      <grid data_object="dbobj" growable="true" num_grid_rows="3">
        <toolbar template="Setup_Form"/>
        <cur_columns>
          <cur_col col_name="name" lng="120"/>
          <cur_col col_name="table_name" lng="200" expand="true"/>
        </cur_columns>
        <cur_filter/>
        <cur_sequence/>
        <grid_methods template="Setup_Grid"/>
      </grid>
      <block/>
      <grid_frame main_object="dbobj">
        <toolbar template="Setup_Form"/>
        <body>
          <block/>
          <vbox/>
          <panel/>
          <row/>
          <col/>
          <text value="Table hooks"/>
          <grid data_object="dbhooks" growable="true" num_grid_rows="5">
            <toolbar template="Setup_Form"/>
            <cur_columns>
              <cur_col col_name="type" lng="200"/>
            </cur_columns>
            <cur_filter/>
            <cur_sequence/>
            <grid_methods template="Setup_Grid"/>
          </grid>
          <vbox_end/>
          <grid_frame main_object="dbhooks">
            <toolbar template="Setup_Form"/>
            <body>
              <block/>
              <panel/>
              <row/>
              <col/>
              <label value="Hook action:"/>
              <row/>
              <col/>
              <input fld="dbhooks.action" lng="400" height="5"/>
            </body>
            <button_row validate="true" template="Grid_Frame"/>
            <frame_methods template="Grid_Frame"/>
          </grid_frame>
        </body>
        <button_row validate="true" template="Grid_Frame"/>
        <frame_methods template="Grid_Frame"/>
      </grid_frame>
    </body>
<!--
    <button_row validate="true">
      <button btn_id="btn_close" btn_label="Close" btn_enabled="true"
          btn_validate="true" btn_default="true" lng="60">
        <pyfunc name="db.formdefn_funcs.dump_db_objects"/>
        <call method="on_req_cancel"/>
      </button>
    </button_row>
-->
    <button_row validate="true" template="Setup_Form"/>
    <frame_methods template="Setup_Form">
<!--
      <method name="on_req_cancel">
        <end_form state="completed"/>
      </method>
      <method name="on_req_close">
        <end_form state="completed"/>
      </method>
-->
      <method name="on_start_form" action="
        <<action>>
          <<pyfunc name=`db.formdefn_funcs.load_db_objects`/>>
        <</action>>
      "/>
      <method name="do_save" action="
        <<action>>
          <<pyfunc name=`db.formdefn_funcs.dump_db_objects`/>>
        <</action>>
      "/>
      <method name="do_restore" action="
        <<action>>
          <<pyfunc name=`db.formdefn_funcs.restore_db_objects`/>>
        <</action>>
      "/>
    </frame_methods>
  </frame>
</form>
"""
