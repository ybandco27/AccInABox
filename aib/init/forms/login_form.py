login_form = """
<form name="login_form">

  <db_objects>
    <db_obj name="dir_user" table_name="dir_users"/>

<!--
    <db_obj name="dir_user" table_name="dir_users" hooks="
      <<hooks>>
        <<hook type=`after_read`>><<pyfunc name=`db.formdefn_funcs.load_form_xml`/>><</hook>>
        <<hook type=`after_init`>><<pyfunc name=`db.formdefn_funcs.load_form_xml`/>><</hook>>
        <<hook type=`after_restore`>><<pyfunc name=`db.formdefn_funcs.load_form_xml`/>><</hook>>
        <<hook type=`before_save`>><<pyfunc name=`db.formdefn_funcs.dump_form_xml`/>><</hook>>
      <</hooks>>
    "/>
-->

  </db_objects>
  <mem_objects>
    <mem_obj name="var" descr="Form variables">
<!--
      <mem_col col_name="user_row_id" data_type="INT" short_descr="User row id"
        long_descr="User row id" col_head="" key_field="N" allow_null="false"
        allow_amend="false" max_len="15" db_scale="0"
        fkey="[`dir_users`, `row_id`, `user`, `user_id`, false]"/>
-->
      <mem_col col_name="user" data_type="TEXT" short_descr="User id"
        long_descr="Enter your user id" col_head="" key_field="N" allow_null="false"
        allow_amend="false" max_len="15" db_scale="0"/>
      <mem_col col_name="pwd" data_type="TEXT" short_descr="Password"
        long_descr="Enter your password" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="display_name" data_type="TEXT" short_descr="Full name"
        long_descr="Full name" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
<!--
      <mem_col col_name="amount" data_type="DEC" short_descr="Amount"
        long_descr="Amount" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="2" dflt_val="0"/>
-->
      <mem_col col_name="choice" data_type="TEXT" short_descr="Choice"
        long_descr="Choice" col_head="" key_field="N" allow_null="false"
        allow_amend="true" max_len="0" db_scale="0"
        choices="[false, false, [[`TEXT`, `Text`, [], []], [`INT`, `Integer`, [], []]]]"/>
      <mem_col col_name="date" data_type="DTE" short_descr="Date"
        long_descr="Date" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0" dflt_val="today"/>
<!--
      <mem_col col_name="bool" data_type="BOOL" short_descr="Bool"
        long_descr="Bool" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="action" data_type="SXML" short_descr="Action"
        long_descr="Action" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"
        dflt_val="<<action>>&amp;#10;  <<case>>&amp;#10;  <</case>>&amp;#10;<</action>>"
        />
      <mem_col col_name="long_descr" data_type="TEXT" short_descr="Description"
        long_descr="Long description" col_head="" key_field="N" allow_null="true"
        allow_amend="true" max_len="0" db_scale="0"/>
-->
    </mem_obj>
  </mem_objects>

  <input_params/>
  <output_params/>

  <rules>
<!--
    <vld_rule fld_name="var.pwd" errmsg="Invalid login">
      <vld_select data_object="dir_user" key="user_id" value="var.user"/>
    </vld_rule>
    <vld_rule fld_name="var.pwd" errmsg="Invalid login">
      <vld_hash method="sha1" src="$value" tgt="dir_user.password"/>
    </vld_rule>
-->
  </rules>

  <frame>
    <toolbar/>
    <body>
      <block/>
      <panel/>
      <row/>
      <col/>
      <text value="Welcome to the Blackbird Property Management System"/>
      <row/>
      <col/>
      <text value="Please enter your user id and password"/>

      <block/>
      <panel/>
      <row/>
      <col/>
      <label value="User Id:"/>
      <col/>
      <input fld="var.user" lng="60"/>
      <display fld="var.display_name" lng="160"/>
<!--
      <row/>
      <col/>
      <label value="Amount:"/>
      <col/>
      <input fld="var.amount" lng="120"/>

      <row/>
      <col/>
      <label value="Choice:"/>
      <col/>
      <input fld="var.choice" lng="120"/>

      <row/>
      <col/>
      <label value="Date:"/>
      <col/>
      <input fld="var.date" lng="120"/>

      <row/>
      <col/>
      <label value="Bool:"/>
      <col/>
      <input fld="var.bool"/>

      <row/>
      <col/>
      <label value="Action:"/>
      <col/>
      <input fld="var.action"/>

      <row/>
      <col/>
      <label value="Long descr:"/>
      <col/>
      <input fld="var.long_descr" lng="200" height="5"/>
-->
      <row/>
      <col/>
      <label value="Password:"/>
      <col/>

      <input fld="var.pwd" lng="120" pwd="true"
        validation="
          <<validations>>
            <<validation>>
              <<select_row obj_name=`dir_user` key=`user_id` value=`var.user`/>>
              <<case>>
                <<obj_exists obj_name=`dir_user`/>>
                <<default>>
                  <<error head=`Login` body=`Invalid login`/>>
                <</default>>
              <</case>>
            <</validation>>
            <<validation>>
              <<case>>
                <<compare src=`$value` op=`eq` tgt=`dir_user.password` hash=`sha1`/>>
                <<default>>
                  <<error head=`Login` body=`Invalid login`/>>
                <</default>>
              <</case>>
            <</validation>>
          <</validations>>
          "

        after="
          <<action>>
            <<!-- if we get here, validations are passed, block amendments -->>
            <<assign>>
              <<!-- redisplay user with correct case (if different) -->>
              <<source>>dir_user.user_id<</source>>
              <<target>>var.user<</target>>
            <</assign>>
            <<assign>>
              <<!-- display full user name -->>
              <<source>>dir_user.display_name<</source>>
              <<target>>var.display_name<</target>>
            <</assign>>
            <<change_button>>
              <<btn_enabled btn_id=`btn_pwd` state=`true`/>>
            <</change_button>>
            <<set_readonly target=`var.user` state=`true`/>>
            <<set_readonly target=`var.pwd` state=`true`/>>
            <<pyfunc name=`ht.htc.on_login_ok`/>>
          <</action>>
        "
      />

<!--
            <<set_readonly target=`var.amount` state=`true`/>>
            <<set_readonly target=`var.choice` state=`true`/>>
            <<set_readonly target=`var.date` state=`true`/>>
            <<set_readonly target=`var.bool` state=`true`/>>
            <<set_readonly target=`var.action` state=`true`/>>
            <<set_readonly target=`var.long_descr` state=`true`/>>
-->
    </body>

    <button_row validate="true">
      <button btn_id="btn_ok" btn_label="Login" btn_enabled="true" btn_validate="true"
        btn_default="true" btn_action="
          <<action>>
            <<end_form state=`completed`/>>
          <</action>>
        "/>
      <button btn_id="btn_can" btn_label="Cancel" btn_enabled="true" btn_validate="false"
        btn_default="false" btn_action="
          <<action>>
            <<call method=`on_req_cancel`/>>
          <</action>>
        "/>
      <button btn_id="btn_pwd" btn_label="Change password"
          btn_enabled="false" btn_validate="false" btn_default="false"
        btn_action="
          <<action>>
            <<sub_form form_name=`chg_pwd_form`>>
              <<call_params/>>
              <<return_params>>
                <<return_param name=`password` type=`data_attr` target=`dir_user.password`/>>
              <</return_params>>
              <<on_return>>
                <<return state=`cancelled`>>
                <</return>>
                <<return state=`completed`>>
                  <<save_obj obj_name=`dir_user`/>>
                  <<set_focus btn_id=`btn_ok`/>>
                <</return>>
              <</on_return>>
            <</sub_form>>
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
