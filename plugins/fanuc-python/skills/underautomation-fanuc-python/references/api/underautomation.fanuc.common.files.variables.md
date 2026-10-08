# underautomation.fanuc.common.files.variables

## AavmmainFile

`from underautomation.fanuc.common.files.variables.aavmmain_file import AavmmainFile`

Describes the Fanuc variable file aavmmain.va

- `AavmmainFile()`
- `i: int (read only)`: Value of variable I
- `rob_grp: int (read only)`: Value of variable ROB_GRP
- `num_axis: int (read only)`: Value of variable NUM_AXIS
- `prm: AavmGrpVariableType (read only)`: Value of variable PRM
- `ps_rob_grp: int (read only)`: Value of variable PS_ROB_GRP
- `cond_num: float (read only)`: Value of variable COND_NUM
- `res_err: float (read only)`: Value of variable RES_ERR
- `res_err_str: str (read only)`: Value of variable RES_ERR_STR
- `param_name: str (read only)`: Value of variable PARAM_NAME
- `data_type: int (read only)`: Value of variable DATA_TYPE
- `dmy_int: int (read only)`: Value of variable DMY_INT
- `dmy_real: float (read only)`: Value of variable DMY_REAL
- `dmy_str: str (read only)`: Value of variable DMY_STR
- `dmy_str2: str (read only)`: Value of variable DMY_STR2
- `dmy_stat: int (read only)`: Value of variable DMY_STAT
- `vfb_mat: typing.List[float] (read only)`: Value of variable VFB_MAT
- `res_err1: float (read only)`: Value of variable RES_ERR1
- `res_er1_thsd: float (read only)`: Value of variable RES_ER1_THSD
- `vtcp_x1_thsd: float (read only)`: Value of variable VTCP_X1_THSD
- `vtcp_z1_thsd: float (read only)`: Value of variable VTCP_Z1_THSD
- `tagt_x1_thsd: float (read only)`: Value of variable TAGT_X1_THSD
- `tagt_z1_thsd: float (read only)`: Value of variable TAGT_Z1_THSD
- `res_err2: float (read only)`: Value of variable RES_ERR2
- `res_er2_thsd: float (read only)`: Value of variable RES_ER2_THSD
- `vtcp_x2_thsd: float (read only)`: Value of variable VTCP_X2_THSD
- `vtcp_z2_thsd: float (read only)`: Value of variable VTCP_Z2_THSD
- `tagt_x2_thsd: float (read only)`: Value of variable TAGT_X2_THSD
- `tagt_z2_thsd: float (read only)`: Value of variable TAGT_Z2_THSD
- `device: int (read only)`: Value of variable DEVICE
- `file_name: str (read only)`: Value of variable FILE_NAME
- `log_port: int (read only)`: Value of variable LOG_PORT
- `aavm_step: int (read only)`: Value of variable AAVM_STEP
- `mast_coun0: typing.List[int] (read only)`: Value of variable MAST_COUN0
- `mast_coun02: typing.List[int] (read only)`: Value of variable MAST_COUN0_2
- `ext_mct0: typing.List[int] (read only)`: Value of variable EXT_MCT0
- `jpos_data: typing.List[float] (read only)`: Value of variable JPOS_DATA
- `vtcp: CartesianPositionVariable (read only)`: Value of variable VTCP
- `vtcp0: CartesianPositionVariable (read only)`: Value of variable VTCP0
- `target: CartesianPositionVariable (read only)`: Value of variable TARGET
- `target0: CartesianPositionVariable (read only)`: Value of variable TARGET0
- `cmp_jpos: typing.List[float] (read only)`: Value of variable CMP_JPOS
- `mast_axis: typing.List[float] (read only)`: Value of variable MAST_AXIS
- `tmp_axis: typing.List[float] (read only)`: Value of variable TMP_AXIS
- `er_vtcpx: float (read only)`: Value of variable ER_VTCPX
- `er_vtcpz: float (read only)`: Value of variable ER_VTCPZ
- `er_targtx: float (read only)`: Value of variable ER_TARGTX
- `er_targty: float (read only)`: Value of variable ER_TARGTY
- `er_targtz: float (read only)`: Value of variable ER_TARGTZ
- `er_vtcpx1: float (read only)`: Value of variable ER_VTCPX1
- `er_vtcpz1: float (read only)`: Value of variable ER_VTCPZ1
- `er_targtx1: float (read only)`: Value of variable ER_TARGTX1
- `er_targtz1: float (read only)`: Value of variable ER_TARGTZ1
- `er_vtcpx2: float (read only)`: Value of variable ER_VTCPX2
- `er_vtcpz2: float (read only)`: Value of variable ER_VTCPZ2
- `er_targtx2: float (read only)`: Value of variable ER_TARGTX2
- `er_targtz2: float (read only)`: Value of variable ER_TARGTZ2
- `meas_pose: typing.List[CartesianPositionVariable] (read only)`: Value of variable MEAS_POSE
- `dual_num: int (read only)`: Value of variable DUAL_NUM
- `s_axis_num: int (read only)`: Value of variable S_AXIS_NUM
- `tpp_run: bool (read only)`: Value of variable TPP_RUN
- `step_su1: int (read only)`: Value of variable STEP_SU1
- `step_su2: int (read only)`: Value of variable STEP_SU2
- `step_su3: int (read only)`: Value of variable STEP_SU3
- `step_su4: int (read only)`: Value of variable STEP_SU4
- `min_num_dots: int (read only)`: Value of variable MIN_NUM_DOTS
- `pix_size_low: float (read only)`: Value of variable PIX_SIZE_LOW
- `pix_siz_high: float (read only)`: Value of variable PIX_SIZ_HIGH
- `aspect_low: float (read only)`: Value of variable ASPECT_LOW
- `is_autoexpo: bool (read only)`: Value of variable IS_AUTOEXPO
- `ae_cont_low: int (read only)`: Value of variable AE_CONT_LOW
- `ae_cont_ave: int (read only)`: Value of variable AE_CONT_AVE
- `ae_num_retry: int (read only)`: Value of variable AE_NUM_RETRY
- `ae_radi_ratio: float (read only)`: Value of variable AE_RADI_RATIO
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## ArrayElement

`from underautomation.fanuc.common.files.variables.array_element import ArrayElement`

Describes all elements inside an array. Basically, a wrapping of GenericField where some properties are inherited from it

