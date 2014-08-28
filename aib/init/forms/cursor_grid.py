cursor_grid = """
<form name="cursor_grid">
  <db_objects>
    <db_obj name="db_cur" table_name="db_cursors" parent="db_table"/>
  </db_objects>
  <mem_objects/>
  <input_params>
    <input_param name="db_table" type="data_obj" target="db_table" required="true"/>
  </input_params>
  <output_params/>
  <rules/>
  <frame main_object="db_cur">
    <toolbar/>
    <body>
      <block/>
      <panel/>
      <row/>
      <col/>
      <text value="Table:"/>
      <col/>
      <display fld="db_table.table_name" lng="160"/>
      <col/>
      <text value="Description:"/>
      <col/>
      <display fld="db_table.short_descr" lng="250"/>
      <block/>
      <grid data_object="db_cur" growable="true" num_grid_rows="3"
          form_name="cursor_form">
        <toolbar template="Setup_Grid"/>
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
</form>
"""
