form_setup_inputs = """
<form name="form_setup_inputs">

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

    <mem_obj name="inputs" descr="Input parameters" parent="form">
      <mem_col col_name="form_name" data_type="TEXT" short_descr="Form name"
        long_descr="Form name" col_head="Form name" key_field="A" allow_null="false"
        allow_amend="false" max_len="20" db_scale="0"
        fkey="[`form`, `form_name`, null, null, true]"/>
      <mem_col col_name="name" data_type="TEXT" short_descr="Name"
        long_descr="Input parameter name" col_head="Name" key_field="A" allow_null="false"
        allow_amend="false" max_len="20" db_scale="0"/>
      <mem_col col_name="type" data_type="TEXT" short_descr="type"
        long_descr="Input parameter type" col_head="Type" key_field="N" allow_null="false"
        allow_amend="true" max_len="20" db_scale="0"       
        choices="[false, false, [[`data_obj`, `Data object`, [], []],
        [`data_attr`, `Data attribute`, [], []], [`data_array`, `Array`, [], []]]]"/>
      <mem_col col_name="target" data_type="TEXT" short_descr="Target"
        long_descr="Input parameter target" col_head="Target" key_field="N" allow_null="false"
        allow_amend="true" max_len="20" db_scale="0"/>
      <mem_col col_name="required" data_type="BOOL" short_descr="Required"
        long_descr="Input parameter required" col_head="Reqd" key_field="N" allow_null="false"
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
      <row/>
      <col/>
      <text value="Title:"/>
      <col/>
      <display fld="form.title" lng="250"/>
      <block/>
      <grid data_object="inputs" growable="true" num_grid_rows="5">
        <cur_columns>
          <cur_col col_name="name" lng="120"/>
          <cur_col col_name="type" lng="120"/>
          <cur_col col_name="target" lng="120" expand="true"/>
          <cur_col col_name="required" lng="40"/>
        </cur_columns>
        <cur_filter/>
        <cur_sequence/>
        <grid_methods template="Setup_Grid"/>
      </grid>
    </body>
    <button_row validate="true" template="Setup_Form"/>
    <frame_methods template="Setup_Form">
      <method name="on_start_form" action="
        <<action>>
          <<pyfunc name=`db.formdefn_funcs.load_input_params`/>>
        <</action>>
      "/>
      <method name="do_save" action="
        <<action>>
          <<pyfunc name=`db.formdefn_funcs.dump_input_params`/>>
        <</action>>
      "/>
      <method name="do_restore" action="
        <<action>>
          <<pyfunc name=`db.formdefn_funcs.restore_input_params`/>>
        <</action>>
      "/>
    </frame_methods>
  </frame>
</form>
"""
