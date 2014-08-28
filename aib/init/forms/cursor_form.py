cursor_form = """
<form name="cursor_form">
  <db_objects/>
  <mem_objects>
    <mem_obj name="column" descr="Cursor columns" parent="db_obj" hooks="
        <<hooks>>
          <<hook type=`before_save`>><<increment_seq/>><</hook>>
          <<hook type=`after_delete`>><<decrement_seq/>><</hook>>
        <</hooks>>
      ">
      <mem_col col_name="seq" data_type="INT" short_descr="Sequence"
        long_descr="Sequence" col_head="Seq" key_field="N"
        allow_null="false" allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="col_name" data_type="TEXT" short_descr="Column name"
        long_descr="Column name" col_head="Column" key_field="N"
        allow_null="false" allow_amend="false" max_len="0" db_scale="0"/>
      <mem_col col_name="lng" data_type="INT" short_descr="Length"
        long_descr="Column length" col_head="Lng" key_field="N"
        allow_null="false" allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="expand" data_type="BOOL" short_descr="Expand?"
        long_descr="Expand column to fill frame?" col_head="Exp?" key_field="N"
        allow_null="false" allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="readonly" data_type="BOOL" short_descr="Read only?"
        long_descr="Read only field?" col_head="R/O?" key_field="N"
        allow_null="false" allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="reverse" data_type="BOOL" short_descr="Reverse?"
        long_descr="Reverse sign? (numeric only)" col_head="Rev?" key_field="N"
        allow_null="false" allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="validation" data_type="SXML" short_descr="Validation"
        long_descr="Validation after input" col_head="Validation" key_field="N"
        allow_null="true" allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="after" data_type="SXML" short_descr="After input"
        long_descr="Action to take after input" col_head="After" key_field="N"
        allow_null="true" allow_amend="true" max_len="0" db_scale="0"/>
    </mem_obj>
    <mem_obj name="filter" descr="Cursor filter" parent="db_obj" hooks="
        <<hooks>>
          <<hook type=`before_save`>><<increment_seq/>><</hook>>
          <<hook type=`after_delete`>><<decrement_seq/>><</hook>>
        <</hooks>>
      ">
      <mem_col col_name="seq" data_type="INT" short_descr="Sequence"
        long_descr="Sequence" col_head="Seq" key_field="N"
        allow_null="false" allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="test" data_type="TEXT" short_descr="Test"
        long_descr="WHERE/AND/OR" col_head="Test" key_field="N"
        allow_null="false" allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="lbr" data_type="TEXT" short_descr="Left bracket"
        long_descr="Left bracket (if required)" col_head="(" key_field="N"
        allow_null="true" allow_amend="true" max_len="1" db_scale="0"/>
      <mem_col col_name="src" data_type="TEXT" short_descr="Source"
        long_descr="Source" col_head="Source" key_field="N"
        allow_null="false" allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="chk" data_type="TEXT" short_descr="Check"
        long_descr="Check to perform" col_head="Check" key_field="N"
        allow_null="false" allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="tgt" data_type="TEXT" short_descr="Target"
        long_descr="Target" col_head="Target" key_field="N"
        allow_null="false" allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="rbr" data_type="TEXT" short_descr="Right bracket"
        long_descr="Right bracket (if required)" col_head=")" key_field="N"
        allow_null="true" allow_amend="true" max_len="1" db_scale="0"/>
    </mem_obj>
    <mem_obj name="sequence" descr="Cursor sequence" parent="db_obj" hooks="
        <<hooks>>
          <<hook type=`before_save`>><<increment_seq/>><</hook>>
          <<hook type=`after_delete`>><<decrement_seq/>><</hook>>
        <</hooks>>
      ">
      <mem_col col_name="seq" data_type="INT" short_descr="Sequence"
        long_descr="Sequence" col_head="Seq" key_field="N"
        allow_null="false" allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="col_name" data_type="TEXT" short_descr="Column name"
        long_descr="Column name" col_head="Column" key_field="N"
        allow_null="false" allow_amend="false" max_len="0" db_scale="0"/>
      <mem_col col_name="descending" data_type="BOOL" short_descr="Descending?"
        long_descr="Descending?" col_head="Desc?" key_field="N"
        allow_null="false" allow_amend="true" max_len="0" db_scale="0" dflt_val="false"/>
    </mem_obj>
  </mem_objects>
  <input_params>
    <!-- input_param name="db_table" type="data_obj" target="db_table" required="true"/ -->
  </input_params>
  <output_params/>
  <rules/>
  <frame main_object="db_obj">
    <toolbar template="Setup_Form"/>
    <body>
      <block/>
      <panel/>
      <row/>
      <col/>
      <text value="Name:"/>
      <col/>
      <input fld="db_obj.cursor_name" lng="160"/>
      <col/>
      <text value="Description:"/>
      <col/>
      <input fld="db_obj.descr" lng="250"/>
      <block/>
      <string value="Columns:" lng="75"/>
      <grid data_object="column" growable="true" num_grid_rows="3">
        <toolbar template="Setup_Form"/>
        <cur_columns>
          <cur_col col_name="col_name" lng="120" expand="true"/>
          <cur_col col_name="lng" lng="40"/>
          <cur_col col_name="expand" lng="40"/>
          <cur_col col_name="readonly" lng="40"/>
          <cur_col col_name="reverse" lng="40"/>
          <cur_col col_name="validation" lng="100"/>
          <cur_col col_name="after" lng="100"/>
        </cur_columns>
        <cur_filter/>
        <cur_sequence>
          <cur_seq col_name="seq" desc="false"/>
        </cur_sequence>
        <grid_methods template="Setup_Grid">
          <method name="do_save" action="
            <<action>>
              <<assign>>
                <<source>>$current_row<</source>>
                <<target>>column.seq<</target>>
              <</assign>>
              <<save_row/>>
            <</action>>
          "/>
       </grid_methods>
     </grid>
      <block/>
      <string value="Filter:" lng="75"/>
      <grid data_object="filter" growable="true" num_grid_rows="2">
        <toolbar template="Setup_Form"/>
        <cur_columns>
          <cur_col col_name="test" lng="80"/>
          <cur_col col_name="lbr" lng="20"/>
          <cur_col col_name="src" lng="160"/>
          <cur_col col_name="chk" lng="60"/>
          <cur_col col_name="tgt" lng="160" expand="true"/>
          <cur_col col_name="rbr" lng="20"/>
        </cur_columns>
        <cur_filter/>
        <cur_sequence>
          <cur_seq col_name="seq" desc="false"/>
        </cur_sequence>
        <grid_methods template="Setup_Grid">
          <method name="do_save" action="
            <<action>>
              <<assign>>
                <<source>>$current_row<</source>>
                <<target>>filter.seq<</target>>
              <</assign>>
              <<save_row/>>
            <</action>>
          "/>
       </grid_methods>
      </grid>
      <block/>
      <string value="Sequence:" lng="75"/>
      <grid data_object="sequence" growable="true" num_grid_rows="2">
        <toolbar template="Setup_Form"/>
        <cur_columns>
          <cur_col col_name="col_name" lng="120" expand="true"/>
          <cur_col col_name="descending" lng="40"/>
        </cur_columns>
        <cur_filter/>
        <cur_sequence>
          <cur_seq col_name="seq" desc="false"/>
        </cur_sequence>
        <grid_methods template="Setup_Grid">
          <method name="do_save" action="
            <<action>>
              <<assign>>
                <<source>>$current_row<</source>>
                <<target>>sequence.seq<</target>>
              <</assign>>
              <<save_row/>>
            <</action>>
          "/>
       </grid_methods>
      </grid>
<!--
        </body>
        <button_row validate="true" template="Grid_Frame"/>
        <frame_methods template="Grid_Frame">
          <method name="on_start_form" action="
            <<action>>
              <<pyfunc name=`db.formdefn_funcs.load_cur_flds`/>>
            <</action>>
          "/>
          <method name="do_save" action="
            <<action>>
              <<pyfunc name=`db.formdefn_funcs.dump_cur_flds`/>>
              <<save_obj obj_name=`db_obj`/>>
            <</action>>
          "/>
        </frame_methods>
      </grid_frame>
-->
    </body>
<!--
    <button_row validate="true">
      <button btn_id="btn_close" btn_label="Close" btn_enabled="true"
          btn_validate="true" btn_default="true" lng="60" btn_action="
        <<action>>
          <<call method=`do_save`/>>
          <<call method=`on_req_cancel`/>>
        <</action>>
      "/>
    </button_row>
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
-->
    <button_row validate="true" template="Setup_Form"/>
    <frame_methods template="Setup_Form">
      <method name="on_start_form" action="
        <<action>>
          <<pyfunc name=`db.formdefn_funcs.load_cur_flds`/>>
        <</action>>
      "/>
      <method name="do_save" action="
        <<action>>
          <<pyfunc name=`db.formdefn_funcs.dump_cur_flds`/>>
          <<save_obj obj_name=`db_obj`/>>
        <</action>>
      "/>
      <method name="do_restore" action="
        <<action>>
          <<restore_obj obj_name=`db_obj`/>>
          <<pyfunc name=`db.formdefn_funcs.load_cur_flds`/>>
        <</action>>
      "/>
    </frame_methods>
  </frame>
</form>
"""
