company_setup = """
<form name="company_setup">
  <db_objects>
    <db_obj name="db_obj" table_name="dir_companies"/>
  </db_objects>
  <mem_objects/>
  <input_params/>
  <output_params/>
  <rules/>
  <frame main_object="db_obj">
    <toolbar/>
    <body>
      <block/>
      <grid data_object="db_obj" growable="true">
        <toolbar template="Setup_Grid"/>
        <cur_columns>
          <cur_col col_name="company_id" lng="100"/>
          <cur_col col_name="company_name" lng="260" expand="true" validation="
            <<validations>>
              <<validation>>
                <<case>>
                  <<obj_exists obj_name=`db_obj`>>
                  <</obj_exists>>
                  <<default>>
                    <<ask title=`New company` enter=`No` escape=`No`
                        question=`This will create a new company in the database&amp;#10;&amp;#10;Ok to proceed?`>>
                      <<response ans=`No`>>
                        <<error head=`` body=``/>>
                      <</response>
                      <<response ans=`Yes`>>
                      <</response>>
                    <</ask>>
                  <</default>>
                <</case>>
              <</validation>>
            <</validations>>
          "/>
        </cur_columns>
        <cur_filter/>
        <cur_sequence>
          <cur_seq col_name="company_id"/>
        </cur_sequence>
        <grid_methods template="Setup_Grid"/>
      </grid>
    </body>
    <button_row validate="false"/>
    <frame_methods template="Setup_Grid"/>
  </frame>
</form>
"""
