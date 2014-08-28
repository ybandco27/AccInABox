chg_pwd_form = """
<form name="chg_pwd_form">

  <db_objects/>
  <mem_objects>
    <mem_obj name="pwd_var" descr="Form variables">
      <mem_col col_name="pwd1" data_type="TEXT" short_descr="First password"
        long_descr="Enter the new password" col_head="" key_field="N"
        allow_null="true" allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="pwd2" data_type="TEXT" short_descr="Second password"
        long_descr="Enter exactly the same password again" col_head="" key_field="N"
        allow_null="true" allow_amend="true" max_len="0" db_scale="0"/>
      <mem_col col_name="password" data_type="TEXT" short_descr="Hashed password"
        long_descr="" col_head="" key_field="N" allow_null="false"
        allow_amend="true" max_len="0" db_scale="0"/>
    </mem_obj>
  </mem_objects>

  <input_params/>
  <output_params>
    <output_param name="password" type="data_attr" source="pwd_var.password"/>
  </output_params>

  <rules>
<!--
    <vld_rule fld_name="pwd_var.pwd2" errmsg="Passwords do not match">
      <vld_compare src="$value" op="eq" tgt="pwd_var.pwd1"/>
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
      <label value="Enter password:"/>
      <col/>
      <input fld="pwd_var.pwd1" lng="160" pwd="true"/>
      <row/>
      <col/>
      <label value="Re-enter password:"/>
      <col/>
      <input fld="pwd_var.pwd2" lng="160" pwd="true"
        validation="
          <<validations>>
            <<validation>>
              <<case>>
                <<compare src=`$value` op=`eq` tgt=`pwd_var.pwd1`/>>
                <<default>>
                  <<error head=`Error` body=`Passwords do not match`/>>
                <</default>>
              <</case>>
            <</validation>>
          <</validations>>
        "/>
    </body>
    <button_row validate="true">
<!--
      <button btn_id="btn_ok" btn_label="Ok" lng="60"
          btn_enabled="true" btn_validate="true" btn_default="true">
        <case>
          <compare src="pwd_var.pwd1" op="eq" tgt="$None">
            <ask title="Password" enter="No" escape="No"
                question="Are you sure you want a blank password?">
              <response ans="Yes">
                <call method="do_ok"/>
              </response>
              <response ans="No">
                <restart_frame/>
              </response>
            </ask>
          </compare>
          <default>
            <call method="do_ok"/>
          </default>
        </case>
      </button>
-->
      <button btn_id="btn_ok" btn_label="Ok" lng="60"
        btn_enabled="true" btn_validate="true" btn_default="true"
        btn_action="
          <<action>>
            <<case>>
              <<compare src=`pwd_var.pwd1` op=`eq` tgt=`$None`>>
                <<ask title=`Password` enter=`No` escape=`No`
                    question=`Are you sure you want a blank password?`>>
                  <<response ans=`Yes`>>
                    <<call method=`do_ok`/>>
                  <</response>>
                  <<response ans=`No`>>
                    <<restart_frame/>>
                  <</response>>
                <</ask>>
              <</compare>>
              <<default>>
                <<call method=`do_ok`/>>
              <</default>>
            <</case>>
          <</action>>
        "/>
<!--
      <button btn_id="btn_can" btn_label="Cancel" lng="60"
          btn_enabled="true" btn_validate="false" btn_default="false">
        <end_form state="cancelled"/>
      </button>
-->
      <button btn_id="btn_can" btn_label="Cancel" lng="60"
        btn_enabled="true" btn_validate="false" btn_default="false"
        btn_action="
          <<action>>
            <<end_form state=`cancelled`/>>
          <</action>>
        "/>
    </button_row>
    <frame_methods>
      <method name="on_req_close" action="
        <<action>>
         <<call method=`do_cancel`/>>
        <</action>>
      "/>
      <method name="on_req_cancel" action="
        <<action>>
          <<call method=`do_cancel`/>>
        <</action>>
      "/>
      <method name="do_ok" action="
        <<action>>
          <<assign>>
            <<source hash=`sha1`>>pwd_var.pwd1<</source>>
            <<target>>pwd_var.password<</target>>
          <</assign>>
          <<end_form state=`completed`/>>
        <</action>>
      "/>
      <method name="do_cancel" action="
        <<action>>
          <<end_form state=`cancelled`/>>
        <</action>>
      "/>
    </frame_methods>
  </frame>
</form>
"""
