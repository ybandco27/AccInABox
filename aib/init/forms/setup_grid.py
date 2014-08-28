setup_grid = """
<form name="setup_grid">
  <db_objects/>
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
        <grid_methods template="Setup_Grid"/>
      </grid>
    </body>
    <button_row validate="false"/>
    <frame_methods template="Setup_Grid"/>
  </frame>
</form>
"""