- `ArrayElement()`
- `access: str (read only)`: Parent Access
- `type: str (read only)`: Parent Type
- `is_register: bool (read only)`: Parent IsRegister
- `string_length: int (read only)`: Parent StringLength
- `name: str (read only)`: Element index, example : [1] or [2,1]
- Inherited from [GenericField](underautomation.fanuc.common.files.variables.md#genericfield): `dimension1`, `dimension2`
- Inherited from [GenericValue](underautomation.fanuc.common.files.variables.md#genericvalue): `parent`, `kind`, `fields`, `is_uninitialized`, `value`, `register_name`, `full_name`

## BicsetupFile

`from underautomation.fanuc.common.files.variables.bicsetup_file import BicsetupFile`

Describes the Fanuc variable file bicsetup.va

- `BicsetupFile()`
- `bic_name: str (read only)`: Value of variable BIC_NAME
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## CbparamFile

`from underautomation.fanuc.common.files.variables.cbparam_file import CbparamFile`

Describes the Fanuc variable file cbparam.va

- `CbparamFile()`
- `payload1: float (read only)`: Value of variable PAYLOAD1
- `payload1_x: float (read only)`: Value of variable PAYLOAD1_X
- `payload1_y: float (read only)`: Value of variable PAYLOAD1_Y
- `payload1_z: float (read only)`: Value of variable PAYLOAD1_Z
- `payload1_ix: float (read only)`: Value of variable PAYLOAD1_IX
- `payload1_iy: float (read only)`: Value of variable PAYLOAD1_IY
- `payload1_iz: float (read only)`: Value of variable PAYLOAD1_IZ
- `payload2: float (read only)`: Value of variable PAYLOAD2
- `payload2_x: float (read only)`: Value of variable PAYLOAD2_X
- `payload2_y: float (read only)`: Value of variable PAYLOAD2_Y
- `payload2_z: float (read only)`: Value of variable PAYLOAD2_Z
- `payload2_ix: float (read only)`: Value of variable PAYLOAD2_IX
- `payload2_iy: float (read only)`: Value of variable PAYLOAD2_IY
- `payload2_iz: float (read only)`: Value of variable PAYLOAD2_IZ
- `tframe_x: typing.List[float] (read only)`: Value of variable TFRAME_X
- `tframe_y: typing.List[float] (read only)`: Value of variable TFRAME_Y
- `tframe_z: typing.List[float] (read only)`: Value of variable TFRAME_Z
- `se_ctrlmode: int (read only)`: Value of variable SE_CTRLMODE
- `data_c1: typing.List[float] (read only)`: Value of variable DATA_C1
- `data_c2: typing.List[float] (read only)`: Value of variable DATA_C2
- `data_c3: typing.List[float] (read only)`: Value of variable DATA_C3
- `data_c4: typing.List[float] (read only)`: Value of variable DATA_C4
- `data_c5: typing.List[float] (read only)`: Value of variable DATA_C5
- `data_c6: typing.List[float] (read only)`: Value of variable DATA_C6
- `data_c7: typing.List[float] (read only)`: Value of variable DATA_C7
- `data_c8: typing.List[float] (read only)`: Value of variable DATA_C8
- `data_c9: typing.List[float] (read only)`: Value of variable DATA_C9
- `data_c10: typing.List[float] (read only)`: Value of variable DATA_C10
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## CellioFile

`from underautomation.fanuc.common.files.variables.cellio_file import CellioFile`

Describes the Fanuc variable file cellio.va

- `CellioFile()`
- `cell_option: bool (read only)`: Value of variable $CELL_OPTION
- `cell_setup: CellsetVariableType (read only)`: Value of variable $CELL_SETUP
- `clmlio: typing.List[ClmlioVariableType] (read only)`: Value of variable $CLMLIO
- `style_comnt: typing.List[str] (read only)`: Value of variable $STYLE_COMNT
- `style_count: int (read only)`: Value of variable $STYLE_COUNT
- `style_enab: typing.List[bool] (read only)`: Value of variable $STYLE_ENAB
- `style_menu: int (read only)`: Value of variable $STYLE_MENU
- `style_name: typing.List[str] (read only)`: Value of variable $STYLE_NAME
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## ComsetFile

`from underautomation.fanuc.common.files.variables.comset_file import ComsetFile`

Describes the Fanuc variable file comset.va

- `ComsetFile()`
- `searchcase: bool (read only)`: Value of variable SEARCHCASE
- `ifc: int (read only)`: Value of variable IFC
- `url: str (read only)`: Value of variable URL
- `respfile: str (read only)`: Value of variable RESPFILE
- `scomment: str (read only)`: Value of variable SCOMMENT
- `sindx: str (read only)`: Value of variable SINDX
- `srealflag: str (read only)`: Value of variable SREALFLAG
- `sfc: str (read only)`: Value of variable SFC
- `svalue: str (read only)`: Value of variable SVALUE
- `scopystr: str (read only)`: Value of variable SCOPYSTR
- `n_status: int (read only)`: Value of variable N_STATUS
- `icomment_len: int (read only)`: Value of variable ICOMMENT_LEN
- `iretsize: int (read only)`: Value of variable IRETSIZE
- `frvrc: bool (read only)`: Value of variable FRVRC
- `searchfile: str (read only)`: Value of variable SEARCHFILE
- `searchcancel: bool (read only)`: Value of variable SEARCHCANCEL
- `reg_almfc: int (read only)`: Value of variable REG_ALMFC
- `preg_almfc: int (read only)`: Value of variable PREG_ALMFC
- `di_almfc: int (read only)`: Value of variable DI_ALMFC
- `do_almfc: int (read only)`: Value of variable DO_ALMFC
- `flag_almfc: int (read only)`: Value of variable FLAG_ALMFC
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## DiocfgsvFile

`from underautomation.fanuc.common.files.variables.diocfgsv_file import DiocfgsvFile`

Describes the Fanuc variable file diocfgsv.va

- `DiocfgsvFile()`
- `cfg_file_ver: int (read only)`: Value of variable CFG_FILE_VER
- `asg_log_pt: typing.List[int] (read only)`: Value of variable ASG_LOG_PT
- `asg_log_pn: typing.List[int] (read only)`: Value of variable ASG_LOG_PN
- `asg_n_pts: typing.List[int] (read only)`: Value of variable ASG_N_PTS
- `asg_rack_no: typing.List[int] (read only)`: Value of variable ASG_RACK_NO
- `asg_slot_no: typing.List[int] (read only)`: Value of variable ASG_SLOT_NO
- `asg_phy_pt: typing.List[int] (read only)`: Value of variable ASG_PHY_PT
- `asg_phy_pn: typing.List[int] (read only)`: Value of variable ASG_PHY_PN
- `name_log_pt: typing.List[int] (read only)`: Value of variable NAME_LOG_PT
- `name_log_pn: typing.List[int] (read only)`: Value of variable NAME_LOG_PN
- `name_name: typing.List[str] (read only)`: Value of variable NAME_NAME
- `name_name2: typing.List[str] (read only)`: Value of variable NAME_NAME2
- `mode_log_pt: typing.List[int] (read only)`: Value of variable MODE_LOG_PT
- `mode_frst_pn: typing.List[int] (read only)`: Value of variable MODE_FRST_PN
- `mode_last_pn: typing.List[int] (read only)`: Value of variable MODE_LAST_PN
- `mode_mode: typing.List[int] (read only)`: Value of variable MODE_MODE
- `ais_rack_no: typing.List[int] (read only)`: Value of variable AIS_RACK_NO
- `ais_slot_no: typing.List[int] (read only)`: Value of variable AIS_SLOT_NO
- `ais_sequence: typing.List[str] (read only)`: Value of variable AIS_SEQUENCE
- `dev_rack: typing.List[int] (read only)`: Value of variable DEV_RACK
- `dev_slot: typing.List[int] (read only)`: Value of variable DEV_SLOT
- `dev_mod_id: typing.List[int] (read only)`: Value of variable DEV_MOD_ID
- `dev_data_type: typing.List[int] (read only)`: Value of variable DEV_DATA_TYPE
- `dev_param1: typing.List[int] (read only)`: Value of variable DEV_PARAM1
- `dev_param2: typing.List[int] (read only)`: Value of variable DEV_PARAM2
- `dev_comment: typing.List[str] (read only)`: Value of variable DEV_COMMENT
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## GemdataFile

`from underautomation.fanuc.common.files.variables.gemdata_file import GemdataFile`

Describes the Fanuc variable file gemdata.va

- `GemdataFile()`
- `answer_delay: int (read only)`: Value of variable ANSWER_DELAY
- `debug_msg: bool (read only)`: Value of variable DEBUG_MSG
- `wait_act: int (read only)`: Value of variable WAIT_ACT
- `wait_time: int (read only)`: Value of variable WAIT_TIME
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## GenericField

`from underautomation.fanuc.common.files.variables.generic_field import GenericField`

Represents a named field within a variable structure

- `GenericField()`
- `access: str (read only)`: Access modifier of the field (e.g. RW, RO)
- `type: str`: Data type name of the field
- `is_register: bool (read only)`: Indicates whether this field is a register
- `string_length: int (read only)`: Maximum string length if the field type is STRING
- `dimension1: int (read only)`: First dimension size of the array, or first index of an array element
- `dimension2: int (read only)`: Second dimension size of the array, or second index of an array element
- Inherited from [GenericValue](underautomation.fanuc.common.files.variables.md#genericvalue): `parent`, `kind`, `fields`, `name`, `is_uninitialized`, `value`, `register_name`, `full_name`

## GenericValue

`from underautomation.fanuc.common.files.variables.generic_value import GenericValue`

Represents a generic variable value with optional child fields

- `GenericValue()`
- `parent: 'GenericValue' (read only)`: Parent value that contains this value
- `kind: ValueKind (read only)`: Kind of value (scalar, array, structure, or file)
- `fields: typing.Any (read only)`: Child fields of this value
- `name: str (read only)`: Name of this value
- `is_uninitialized: bool (read only)`: Indicates whether this value is uninitialized
- `value: str (read only)`: String representation of the value
- `register_name: str (read only)`: Register name associated with this value
- `full_name: str (read only)`: Fully qualified name including all parent names

## GenericVariable

`from underautomation.fanuc.common.files.variables.generic_variable import GenericVariable`

Represents a top-level variable declaration with scope and storage information

- `GenericVariable()`
- `scope: str (read only)`: Variable scope (e.g. PROG, SYS)
- `storage: str (read only)`: Storage type of the variable (e.g. CMOS, DRAM)
- `parent: IGenericVariableType (read only)`: Parent container of this variable
- Inherited from [GenericField](underautomation.fanuc.common.files.variables.md#genericfield): `access`, `type`, `is_register`, `string_length`, `dimension1`, `dimension2`
- Inherited from [GenericValue](underautomation.fanuc.common.files.variables.md#genericvalue): `kind`, `fields`, `name`, `is_uninitialized`, `value`, `register_name`, `full_name`

## GenericVariableFile

`from underautomation.fanuc.common.files.variables.generic_variable_file import GenericVariableFile`

Represents a parsed Fanuc variable file containing one or more variables

- `GenericVariableFile()`
- `get_field(name: str) -> GenericVariable`: Gets a variable by name (case-insensitive)
- `generate_va(pathToVa: str) -> None`: Generates a .va file and writes it to the specified path
- `generated_va() -> str`: Generates the content of a .va variable file as a string.
- `variables: typing.List[GenericVariable] (read only)`: Variables declared in this file
- `name: str (read only)`: File name
- `parent: IGenericVariableType`: Parent container

## GenericVariableTypeHelpers

`from underautomation.fanuc.common.files.variables.generic_variable_type_helpers import GenericVariableTypeHelpers`

Extension methods for IGenericVariableType

- `static get_ancestors(element: IGenericVariableType) -> typing.List[IGenericVariableType]`: Recursively get parents in an array. The first element is the root element and the last one is the direct parent of the element.
- `static get_field(element: IGenericVariableType, name: str) -> IGenericVariableType`: Get a field by its name (case insensitive)

## HtcolrecFile

`from underautomation.fanuc.common.files.variables.htcolrec_file import HtcolrecFile`

Describes the Fanuc variable file htcolrec.va

- `HtcolrecFile()`
- `col_rec: bool (read only)`: Value of variable COL_REC
- `col_recov: AutoColRecVariableType (read only)`: Value of variable COL_RECOV
- `col_dbg: bool (read only)`: Value of variable COL_DBG
- `abort_delay: int (read only)`: Value of variable ABORT_DELAY
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## HttpkclFile

`from underautomation.fanuc.common.files.variables.httpkcl_file import HttpkclFile`

Describes the Fanuc variable file httpkcl.va

- `HttpkclFile()`
- `cmds: typing.List[str] (read only)`: Value of variable CMDS
- `url: str (read only)`: Value of variable URL
- `newcmd: str (read only)`: Value of variable NEWCMD
- `first_token: str (read only)`: Value of variable FIRST_TOKEN
- `status: int (read only)`: Value of variable STATUS
- `found: bool (read only)`: Value of variable FOUND
- `ill_flg: bool (read only)`: Value of variable ILL_FLG
- `i: int (read only)`: Value of variable I
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## IrcCounterFile

`from underautomation.fanuc.common.files.variables.irc_counter_file import IrcCounterFile`

Describes the Fanuc variable file irc_counter.va

- `IrcCounterFile()`
- `attach_files: typing.List[str] (read only)`: Value of variable ATTACH_FILES
- `counter_mode: int (read only)`: Value of variable COUNTER_MODE
- `cur_time: int (read only)`: Value of variable CUR_TIME
- `cur_time_str: str (read only)`: Value of variable CUR_TIME_STR
- `dbg_rc: bool (read only)`: Value of variable DBG_RC
- `file_name: str (read only)`: Value of variable FILE_NAME
- `irc_gnrc: IrcGnrcVariableType (read only)`: Value of variable IRC_GNRC
- `pkrcxmlfile: str (read only)`: Value of variable PKRCXMLFILE
- `send_email: bool (read only)`: Value of variable SEND_EMAIL
- `snd_priority: int (read only)`: Value of variable SND_PRIORITY
- `status: int (read only)`: Value of variable STATUS
- `thr_duration: int (read only)`: Value of variable THR_DURATION
- `thr_prvtime: int (read only)`: Value of variable THR_PRVTIME
- `tpp_gencall: bool (read only)`: Value of variable TPP_GENCALL
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## IrcMsgFile

`from underautomation.fanuc.common.files.variables.irc_msg_file import IrcMsgFile`

Describes the Fanuc variable file irc_msg.va

- `IrcMsgFile()`
- `attach_files: typing.List[str] (read only)`: Value of variable ATTACH_FILES
- `cur_time: int (read only)`: Value of variable CUR_TIME
- `cur_time_str: str (read only)`: Value of variable CUR_TIME_STR
- `dbg_rc: bool (read only)`: Value of variable DBG_RC
- `file_name: str (read only)`: Value of variable FILE_NAME
- `irc_gnrc: IrcGnrcVariableType (read only)`: Value of variable IRC_GNRC
- `pkrcxmlfile: str (read only)`: Value of variable PKRCXMLFILE
- `send_email: bool (read only)`: Value of variable SEND_EMAIL
- `snd_priority: int (read only)`: Value of variable SND_PRIORITY
- `status: int (read only)`: Value of variable STATUS
- `thr_duration: int (read only)`: Value of variable THR_DURATION
- `thr_prvtime: int (read only)`: Value of variable THR_PRVTIME
- `tpp_gencall: bool (read only)`: Value of variable TPP_GENCALL
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## IrcStatusFile

`from underautomation.fanuc.common.files.variables.irc_status_file import IrcStatusFile`

Describes the Fanuc variable file irc_status.va

- `IrcStatusFile()`
- `attach_files: typing.List[str] (read only)`: Value of variable ATTACH_FILES
- `cur_time: int (read only)`: Value of variable CUR_TIME
- `cur_time_str: str (read only)`: Value of variable CUR_TIME_STR
- `dbg_rc: bool (read only)`: Value of variable DBG_RC
- `file_name: str (read only)`: Value of variable FILE_NAME
- `irc_gnrc: IrcGnrcVariableType (read only)`: Value of variable IRC_GNRC
- `pkrcxmlfile: str (read only)`: Value of variable PKRCXMLFILE
- `send_email: bool (read only)`: Value of variable SEND_EMAIL
- `snd_priority: int (read only)`: Value of variable SND_PRIORITY
- `status: int (read only)`: Value of variable STATUS
- `thr_duration: int (read only)`: Value of variable THR_DURATION
- `thr_prvtime: int (read only)`: Value of variable THR_PRVTIME
- `tpp_gencall: bool (read only)`: Value of variable TPP_GENCALL
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## IrcStlabelFile

`from underautomation.fanuc.common.files.variables.irc_stlabel_file import IrcStlabelFile`

Describes the Fanuc variable file irc_stlabel.va

- `IrcStlabelFile()`
- `attach_files: typing.List[str] (read only)`: Value of variable ATTACH_FILES
- `cur_time: int (read only)`: Value of variable CUR_TIME
- `cur_time_str: str (read only)`: Value of variable CUR_TIME_STR
- `dbg_rc: bool (read only)`: Value of variable DBG_RC
- `file_name: str (read only)`: Value of variable FILE_NAME
- `irc_gnrc: IrcGnrcVariableType (read only)`: Value of variable IRC_GNRC
- `pkrcxmlfile: str (read only)`: Value of variable PKRCXMLFILE
- `send_email: bool (read only)`: Value of variable SEND_EMAIL
- `snd_priority: int (read only)`: Value of variable SND_PRIORITY
- `status: int (read only)`: Value of variable STATUS
- `thr_duration: int (read only)`: Value of variable THR_DURATION
- `thr_prvtime: int (read only)`: Value of variable THR_PRVTIME
- `tpp_gencall: bool (read only)`: Value of variable TPP_GENCALL
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## KlactionFile

`from underautomation.fanuc.common.files.variables.klaction_file import KlactionFile`

Describes the Fanuc variable file klaction.va

- `KlactionFile()`
- `data_type: int (read only)`: Value of variable DATA_TYPE
- `int_value: int (read only)`: Value of variable INT_VALUE
- `real_value: float (read only)`: Value of variable REAL_VALUE
- `string_value: str (read only)`: Value of variable STRING_VALUE
- `status: int (read only)`: Value of variable STATUS
- `param_ok: bool (read only)`: Value of variable PARAM_OK
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## MixlogicFile

`from underautomation.fanuc.common.files.variables.mixlogic_file import MixlogicFile`

Describes the Fanuc variable file mixlogic.va

- `MixlogicFile()`
- `dryrun: DryrunVariableType (read only)`: Value of variable $DRYRUN
- `dryrun_port: typing.List[DryrunPortVariableType] (read only)`: Value of variable $DRYRUN_PORT
- `dryrun_sub: typing.List[str] (read only)`: Value of variable $DRYRUN_SUB
- `mix_bg: typing.List[MixBgVariableType] (read only)`: Value of variable $MIX_BG
- `mix_logic: MixLogicVariableType (read only)`: Value of variable $MIX_LOGIC
- `mix_mkr: typing.List[MixMkrVariableType] (read only)`: Value of variable $MIX_MKR
- `on_path: OnPathVariableType (read only)`: Value of variable $ON_PATH
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## MtparamFile

`from underautomation.fanuc.common.files.variables.mtparam_file import MtparamFile`

Describes the Fanuc variable file mtparam.va

- `MtparamFile()`
- `def_itm: typing.List[int] (read only)`: Value of variable DEF_ITM
- `intl_act: typing.List[int] (read only)`: Value of variable INTL_ACT
- `intl_run: typing.List[int] (read only)`: Value of variable INTL_RUN
- `due_once: typing.List[int] (read only)`: Value of variable DUE_ONCE
- `def_itm2: typing.List[int] (read only)`: Value of variable DEF_ITM2
- `intl_act2: typing.List[int] (read only)`: Value of variable INTL_ACT2
- `intl_run2: typing.List[int] (read only)`: Value of variable INTL_RUN2
- `due_once2: typing.List[int] (read only)`: Value of variable DUE_ONCE2
- `def_itm_i: typing.List[int] (read only)`: Value of variable DEF_ITM_I
- `intl_act_i: typing.List[int] (read only)`: Value of variable INTL_ACT_I
- `intl_run_i: typing.List[int] (read only)`: Value of variable INTL_RUN_I
- `due_once_i: typing.List[int] (read only)`: Value of variable DUE_ONCE_I
- `intell_grs: int (read only)`: Value of variable INTELL_GRS
- `coulomb_n: typing.List[float] (read only)`: Value of variable COULOMB_N
- `coulomb_n0: typing.List[float] (read only)`: Value of variable COULOMB_N0
- `viscosity: typing.List[float] (read only)`: Value of variable VISCOSITY
- `a_motor: typing.List[float] (read only)`: Value of variable A_MOTOR
- `a_friction: typing.List[float] (read only)`: Value of variable A_FRICTION
- `a_dissip: typing.List[float] (read only)`: Value of variable A_DISSIP
- `a_other1: typing.List[float] (read only)`: Value of variable A_OTHER1
- `a_other2: typing.List[float] (read only)`: Value of variable A_OTHER2
- `a_other3: typing.List[float] (read only)`: Value of variable A_OTHER3
- `a_other4: typing.List[float] (read only)`: Value of variable A_OTHER4
- `a_other5: typing.List[float] (read only)`: Value of variable A_OTHER5
- `a_other6: typing.List[float] (read only)`: Value of variable A_OTHER6
- `a_exponent: typing.List[float] (read only)`: Value of variable A_EXPONENT
- `distance: typing.List[float] (read only)`: Value of variable DISTANCE
- `max_v_motor: typing.List[float] (read only)`: Value of variable MAX_V_MOTOR
- `coeff_off: typing.List[float] (read only)`: Value of variable COEFF_OFF
- `sg_rate: typing.List[float] (read only)`: Value of variable SG_RATE
- `t_grs_lim: typing.List[float] (read only)`: Value of variable T_GRS_LIM
- `formula_id: typing.List[int] (read only)`: Value of variable FORMULA_ID
- `t_grs_thre: typing.List[float] (read only)`: Value of variable T_GRS_THRE
- `grs_life: typing.List[float] (read only)`: Value of variable GRS_LIFE
- `weight1: typing.List[float] (read only)`: Value of variable WEIGHT_1
- `weight2: typing.List[float] (read only)`: Value of variable WEIGHT_2
- `weight3: typing.List[float] (read only)`: Value of variable WEIGHT_3
- `weight4: typing.List[float] (read only)`: Value of variable WEIGHT_4
- `weight5: typing.List[float] (read only)`: Value of variable WEIGHT_5
- `theta1: typing.List[float] (read only)`: Value of variable THETA_1
- `theta2: typing.List[float] (read only)`: Value of variable THETA_2
- `theta3: typing.List[float] (read only)`: Value of variable THETA_3
- `theta4: typing.List[float] (read only)`: Value of variable THETA_4
- `theta5: typing.List[float] (read only)`: Value of variable THETA_5
- `limit: typing.List[float] (read only)`: Value of variable LIMIT
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## NumregFile

`from underautomation.fanuc.common.files.variables.numreg_file import NumregFile`

Describes the Fanuc variable file numreg.va

- `NumregFile()`
- `numreg: typing.List[float] (read only)`: Value of variable $NUMREG
- `maxregnum: int (read only)`: Value of variable $MAXREGNUM
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## PalregFile

`from underautomation.fanuc.common.files.variables.palreg_file import PalregFile`

Describes the Fanuc variable file palreg.va

- `PalregFile()`
- `palregnum: int (read only)`: Value of variable $PALREGNUM
- `palreg: typing.List[int] (read only)`: Value of variable $PALREG
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## PosregFile

`from underautomation.fanuc.common.files.variables.posreg_file import PosregFile`

Describes the Fanuc variable file posreg.va

- `PosregFile()`
- `posreg: typing.List[PositionRegister] (read only)`: Value of variable $POSREG
- `maxpregnum: int (read only)`: Value of variable $MAXPREGNUM
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## StrregFile

`from underautomation.fanuc.common.files.variables.strreg_file import StrregFile`

Describes the Fanuc variable file strreg.va

- `StrregFile()`
- `strreg: typing.List[str] (read only)`: Value of variable $STRREG
- `maxsregnum: int (read only)`: Value of variable $MAXSREGNUM
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## SwiupdtFile

`from underautomation.fanuc.common.files.variables.swiupdt_file import SwiupdtFile`

Describes the Fanuc variable file swiupdt.va

- `SwiupdtFile()`
- `run_once: int (read only)`: Value of variable RUN_ONCE
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## SycldintFile

`from underautomation.fanuc.common.files.variables.sycldint_file import SycldintFile`

Describes the Fanuc variable file sycldint.va

- `SycldintFile()`
- `erseverity: int (read only)`: Value of variable $ERSEVERITY
- `jcr: JcrVariableType (read only)`: Value of variable $JCR
- `jcr_grp: typing.List[JcrGrpVariableType] (read only)`: Value of variable $JCR_GRP
- `load_device: str (read only)`: Value of variable $LOAD_DEVICE
- `mcr: McrVariableType (read only)`: Value of variable $MCR
- `mcr_grp: typing.List[McrGrpVariableType] (read only)`: Value of variable $MCR_GRP
- `mor: MorVariableType (read only)`: Value of variable $MOR
- `mor_grp: typing.List[MorGrpVariableType] (read only)`: Value of variable $MOR_GRP
- `pwr_up_rtn: typing.List[str] (read only)`: Value of variable $PWR_UP_RTN
- `tpabrt_used: bool (read only)`: Value of variable $TPABRT_USED
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## SymotnFile

`from underautomation.fanuc.common.files.variables.symotn_file import SymotnFile`

Describes the Fanuc variable file symotn.va

- `SymotnFile()`
- `cf_paramgp: typing.List[CfParamgpVariableType] (read only)`: Value of variable $CF_PARAMGP
- `crcfg: CrcfgVariableType (read only)`: Value of variable $CRCFG
- `enc_stat: typing.List[EncStatVariableType] (read only)`: Value of variable $ENC_STAT
- `fmr2_grp: typing.List[Fmr2GrpVariableType] (read only)`: Value of variable $FMR2_GRP
- `group: typing.List[UprVariableType] (read only)`: Value of variable $GROUP
- `hscd_group: typing.List[HscdGrpVariableType] (read only)`: Value of variable $HSCD_GROUP
- `jog_group: typing.List[UjrGrpVariableType] (read only)`: Value of variable $JOG_GROUP
- `misc: typing.List[MiscGrpVariableType] (read only)`: Value of variable $MISC
- `motask_data: int (read only)`: Value of variable $MOTASK_DATA
- `mrr2_grp: typing.List[Mrr2GrpVariableType] (read only)`: Value of variable $MRR2_GRP
- `mrr_grp: typing.List[MrrGrpVariableType] (read only)`: Value of variable $MRR_GRP
- `param2_grp: typing.List[Mrr2GrpVariableType] (read only)`: Value of variable $PARAM2_GRP
- `param_group: typing.List[MrrGrpVariableType] (read only)`: Value of variable $PARAM_GROUP
- `plid_grp: typing.List[PlidGrpVariableType] (read only)`: Value of variable $PLID_GRP
- `plid_sv: PlidSvVariableType (read only)`: Value of variable $PLID_SV
- `plst_grp1: typing.List[PlstGrpVariableType] (read only)`: Value of variable $PLST_GRP1
- `plst_grp2: typing.List[PlstGrpVariableType] (read only)`: Value of variable $PLST_GRP2
- `plst_grp3: typing.List[PlstGrpVariableType] (read only)`: Value of variable $PLST_GRP3
- `plst_grp4: typing.List[PlstGrpVariableType] (read only)`: Value of variable $PLST_GRP4
- `plst_grp5: typing.List[PlstGrpVariableType] (read only)`: Value of variable $PLST_GRP5
- `plst_grpmad: int (read only)`: Value of variable $PLST_GRPMAD
- `plst_parnum: typing.List[int] (read only)`: Value of variable $PLST_PARNUM
- `plst_schmad: int (read only)`: Value of variable $PLST_SCHMAD
- `plst_schnum: int (read only)`: Value of variable $PLST_SCHNUM
- `plst_updnum: typing.List[int] (read only)`: Value of variable $PLST_UPDNUM
- `podata_grp: typing.List[PodataVariableType] (read only)`: Value of variable $PODATA_GRP
- `poinfo_grp: typing.List[PoinfoVariableType] (read only)`: Value of variable $POINFO_GRP
- `poio_grp: typing.List[PoioVariableType] (read only)`: Value of variable $POIO_GRP
- `pssave_grp: typing.List[PssaveGrpVariableType] (read only)`: Value of variable $PSSAVE_GRP
- `scr: ScrVariableType (read only)`: Value of variable $SCR
- `scr_grp: typing.List[ScrGrpVariableType] (read only)`: Value of variable $SCR_GRP
- `tbccfg: TbccfgVariableType (read only)`: Value of variable $TBCCFG
- `tbc_grp: typing.List[TbcGrpVariableType] (read only)`: Value of variable $TBC_GRP
- `tbjcfg: TbjcfgVariableType (read only)`: Value of variable $TBJCFG
- `tbj_grp: typing.List[TbjGrpVariableType] (read only)`: Value of variable $TBJ_GRP
- `torqctrl: TorqctrlVariableType (read only)`: Value of variable $TORQCTRL
- `tsr_grp: typing.List[TsrGrpVariableType] (read only)`: Value of variable $TSR_GRP
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## SynosaveFile

`from underautomation.fanuc.common.files.variables.synosave_file import SynosaveFile`

Describes the Fanuc variable file synosave.va

- `SynosaveFile()`
- `aavm_grp: typing.List[AavmGrpVariableType] (read only)`: Value of variable $AAVM_GRP
- `aimage_back: int (read only)`: Value of variable $AIMAGE_BACK
- `autoupdt_st: int (read only)`: Value of variable $AUTOUPDT_ST
- `blt: int (read only)`: Value of variable $BLT
- `daq_gfd_use: int (read only)`: Value of variable $DAQ_GFD_USE
- `dbwork: typing.List[DbworkVariableType] (read only)`: Value of variable $DBWORK
- `device: str (read only)`: Value of variable $DEVICE
- `dfmtn0_no: int (read only)`: Value of variable $DFMTN0_NO
- `dhcp_int: typing.List[DhcpIntVariableType] (read only)`: Value of variable $DHCP_INT
- `distbf_data: int (read only)`: Value of variable $DISTBF_DATA
- `fast_clock: int (read only)`: Value of variable $FAST_CLOCK
- `fileconfig: FileconfigVariableType (read only)`: Value of variable $FILECONFIG
- `filesetup: FileSetupVariableType (read only)`: Value of variable $FILESETUP
- `file_basept: int (read only)`: Value of variable $FILE_BASEPT
- `file_errbck: typing.List[FileBackVariableType] (read only)`: Value of variable $FILE_ERRBCK
- `file_maxsec: int (read only)`: Value of variable $FILE_MAXSEC
- `file_sysbck: typing.List[FileBackVariableType] (read only)`: Value of variable $FILE_SYSBCK
- `glofatt: typing.List[GlofattVariableType] (read only)`: Value of variable $GLOFATT
- `glofset: GlofsetVariableType (read only)`: Value of variable $GLOFSET
- `imsave_done: bool (read only)`: Value of variable $IMSAVE_DONE
- `kcl_rpcout: str (read only)`: Value of variable $KCL_RPCOUT
- `lastpauspos: typing.List[JointPositionVariable] (read only)`: Value of variable $LASTPAUSPOS
- `master_enb: int (read only)`: Value of variable $MASTER_ENB
- `memo: MemoMemoVariableType (read only)`: Value of variable $MEMO
- `moptimiz: MoptimizVariableType (read only)`: Value of variable $MOPTIMIZ
- `null_cycle: int (read only)`: Value of variable $NULL_CYCLE
- `opt_state: OptstateVariableType (read only)`: Value of variable $OPT_STATE
- `padj_schnum: int (read only)`: Value of variable $PADJ_SCHNUM
- `pg_max_sped: typing.List[PgmaxspdVariableType] (read only)`: Value of variable $PG_MAX_SPED
- `prgadj_sch: typing.List[PrgadjSchVariableType] (read only)`: Value of variable $PRGADJ_SCH
- `shell_wrk: ShellWrkVariableType (read only)`: Value of variable $SHELL_WRK
- `smh_made: SmhMadeVariableType (read only)`: Value of variable $SMH_MADE
- `startup_dbg: int (read only)`: Value of variable $STARTUP_DBG
- `sys_config: SscbkVariableType (read only)`: Value of variable $SYS_CONFIG
- `sys_time: SysTimeVariableType (read only)`: Value of variable $SYS_TIME
- `tick_rate: int (read only)`: Value of variable $TICK_RATE
- `tp_curscrn: typing.List[TpCurscrnVariableType] (read only)`: Value of variable $TP_CURSCRN
- `tx: TxVariableType (read only)`: Value of variable $TX
- `txram: TxramVariableType (read only)`: Value of variable $TXRAM
- `ui_curscrn: typing.List[TpCurscrnVariableType] (read only)`: Value of variable $UI_CURSCRN
- `ui_fctnfav: typing.List[UiFctnfavVariableType] (read only)`: Value of variable $UI_FCTNFAV
- `ui_panelink: typing.List[UiPanelnkVariableType] (read only)`: Value of variable $UI_PANELINK
- `umr: UmrVariableType (read only)`: Value of variable $UMR
- `vcrsm_cfg: VcrsmCfgVariableType (read only)`: Value of variable $VCRSM_CFG
- `vcwm_cfg: VcwmCfgVariableType (read only)`: Value of variable $VCWM_CFG
- `vcwm_grp: typing.List[VcwmGrpVariableType] (read only)`: Value of variable $VCWM_GRP
- `vdate: str (read only)`: Value of variable $VDATE
- `version: str (read only)`: Value of variable $VERSION
- `vsmo_tmp: VsmoTmpVariableType (read only)`: Value of variable $VSMO_TMP
- `vsmo_val: VsmoValVariableType (read only)`: Value of variable $VSMO_VAL
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## SysframeFile

`from underautomation.fanuc.common.files.variables.sysframe_file import SysframeFile`

Describes the Fanuc variable file sysframe.va

- `SysframeFile()`
- `cell_floor: CartesianPositionVariable (read only)`: Value of variable $CELL_FLOOR
- `cell_grp: typing.List[CellGrpVariableType] (read only)`: Value of variable $CELL_GRP
- `mnuframe: typing.List[CartesianPositionVariable] (read only)`: Value of variable $MNUFRAME
- `mnuframenum: typing.List[int] (read only)`: Value of variable $MNUFRAMENUM
- `mnutool: typing.List[CartesianPositionVariable] (read only)`: Value of variable $MNUTOOL
- `mnutoolnum: typing.List[int] (read only)`: Value of variable $MNUTOOLNUM
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## SysfsacFile

`from underautomation.fanuc.common.files.variables.sysfsac_file import SysfsacFile`

Describes the Fanuc variable file sysfsac.va

- `SysfsacFile()`
- `fsac_def_lv: int (read only)`: Value of variable $FSAC_DEF_LV
- `fsac_enable: int (read only)`: Value of variable $FSAC_ENABLE
- `fsac_list: typing.List[FsacLstVariableType] (read only)`: Value of variable $FSAC_LIST
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## SyshostFile

`from underautomation.fanuc.common.files.variables.syshost_file import SyshostFile`

Describes the Fanuc variable file syshost.va

- `SyshostFile()`
- `bin_cfg: BinCfgVariableType (read only)`: Value of variable $BIN_CFG
- `dhcp_ctrl: typing.List[DhcpCtrlVariableType] (read only)`: Value of variable $DHCP_CTRL
- `dnss_cfg: DnssCfgVariableType (read only)`: Value of variable $DNSS_CFG
- `dns_cfg: DnsCfgVariableType (read only)`: Value of variable $DNS_CFG
- `dns_loc_dom: typing.List[int] (read only)`: Value of variable $DNS_LOC_DOM
- `eth_fltr: typing.List[int] (read only)`: Value of variable $ETH_FLTR
- `ftp_ctrl: FtpCtrlVariableType (read only)`: Value of variable $FTP_CTRL
- `host_shared: typing.List[HostentVariableType] (read only)`: Value of variable $HOST_SHARED
- `ppp_list: typing.List[PppcfgLstVariableType] (read only)`: Value of variable $PPP_LIST
- `rcmcfg: RcmcfgVariableType (read only)`: Value of variable $RCMCFG
- `rdm_cfg: RdmCfgVariableType (read only)`: Value of variable $RDM_CFG
- `smb: SmbVariableType (read only)`: Value of variable $SMB
- `smb_clnt: typing.List[SmbClntVariableType] (read only)`: Value of variable $SMB_CLNT
- `smtp_ctrl: SmtpCtrlVariableType (read only)`: Value of variable $SMTP_CTRL
- `sntp_cfg: SntpCfgVariableType (read only)`: Value of variable $SNTP_CFG
- `sntp_custom: SntpCustomVariableType (read only)`: Value of variable $SNTP_CUSTOM
- `tcpipcfg: TcpipcfgVariableType (read only)`: Value of variable $TCPIPCFG
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## SysmacroFile

`from underautomation.fanuc.common.files.variables.sysmacro_file import SysmacroFile`

Describes the Fanuc variable file sysmacro.va

- `SysmacroFile()`
- `macrolduimt: bool (read only)`: Value of variable $MACROLDUIMT
- `macromaxdri: int (read only)`: Value of variable $MACROMAXDRI
- `macrotable: typing.List[MnMcrTableVariableType] (read only)`: Value of variable $MACROTABLE
- `macro_maxnu: int (read only)`: Value of variable $MACRO_MAXNU
- `macrsopenbl: MnMcrSopVariableType (read only)`: Value of variable $MACRSOPENBL
- `macrspdimsk: int (read only)`: Value of variable $MACRSPDIMSK
- `macrspsumsk: int (read only)`: Value of variable $MACRSPSUMSK
- `macrtpdsbex: bool (read only)`: Value of variable $MACRTPDSBEX
- `macruopenbl: MnMcrUopVariableType (read only)`: Value of variable $MACRUOPENBL
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## SysmastFile

`from underautomation.fanuc.common.files.variables.sysmast_file import SysmastFile`

Describes the Fanuc variable file sysmast.va

- `SysmastFile()`
- `dmr_grp: typing.List[DmrGrpVariableType] (read only)`: Value of variable $DMR_GRP
- `fms_grp: typing.List[FmsGrpVariableType] (read only)`: Value of variable $FMS_GRP
- `plcl_grp: typing.List[PlclGrpVariableType] (read only)`: Value of variable $PLCL_GRP
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## SyspassFile

`from underautomation.fanuc.common.files.variables.syspass_file import SyspassFile`

Describes the Fanuc variable file syspass.va

- `SyspassFile()`
- `passname: typing.List[PassnameVariableType] (read only)`: Value of variable $PASSNAME
- `passsuper: PassnameVariableType (read only)`: Value of variable $PASSSUPER
- `password: PasswordVariableType (read only)`: Value of variable $PASSWORD
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## SysservoFile

`from underautomation.fanuc.common.files.variables.sysservo_file import SysservoFile`

Describes the Fanuc variable file sysservo.va

- `SysservoFile()`
- `sbr: typing.List[SbrVariableType] (read only)`: Value of variable $SBR
- `sbr2: typing.List[Sbr2VariableType] (read only)`: Value of variable $SBR2
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## SystemFile

`from underautomation.fanuc.common.files.variables.system_file import SystemFile`

Describes the Fanuc variable file system.va

- `SystemFile()`
- `aavm_wrk: typing.List[AavmWrkVariableType] (read only)`: Value of variable $AAVM_WRK
- `abspos_grp: typing.List[AbsposGrpVariableType] (read only)`: Value of variable $ABSPOS_GRP
- `acc_maxlmt: int (read only)`: Value of variable $ACC_MAXLMT
- `acc_minlmt: int (read only)`: Value of variable $ACC_MINLMT
- `acc_pre_exe: int (read only)`: Value of variable $ACC_PRE_EXE
- `ac_update: int (read only)`: Value of variable $AC_UPDATE
- `aiocnv_num: int (read only)`: Value of variable $AIOCNV_NUM
- `aiocnv_use: int (read only)`: Value of variable $AIOCNV_USE
- `aio_cnv: typing.List[AioCnvVariableType] (read only)`: Value of variable $AIO_CNV
- `almdg: AlmdgVariableType (read only)`: Value of variable $ALMDG
- `alm_if: AlmIfVariableType (read only)`: Value of variable $ALM_IF
- `angtol: typing.List[float] (read only)`: Value of variable $ANGTOL
- `appinfo: AppinfoVariableType (read only)`: Value of variable $APPINFO
- `application: typing.List[str] (read only)`: Value of variable $APPLICATION
- `ap_active: int (read only)`: Value of variable $AP_ACTIVE
- `ap_automode: bool (read only)`: Value of variable $AP_AUTOMODE
- `ap_chgaponl: bool (read only)`: Value of variable $AP_CHGAPONL
- `ap_coupled: typing.List[ApcoupledVariableType] (read only)`: Value of variable $AP_COUPLED
- `ap_cureq: typing.List[ApcureqVariableType] (read only)`: Value of variable $AP_CUREQ
- `ap_curtool: int (read only)`: Value of variable $AP_CURTOOL
- `ap_do_clean: bool (read only)`: Value of variable $AP_DO_CLEAN
- `ap_do_clenm: typing.List[bool] (read only)`: Value of variable $AP_DO_CLENM
- `ap_dspdryrn: bool (read only)`: Value of variable $AP_DSPDRYRN
- `ap_hide: typing.List[bool] (read only)`: Value of variable $AP_HIDE
- `ap_maxapp: int (read only)`: Value of variable $AP_MAXAPP
- `ap_maxax: int (read only)`: Value of variable $AP_MAXAX
- `ap_plugged: int (read only)`: Value of variable $AP_PLUGGED
- `ap_prc_dsbm: typing.List[int] (read only)`: Value of variable $AP_PRC_DSBM
- `ap_proc_dsb: bool (read only)`: Value of variable $AP_PROC_DSB
- `ap_segf_chk: bool (read only)`: Value of variable $AP_SEGF_CHK
- `ap_seg_chkm: typing.List[bool] (read only)`: Value of variable $AP_SEG_CHKM
- `ap_selap: typing.List[bool] (read only)`: Value of variable $AP_SELAP
- `ap_totalax: int (read only)`: Value of variable $AP_TOTALAX
- `ap_usenum: typing.List[int] (read only)`: Value of variable $AP_USENUM
- `argdispmmck: float (read only)`: Value of variable $ARGDISPMMCK
- `argdispmode: int (read only)`: Value of variable $ARGDISPMODE
- `arg_string: typing.List[ArgStrVariableType] (read only)`: Value of variable $ARG_STRING
- `arg_word: typing.List[str] (read only)`: Value of variable $ARG_WORD
- `asbn_config: AsbnCfgVariableType (read only)`: Value of variable $ASBN_CONFIG
- `atcellsetup: AtCellsetupVariableType (read only)`: Value of variable $ATCELLSETUP
- `autobackup: AutobackupVariableType (read only)`: Value of variable $AUTOBACKUP
- `autoinit: int (read only)`: Value of variable $AUTOINIT
- `automessage: int (read only)`: Value of variable $AUTOMESSAGE
- `automode_do: bool (read only)`: Value of variable $AUTOMODE_DO
- `automode_ov: bool (read only)`: Value of variable $AUTOMODE_OV
- `autopauspos: typing.List[JointPositionVariable] (read only)`: Value of variable $AUTOPAUSPOS
- `autoppostsk: typing.List[int] (read only)`: Value of variable $AUTOPPOSTSK
- `autoupdtmod: int (read only)`: Value of variable $AUTOUPDTMOD
- `auxwzd_enb: int (read only)`: Value of variable $AUXWZD_ENB
- `auxwzd_stat: int (read only)`: Value of variable $AUXWZD_STAT
- `axscrdcfg: typing.List[AxscrdcfgVariableType] (read only)`: Value of variable $AXSCRDCFG
- `background: bool (read only)`: Value of variable $BACKGROUND
- `backup_name: str (read only)`: Value of variable $BACKUP_NAME
- `back_edit: typing.List[BackEditVariableType] (read only)`: Value of variable $BACK_EDIT
- `bck_no_del: bool (read only)`: Value of variable $BCK_NO_DEL
- `bge_unusend: bool (read only)`: Value of variable $BGE_UNUSEND
- `bigallow: typing.List[BigallowVariableType] (read only)`: Value of variable $BIGALLOW
- `blal_out: BlalOutVariableType (read only)`: Value of variable $BLAL_OUT
- `bwd_abort: bool (read only)`: Value of variable $BWD_ABORT
- `bwd_itr_rtn: int (read only)`: Value of variable $BWD_ITR_RTN
- `bwd_nonstop: int (read only)`: Value of variable $BWD_NONSTOP
- `ce_option: int (read only)`: Value of variable $CE_OPTION
- `ce_ria_id: int (read only)`: Value of variable $CE_RIA_ID
- `cfcfg: CfcfgVariableType (read only)`: Value of variable $CFCFG
- `checkconfig: bool (read only)`: Value of variable $CHECKCONFIG
- `chg_pri: typing.List[ChgPriVariableType] (read only)`: Value of variable $CHG_PRI
- `chkpauspos: typing.List[ChkposVariableType] (read only)`: Value of variable $CHKPAUSPOS
- `cmd_info: typing.List[CmdInfoVariableType] (read only)`: Value of variable $CMD_INFO
- `cocfg: CocfgVariableType (read only)`: Value of variable $COCFG
- `collect_cfg: CollectVariableType (read only)`: Value of variable $COLLECT_CFG
- `collect_enb: int (read only)`: Value of variable $COLLECT_ENB
- `condet_cfg: CondetCfgVariableType (read only)`: Value of variable $CONDET_CFG
- `condet_grp: typing.List[CondetGrpVariableType] (read only)`: Value of variable $CONDET_GRP
- `condet_io: CondetIoVariableType (read only)`: Value of variable $CONDET_IO
- `condet_trgp: typing.List[CondetTrgpVariableType] (read only)`: Value of variable $CONDET_TRGP
- `condet_trig: CondetTrigVariableType (read only)`: Value of variable $CONDET_TRIG
- `co_morgrp: typing.List[CoMorgrpVariableType] (read only)`: Value of variable $CO_MORGRP
- `co_paramgrp: typing.List[CoParamgpVariableType] (read only)`: Value of variable $CO_PARAMGRP
- `cpcfg: CpcfgVariableType (read only)`: Value of variable $CPCFG
- `cpdbg: CpdbgVariableType (read only)`: Value of variable $CPDBG
- `cp_mcrgrp: typing.List[CpMcrgrpVariableType] (read only)`: Value of variable $CP_MCRGRP
- `cp_morgrp: typing.List[CpMorgrpVariableType] (read only)`: Value of variable $CP_MORGRP
- `cp_paramgrp: typing.List[CpParamgpVariableType] (read only)`: Value of variable $CP_PARAMGRP
- `cp_t1_grp: typing.List[CpT1GrpVariableType] (read only)`: Value of variable $CP_T1_GRP
- `cp_t1_mode: CpT1ModeVariableType (read only)`: Value of variable $CP_T1_MODE
- `crt_defprog: str (read only)`: Value of variable $CRT_DEFPROG
- `crt_inuser: bool (read only)`: Value of variable $CRT_INUSER
- `crt_key_tbl: typing.List[int] (read only)`: Value of variable $CRT_KEY_TBL
- `crt_lckuser: bool (read only)`: Value of variable $CRT_LCKUSER
- `crt_usestat: bool (read only)`: Value of variable $CRT_USESTAT
- `cr_auto_do: int (read only)`: Value of variable $CR_AUTO_DO
- `cr_indt_enb: bool (read only)`: Value of variable $CR_INDT_ENB
- `cr_t1_do: int (read only)`: Value of variable $CR_T1_DO
- `cr_t2_do: int (read only)`: Value of variable $CR_T2_DO
- `cstop: bool (read only)`: Value of variable $CSTOP
- `ctrl_delete: int (read only)`: Value of variable $CTRL_DELETE
- `ct_screen: str (read only)`: Value of variable $CT_SCREEN
- `custommenu: typing.List[CustommenuVariableType] (read only)`: Value of variable $CUSTOMMENU
- `cust_manual: bool (read only)`: Value of variable $CUST_MANUAL
- `dbcondtrig: int (read only)`: Value of variable $DBCONDTRIG
- `dbg_errlog: DbgErrlogVariableType (read only)`: Value of variable $DBG_ERRLOG
- `dbnumlim: int (read only)`: Value of variable $DBNUMLIM
- `dbpxwork: typing.List[DbpxworkVariableType] (read only)`: Value of variable $DBPXWORK
- `dbtb_ctrl: DbtbCtrlVariableType (read only)`: Value of variable $DBTB_CTRL
- `db_awaytrig: float (read only)`: Value of variable $DB_AWAYTRIG
- `db_away_alm: bool (read only)`: Value of variable $DB_AWAY_ALM
- `db_condtyp: int (read only)`: Value of variable $DB_CONDTYP
- `db_dbg: typing.List[DbDbgVariableType] (read only)`: Value of variable $DB_DBG
- `db_mindist: float (read only)`: Value of variable $DB_MINDIST
- `db_montime: int (read only)`: Value of variable $DB_MONTIME
- `db_montyp: int (read only)`: Value of variable $DB_MONTYP
- `db_motnend: bool (read only)`: Value of variable $DB_MOTNEND
- `db_record: typing.List[DbRecordVariableType] (read only)`: Value of variable $DB_RECORD
- `db_tolerenc: float (read only)`: Value of variable $DB_TOLERENC
- `dcss_cnstcy: typing.List[DcssCnstcyVariableType] (read only)`: Value of variable $DCSS_CNSTCY
- `dcss_device: typing.List[DcssDeviceVariableType] (read only)`: Value of variable $DCSS_DEVICE
- `dcss_hndgd: DcssHndgdVariableType (read only)`: Value of variable $DCSS_HNDGD
- `dcss_ls: typing.List[DcssLsVariableType] (read only)`: Value of variable $DCSS_LS
- `dcss_param: DcssParamVariableType (read only)`: Value of variable $DCSS_PARAM
- `dcss_slave: DcssSlaveVariableType (read only)`: Value of variable $DCSS_SLAVE
- `dcs_cfg: DcsCfgVariableType (read only)`: Value of variable $DCS_CFG
- `dcs_crc_out: DcsCrcOutVariableType (read only)`: Value of variable $DCS_CRC_OUT
- `dcs_nocode: DcsNocodeVariableType (read only)`: Value of variable $DCS_NOCODE
- `dcs_sgn: DcsSgnVariableType (read only)`: Value of variable $DCS_SGN
- `dcs_version: str (read only)`: Value of variable $DCS_VERSION
- `deflogic: typing.List[DeflogicVariableType] (read only)`: Value of variable $DEFLOGIC
- `defprog_enb: bool (read only)`: Value of variable $DEFPROG_ENB
- `defpulse: int (read only)`: Value of variable $DEFPULSE
- `def_acclim: int (read only)`: Value of variable $DEF_ACCLIM
- `def_wrstjnt: int (read only)`: Value of variable $DEF_WRSTJNT
- `demo_init: DemoInitVariableType (read only)`: Value of variable $DEMO_INIT
- `dev_index: int (read only)`: Value of variable $DEV_INDEX
- `dev_path: str (read only)`: Value of variable $DEV_PATH
- `dhcp_clntid: typing.List[str] (read only)`: Value of variable $DHCP_CLNTID
- `diag_grp: typing.List[DiagGrpVariableType] (read only)`: Value of variable $DIAG_GRP
- `dict_config: DictCfgVariableType (read only)`: Value of variable $DICT_CONFIG
- `distbf_tts: int (read only)`: Value of variable $DISTBF_TTS
- `distbf_ver: int (read only)`: Value of variable $DISTBF_VER
- `dmaurst: bool (read only)`: Value of variable $DMAURST
- `dmsw_cfg: DmswCfgVariableType (read only)`: Value of variable $DMSW_CFG
- `docviewer: DocviewerVariableType (read only)`: Value of variable $DOCVIEWER
- `drc_cfg: DrcCfgVariableType (read only)`: Value of variable $DRC_CFG
- `dsbl_fault: DsblFaultVariableType (read only)`: Value of variable $DSBL_FAULT
- `dsbl_gpmsk: int (read only)`: Value of variable $DSBL_GPMSK
- `dtdiag: DtrecVariableType (read only)`: Value of variable $DTDIAG
- `dtrecp: DtrecVariableType (read only)`: Value of variable $DTRECP
- `dump_option: int (read only)`: Value of variable $DUMP_OPTION
- `dutr_cfg: int (read only)`: Value of variable $DUTR_CFG
- `dutr_cpmes: int (read only)`: Value of variable $DUTR_CPMES
- `duty_temp: float (read only)`: Value of variable $DUTY_TEMP
- `duty_unit: int (read only)`: Value of variable $DUTY_UNIT
- `dyn_brk: DynBrkVariableType (read only)`: Value of variable $DYN_BRK
- `editor_optn: int (read only)`: Value of variable $EDITOR_OPTN
- `edit_recent: typing.List[EdtRecentVariableType] (read only)`: Value of variable $EDIT_RECENT
- `emgdi_stat: int (read only)`: Value of variable $EMGDI_STAT
- `enc_info: typing.List[EncInfoVariableType] (read only)`: Value of variable $ENC_INFO
- `enetmode: typing.List[EnetmodeVariableType] (read only)`: Value of variable $ENETMODE
- `eoatcfg: EoatcfgVariableType (read only)`: Value of variable $EOATCFG
- `eoatdata: typing.List[EoatdataVariableType] (read only)`: Value of variable $EOATDATA
- `erpost_log: ErpostLogVariableType (read only)`: Value of variable $ERPOST_LOG
- `error_prog: str (read only)`: Value of variable $ERROR_PROG
- `error_table: typing.List[int] (read only)`: Value of variable $ERROR_TABLE
- `errsev_num: int (read only)`: Value of variable $ERRSEV_NUM
- `er_auto_enb: bool (read only)`: Value of variable $ER_AUTO_ENB
- `er_noauto: ErNoautoVariableType (read only)`: Value of variable $ER_NOAUTO
- `er_nofltr: bool (read only)`: Value of variable $ER_NOFLTR
- `er_nohis: int (read only)`: Value of variable $ER_NOHIS
- `er_no_alm: typing.List[ErNoalmVariableType] (read only)`: Value of variable $ER_NO_ALM
- `er_sev_noau: typing.List[bool] (read only)`: Value of variable $ER_SEV_NOAU
- `etcp_ver: str (read only)`: Value of variable $ETCP_VER
- `extlog_req: int (read only)`: Value of variable $EXTLOG_REQ
- `extlog_siz: int (read only)`: Value of variable $EXTLOG_SIZ
- `extstksiz: int (read only)`: Value of variable $EXTSTKSIZ
- `exttol: float (read only)`: Value of variable $EXTTOL
- `ext_bwd_sel: bool (read only)`: Value of variable $EXT_BWD_SEL
- `ext_di_bwd: ExtSetVariableType (read only)`: Value of variable $EXT_DI_BWD
- `ext_di_step: ExtSetVariableType (read only)`: Value of variable $EXT_DI_STEP
- `e_stop_do: int (read only)`: Value of variable $E_STOP_DO
- `factory_tun: int (read only)`: Value of variable $FACTORY_TUN
- `fdr_grp: typing.List[FdrGrpVariableType] (read only)`: Value of variable $FDR_GRP
- `feature: FeatureVariableType (read only)`: Value of variable $FEATURE
- `feat_add: typing.List[str] (read only)`: Value of variable $FEAT_ADD
- `feat_demo: FeatureVariableType (read only)`: Value of variable $FEAT_DEMO
- `feat_demoin: int (read only)`: Value of variable $FEAT_DEMOIN
- `feat_index: int (read only)`: Value of variable $FEAT_INDEX
- `filecomp: FilecompVariableType (read only)`: Value of variable $FILECOMP
- `filesetup2: FileSetup2VariableType (read only)`: Value of variable $FILESETUP2
- `file_ap2bck: typing.List[FileBackVariableType] (read only)`: Value of variable $FILE_AP2BCK
- `file_appbck: typing.List[FileBackVariableType] (read only)`: Value of variable $FILE_APPBCK
- `file_dgbck: typing.List[FileBackVariableType] (read only)`: Value of variable $FILE_DGBCK
- `file_frsprt: bool (read only)`: Value of variable $FILE_FRSPRT
- `file_visbck: typing.List[FileBackVariableType] (read only)`: Value of variable $FILE_VISBCK
- `flui_config: FluiCfgVariableType (read only)`: Value of variable $FLUI_CONFIG
- `flui_data: FluiDataVariableType (read only)`: Value of variable $FLUI_DATA
- `flui_result: typing.List[FluiResVariableType] (read only)`: Value of variable $FLUI_RESULT
- `fmr_cfg: FmrCfgVariableType (read only)`: Value of variable $FMR_CFG
- `fno: str (read only)`: Value of variable $FNO
- `frm_chktyp: int (read only)`: Value of variable $FRM_CHKTYP
- `fromchk_min: int (read only)`: Value of variable $FROMCHK_MIN
- `fssb_cfg: FssbCfgVariableType (read only)`: Value of variable $FSSB_CFG
- `ftp_def_ow: bool (read only)`: Value of variable $FTP_DEF_OW
- `ftp_dircomp: bool (read only)`: Value of variable $FTP_DIRCOMP
- `genov_enb: bool (read only)`: Value of variable $GENOV_ENB
- `gravc_grp: typing.List[GravcGrpVariableType] (read only)`: Value of variable $GRAVC_GRP
- `grsmt_grp: typing.List[GrsmtGrpVariableType] (read only)`: Value of variable $GRSMT_GRP
- `hostc_cfg: typing.List[HostCfgVariableType] (read only)`: Value of variable $HOSTC_CFG
- `hostent: typing.List[HostentVariableType] (read only)`: Value of variable $HOSTENT
- `hostname: str (read only)`: Value of variable $HOSTNAME
- `hosts_cfg: typing.List[HostCfgVariableType] (read only)`: Value of variable $HOSTS_CFG
- `host_err: ErrMaskVariableType (read only)`: Value of variable $HOST_ERR
- `host_pdusiz: int (read only)`: Value of variable $HOST_PDUSIZ
- `hscdmngrp: typing.List[HscdMngVariableType] (read only)`: Value of variable $HSCDMNGRP
- `hscd_qupd: bool (read only)`: Value of variable $HSCD_QUPD
- `hscd_updtyp: int (read only)`: Value of variable $HSCD_UPDTYP
- `http_auth: typing.List[HttpAuthVariableType] (read only)`: Value of variable $HTTP_AUTH
- `http_ctrl: HttpVariableType (read only)`: Value of variable $HTTP_CTRL
- `hwr_config: HwrConfigVariableType (read only)`: Value of variable $HWR_CONFIG
- `idl_cpu_pct: float (read only)`: Value of variable $IDL_CPU_PCT
- `idl_min_pct: float (read only)`: Value of variable $IDL_MIN_PCT
- `ignr_ioerr: int (read only)`: Value of variable $IGNR_IOERR
- `inpt_sim_do: int (read only)`: Value of variable $INPT_SIM_DO
- `instal_scrn: int (read only)`: Value of variable $INSTAL_SCRN
- `intpmodntol: int (read only)`: Value of variable $INTPMODNTOL
- `intp_prty: int (read only)`: Value of variable $INTP_PRTY
- `invistp_enb: int (read only)`: Value of variable $INVISTP_ENB
- `iolnk: typing.List[IolnkVariableType] (read only)`: Value of variable $IOLNK
- `iomaster: bool (read only)`: Value of variable $IOMASTER
- `ioslave: IoslaveVariableType (read only)`: Value of variable $IOSLAVE
- `iosramcache: bool (read only)`: Value of variable $IOSRAMCACHE
- `io_auto_cfg: bool (read only)`: Value of variable $IO_AUTO_CFG
- `io_auto_uop: bool (read only)`: Value of variable $IO_AUTO_UOP
- `io_cmt_opt: int (read only)`: Value of variable $IO_CMT_OPT
- `io_cycle: bool (read only)`: Value of variable $IO_CYCLE
- `io_def_asg: typing.List[IoDefAsgVariableType] (read only)`: Value of variable $IO_DEF_ASG
- `io_def_num: int (read only)`: Value of variable $IO_DEF_NUM
- `io_ipche: bool (read only)`: Value of variable $IO_IPCHE
- `io_rtry_cnt: int (read only)`: Value of variable $IO_RTRY_CNT
- `io_scrn_upd: int (read only)`: Value of variable $IO_SCRN_UPD
- `io_uop_cfg: IoUopCfgVariableType (read only)`: Value of variable $IO_UOP_CFG
- `irca_acc: typing.List[ItemAccVariableType] (read only)`: Value of variable $IRCA_ACC
- `irca_buf001: typing.List[ItemBuffElVariableType] (read only)`: Value of variable $IRCA_BUF001
- `irca_buf002: typing.List[ItemBuffElVariableType] (read only)`: Value of variable $IRCA_BUF002
- `irca_buf003: typing.List[ItemBuffElVariableType] (read only)`: Value of variable $IRCA_BUF003
- `irca_cfg: typing.List[IrcaCnfVariableType] (read only)`: Value of variable $IRCA_CFG
- `irca_his001: typing.List[HistDayVariableType] (read only)`: Value of variable $IRCA_HIS001
- `irca_his002: typing.List[HistDayVariableType] (read only)`: Value of variable $IRCA_HIS002
- `irca_his003: typing.List[HistDayVariableType] (read only)`: Value of variable $IRCA_HIS003
- `irca_i_cfg: typing.List[ItemNameVariableType] (read only)`: Value of variable $IRCA_I_CFG
- `irprog_cfg: IrprogCfgVariableType (read only)`: Value of variable $IRPROG_CFG
- `isdt_isolc: typing.List[int] (read only)`: Value of variable $ISDT_ISOLC
- `j23_dsp_enb: bool (read only)`: Value of variable $J23_DSP_ENB
- `jinc: JincVariableType (read only)`: Value of variable $JINC
- `jobproc_enb: int (read only)`: Value of variable $JOBPROC_ENB
- `jog_in_auto: int (read only)`: Value of variable $JOG_IN_AUTO
- `jposrec_enb: int (read only)`: Value of variable $JPOSREC_ENB
- `kanji_mask: int (read only)`: Value of variable $KANJI_MASK
- `karelmon: KarelmonVariableType (read only)`: Value of variable $KARELMON
- `karel_cfg: KarelCfgVariableType (read only)`: Value of variable $KAREL_CFG
- `karel_enb: int (read only)`: Value of variable $KAREL_ENB
- `kcl_lin_num: bool (read only)`: Value of variable $KCL_LIN_NUM
- `keylogging: int (read only)`: Value of variable $KEYLOGGING
- `language: str (read only)`: Value of variable $LANGUAGE
- `lgcfg: LgcfgVariableType (read only)`: Value of variable $LGCFG
- `ln_disp: LnDispVariableType (read only)`: Value of variable $LN_DISP
- `loctol: float (read only)`: Value of variable $LOCTOL
- `logbook: LogbookVariableType (read only)`: Value of variable $LOGBOOK
- `log_buff: typing.List[LogBuffVariableType] (read only)`: Value of variable $LOG_BUFF
- `log_dcs: LogDcsVariableType (read only)`: Value of variable $LOG_DCS
- `log_dio: typing.List[LogDioVariableType] (read only)`: Value of variable $LOG_DIO
- `log_er_itm: typing.List[int] (read only)`: Value of variable $LOG_ER_ITM
- `log_er_sev: int (read only)`: Value of variable $LOG_ER_SEV
- `log_er_typ: typing.List[int] (read only)`: Value of variable $LOG_ER_TYP
- `log_rec_rst: bool (read only)`: Value of variable $LOG_REC_RST
- `log_scrn_fl: typing.List[LogScrnFlVariableType] (read only)`: Value of variable $LOG_SCRN_FL
- `log_tpkey: typing.List[int] (read only)`: Value of variable $LOG_TPKEY
- `longnam_enb: bool (read only)`: Value of variable $LONGNAM_ENB
- `lups_digit: int (read only)`: Value of variable $LUPS_DIGIT
- `lu_loadprog: str (read only)`: Value of variable $LU_LOADPROG
- `maxualrmnum: int (read only)`: Value of variable $MAXUALRMNUM
- `max_dig_prt: int (read only)`: Value of variable $MAX_DIG_PRT
- `mcsp: McspVariableType (read only)`: Value of variable $MCSP
- `mcsp_grp: typing.List[McspGrpVariableType] (read only)`: Value of variable $MCSP_GRP
- `md_ldxdisab: int (read only)`: Value of variable $MD_LDXDISAB
- `memo_apname: typing.List[str] (read only)`: Value of variable $MEMO_APNAME
- `mfrq_cfg: MfrqCfgVariableType (read only)`: Value of variable $MFRQ_CFG
- `mfrq_grp: typing.List[MfrqGrpVariableType] (read only)`: Value of variable $MFRQ_GRP
- `misc_mstr: MiscMstrVariableType (read only)`: Value of variable $MISC_MSTR
- `misc_scd: typing.List[MiscScdVariableType] (read only)`: Value of variable $MISC_SCD
- `mkcfg: MkcfgVariableType (read only)`: Value of variable $MKCFG
- `mltarm_cfg: MltarmCfgVariableType (read only)`: Value of variable $MLTARM_CFG
- `mmetpu: int (read only)`: Value of variable $MMETPU
- `mndsp_adcol: int (read only)`: Value of variable $MNDSP_ADCOL
- `mndsp_cmnt: int (read only)`: Value of variable $MNDSP_CMNT
- `mndsp_fncmn: int (read only)`: Value of variable $MNDSP_FNCMN
- `mndsp_fstli: int (read only)`: Value of variable $MNDSP_FSTLI
- `mndsp_mst: MndspMstVariableType (read only)`: Value of variable $MNDSP_MST
- `mndsp_poscf: int (read only)`: Value of variable $MNDSP_POSCF
- `mndsp_prpmt: int (read only)`: Value of variable $MNDSP_PRPMT
- `mndsp_pstol: typing.List[MndsppstlVariableType] (read only)`: Value of variable $MNDSP_PSTOL
- `mnsing_chk: bool (read only)`: Value of variable $MNSING_CHK
- `modaq_cfg: ModaqCfgVariableType (read only)`: Value of variable $MODAQ_CFG
- `modaq_dev: str (read only)`: Value of variable $MODAQ_DEV
- `modaq_hsize: int (read only)`: Value of variable $MODAQ_HSIZE
- `modaq_task: str (read only)`: Value of variable $MODAQ_TASK
- `modaq_trig: typing.List[FxTriggerVariableType] (read only)`: Value of variable $MODAQ_TRIG
- `modaq_type: int (read only)`: Value of variable $MODAQ_TYPE
- `modem_inf: typing.List[ModemInfVariableType] (read only)`: Value of variable $MODEM_INF
- `monitor_msg: typing.List[str] (read only)`: Value of variable $MONITOR_MSG
- `mor_grp_sv: typing.List[MorGrpSvVariableType] (read only)`: Value of variable $MOR_GRP_SV
- `motion_dbg: MotionDbgVariableType (read only)`: Value of variable $MOTION_DBG
- `mpl_name: str (read only)`: Value of variable $MPL_NAME
- `mr_hist: typing.List[MrHistVariableType] (read only)`: Value of variable $MR_HIST
- `mskcfmap: typing.List[int] (read only)`: Value of variable $MSKCFMAP
- `mskconrel: int (read only)`: Value of variable $MSKCONREL
- `mskexcfenb: int (read only)`: Value of variable $MSKEXCFENB
- `mskexcffnc: int (read only)`: Value of variable $MSKEXCFFNC
- `mskjogovlim: int (read only)`: Value of variable $MSKJOGOVLIM
- `mskkey: int (read only)`: Value of variable $MSKKEY
- `mskkey_panl: int (read only)`: Value of variable $MSKKEY_PANL
- `mskrunovlim: int (read only)`: Value of variable $MSKRUNOVLIM
- `msksfspdtyp: int (read only)`: Value of variable $MSKSFSPDTYP
- `msksign: int (read only)`: Value of variable $MSKSIGN
- `mskt1motlim: int (read only)`: Value of variable $MSKT1MOTLIM
- `msk_ce_grp: typing.List[MskCeGrpVariableType] (read only)`: Value of variable $MSK_CE_GRP
- `msqz_edit: int (read only)`: Value of variable $MSQZ_EDIT
- `mtcom_cfg: typing.List[MtcomCfgVariableType] (read only)`: Value of variable $MTCOM_CFG
- `mt_arc_enb: bool (read only)`: Value of variable $MT_ARC_ENB
- `mt_mn_mode: int (read only)`: Value of variable $MT_MN_MODE
- `mt_spl_enb: bool (read only)`: Value of variable $MT_SPL_ENB
- `muap_cplenb: bool (read only)`: Value of variable $MUAP_CPLENB
- `nocheck: typing.List[str] (read only)`: Value of variable $NOCHECK
- `no_wait_ln: int (read only)`: Value of variable $NO_WAIT_LN
- `num_rspace: typing.List[int] (read only)`: Value of variable $NUM_RSPACE
- `odrdsp_enb: int (read only)`: Value of variable $ODRDSP_ENB
- `offset_cart: bool (read only)`: Value of variable $OFFSET_CART
- `offset_dis: bool (read only)`: Value of variable $OFFSET_DIS
- `ofs_at_mark: int (read only)`: Value of variable $OFS_AT_MARK
- `open_files: int (read only)`: Value of variable $OPEN_FILES
- `option_io: int (read only)`: Value of variable $OPTION_IO
- `optm_prg: str (read only)`: Value of variable $OPTM_PRG
- `opwork: OpworkVariableType (read only)`: Value of variable $OPWORK
- `org_dsbl: typing.List[int] (read only)`: Value of variable $ORG_DSBL
- `orienttol: float (read only)`: Value of variable $ORIENTTOL
- `out_sim_do: int (read only)`: Value of variable $OUT_SIM_DO
- `ovrdslct: OvrdslctVariableType (read only)`: Value of variable $OVRDSLCT
- `ovrd_pexe: bool (read only)`: Value of variable $OVRD_PEXE
- `ovrd_rate: int (read only)`: Value of variable $OVRD_RATE
- `ovrd_setup: OvrdSetupVariableType (read only)`: Value of variable $OVRD_SETUP
- `palcfg: PlcfgVariableType (read only)`: Value of variable $PALCFG
- `pal_pos_chk: bool (read only)`: Value of variable $PAL_POS_CHK
- `param_menu: typing.List[str] (read only)`: Value of variable $PARAM_MENU
- `pause_prog: str (read only)`: Value of variable $PAUSE_PROG
- `pccrt: int (read only)`: Value of variable $PCCRT
- `pccrt_host: str (read only)`: Value of variable $PCCRT_HOST
- `pctp: int (read only)`: Value of variable $PCTP
- `pctp_host: str (read only)`: Value of variable $PCTP_HOST
- `pc_timeout: int (read only)`: Value of variable $PC_TIMEOUT
- `pgdebug: int (read only)`: Value of variable $PGDEBUG
- `pginp_flmsk: int (read only)`: Value of variable $PGINP_FLMSK
- `pginp_fltr: int (read only)`: Value of variable $PGINP_FLTR
- `pginp_pgatr: typing.List[int] (read only)`: Value of variable $PGINP_PGATR
- `pginp_pgchk: int (read only)`: Value of variable $PGINP_PGCHK
- `pginp_type: typing.List[str] (read only)`: Value of variable $PGINP_TYPE
- `pginp_word: typing.List[str] (read only)`: Value of variable $PGINP_WORD
- `pglog: int (read only)`: Value of variable $PGLOG
- `pgtracectl: typing.List[TracectlVariableType] (read only)`: Value of variable $PGTRACECTL
- `pgtracedt: typing.List[TracedtVariableType] (read only)`: Value of variable $PGTRACEDT
- `pgtracelen: int (read only)`: Value of variable $PGTRACELEN
- `pgtrace_up: TraceupVariableType (read only)`: Value of variable $PGTRACE_UP
- `pg_cfg: PgCfgVariableType (read only)`: Value of variable $PG_CFG
- `pg_defspd: PgDefspdVariableType (read only)`: Value of variable $PG_DEFSPD
- `ping_ctrl: PingVariableType (read only)`: Value of variable $PING_CTRL
- `pipe_config: PipeCfgVariableType (read only)`: Value of variable $PIPE_CONFIG
- `plid_cfg: PlidCfgVariableType (read only)`: Value of variable $PLID_CFG
- `plid_cllb: typing.List[PlidCllbVariableType] (read only)`: Value of variable $PLID_CLLB
- `plid_know_m: bool (read only)`: Value of variable $PLID_KNOW_M
- `plim_grp: typing.List[PlimGrpVariableType] (read only)`: Value of variable $PLIM_GRP
- `plmr_grp: typing.List[PlmrGrpVariableType] (read only)`: Value of variable $PLMR_GRP
- `ploadbanfwd: bool (read only)`: Value of variable $PLOADBANFWD
- `plst_grp6: typing.List[PlstGrpVariableType] (read only)`: Value of variable $PLST_GRP6
- `plst_grp7: typing.List[PlstGrpVariableType] (read only)`: Value of variable $PLST_GRP7
- `plst_grp8: typing.List[PlstGrpVariableType] (read only)`: Value of variable $PLST_GRP8
- `plst_ovld: typing.List[bool] (read only)`: Value of variable $PLST_OVLD
- `pls_cmp_lim: int (read only)`: Value of variable $PLS_CMP_LIM
- `pls_er_chk: int (read only)`: Value of variable $PLS_ER_CHK
- `pls_er_lim: int (read only)`: Value of variable $PLS_ER_LIM
- `pls_er_rst: bool (read only)`: Value of variable $PLS_ER_RST
- `pl_mod: bool (read only)`: Value of variable $PL_MOD
- `pl_mod_st: bool (read only)`: Value of variable $PL_MOD_ST
- `pl_res_g1: typing.List[PlResGVariableType] (read only)`: Value of variable $PL_RES_G1
- `pl_res_g2: typing.List[PlResGVariableType] (read only)`: Value of variable $PL_RES_G2
- `pl_res_g3: typing.List[PlResGVariableType] (read only)`: Value of variable $PL_RES_G3
- `pl_res_g4: typing.List[PlResGVariableType] (read only)`: Value of variable $PL_RES_G4
- `pl_res_g5: typing.List[PlResGVariableType] (read only)`: Value of variable $PL_RES_G5
- `pl_res_g6: typing.List[PlResGVariableType] (read only)`: Value of variable $PL_RES_G6
- `pl_res_g7: typing.List[PlResGVariableType] (read only)`: Value of variable $PL_RES_G7
- `pl_res_g8: typing.List[PlResGVariableType] (read only)`: Value of variable $PL_RES_G8
- `pl_thr_inrt: int (read only)`: Value of variable $PL_THR_INRT
- `pl_thr_mass: int (read only)`: Value of variable $PL_THR_MASS
- `pl_thr_mmnt: int (read only)`: Value of variable $PL_THR_MMNT
- `pmon_queue: PmonQueVariableType (read only)`: Value of variable $PMON_QUEUE
- `pns_cur_lin: int (read only)`: Value of variable $PNS_CUR_LIN
- `pns_end_cur: bool (read only)`: Value of variable $PNS_END_CUR
- `pns_end_exe: bool (read only)`: Value of variable $PNS_END_EXE
- `pns_number: int (read only)`: Value of variable $PNS_NUMBER
- `pns_option: int (read only)`: Value of variable $PNS_OPTION
- `pns_program: str (read only)`: Value of variable $PNS_PROGRAM
- `pns_task_id: int (read only)`: Value of variable $PNS_TASK_ID
- `pocfg: PocfgVariableType (read only)`: Value of variable $POCFG
- `pos_edit: PosEditVariableType (read only)`: Value of variable $POS_EDIT
- `prgadj: PrgadjVariableType (read only)`: Value of variable $PRGADJ
- `prgns_cfg: PrgnsCfgVariableType (read only)`: Value of variable $PRGNS_CFG
- `prgns_grp: typing.List[PrgnsGrpVariableType] (read only)`: Value of variable $PRGNS_GRP
- `prgns_pref: PrgnsPrefVariableType (read only)`: Value of variable $PRGNS_PREF
- `priority: int (read only)`: Value of variable $PRIORITY
- `product_id: str (read only)`: Value of variable $PRODUCT_ID
- `proggrp_tgl: int (read only)`: Value of variable $PROGGRP_TGL
- `prohibit_do: bool (read only)`: Value of variable $PROHIBIT_DO
- `protoent: typing.List[ProtoentVariableType] (read only)`: Value of variable $PROTOENT
- `proxy_cfg: ProxyCfgVariableType (read only)`: Value of variable $PROXY_CFG
- `pro_cfg: PfCfgVariableType (read only)`: Value of variable $PRO_CFG
- `pro_enhance: PfEnhanceVariableType (read only)`: Value of variable $PRO_ENHANCE
- `pro_pref: PfPrefVariableType (read only)`: Value of variable $PRO_PREF
- `prport_num: int (read only)`: Value of variable $PRPORT_NUM
- `pr_cartrep: bool (read only)`: Value of variable $PR_CARTREP
- `pskstat: int (read only)`: Value of variable $PSKSTAT
- `pslgset: PslgsetVariableType (read only)`: Value of variable $PSLGSET
- `pslgtemp: PslgtempVariableType (read only)`: Value of variable $PSLGTEMP
- `pslgversion: str (read only)`: Value of variable $PSLGVERSION
- `pssave: PssaveVariableType (read only)`: Value of variable $PSSAVE
- `purge_enbl: bool (read only)`: Value of variable $PURGE_ENBL
- `pwf_io: int (read only)`: Value of variable $PWF_IO
- `pwrup_delay: PwrupDlyVariableType (read only)`: Value of variable $PWRUP_DELAY
- `pwr_normal: str (read only)`: Value of variable $PWR_NORMAL
- `pwr_semi: str (read only)`: Value of variable $PWR_SEMI
- `qskip_grp: typing.List[QskipGrpVariableType] (read only)`: Value of variable $QSKIP_GRP
- `rbtif: int (read only)`: Value of variable $RBTIF
- `rcvtmout: int (read only)`: Value of variable $RCVTMOUT
- `rdcr_grp: typing.List[RdcrGrpVariableType] (read only)`: Value of variable $RDCR_GRP
- `rdio_type: typing.List[int] (read only)`: Value of variable $RDIO_TYPE
- `redprot_cfg: RedprotCfgVariableType (read only)`: Value of variable $REDPROT_CFG
- `redprot_grp: typing.List[RedprotGrpVariableType] (read only)`: Value of variable $REDPROT_GRP
- `refpos1: typing.List[Refpos11VariableType] (read only)`: Value of variable $REFPOS1
- `refpos2: typing.List[Refpos21VariableType] (read only)`: Value of variable $REFPOS2
- `refpos3: typing.List[Refpos31VariableType] (read only)`: Value of variable $REFPOS3
- `refpos4: typing.List[Refpos41VariableType] (read only)`: Value of variable $REFPOS4
- `refpos5: typing.List[Refpos51VariableType] (read only)`: Value of variable $REFPOS5
- `refpos6: typing.List[Refpos61VariableType] (read only)`: Value of variable $REFPOS6
- `refpos7: typing.List[Refpos71VariableType] (read only)`: Value of variable $REFPOS7
- `refpos8: typing.List[Refpos81VariableType] (read only)`: Value of variable $REFPOS8
- `refposmask: typing.List[RefpsmskVariableType] (read only)`: Value of variable $REFPOSMASK
- `refposmaxno: typing.List[int] (read only)`: Value of variable $REFPOSMAXNO
- `remote: int (read only)`: Value of variable $REMOTE
- `remote_cfg: RemoteCfgVariableType (read only)`: Value of variable $REMOTE_CFG
- `repl_range: int (read only)`: Value of variable $REPL_RANGE
- `repower: RepowerVariableType (read only)`: Value of variable $REPOWER
- `resm_dryprg: str (read only)`: Value of variable $RESM_DRYPRG
- `restart: RestartVariableType (read only)`: Value of variable $RESTART
- `resume_prog: str (read only)`: Value of variable $RESUME_PROG
- `re_exec_enb: bool (read only)`: Value of variable $RE_EXEC_ENB
- `rgspd_prexe: bool (read only)`: Value of variable $RGSPD_PREXE
- `rgtdb_prexe: bool (read only)`: Value of variable $RGTDB_PREXE
- `rgtrm_prexe: bool (read only)`: Value of variable $RGTRM_PREXE
- `ri_airpurge: typing.List[bool] (read only)`: Value of variable $RI_AIRPURGE
- `rmt_master: int (read only)`: Value of variable $RMT_MASTER
- `robot_isolc: typing.List[int] (read only)`: Value of variable $ROBOT_ISOLC
- `robot_name: str (read only)`: Value of variable $ROBOT_NAME
- `rob_categ: typing.List[int] (read only)`: Value of variable $ROB_CATEG
- `rob_ord_num: typing.List[str] (read only)`: Value of variable $ROB_ORD_NUM
- `rpc_timeout: int (read only)`: Value of variable $RPC_TIMEOUT
- `rs232_cfg: typing.List[Rs232CfgVariableType] (read only)`: Value of variable $RS232_CFG
- `rs232_nport: int (read only)`: Value of variable $RS232_NPORT
- `rsch_log: RschVariableType (read only)`: Value of variable $RSCH_LOG
- `rsmavailnum: int (read only)`: Value of variable $RSMAVAILNUM
- `rspace1: typing.List[RspaceVariableType] (read only)`: Value of variable $RSPACE1
- `rspace2: typing.List[RspaceVariableType] (read only)`: Value of variable $RSPACE2
- `rspace3: typing.List[RspaceVariableType] (read only)`: Value of variable $RSPACE3
- `rspace4: typing.List[RspaceVariableType] (read only)`: Value of variable $RSPACE4
- `rspace5: typing.List[RspaceVariableType] (read only)`: Value of variable $RSPACE5
- `rspace6: typing.List[RspaceVariableType] (read only)`: Value of variable $RSPACE6
- `rspace7: typing.List[RspaceVariableType] (read only)`: Value of variable $RSPACE7
- `rspace8: typing.List[RspaceVariableType] (read only)`: Value of variable $RSPACE8
- `rspaceg: RspacegVariableType (read only)`: Value of variable $RSPACEG
- `rspace_mode: int (read only)`: Value of variable $RSPACE_MODE
- `rspace_s: RspacesrVariableType (read only)`: Value of variable $RSPACE_S
- `rspcwork_ad: int (read only)`: Value of variable $RSPCWORK_AD
- `rsr: typing.List[int] (read only)`: Value of variable $RSR
- `rsr_intval: int (read only)`: Value of variable $RSR_INTVAL
- `rsr_option: int (read only)`: Value of variable $RSR_OPTION
- `saf_do_puls: int (read only)`: Value of variable $SAF_DO_PULS
- `scan_time: int (read only)`: Value of variable $SCAN_TIME
- `sel_default: int (read only)`: Value of variable $SEL_DEFAULT
- `sel_hotstrt: int (read only)`: Value of variable $SEL_HOTSTRT
- `semipowerfl: bool (read only)`: Value of variable $SEMIPOWERFL
- `semipwfdo: int (read only)`: Value of variable $SEMIPWFDO
- `servent: typing.List[ServentVariableType] (read only)`: Value of variable $SERVENT
- `service_kl: typing.List[str] (read only)`: Value of variable $SERVICE_KL
- `service_prg: typing.List[str] (read only)`: Value of variable $SERVICE_PRG
- `serv_dev: str (read only)`: Value of variable $SERV_DEV
- `serv_mail: int (read only)`: Value of variable $SERV_MAIL
- `serv_output: int (read only)`: Value of variable $SERV_OUTPUT
- `serv_save: int (read only)`: Value of variable $SERV_SAVE
- `serv_type: int (read only)`: Value of variable $SERV_TYPE
- `sfzn_cfg: SfznCfgVariableType (read only)`: Value of variable $SFZN_CFG
- `sfzn_grp: typing.List[SfznGrpVariableType] (read only)`: Value of variable $SFZN_GRP
- `shell_cfg: ShellCfgVariableType (read only)`: Value of variable $SHELL_CFG
- `shell_chk: typing.List[ShellChkVariableType] (read only)`: Value of variable $SHELL_CHK
- `shell_comm: ShellCommVariableType (read only)`: Value of variable $SHELL_COMM
- `shftov_enb: int (read only)`: Value of variable $SHFTOV_ENB
- `show_reg_ui: int (read only)`: Value of variable $SHOW_REG_UI
- `simiofwdlm: SimiofwdlmVariableType (read only)`: Value of variable $SIMIOFWDLM
- `si_unit_enb: bool (read only)`: Value of variable $SI_UNIT_ENB
- `slc_retry: int (read only)`: Value of variable $SLC_RETRY
- `smon_alias: typing.List[str] (read only)`: Value of variable $SMON_ALIAS
- `smon_defprog: str (read only)`: Value of variable $SMON_DEFPROG
- `smon_recall: typing.List[str] (read only)`: Value of variable $SMON_RECALL
- `snpx_asg: typing.List[SnpxAsgVariableType] (read only)`: Value of variable $SNPX_ASG
- `snpx_param: SnpxParamVariableType (read only)`: Value of variable $SNPX_PARAM
- `soft_kb_cfg: int (read only)`: Value of variable $SOFT_KB_CFG
- `sopin_sim: typing.List[int] (read only)`: Value of variable $SOPIN_SIM
- `srvnordy_do: bool (read only)`: Value of variable $SRVNORDY_DO
- `srvqstp_dsb: typing.List[int] (read only)`: Value of variable $SRVQSTP_DSB
- `ssr: SsrVariableType (read only)`: Value of variable $SSR
- `stop_on_err: bool (read only)`: Value of variable $STOP_ON_ERR
- `stop_ptn: str (read only)`: Value of variable $STOP_PTN
- `string_prm: bool (read only)`: Value of variable $STRING_PRM
- `svdt_grp: typing.List[SvdtGrpVariableType] (read only)`: Value of variable $SVDT_GRP
- `svprg_count: int (read only)`: Value of variable $SVPRG_COUNT
- `svprg_enb: bool (read only)`: Value of variable $SVPRG_ENB
- `svprm_enb: int (read only)`: Value of variable $SVPRM_ENB
- `svprm_upd: typing.List[SvprmUpdVariableType] (read only)`: Value of variable $SVPRM_UPD
- `sv_info: typing.List[SvInfoVariableType] (read only)`: Value of variable $SV_INFO
- `sysdebug: int (read only)`: Value of variable $SYSDEBUG
- `sysdsp_pass: int (read only)`: Value of variable $SYSDSP_PASS
- `syslog: SyslogVariableType (read only)`: Value of variable $SYSLOG
- `syslog_mpc: SyslogVariableType (read only)`: Value of variable $SYSLOG_MPC
- `syslog_sav: SyslogSavVariableType (read only)`: Value of variable $SYSLOG_SAV
- `system_time: typing.List[SystemTimerVariableType] (read only)`: Value of variable $SYSTEM_TIME
- `systskmem: typing.List[int] (read only)`: Value of variable $SYSTSKMEM
- `t1svgunspd: int (read only)`: Value of variable $T1SVGUNSPD
- `t2mode_lim: T2modeLimVariableType (read only)`: Value of variable $T2MODE_LIM
- `t2spdlim: T2spdlimVariableType (read only)`: Value of variable $T2SPDLIM
- `ta_disp_enb: bool (read only)`: Value of variable $TA_DISP_ENB
- `tbc2_grp: typing.List[Tbc2GrpVariableType] (read only)`: Value of variable $TBC2_GRP
- `tbcsg_grp: typing.List[TbcsgGrpVariableType] (read only)`: Value of variable $TBCSG_GRP
- `tbj2_grp: typing.List[Tbj2GrpVariableType] (read only)`: Value of variable $TBJ2_GRP
- `tbjop_grp: typing.List[TbjopGrpVariableType] (read only)`: Value of variable $TBJOP_GRP
- `threstable: typing.List[TpThrTableVariableType] (read only)`: Value of variable $THRESTABLE
- `thrrditable: typing.List[TpThrTableVariableType] (read only)`: Value of variable $THRRDITABLE
- `thrrdotable: typing.List[TpThrTableVariableType] (read only)`: Value of variable $THRRDOTABLE
- `thrsditable: typing.List[TpThrTableVariableType] (read only)`: Value of variable $THRSDITABLE
- `thrsitable: typing.List[TpThrTableVariableType] (read only)`: Value of variable $THRSITABLE
- `thrtablenum: typing.List[int] (read only)`: Value of variable $THRTABLENUM
- `thr_cfg: ThrCfgVariableType (read only)`: Value of variable $THR_CFG
- `timebf_tts: int (read only)`: Value of variable $TIMEBF_TTS
- `timebf_ver: int (read only)`: Value of variable $TIMEBF_VER
- `timer: typing.List[TimerVariableType] (read only)`: Value of variable $TIMER
- `timer_num: int (read only)`: Value of variable $TIMER_NUM
- `tmi_chan: int (read only)`: Value of variable $TMI_CHAN
- `tmi_dbglvl: int (read only)`: Value of variable $TMI_DBGLVL
- `tmi_etherad: typing.List[str] (read only)`: Value of variable $TMI_ETHERAD
- `tmi_router: str (read only)`: Value of variable $TMI_ROUTER
- `tmi_snmask: typing.List[str] (read only)`: Value of variable $TMI_SNMASK
- `toolofs_dis: bool (read only)`: Value of variable $TOOLOFS_DIS
- `tpe_detail: int (read only)`: Value of variable $TPE_DETAIL
- `tpgl_config: TpglConfVariableType (read only)`: Value of variable $TPGL_CONFIG
- `tpgl_output: TpglOutVariableType (read only)`: Value of variable $TPGL_OUTPUT
- `tpoff_lim: int (read only)`: Value of variable $TPOFF_LIM
- `tpon_svoff: bool (read only)`: Value of variable $TPON_SVOFF
- `tpp_mon: TppMonVariableType (read only)`: Value of variable $TPP_MON
- `tpstrtchk: TpstrtchkVariableType (read only)`: Value of variable $TPSTRTCHK
- `tpvtcompat: bool (read only)`: Value of variable $TPVTCOMPAT
- `tpvwvar: TpvwvarVariableType (read only)`: Value of variable $TPVWVAR
- `tp_defprog: str (read only)`: Value of variable $TP_DEFPROG
- `tp_display: int (read only)`: Value of variable $TP_DISPLAY
- `tp_inst_msk: typing.List[int] (read only)`: Value of variable $TP_INST_MSK
- `tp_inuser: bool (read only)`: Value of variable $TP_INUSER
- `tp_lckuser: bool (read only)`: Value of variable $TP_LCKUSER
- `tp_quickmen: bool (read only)`: Value of variable $TP_QUICKMEN
- `tp_screen: str (read only)`: Value of variable $TP_SCREEN
- `tp_userscrn: str (read only)`: Value of variable $TP_USERSCRN
- `tp_usestat: bool (read only)`: Value of variable $TP_USESTAT
- `trace_cfg: TraceCfgVariableType (read only)`: Value of variable $TRACE_CFG
- `trace_chnl: typing.List[TraceChnlVariableType] (read only)`: Value of variable $TRACE_CHNL
- `trace_item: typing.List[TraceItemVariableType] (read only)`: Value of variable $TRACE_ITEM
- `tscfg: TscfgVariableType (read only)`: Value of variable $TSCFG
- `tsscb: typing.List[TsscbVariableType] (read only)`: Value of variable $TSSCB
- `tutorial: TutorialVariableType (read only)`: Value of variable $TUTORIAL
- `tv_config: TvConfigVariableType (read only)`: Value of variable $TV_CONFIG
- `tv_output: TvOutputVariableType (read only)`: Value of variable $TV_OUTPUT
- `tx_screen: typing.List[TxscreenVariableType] (read only)`: Value of variable $TX_SCREEN
- `ualrm_msg: typing.List[str] (read only)`: Value of variable $UALRM_MSG
- `ualrm_sev: typing.List[int] (read only)`: Value of variable $UALRM_SEV
- `uecfg: UecfgVariableType (read only)`: Value of variable $UECFG
- `uegrp: typing.List[UegrpVariableType] (read only)`: Value of variable $UEGRP
- `ui_bbl_note: BblNtWndVariableType (read only)`: Value of variable $UI_BBL_NOTE
- `ui_defprog: typing.List[str] (read only)`: Value of variable $UI_DEFPROG
- `ui_fkeydata: typing.List[UiFkeydatVariableType] (read only)`: Value of variable $UI_FKEYDATA
- `ui_inuser: typing.List[bool] (read only)`: Value of variable $UI_INUSER
- `ui_menhist: typing.List[UiMenhisVariableType] (read only)`: Value of variable $UI_MENHIST
- `ui_panedata: typing.List[UiPanedatVariableType] (read only)`: Value of variable $UI_PANEDATA
- `ui_postype: typing.List[int] (read only)`: Value of variable $UI_POSTYPE
- `ui_quickmen: typing.List[bool] (read only)`: Value of variable $UI_QUICKMEN
- `ui_restore: typing.List[UiUsrviewVariableType] (read only)`: Value of variable $UI_RESTORE
- `ui_screen: typing.List[str] (read only)`: Value of variable $UI_SCREEN
- `ui_state: typing.List[int] (read only)`: Value of variable $UI_STATE
- `ui_userscrn: typing.List[str] (read only)`: Value of variable $UI_USERSCRN
- `undo_cfg: UndoCfgVariableType (read only)`: Value of variable $UNDO_CFG
- `uop_crm5: bool (read only)`: Value of variable $UOP_CRM5
- `update: str (read only)`: Value of variable $UPDATE
- `user_info: typing.List[UserInfoVariableType] (read only)`: Value of variable $USER_INFO
- `user_offset: UserOffstVariableType (read only)`: Value of variable $USER_OFFSET
- `user_work: UserWorkVariableType (read only)`: Value of variable $USER_WORK
- `useuframe: bool (read only)`: Value of variable $USEUFRAME
- `usrtol_abrt: bool (read only)`: Value of variable $USRTOL_ABRT
- `usrtol_enb: bool (read only)`: Value of variable $USRTOL_ENB
- `usrtol_grp: typing.List[UsrtolGrpVariableType] (read only)`: Value of variable $USRTOL_GRP
- `usrtol_msk: int (read only)`: Value of variable $USRTOL_MSK
- `usrtol_name: str (read only)`: Value of variable $USRTOL_NAME
- `usr_evnt: int (read only)`: Value of variable $USR_EVNT
- `usr_ev_cfg: typing.List[UsrEvCfgVariableType] (read only)`: Value of variable $USR_EV_CFG
- `usr_ev_wrk: typing.List[UsrEvWrkVariableType] (read only)`: Value of variable $USR_EV_WRK
- `vars_config: VarsConfigVariableType (read only)`: Value of variable $VARS_CONFIG
- `vcmr_grp: typing.List[VcmrGrpVariableType] (read only)`: Value of variable $VCMR_GRP
- `via_work: ViaWorkVariableType (read only)`: Value of variable $VIA_WORK
- `visiontmout: int (read only)`: Value of variable $VISIONTMOUT
- `vision_cfg: VisionCfgVariableType (read only)`: Value of variable $VISION_CFG
- `vision_grp: typing.List[VisionGrpVariableType] (read only)`: Value of variable $VISION_GRP
- `vis_ge_cfg: VisGeCfgVariableType (read only)`: Value of variable $VIS_GE_CFG
- `vis_logreg: VisLogregVariableType (read only)`: Value of variable $VIS_LOGREG
- `vlexe_cfg: VlexeCfgVariableType (read only)`: Value of variable $VLEXE_CFG
- `vrtd_filter: typing.List[VrtdFiltVariableType] (read only)`: Value of variable $VRTD_FILTER
- `vshiftmenu: typing.List[CustommenuVariableType] (read only)`: Value of variable $VSHIFTMENU
- `vshift_cfg: VsftCfgVariableType (read only)`: Value of variable $VSHIFT_CFG
- `vsmo_cfg: VsmoCfgVariableType (read only)`: Value of variable $VSMO_CFG
- `vzdt_cfg: VzdtCfgVariableType (read only)`: Value of variable $VZDT_CFG
- `waitrelease: bool (read only)`: Value of variable $WAITRELEASE
- `waittmout: int (read only)`: Value of variable $WAITTMOUT
- `wait_active: bool (read only)`: Value of variable $WAIT_ACTIVE
- `wait_data: WaitDataVariableType (read only)`: Value of variable $WAIT_DATA
- `wait_rdisp: bool (read only)`: Value of variable $WAIT_RDISP
- `xvrcfg: XvrcfgVariableType (read only)`: Value of variable $XVRCFG
- `zabc_grp: typing.List[ZabcGrpVariableType] (read only)`: Value of variable $ZABC_GRP
- `zdt_actvspt: ZdtActvsptVariableType (read only)`: Value of variable $ZDT_ACTVSPT
- `zdt_dcschg: ZdtDcschgVariableType (read only)`: Value of variable $ZDT_DCSCHG
- `zip_cfg: ZipCfgVariableType (read only)`: Value of variable $ZIP_CFG
- `zmpcf_g: typing.List[ZmpcfGrpVariableType] (read only)`: Value of variable $ZMPCF_G
- `zmp_grp: typing.List[ZmposGrpVariableType] (read only)`: Value of variable $ZMP_GRP
- `zpcfg: ZpCfgVariableType (read only)`: Value of variable $ZPCFG
- `zp_cylinder: typing.List[ZpCylinderVariableType] (read only)`: Value of variable $ZP_CYLINDER
- `zp_grp: typing.List[ZpGrpVariableType] (read only)`: Value of variable $ZP_GRP
- `zp_sphere: typing.List[ZpSphereVariableType] (read only)`: Value of variable $ZP_SPHERE
- `zzz: int (read only)`: Value of variable $ZZZ
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## SysuifFile

`from underautomation.fanuc.common.files.variables.sysuif_file import SysuifFile`

Describes the Fanuc variable file sysuif.va

- `SysuifFile()`
- `ui_config: UiConfigVariableType (read only)`: Value of variable $UI_CONFIG
- `ui_custom: typing.List[UiCustomVariableType] (read only)`: Value of variable $UI_CUSTOM
- `ui_topmenu: typing.List[UiTopmenuVariableType] (read only)`: Value of variable $UI_TOPMENU
- `ui_userview: typing.List[UiUsrviewVariableType] (read only)`: Value of variable $UI_USERVIEW
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## TpsnapFile

`from underautomation.fanuc.common.files.variables.tpsnap_file import TpsnapFile`

Describes the Fanuc variable file tpsnap.va

- `TpsnapFile()`
- `day: int (read only)`: Value of variable DAY
- `day_str: str (read only)`: Value of variable DAY_STR
- `dev_path_str: str (read only)`: Value of variable DEV_PATH_STR
- `dev_str: str (read only)`: Value of variable DEV_STR
- `entry: int (read only)`: Value of variable ENTRY
- `hour: int (read only)`: Value of variable HOUR
- `hour_str: str (read only)`: Value of variable HOUR_STR
- `lang_str: str (read only)`: Value of variable LANG_STR
- `min: int (read only)`: Value of variable MIN
- `min_str: str (read only)`: Value of variable MIN_STR
- `month: int (read only)`: Value of variable MONTH
- `month_str: str (read only)`: Value of variable MONTH_STR
- `png_str: str (read only)`: Value of variable PNG_STR
- `sec: int (read only)`: Value of variable SEC
- `sec_str: str (read only)`: Value of variable SEC_STR
- `status: int (read only)`: Value of variable STATUS
- `time_int: int (read only)`: Value of variable TIME_INT
- `time_str: str (read only)`: Value of variable TIME_STR
- `time_str2: str (read only)`: Value of variable TIME_STR2
- `t_int: int (read only)`: Value of variable T_INT
- `t_str: str (read only)`: Value of variable T_STR
- `year: int (read only)`: Value of variable YEAR
- `year_str: str (read only)`: Value of variable YEAR_STR
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`

## ValueKind

`from underautomation.fanuc.common.files.variables.value_kind import ValueKind`

Describes the kind of a variable value

- Value: A single scalar value
- Array: An array of values
- Structure: A structured type with named fields
- File: A file-level container

## VariableFile

`from underautomation.fanuc.common.files.variables.variable_file import VariableFile`

Abstract base class for typed variable file readers

- `file_name: str (read only)`: Name of the variable file

## VariableFileList

`from underautomation.fanuc.common.files.variables.variable_file_list import VariableFileList`

Collection of variable files that aggregates all variables from the controller

- `VariableFileList()`
- `name: str`: Name of this variable file list
- `parent: IGenericVariableType`: Parent container

## VariableReader1

`from underautomation.fanuc.common.files.variables.variable_reader_1 import VariableReader1`

Typed variable file reader for specific variable file types

- `read_file(filePath: str, language: Languages) -> T`: Read and decode the file on disc
- Inherited from [FileReader](underautomation.fanuc.common.files.md#filereader): `file_name`

## VariableReader

`from underautomation.fanuc.common.files.variables.variable_reader import VariableReader`

Reader for Fanuc variable files (*.va)

- `static read_variable_file(fileName: str, language: Languages) -> GenericVariableFile`: Reads and parses a variable file from a file path
- `static AavmmainFile: VariableReader1[AavmmainFile]`
- `static BicsetupFile: VariableReader1[BicsetupFile]`
- `static CbparamFile: VariableReader1[CbparamFile]`
- `static CellioFile: VariableReader1[CellioFile]`
- `static ComsetFile: VariableReader1[ComsetFile]`
- `static DiocfgsvFile: VariableReader1[DiocfgsvFile]`
- `static GemdataFile: VariableReader1[GemdataFile]`
- `static HtcolrecFile: VariableReader1[HtcolrecFile]`
- `static HttpkclFile: VariableReader1[HttpkclFile]`
- `static IrcCounterFile: VariableReader1[IrcCounterFile]`
- `static IrcMsgFile: VariableReader1[IrcMsgFile]`
- `static IrcStatusFile: VariableReader1[IrcStatusFile]`
- `static IrcStlabelFile: VariableReader1[IrcStlabelFile]`
- `static KlactionFile: VariableReader1[KlactionFile]`
- `static MixlogicFile: VariableReader1[MixlogicFile]`
- `static MtparamFile: VariableReader1[MtparamFile]`
- `static NumregFile: VariableReader1[NumregFile]`
- `static PalregFile: VariableReader1[PalregFile]`
- `static PosregFile: VariableReader1[PosregFile]`
- `static StrregFile: VariableReader1[StrregFile]`
- `static SwiupdtFile: VariableReader1[SwiupdtFile]`
- `static SycldintFile: VariableReader1[SycldintFile]`
- `static SymotnFile: VariableReader1[SymotnFile]`
- `static SynosaveFile: VariableReader1[SynosaveFile]`
- `static SysframeFile: VariableReader1[SysframeFile]`
- `static SysfsacFile: VariableReader1[SysfsacFile]`
- `static SyshostFile: VariableReader1[SyshostFile]`
- `static SysmacroFile: VariableReader1[SysmacroFile]`
- `static SysmastFile: VariableReader1[SysmastFile]`
- `static SyspassFile: VariableReader1[SyspassFile]`
- `static SysservoFile: VariableReader1[SysservoFile]`
- `static SystemFile: VariableReader1[SystemFile]`
- `static SysuifFile: VariableReader1[SysuifFile]`
- `static TpsnapFile: VariableReader1[TpsnapFile]`
- `static VcmrinitFile: VariableReader1[VcmrinitFile]`
- `read_file(filePath: str, language: Languages) -> GenericVariableFile`: Read and decode the file on disc
- Inherited from [FileReader](underautomation.fanuc.common.files.md#filereader): `file_name`

## VcmrinitFile

`from underautomation.fanuc.common.files.variables.vcmrinit_file import VcmrinitFile`

Describes the Fanuc variable file vcmrinit.va

- `VcmrinitFile()`
- `vdetect_var: VcalVdVariableType (read only)`: Value of variable VDETECT_VAR
- `vfb_var: VcalVfVariableType (read only)`: Value of variable VFB_VAR
- `move_var: VcalMvVariableType (read only)`: Value of variable MOVE_VAR
- `vtcp_var: VtcpsetVariableType (read only)`: Value of variable VTCP_VAR
- `select_grp: int (read only)`: Value of variable SELECT_GRP
- `arg_str: str (read only)`: Value of variable ARG_STR
- `data_type: int (read only)`: Value of variable DATA_TYPE
- `dmy_int: int (read only)`: Value of variable DMY_INT
- `dmy_real: float (read only)`: Value of variable DMY_REAL
- `dmy_str: str (read only)`: Value of variable DMY_STR
- `dmy_stat: int (read only)`: Value of variable DMY_STAT
- `param_val: str (read only)`: Value of variable PARAM_VAL
- `prm_set_done: bool (read only)`: Value of variable PRM_SET_DONE
- Inherited from [GenericVariableFile](underautomation.fanuc.common.files.variables.md#genericvariablefile): `get_field`, `generate_va`, `generated_va`, `variables`, `name`, `parent`
