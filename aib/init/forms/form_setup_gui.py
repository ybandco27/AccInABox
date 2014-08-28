form_setup_gui = """
<form name="form_setup_gui">

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

    <mem_obj name="toolbar" descr="Toolbar" parent="form">
      <mem_col col_name="form_name" data_type="TEXT" short_descr="Form name"
        long_descr="Form name" col_head="Form name" key_field="A" allow_null="false"
        allow_amend="false" max_len="20" db_scale="0"
        fkey="[`form`, `form_name`, null, null, true]"/>
      <mem_col col_name="template" data_type="TEXT" short_descr="Template"
        long_descr="Template" col_head="Template" key_field="N" allow_null="true"
        allow_amend="true" max_len="120" db_scale="0"/>
    </mem_obj>

    <mem_obj name="tool" descr="Toolbar elements" parent="toolbar">
      <mem_col col_name="form_name" data_type="TEXT" short_descr="Form name"
        long_descr="Form name" col_head="Form" key_field="A" allow_null="false"
        allow_amend="false" max_len="20" db_scale="0"
        fkey="[`toolbar`, `form_name`, null, null, true]"/>
      <mem_col col_name="type" data_type="TEXT" short_descr="Tool type"
        long_descr="Tool type" col_head="Tool type" key_field="A" allow_null="false"
        allow_amend="false" max_len="80" db_scale="0"/>
      <mem_col col_name="label" data_type="TEXT" short_descr="Tool label"
        long_descr="Tool label" col_head="Tool label" key_field="N" allow_null="true"
        allow_amend="true" max_len="120" db_scale="0"/>
      <mem_col col_name="tip" data_type="TEXT" short_descr="Tool tip"
        long_descr="Tool tip" col_head="Tool tip" key_field="N" allow_null="true"
        allow_amend="true" max_len="120" db_scale="0"/>
      <mem_col col_name="confirm" data_type="BOOL" short_descr="Request confirmation"
        long_descr="Request confirmation (only for Delete)" col_head="Confirm" key_field="N"
        allow_null="true" allow_amend="true" max_len="120" db_scale="0"/>
    </mem_obj>

    <mem_obj name="body" descr="Body definition elements" parent="form">
      <mem_col col_name="form_name" data_type="TEXT" short_descr="Form name"
        long_descr="Form name" col_head="Form name" key_field="A" allow_null="false"
        allow_amend="false" max_len="20" db_scale="0"
        fkey="[`form`, `form_name`, null, null, true]"/>
      <mem_col col_name="type" data_type="TEXT" short_descr="Type"
        long_descr="Gui object type" col_head="Type" key_field="N" allow_null="false"
        allow_amend="false" max_len="20" db_scale="0"
        choices="[true, true,
            [[`block`, `Block`, [], []]
            ,[`vbox`, `Vertical box`, [], []]
            ,[`vbox_end`, `End vertical box`, [], []]
            ,[`panel`, `Panel`, [], []]
            ,[`row`, `New row`, [], []]
            ,[`col`, `New column`, [[`rowspan`, false], [`colspan`, false]], []]
            ,[`text`, `Text string`, [[`value`, true]], [[`value`, ``]]]
            ,[`label`, `Input label`, [[`value`, true]], [[`value`, ``]]]
            ,[`input`, `Input field`, [[`fld`, true], [`lng`, false], [`height`, false],
                [`pwd`, false], [`readonly`, false], [`reverse`, false], [`choice`, false],
                [`lookup`, false], [`validation`, false], [`after`, false]], [[`fld`, ``]]]
            ,[`display`, `Display field`, [[`fld`, true], [`lng`, true]], [[`fld`, ``]]]
            ,[`button`, `Button`, [[`btn_id`, true], [`btn_label`, true], [`lng`, false],
                [`btn_enabled`, true], [`btn_validate`, true], [`btn_action`, true]],
                [[`btn_label`, ``]]]
            ,[`nb_start`, `Notebook start`, [], []]
            ,[`nb_page`, `Notebook page`, [[`label`, true]], []]
            ,[`nb_end`, `Notebook end`, [], []]
            ,[`grid`, `Data grid`, [[`data_object`, true], [`growable`, false],
                [`num_grid_rows`, false], [`cursor`, false], [`cur_cols`, false],
                [`cur_filter`, false], [`cur_seq`, false]],
                [[`data_object`, ` `], [`num_grid_rows`, ``]]]
            ,[`grid_frame`, `Grid frame`, [], []]
            ,[`subtype_panel`, `Sub-type panel`, [[`subtype`, true]], []]
            ]]"/>
      <mem_col col_name="rowspan" data_type="INT" short_descr="Row span"
        long_descr="Row span" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="colspan" data_type="INT" short_descr="Col span"
        long_descr="Col span" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="value" data_type="TEXT" short_descr="Value"
        long_descr="Value for text control" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="fld" data_type="TEXT" short_descr="Field"
        long_descr="Field" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="lng" data_type="INT" short_descr="Length"
        long_descr="Length" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="height" data_type="INT" short_descr="Height"
        long_descr="Height - multi-line only" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="pwd" data_type="BOOL" short_descr="Password?"
        long_descr="Password?" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="readonly" data_type="BOOL" short_descr="Read only?"
        long_descr="Read only?" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="reverse" data_type="BOOL" short_descr="Reverse sign?"
        long_descr="Reverse sign? (numeric only)" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="choice" data_type="BOOL" short_descr="Allow choices?"
        long_descr="Allow choices?" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="lookup" data_type="BOOL" short_descr="Allow lookup?"
        long_descr="Allow lookup?" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="validation" data_type="SXML" short_descr="Validation"
        long_descr="Validation after input" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="after" data_type="SXML" short_descr="After input"
        long_descr="Action to take after input" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>

      <mem_col col_name="btn_id" data_type="TEXT" short_descr="Button id"
        long_descr="Button id" col_head="Button id" key_field="N" allow_null="true"
        allow_amend="false" max_len="0" db_scale="0"/>
      <mem_col col_name="btn_label" data_type="TEXT" short_descr="Button label"
        long_descr="Button label" col_head="Label" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="btn_enabled" data_type="BOOL" short_descr="Enabled?"
        long_descr="Button enabled?" col_head="Enabled" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="btn_validate" data_type="BOOL" short_descr="Validate?"
        long_descr="Validate before action?" col_head="Vld" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="btn_action" data_type="SXML" short_descr="Action"
        long_descr="Action to take on click" col_head="Action" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>

      <mem_col col_name="label" data_type="TEXT" short_descr="Label"
        long_descr="Label for notebook tab" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="subtype" data_type="TEXT" short_descr="Subtype name"
        long_descr="Subtype name for subtype panel" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="data_object" data_type="TEXT" short_descr="Data object"
        long_descr="Data object" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="growable" data_type="BOOL" short_descr="Growable"
        long_descr="Growable" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="num_grid_rows" data_type="INT" short_descr="Number of rows"
        long_descr="Number of grid rows" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="cursor" data_type="TEXT" short_descr="Cursor"
        long_descr="Name of database cursor" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="cur_cols" data_type="JSON" short_descr="Cursor columns"
        long_descr="Cursor columns" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="cur_filter" data_type="JSON" short_descr="Cursor filter"
        long_descr="Cursor filter" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="cur_seq" data_type="JSON" short_descr="Cursor sequence"
        long_descr="Cursor sequence" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
    </mem_obj>

    <mem_obj name="button_row" descr="Button row" parent="form">
      <mem_col col_name="form_name" data_type="TEXT" short_descr="Form name"
        long_descr="Form name" col_head="Form name" key_field="A" allow_null="false"
        allow_amend="false" max_len="20" db_scale="0"
        fkey="[`form`, `form_name`, null, null, true]"/>
      <mem_col col_name="template" data_type="TEXT" short_descr="Template"
        long_descr="Template" col_head="Template" key_field="N" allow_null="true"
        allow_amend="true" max_len="120" db_scale="0"/>
      <mem_col col_name="validate" data_type="BOOL" short_descr="Validate?"
        long_descr="Validate form up to this point?" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0" dflt_val="true"/>
    </mem_obj>

    <mem_obj name="button" descr="Button" parent="button_row">
      <mem_col col_name="form_name" data_type="TEXT" short_descr="Form name"
        long_descr="Form name" col_head="Form" key_field="A" allow_null="false"
        allow_amend="false" max_len="20" db_scale="0"
        fkey="[`button_row`, `form_name`, null, null, true]"/>
      <mem_col col_name="btn_id" data_type="TEXT" short_descr="Button id"
        long_descr="Button id" col_head="Button id" key_field="A" allow_null="false"
        allow_amend="false" max_len="0" db_scale="0"/>
      <mem_col col_name="btn_label" data_type="TEXT" short_descr="Button label"
        long_descr="Button label" col_head="Label" key_field="N" allow_null="false"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="lng" data_type="INT" short_descr="Length"
        long_descr="Length" col_head="Lng" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="btn_default" data_type="BOOL" short_descr="Default?"
        long_descr="Default button?" col_head="Default" key_field="N" allow_null="false"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="btn_enabled" data_type="BOOL" short_descr="Enabled?"
        long_descr="Button enabled?" col_head="Enabled" key_field="N" allow_null="false"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="btn_validate" data_type="BOOL" short_descr="Validate?"
        long_descr="Validate before action?" col_head="Vld" key_field="N" allow_null="false"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="btn_action" data_type="SXML" short_descr="Action"
        long_descr="Action to take on click" col_head="Action" key_field="N" allow_null="false"
        allow_amend="true" max_len="0" db_scale="0"/>
    </mem_obj>

    <mem_obj name="method_row" descr="Method row" parent="form">
      <mem_col col_name="form_name" data_type="TEXT" short_descr="Form name"
        long_descr="Form name" col_head="Form name" key_field="A" allow_null="false"
        allow_amend="false" max_len="20" db_scale="0"
        fkey="[`form`, `form_name`, null, null, true]"/>
      <mem_col col_name="template" data_type="TEXT" short_descr="Template"
        long_descr="Template" col_head="Template" key_field="N" allow_null="true"
        allow_amend="true" max_len="120" db_scale="0"/>
    </mem_obj>

    <mem_obj name="frame_methods" descr="Frame methods" parent="method_row">
      <mem_col col_name="form_name" data_type="TEXT" short_descr="Form name"
        long_descr="Form name" col_head="Form name" key_field="A" allow_null="false"
        allow_amend="false" max_len="20" db_scale="0"
        fkey="[`method_row`, `form_name`, null, null, true]"/>
      <mem_col col_name="name" data_type="TEXT" short_descr="Method name"
        long_descr="Method name" col_head="Name" key_field="N" allow_null="false"
        allow_amend="false" max_len="20" db_scale="0"/>
      <mem_col col_name="action" data_type="SXML" short_descr="Method action"
        long_descr="Method action" col_head="Action" key_field="N" allow_null="false"
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
      <nb_start/>
      <nb_page label="Toolbar"/>
      <block/>
      <vbox/>
      <panel/>
      <row/>
      <col/>
      <label value="Template:"/>
      <col/>
      <input fld="toolbar.template" lng="120"/>
      <grid data_object="tool" growable="true" num_grid_rows="5">
        <cur_columns>
          <cur_col col_name="type" lng="120"/>
        </cur_columns>
        <cur_filter/>
        <cur_sequence/>
        <grid_methods template="Setup_Grid"/>
      </grid>
      <vbox_end/>
      <grid_frame main_object="tool">
        <toolbar template="Setup_Form"/>
        <body>
          <block/>
          <panel/>
          <row/>
          <col/>
          <label value="Label:"/>
          <col/>
          <input fld="tool.label" lng="120"/>
          <row/>
          <col/>
          <label value="Tip:"/>
          <col/>
          <input fld="tool.tip" lng="120"/>
          <row/>
          <col/>
          <label value="Confirm?"/>
          <col/>
          <input fld="tool.confirm"/>
        </body>
        <button_row validate="true" template="Grid_Frame"/>
        <frame_methods template="Grid_Frame"/>
      </grid_frame>
      <nb_page label="Gui objects"/>
      <block/>
      <grid data_object="body" growable="true" num_grid_rows="12">
        <cur_columns>
          <cur_col col_name="type" lng="120" readonly="true"/>
          <cur_col col_name="display_name" lng="150" expand="true" readonly="true"/>
        </cur_columns>
        <cur_filter/>
        <cur_sequence/>
        <grid_methods template="Setup_Grid"/>
      </grid>
      <grid_frame main_object="body">
        <toolbar template="Setup_Form"/>
        <body>
          <block/>
          <panel/>
          <row/>
          <col/>
          <label value="Type:"/>
          <col/>
          <input fld="body.type" lng="120"/>
          <block/>
          <subtype_panel subtype="body.type">
            <subtype_body subtype_id="text">
              <row/>
              <col/>
              <label value="Text:"/>
              <col/>
              <input fld="body.value" lng="180"/>
            </subtype_body>
            <subtype_body subtype_id="label">
              <row/>
              <col/>
              <label value="Label:"/>
              <col/>
              <input fld="body.value" lng="180"/>
            </subtype_body>
            <subtype_body subtype_id="input">
              <row/>
              <col/>
              <label value="Field:"/>
              <col/>
              <input fld="body.fld" lng="120"/>
              <row/>
              <col/>
              <label value="Length:"/>
              <col/>
              <input fld="body.lng" lng="40"/>
              <col/>
              <label value="Height:"/>
              <col/>
              <input fld="body.height" lng="40"/>
              <row/>
              <col/>
              <label value="Password?"/>
              <col/>
              <input fld="body.pwd"/>
              <col/>
              <label value="Read only?"/>
              <col/>
              <input fld="body.readonly"/>
              <row/>
              <col/>
              <label value="Reverse sign?"/>
              <col/>
              <input fld="body.reverse"/>
              <row/>
              <col/>
              <label value="Action after:"/>
              <col colspan="3"/>
              <input fld="body.after" lng="300" height="5"/>
            </subtype_body>
            <subtype_body subtype_id="display">
              <row/>
              <col/>
              <label value="Field:"/>
              <col/>
              <input fld="body.fld" lng="120"/>
              <row/>
              <col/>
              <label value="Length:"/>
              <col/>
              <input fld="body.lng" lng="40"/>
            </subtype_body>
          </subtype_panel>
        </body>
        <button_row validate="true" template="Grid_Frame"/>
        <frame_methods template="Grid_Frame"/>
      </grid_frame>
      <nb_page label="Button row"/>
      <block/>
      <vbox/>
      <panel/>
      <row/>
      <col/>
      <label value="Template:"/>
      <col/>
      <input fld="button_row.template" lng="120"/>
      <row/>
      <col/>
      <label value="Validate?"/>
      <col/>
      <input fld="button_row.validate"/>
      <grid data_object="button" growable="true" num_grid_rows="5">
        <cur_columns>
          <cur_col col_name="btn_id" lng="120"/>
        </cur_columns>
        <cur_filter/>
        <cur_sequence/>
        <grid_methods template="Setup_Grid"/>
      </grid>
      <vbox_end/>
      <grid_frame main_object="button">
        <toolbar template="Setup_Form"/>
        <body>
          <block/>
          <panel/>
          <row/>
          <col/>
          <label value="Label:"/>
          <col/>
          <input fld="button.btn_label" lng="120"/>
          <row/>
          <col/>
          <label value="Length:"/>
          <col/>
          <input fld="button.lng" lng="30"/>
          <row/>
          <col/>
          <label value="Default?"/>
          <col/>
          <input fld="button.btn_default"/>
          <row/>
          <col/>
          <label value="Enabled?"/>
          <col/>
          <input fld="button.btn_enabled"/>
          <row/>
          <col/>
          <label value="Validate?"/>
          <col/>
          <input fld="button.btn_validate"/>
          <row/>
          <col/>
          <label value="Action:"/>
          <col/>
          <input fld="button.btn_action" lng="400" height="5"/>
        </body>
        <button_row validate="true" template="Grid_Frame"/>
        <frame_methods template="Grid_Frame"/>
      </grid_frame>
<!--
      <nb_page label="Methods"/>
-->
      <nb_end/>
    </body>
    <button_row validate="true" template="Setup_Form"/>
    <frame_methods template="Setup_Form">
      <method name="on_start_form" action="
        <<action>>
          <<pyfunc name=`db.formdefn_funcs.load_frame`/>>
        <</action>>
      "/>
      <method name="do_save" action="
        <<action>>
          <<pyfunc name=`db.formdefn_funcs.dump_frame`/>>
        <</action>>
      "/>
      <method name="do_restore" action="
        <<action>>
          <<pyfunc name=`db.formdefn_funcs.restore_frame`/>>
        <</action>>
      "/>
    </frame_methods>
  </frame>
</form>
"""
