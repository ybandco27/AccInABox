col_checks = """
<form name="col_checks">

  <db_objects/>
  <mem_objects>
    <mem_obj name="check_array" descr="Expanded array for column checks">
      <mem_col col_name="test" data_type="TEXT" short_descr="Test"
        long_descr="CHECK/AND/OR" col_head="Test" key_field="N" allow_null="false"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="lbr" data_type="TEXT" short_descr="Left bracket"
        long_descr="Left bracket (if required)" col_head="(" key_field="N" allow_null="true"
        allow_amend="true" max_len="1" db_scale="0"/>
      <mem_col col_name="src" data_type="TEXT" short_descr="Source"
        long_descr="Source" col_head="Source" key_field="N" allow_null="false"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="chk" data_type="TEXT" short_descr="Check"
        long_descr="Check to perform" col_head="Check" key_field="N" allow_null="false"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="tgt" data_type="TEXT" short_descr="Target"
        long_descr="Target" col_head="Target" key_field="N" allow_null="false"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="rbr" data_type="TEXT" short_descr="Right bracket"
        long_descr="Right bracket (if required)" col_head=")" key_field="N" allow_null="true"
        allow_amend="true" max_len="1" db_scale="0"/>
    </mem_obj>
  </mem_objects>

  <input_params>
    <input_param name="col_chks" type="data_array" target="check_array" required="true"/>
  </input_params>

  <output_params>
    <output_param name="col_chks" type="data_array" source="check_array"/>
  </output_params>

  <rules/>

  <frame main_object="check_array">
    <toolbar/>
    <body>
      <block/>
      <grid data_object="check_array" growable="true" num_grid_rows="5">
        <cur_columns>
          <cur_col col_name="test" lng="80"/>
          <cur_col col_name="lbr" lng="20"/>
          <cur_col col_name="src" lng="160"/>
          <cur_col col_name="chk" lng="60"/>
          <cur_col col_name="tgt" lng="160" expand="true"/>
          <cur_col col_name="rbr" lng="20"/>
        </cur_columns>
        <cur_filter/>
        <cur_sequence/>
        <grid_methods template="Setup_Grid"/>
      </grid>
    </body>
    <button_row validate="true">
      <button btn_id="btn_ok" btn_label="Ok" lng="60"
          btn_enabled="true" btn_validate="true" btn_default="true" btn_action="
        <<action>>
          <<end_form state=`completed`/>>
        <</action>>
      "/>
      <button btn_id="btn_can" btn_label="Cancel" lng="60"
          btn_enabled="true" btn_validate="false" btn_default="false" btn_action="
        <<action>>
          <<end_form state=`cancelled`/>>
        <</action>>
      "/>
    </button_row>
    <frame_methods>
      <method name="on_req_cancel" action="
        <<action>>
          <<end_form state=`cancelled`/>>
        <</action>>
      "/>
      <method name="on_req_close" action="
        <<action>>
          <<end_form state=`cancelled`/>>
        <</action>>
      "/>
    </frame_methods>
  </frame>
</form>
"""
