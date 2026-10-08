# UnderAutomation.Fanuc.Common.Files.Variables

## AavmmainFile

`class AavmmainFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file aavmmain.va

- `AavmmainFile()`
- `int AavmStep { get; }`: Value of variable AAVM_STEP
- `int AeContAve { get; }`: Value of variable AE_CONT_AVE
- `int AeContLow { get; }`: Value of variable AE_CONT_LOW
- `int AeNumRetry { get; }`: Value of variable AE_NUM_RETRY
- `double AeRadiRatio { get; }`: Value of variable AE_RADI_RATIO
- `double AspectLow { get; }`: Value of variable ASPECT_LOW
- `double[] CmpJpos { get; }`: Value of variable CMP_JPOS
- `double CondNum { get; }`: Value of variable COND_NUM
- `int DataType { get; }`: Value of variable DATA_TYPE
- `int Device { get; }`: Value of variable DEVICE
- `int DmyInt { get; }`: Value of variable DMY_INT
- `double DmyReal { get; }`: Value of variable DMY_REAL
- `int DmyStat { get; }`: Value of variable DMY_STAT
- `string DmyStr { get; }`: Value of variable DMY_STR
- `string DmyStr2 { get; }`: Value of variable DMY_STR2
- `int DualNum { get; }`: Value of variable DUAL_NUM
- `double ErTargtx { get; }`: Value of variable ER_TARGTX
- `double ErTargtx1 { get; }`: Value of variable ER_TARGTX1
- `double ErTargtx2 { get; }`: Value of variable ER_TARGTX2
- `double ErTargty { get; }`: Value of variable ER_TARGTY
- `double ErTargtz { get; }`: Value of variable ER_TARGTZ
- `double ErTargtz1 { get; }`: Value of variable ER_TARGTZ1
- `double ErTargtz2 { get; }`: Value of variable ER_TARGTZ2
- `double ErVtcpx { get; }`: Value of variable ER_VTCPX
- `double ErVtcpx1 { get; }`: Value of variable ER_VTCPX1
- `double ErVtcpx2 { get; }`: Value of variable ER_VTCPX2
- `double ErVtcpz { get; }`: Value of variable ER_VTCPZ
- `double ErVtcpz1 { get; }`: Value of variable ER_VTCPZ1
- `double ErVtcpz2 { get; }`: Value of variable ER_VTCPZ2
- `int[] ExtMct0 { get; }`: Value of variable EXT_MCT0
- `string FileName { get; }`: Value of variable FILE_NAME
- `int I { get; }`: Value of variable I
- `bool IsAutoexpo { get; }`: Value of variable IS_AUTOEXPO
- `double[,] JposData { get; }`: Value of variable JPOS_DATA
- `int LogPort { get; }`: Value of variable LOG_PORT
- `double[] MastAxis { get; }`: Value of variable MAST_AXIS
- `int[] MastCoun0 { get; }`: Value of variable MAST_COUN0
- `int[] MastCoun02 { get; }`: Value of variable MAST_COUN0_2
- `CartesianPositionVariable[] MeasPose { get; }`: Value of variable MEAS_POSE
- `int MinNumDots { get; }`: Value of variable MIN_NUM_DOTS
- `int NumAxis { get; }`: Value of variable NUM_AXIS
- `string ParamName { get; }`: Value of variable PARAM_NAME
- `double PixSizHigh { get; }`: Value of variable PIX_SIZ_HIGH
- `double PixSizeLow { get; }`: Value of variable PIX_SIZE_LOW
- `AavmGrpVariableType Prm { get; }`: Value of variable PRM
- `int PsRobGrp { get; }`: Value of variable PS_ROB_GRP
- `double ResEr1Thsd { get; }`: Value of variable RES_ER1_THSD
- `double ResEr2Thsd { get; }`: Value of variable RES_ER2_THSD
- `double ResErr { get; }`: Value of variable RES_ERR
- `double ResErr1 { get; }`: Value of variable RES_ERR1
- `double ResErr2 { get; }`: Value of variable RES_ERR2
- `string ResErrStr { get; }`: Value of variable RES_ERR_STR
- `int RobGrp { get; }`: Value of variable ROB_GRP
- `int SAxisNum { get; }`: Value of variable S_AXIS_NUM
- `int StepSu1 { get; }`: Value of variable STEP_SU1
- `int StepSu2 { get; }`: Value of variable STEP_SU2
- `int StepSu3 { get; }`: Value of variable STEP_SU3
- `int StepSu4 { get; }`: Value of variable STEP_SU4
- `double TagtX1Thsd { get; }`: Value of variable TAGT_X1_THSD
- `double TagtX2Thsd { get; }`: Value of variable TAGT_X2_THSD
- `double TagtZ1Thsd { get; }`: Value of variable TAGT_Z1_THSD
- `double TagtZ2Thsd { get; }`: Value of variable TAGT_Z2_THSD
- `CartesianPositionVariable Target { get; }`: Value of variable TARGET
- `CartesianPositionVariable Target0 { get; }`: Value of variable TARGET0
- `double[] TmpAxis { get; }`: Value of variable TMP_AXIS
- `bool TppRun { get; }`: Value of variable TPP_RUN
- `double[,] VfbMat { get; }`: Value of variable VFB_MAT
- `CartesianPositionVariable Vtcp { get; }`: Value of variable VTCP
- `CartesianPositionVariable Vtcp0 { get; }`: Value of variable VTCP0
- `double VtcpX1Thsd { get; }`: Value of variable VTCP_X1_THSD
- `double VtcpX2Thsd { get; }`: Value of variable VTCP_X2_THSD
- `double VtcpZ1Thsd { get; }`: Value of variable VTCP_Z1_THSD
- `double VtcpZ2Thsd { get; }`: Value of variable VTCP_Z2_THSD
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## ArrayElement

`class ArrayElement : GenericField, IGenericVariableType`

Describes all elements inside an array. Basically, a wrapping of GenericField where some properties are inherited from it

- `ArrayElement()`
- `string Access { get; }`: Parent Access
- `bool IsRegister { get; }`: Parent IsRegister
- `string Name { get; }`: Element index, example : [1] or [2,1]
- `int StringLength { get; }`: Parent StringLength
- `string Type { get; }`: Parent Type
- Inherited from [GenericField](UnderAutomation.Fanuc.Common.Files.Variables.md#genericfield): `Dimension1`, `Dimension2`
- Inherited from [GenericValue](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvalue): `Parent`, `Kind`, `Fields`, `IsUninitialized`, `Value`, `RegisterName`, `FullName`

## BicsetupFile

`class BicsetupFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file bicsetup.va

- `BicsetupFile()`
- `string BicName { get; }`: Value of variable BIC_NAME
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## CbparamFile

`class CbparamFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file cbparam.va

- `CbparamFile()`
- `double[] DataC1 { get; }`: Value of variable DATA_C1
- `double[] DataC10 { get; }`: Value of variable DATA_C10
- `double[] DataC2 { get; }`: Value of variable DATA_C2
- `double[] DataC3 { get; }`: Value of variable DATA_C3
- `double[] DataC4 { get; }`: Value of variable DATA_C4
- `double[] DataC5 { get; }`: Value of variable DATA_C5
- `double[] DataC6 { get; }`: Value of variable DATA_C6
- `double[] DataC7 { get; }`: Value of variable DATA_C7
- `double[] DataC8 { get; }`: Value of variable DATA_C8
- `double[] DataC9 { get; }`: Value of variable DATA_C9
- `double Payload1 { get; }`: Value of variable PAYLOAD1
- `double Payload1Ix { get; }`: Value of variable PAYLOAD1_IX
- `double Payload1Iy { get; }`: Value of variable PAYLOAD1_IY
- `double Payload1Iz { get; }`: Value of variable PAYLOAD1_IZ
- `double Payload1X { get; }`: Value of variable PAYLOAD1_X
- `double Payload1Y { get; }`: Value of variable PAYLOAD1_Y
- `double Payload1Z { get; }`: Value of variable PAYLOAD1_Z
- `double Payload2 { get; }`: Value of variable PAYLOAD2
- `double Payload2Ix { get; }`: Value of variable PAYLOAD2_IX
- `double Payload2Iy { get; }`: Value of variable PAYLOAD2_IY
- `double Payload2Iz { get; }`: Value of variable PAYLOAD2_IZ
- `double Payload2X { get; }`: Value of variable PAYLOAD2_X
- `double Payload2Y { get; }`: Value of variable PAYLOAD2_Y
- `double Payload2Z { get; }`: Value of variable PAYLOAD2_Z
- `int SeCtrlmode { get; }`: Value of variable SE_CTRLMODE
- `double[] TframeX { get; }`: Value of variable TFRAME_X
- `double[] TframeY { get; }`: Value of variable TFRAME_Y
- `double[] TframeZ { get; }`: Value of variable TFRAME_Z
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## CellioFile

`class CellioFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file cellio.va

- `CellioFile()`
- `bool CellOption { get; }`: Value of variable $CELL_OPTION
- `CellsetVariableType CellSetup { get; }`: Value of variable $CELL_SETUP
- `ClmlioVariableType[] Clmlio { get; }`: Value of variable $CLMLIO
- `string[] StyleComnt { get; }`: Value of variable $STYLE_COMNT
- `int StyleCount { get; }`: Value of variable $STYLE_COUNT
- `bool[] StyleEnab { get; }`: Value of variable $STYLE_ENAB
- `int StyleMenu { get; }`: Value of variable $STYLE_MENU
- `string[] StyleName { get; }`: Value of variable $STYLE_NAME
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## ComsetFile

`class ComsetFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file comset.va

- `ComsetFile()`
- `int DiAlmfc { get; }`: Value of variable DI_ALMFC
- `int DoAlmfc { get; }`: Value of variable DO_ALMFC
- `int FlagAlmfc { get; }`: Value of variable FLAG_ALMFC
- `bool Frvrc { get; }`: Value of variable FRVRC
- `int IcommentLen { get; }`: Value of variable ICOMMENT_LEN
- `int Ifc { get; }`: Value of variable IFC
- `int Iretsize { get; }`: Value of variable IRETSIZE
- `int NStatus { get; }`: Value of variable N_STATUS
- `int PregAlmfc { get; }`: Value of variable PREG_ALMFC
- `int RegAlmfc { get; }`: Value of variable REG_ALMFC
- `string Respfile { get; }`: Value of variable RESPFILE
- `string Scomment { get; }`: Value of variable SCOMMENT
- `string Scopystr { get; }`: Value of variable SCOPYSTR
- `bool Searchcancel { get; }`: Value of variable SEARCHCANCEL
- `bool Searchcase { get; }`: Value of variable SEARCHCASE
- `string Searchfile { get; }`: Value of variable SEARCHFILE
- `string Sfc { get; }`: Value of variable SFC
- `string Sindx { get; }`: Value of variable SINDX
- `string Srealflag { get; }`: Value of variable SREALFLAG
- `string Svalue { get; }`: Value of variable SVALUE
- `string Url { get; }`: Value of variable URL
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## DiocfgsvFile

`class DiocfgsvFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file diocfgsv.va

- `DiocfgsvFile()`
- `byte[] AisRackNo { get; }`: Value of variable AIS_RACK_NO
- `string[] AisSequence { get; }`: Value of variable AIS_SEQUENCE
- `byte[] AisSlotNo { get; }`: Value of variable AIS_SLOT_NO
- `short[] AsgLogPn { get; }`: Value of variable ASG_LOG_PN
- `byte[] AsgLogPt { get; }`: Value of variable ASG_LOG_PT
- `short[] AsgNPts { get; }`: Value of variable ASG_N_PTS
- `short[] AsgPhyPn { get; }`: Value of variable ASG_PHY_PN
- `byte[] AsgPhyPt { get; }`: Value of variable ASG_PHY_PT
- `byte[] AsgRackNo { get; }`: Value of variable ASG_RACK_NO
- `byte[] AsgSlotNo { get; }`: Value of variable ASG_SLOT_NO
- `int CfgFileVer { get; }`: Value of variable CFG_FILE_VER
- `string[] DevComment { get; }`: Value of variable DEV_COMMENT
- `short[] DevDataType { get; }`: Value of variable DEV_DATA_TYPE
- `short[] DevModId { get; }`: Value of variable DEV_MOD_ID
- `short[] DevParam1 { get; }`: Value of variable DEV_PARAM1
- `short[] DevParam2 { get; }`: Value of variable DEV_PARAM2
- `short[] DevRack { get; }`: Value of variable DEV_RACK
- `short[] DevSlot { get; }`: Value of variable DEV_SLOT
- `short[] ModeFrstPn { get; }`: Value of variable MODE_FRST_PN
- `short[] ModeLastPn { get; }`: Value of variable MODE_LAST_PN
- `byte[] ModeLogPt { get; }`: Value of variable MODE_LOG_PT
- `byte[] ModeMode { get; }`: Value of variable MODE_MODE
- `short[] NameLogPn { get; }`: Value of variable NAME_LOG_PN
- `byte[] NameLogPt { get; }`: Value of variable NAME_LOG_PT
- `string[] NameName { get; }`: Value of variable NAME_NAME
- `string[] NameName2 { get; }`: Value of variable NAME_NAME2
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## GemdataFile

`class GemdataFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file gemdata.va

- `GemdataFile()`
- `int AnswerDelay { get; }`: Value of variable ANSWER_DELAY
- `bool DebugMsg { get; }`: Value of variable DEBUG_MSG
- `int WaitAct { get; }`: Value of variable WAIT_ACT
- `int WaitTime { get; }`: Value of variable WAIT_TIME
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## GenericField

`class GenericField : GenericValue, IGenericVariableType`

Represents a named field within a variable structure

- `GenericField()`
- `string Access { get; }`: Access modifier of the field (e.g. RW, RO)
- `int Dimension1 { get; }`: First dimension size of the array, or first index of an array element
- `int Dimension2 { get; }`: Second dimension size of the array, or second index of an array element
- `bool IsRegister { get; }`: Indicates whether this field is a register
- `int StringLength { get; }`: Maximum string length if the field type is STRING
- `string Type { get; set; }`: Data type name of the field
- Inherited from [GenericValue](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvalue): `Parent`, `Kind`, `Fields`, `Name`, `IsUninitialized`, `Value`, `RegisterName`, `FullName`

## GenericValue

`class GenericValue : IGenericVariableType`

Represents a generic variable value with optional child fields

- `GenericValue()`
- `GenericField[] Fields { get; }`: Child fields of this value
- `string FullName { get; }`: Fully qualified name including all parent names
- `bool IsUninitialized { get; }`: Indicates whether this value is uninitialized
- `ValueKind Kind { get; }`: Kind of value (scalar, array, structure, or file)
- `string Name { get; }`: Name of this value
- `GenericValue Parent { get; }`: Parent value that contains this value
- `string RegisterName { get; }`: Register name associated with this value
- `string Value { get; }`: String representation of the value

## GenericVariable

`class GenericVariable : GenericField, IGenericVariableType`

Represents a top-level variable declaration with scope and storage information

- `GenericVariable()`
- `IGenericVariableType Parent { get; }`: Parent container of this variable
- `string Scope { get; }`: Variable scope (e.g. PROG, SYS)
- `string Storage { get; }`: Storage type of the variable (e.g. CMOS, DRAM)
- Inherited from [GenericField](UnderAutomation.Fanuc.Common.Files.Variables.md#genericfield): `Access`, `Type`, `IsRegister`, `StringLength`, `Dimension1`, `Dimension2`
- Inherited from [GenericValue](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvalue): `Kind`, `Fields`, `Name`, `IsUninitialized`, `Value`, `RegisterName`, `FullName`

## GenericVariableFile

`class GenericVariableFile : IGenericVariableType, IFanucContent`

Represents a parsed Fanuc variable file containing one or more variables

- `GenericVariableFile()`
- `void GenerateVa(Stream stream)`: Generates a .va file and writes it to the specified stream
- `void GenerateVa(string pathToVa)`: Generates a .va file and writes it to the specified path
- `string GeneratedVa()`: Generates the content of a .va variable file as a string.
- `GenericVariable GetField(string name)`: Gets a variable by name (case-insensitive)
- `string Name { get; }`: File name
- `IGenericVariableType Parent { get; set; }`: Parent container
- `GenericVariable[] Variables { get; }`: Variables declared in this file

## GenericVariableTypeHelpers

`static class GenericVariableTypeHelpers`

Extension methods for IGenericVariableType

- `static IGenericVariableType[] GetAncestors(this IGenericVariableType element)`: Recursively get parents in an array. The first element is the root element and the last one is the direct parent of the element.
- `static IGenericVariableType GetField(this IGenericVariableType element, string name)`: Get a field by its name (case insensitive)

## HtcolrecFile

`class HtcolrecFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file htcolrec.va

- `HtcolrecFile()`
- `int AbortDelay { get; }`: Value of variable ABORT_DELAY
- `bool ColDbg { get; }`: Value of variable COL_DBG
- `bool ColRec { get; }`: Value of variable COL_REC
- `AutoColRecVariableType ColRecov { get; }`: Value of variable COL_RECOV
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## HttpkclFile

`class HttpkclFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file httpkcl.va

- `HttpkclFile()`
- `string[] Cmds { get; }`: Value of variable CMDS
- `string FirstToken { get; }`: Value of variable FIRST_TOKEN
- `bool Found { get; }`: Value of variable FOUND
- `int I { get; }`: Value of variable I
- `bool IllFlg { get; }`: Value of variable ILL_FLG
- `string Newcmd { get; }`: Value of variable NEWCMD
- `int Status { get; }`: Value of variable STATUS
- `string Url { get; }`: Value of variable URL
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## IrcCounterFile

`class IrcCounterFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file irc_counter.va

- `IrcCounterFile()`
- `string[] AttachFiles { get; }`: Value of variable ATTACH_FILES
- `int CounterMode { get; }`: Value of variable COUNTER_MODE
- `int CurTime { get; }`: Value of variable CUR_TIME
- `string CurTimeStr { get; }`: Value of variable CUR_TIME_STR
- `bool DbgRc { get; }`: Value of variable DBG_RC
- `string FileName { get; }`: Value of variable FILE_NAME
- `IrcGnrcVariableType IrcGnrc { get; }`: Value of variable IRC_GNRC
- `string Pkrcxmlfile { get; }`: Value of variable PKRCXMLFILE
- `bool SendEmail { get; }`: Value of variable SEND_EMAIL
- `int SndPriority { get; }`: Value of variable SND_PRIORITY
- `int Status { get; }`: Value of variable STATUS
- `int ThrDuration { get; }`: Value of variable THR_DURATION
- `int ThrPrvtime { get; }`: Value of variable THR_PRVTIME
- `bool TppGencall { get; }`: Value of variable TPP_GENCALL
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## IrcMsgFile

`class IrcMsgFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file irc_msg.va

- `IrcMsgFile()`
- `string[] AttachFiles { get; }`: Value of variable ATTACH_FILES
- `int CurTime { get; }`: Value of variable CUR_TIME
- `string CurTimeStr { get; }`: Value of variable CUR_TIME_STR
- `bool DbgRc { get; }`: Value of variable DBG_RC
- `string FileName { get; }`: Value of variable FILE_NAME
- `IrcGnrcVariableType IrcGnrc { get; }`: Value of variable IRC_GNRC
- `string Pkrcxmlfile { get; }`: Value of variable PKRCXMLFILE
- `bool SendEmail { get; }`: Value of variable SEND_EMAIL
- `int SndPriority { get; }`: Value of variable SND_PRIORITY
- `int Status { get; }`: Value of variable STATUS
- `int ThrDuration { get; }`: Value of variable THR_DURATION
- `int ThrPrvtime { get; }`: Value of variable THR_PRVTIME
- `bool TppGencall { get; }`: Value of variable TPP_GENCALL
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## IrcStatusFile

`class IrcStatusFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file irc_status.va

- `IrcStatusFile()`
- `string[] AttachFiles { get; }`: Value of variable ATTACH_FILES
- `int CurTime { get; }`: Value of variable CUR_TIME
- `string CurTimeStr { get; }`: Value of variable CUR_TIME_STR
- `bool DbgRc { get; }`: Value of variable DBG_RC
- `string FileName { get; }`: Value of variable FILE_NAME
- `IrcGnrcVariableType IrcGnrc { get; }`: Value of variable IRC_GNRC
- `string Pkrcxmlfile { get; }`: Value of variable PKRCXMLFILE
- `bool SendEmail { get; }`: Value of variable SEND_EMAIL
- `int SndPriority { get; }`: Value of variable SND_PRIORITY
- `int Status { get; }`: Value of variable STATUS
- `int ThrDuration { get; }`: Value of variable THR_DURATION
- `int ThrPrvtime { get; }`: Value of variable THR_PRVTIME
- `bool TppGencall { get; }`: Value of variable TPP_GENCALL
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## IrcStlabelFile

`class IrcStlabelFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file irc_stlabel.va

- `IrcStlabelFile()`
- `string[] AttachFiles { get; }`: Value of variable ATTACH_FILES
- `int CurTime { get; }`: Value of variable CUR_TIME
- `string CurTimeStr { get; }`: Value of variable CUR_TIME_STR
- `bool DbgRc { get; }`: Value of variable DBG_RC
- `string FileName { get; }`: Value of variable FILE_NAME
- `IrcGnrcVariableType IrcGnrc { get; }`: Value of variable IRC_GNRC
- `string Pkrcxmlfile { get; }`: Value of variable PKRCXMLFILE
- `bool SendEmail { get; }`: Value of variable SEND_EMAIL
- `int SndPriority { get; }`: Value of variable SND_PRIORITY
- `int Status { get; }`: Value of variable STATUS
- `int ThrDuration { get; }`: Value of variable THR_DURATION
- `int ThrPrvtime { get; }`: Value of variable THR_PRVTIME
- `bool TppGencall { get; }`: Value of variable TPP_GENCALL
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## KlactionFile

`class KlactionFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file klaction.va

- `KlactionFile()`
- `int DataType { get; }`: Value of variable DATA_TYPE
- `int IntValue { get; }`: Value of variable INT_VALUE
- `bool ParamOk { get; }`: Value of variable PARAM_OK
- `double RealValue { get; }`: Value of variable REAL_VALUE
- `int Status { get; }`: Value of variable STATUS
- `string StringValue { get; }`: Value of variable STRING_VALUE
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## MixlogicFile

`class MixlogicFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file mixlogic.va

- `MixlogicFile()`
- `DryrunVariableType Dryrun { get; }`: Value of variable $DRYRUN
- `DryrunPortVariableType[] DryrunPort { get; }`: Value of variable $DRYRUN_PORT
- `string[] DryrunSub { get; }`: Value of variable $DRYRUN_SUB
- `MixBgVariableType[] MixBg { get; }`: Value of variable $MIX_BG
- `MixLogicVariableType MixLogic { get; }`: Value of variable $MIX_LOGIC
- `MixMkrVariableType[] MixMkr { get; }`: Value of variable $MIX_MKR
- `OnPathVariableType OnPath { get; }`: Value of variable $ON_PATH
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## MtparamFile

`class MtparamFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file mtparam.va

- `MtparamFile()`
- `double[] ADissip { get; }`: Value of variable A_DISSIP
- `double[] AExponent { get; }`: Value of variable A_EXPONENT
- `double[] AFriction { get; }`: Value of variable A_FRICTION
- `double[] AMotor { get; }`: Value of variable A_MOTOR
- `double[] AOther1 { get; }`: Value of variable A_OTHER1
- `double[] AOther2 { get; }`: Value of variable A_OTHER2
- `double[] AOther3 { get; }`: Value of variable A_OTHER3
- `double[] AOther4 { get; }`: Value of variable A_OTHER4
- `double[] AOther5 { get; }`: Value of variable A_OTHER5
- `double[] AOther6 { get; }`: Value of variable A_OTHER6
- `double[] CoeffOff { get; }`: Value of variable COEFF_OFF
- `double[] CoulombN { get; }`: Value of variable COULOMB_N
- `double[] CoulombN0 { get; }`: Value of variable COULOMB_N0
- `int[] DefItm { get; }`: Value of variable DEF_ITM
- `int[] DefItm2 { get; }`: Value of variable DEF_ITM2
- `int[] DefItmI { get; }`: Value of variable DEF_ITM_I
- `double[] Distance { get; }`: Value of variable DISTANCE
- `int[] DueOnce { get; }`: Value of variable DUE_ONCE
- `int[] DueOnce2 { get; }`: Value of variable DUE_ONCE2
- `int[] DueOnceI { get; }`: Value of variable DUE_ONCE_I
- `int[] FormulaId { get; }`: Value of variable FORMULA_ID
- `double[] GrsLife { get; }`: Value of variable GRS_LIFE
- `int IntellGrs { get; }`: Value of variable INTELL_GRS
- `int[] IntlAct { get; }`: Value of variable INTL_ACT
- `int[] IntlAct2 { get; }`: Value of variable INTL_ACT2
- `int[] IntlActI { get; }`: Value of variable INTL_ACT_I
- `int[] IntlRun { get; }`: Value of variable INTL_RUN
- `int[] IntlRun2 { get; }`: Value of variable INTL_RUN2
- `int[] IntlRunI { get; }`: Value of variable INTL_RUN_I
- `double[] Limit { get; }`: Value of variable LIMIT
- `double[] MaxVMotor { get; }`: Value of variable MAX_V_MOTOR
- `double[] SgRate { get; }`: Value of variable SG_RATE
- `double[] TGrsLim { get; }`: Value of variable T_GRS_LIM
- `double[] TGrsThre { get; }`: Value of variable T_GRS_THRE
- `double[] Theta1 { get; }`: Value of variable THETA_1
- `double[] Theta2 { get; }`: Value of variable THETA_2
- `double[] Theta3 { get; }`: Value of variable THETA_3
- `double[] Theta4 { get; }`: Value of variable THETA_4
- `double[] Theta5 { get; }`: Value of variable THETA_5
- `double[] Viscosity { get; }`: Value of variable VISCOSITY
- `double[] Weight1 { get; }`: Value of variable WEIGHT_1
- `double[] Weight2 { get; }`: Value of variable WEIGHT_2
- `double[] Weight3 { get; }`: Value of variable WEIGHT_3
- `double[] Weight4 { get; }`: Value of variable WEIGHT_4
- `double[] Weight5 { get; }`: Value of variable WEIGHT_5
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## NumregFile

`class NumregFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file numreg.va

- `NumregFile()`
- `int Maxregnum { get; }`: Value of variable $MAXREGNUM
- `double[] Numreg { get; }`: Value of variable $NUMREG
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## PalregFile

`class PalregFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file palreg.va

- `PalregFile()`
- `byte[] Palreg { get; }`: Value of variable $PALREG
- `int Palregnum { get; }`: Value of variable $PALREGNUM
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## PosregFile

`class PosregFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file posreg.va

- `PosregFile()`
- `int Maxpregnum { get; }`: Value of variable $MAXPREGNUM
- `PositionRegister[,] Posreg { get; }`: Value of variable $POSREG
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## StrregFile

`class StrregFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file strreg.va

- `StrregFile()`
- `int Maxsregnum { get; }`: Value of variable $MAXSREGNUM
- `string[] Strreg { get; }`: Value of variable $STRREG
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## SwiupdtFile

`class SwiupdtFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file swiupdt.va

- `SwiupdtFile()`
- `int RunOnce { get; }`: Value of variable RUN_ONCE
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## SycldintFile

`class SycldintFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file sycldint.va

- `SycldintFile()`
- `int Erseverity { get; }`: Value of variable $ERSEVERITY
- `JcrVariableType Jcr { get; }`: Value of variable $JCR
- `JcrGrpVariableType[] JcrGrp { get; }`: Value of variable $JCR_GRP
- `string LoadDevice { get; }`: Value of variable $LOAD_DEVICE
- `McrVariableType Mcr { get; }`: Value of variable $MCR
- `McrGrpVariableType[] McrGrp { get; }`: Value of variable $MCR_GRP
- `MorVariableType Mor { get; }`: Value of variable $MOR
- `MorGrpVariableType[] MorGrp { get; }`: Value of variable $MOR_GRP
- `string[] PwrUpRtn { get; }`: Value of variable $PWR_UP_RTN
- `bool TpabrtUsed { get; }`: Value of variable $TPABRT_USED
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## SymotnFile

`class SymotnFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file symotn.va

- `SymotnFile()`
- `CfParamgpVariableType[] CfParamgp { get; }`: Value of variable $CF_PARAMGP
- `CrcfgVariableType Crcfg { get; }`: Value of variable $CRCFG
- `EncStatVariableType[] EncStat { get; }`: Value of variable $ENC_STAT
- `Fmr2GrpVariableType[] Fmr2Grp { get; }`: Value of variable $FMR2_GRP
- `UprVariableType[] Group { get; }`: Value of variable $GROUP
- `HscdGrpVariableType[] HscdGroup { get; }`: Value of variable $HSCD_GROUP
- `UjrGrpVariableType[] JogGroup { get; }`: Value of variable $JOG_GROUP
- `MiscGrpVariableType[] Misc { get; }`: Value of variable $MISC
- `int MotaskData { get; }`: Value of variable $MOTASK_DATA
- `Mrr2GrpVariableType[] Mrr2Grp { get; }`: Value of variable $MRR2_GRP
- `MrrGrpVariableType[] MrrGrp { get; }`: Value of variable $MRR_GRP
- `Mrr2GrpVariableType[] Param2Grp { get; }`: Value of variable $PARAM2_GRP
- `MrrGrpVariableType[] ParamGroup { get; }`: Value of variable $PARAM_GROUP
- `PlidGrpVariableType[] PlidGrp { get; }`: Value of variable $PLID_GRP
- `PlidSvVariableType PlidSv { get; }`: Value of variable $PLID_SV
- `PlstGrpVariableType[] PlstGrp1 { get; }`: Value of variable $PLST_GRP1
- `PlstGrpVariableType[] PlstGrp2 { get; }`: Value of variable $PLST_GRP2
- `PlstGrpVariableType[] PlstGrp3 { get; }`: Value of variable $PLST_GRP3
- `PlstGrpVariableType[] PlstGrp4 { get; }`: Value of variable $PLST_GRP4
- `PlstGrpVariableType[] PlstGrp5 { get; }`: Value of variable $PLST_GRP5
- `int PlstGrpmad { get; }`: Value of variable $PLST_GRPMAD
- `int[] PlstParnum { get; }`: Value of variable $PLST_PARNUM
- `int PlstSchmad { get; }`: Value of variable $PLST_SCHMAD
- `int PlstSchnum { get; }`: Value of variable $PLST_SCHNUM
- `int[] PlstUpdnum { get; }`: Value of variable $PLST_UPDNUM
- `PodataVariableType[] PodataGrp { get; }`: Value of variable $PODATA_GRP
- `PoinfoVariableType[] PoinfoGrp { get; }`: Value of variable $POINFO_GRP
- `PoioVariableType[] PoioGrp { get; }`: Value of variable $POIO_GRP
- `PssaveGrpVariableType[] PssaveGrp { get; }`: Value of variable $PSSAVE_GRP
- `ScrVariableType Scr { get; }`: Value of variable $SCR
- `ScrGrpVariableType[] ScrGrp { get; }`: Value of variable $SCR_GRP
- `TbcGrpVariableType[] TbcGrp { get; }`: Value of variable $TBC_GRP
- `TbccfgVariableType Tbccfg { get; }`: Value of variable $TBCCFG
- `TbjGrpVariableType[] TbjGrp { get; }`: Value of variable $TBJ_GRP
- `TbjcfgVariableType Tbjcfg { get; }`: Value of variable $TBJCFG
- `TorqctrlVariableType Torqctrl { get; }`: Value of variable $TORQCTRL
- `TsrGrpVariableType[] TsrGrp { get; }`: Value of variable $TSR_GRP
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## SynosaveFile

`class SynosaveFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file synosave.va

- `SynosaveFile()`
- `AavmGrpVariableType[] AavmGrp { get; }`: Value of variable $AAVM_GRP
- `int AimageBack { get; }`: Value of variable $AIMAGE_BACK
- `int AutoupdtSt { get; }`: Value of variable $AUTOUPDT_ST
- `int Blt { get; }`: Value of variable $BLT
- `int DaqGfdUse { get; }`: Value of variable $DAQ_GFD_USE
- `DbworkVariableType[] Dbwork { get; }`: Value of variable $DBWORK
- `string Device { get; }`: Value of variable $DEVICE
- `int Dfmtn0No { get; }`: Value of variable $DFMTN0_NO
- `DhcpIntVariableType[] DhcpInt { get; }`: Value of variable $DHCP_INT
- `int DistbfData { get; }`: Value of variable $DISTBF_DATA
- `int FastClock { get; }`: Value of variable $FAST_CLOCK
- `int FileBasept { get; }`: Value of variable $FILE_BASEPT
- `FileBackVariableType[] FileErrbck { get; }`: Value of variable $FILE_ERRBCK
- `int FileMaxsec { get; }`: Value of variable $FILE_MAXSEC
- `FileBackVariableType[] FileSysbck { get; }`: Value of variable $FILE_SYSBCK
- `FileconfigVariableType Fileconfig { get; }`: Value of variable $FILECONFIG
- `FileSetupVariableType Filesetup { get; }`: Value of variable $FILESETUP
- `GlofattVariableType[] Glofatt { get; }`: Value of variable $GLOFATT
- `GlofsetVariableType Glofset { get; }`: Value of variable $GLOFSET
- `bool ImsaveDone { get; }`: Value of variable $IMSAVE_DONE
- `string KclRpcout { get; }`: Value of variable $KCL_RPCOUT
- `JointPositionVariable[] Lastpauspos { get; }`: Value of variable $LASTPAUSPOS
- `int MasterEnb { get; }`: Value of variable $MASTER_ENB
- `MemoMemoVariableType Memo { get; }`: Value of variable $MEMO
- `MoptimizVariableType Moptimiz { get; }`: Value of variable $MOPTIMIZ
- `int NullCycle { get; }`: Value of variable $NULL_CYCLE
- `OptstateVariableType OptState { get; }`: Value of variable $OPT_STATE
- `int PadjSchnum { get; }`: Value of variable $PADJ_SCHNUM
- `PgmaxspdVariableType[] PgMaxSped { get; }`: Value of variable $PG_MAX_SPED
- `PrgadjSchVariableType[] PrgadjSch { get; }`: Value of variable $PRGADJ_SCH
- `ShellWrkVariableType ShellWrk { get; }`: Value of variable $SHELL_WRK
- `SmhMadeVariableType SmhMade { get; }`: Value of variable $SMH_MADE
- `int StartupDbg { get; }`: Value of variable $STARTUP_DBG
- `SscbkVariableType SysConfig { get; }`: Value of variable $SYS_CONFIG
- `SysTimeVariableType SysTime { get; }`: Value of variable $SYS_TIME
- `int TickRate { get; }`: Value of variable $TICK_RATE
- `TpCurscrnVariableType[] TpCurscrn { get; }`: Value of variable $TP_CURSCRN
- `TxVariableType Tx { get; }`: Value of variable $TX
- `TxramVariableType Txram { get; }`: Value of variable $TXRAM
- `TpCurscrnVariableType[,] UiCurscrn { get; }`: Value of variable $UI_CURSCRN
- `UiFctnfavVariableType[] UiFctnfav { get; }`: Value of variable $UI_FCTNFAV
- `UiPanelnkVariableType[] UiPanelink { get; }`: Value of variable $UI_PANELINK
- `UmrVariableType Umr { get; }`: Value of variable $UMR
- `VcrsmCfgVariableType VcrsmCfg { get; }`: Value of variable $VCRSM_CFG
- `VcwmCfgVariableType VcwmCfg { get; }`: Value of variable $VCWM_CFG
- `VcwmGrpVariableType[] VcwmGrp { get; }`: Value of variable $VCWM_GRP
- `string Vdate { get; }`: Value of variable $VDATE
- `string Version { get; }`: Value of variable $VERSION
- `VsmoTmpVariableType VsmoTmp { get; }`: Value of variable $VSMO_TMP
- `VsmoValVariableType VsmoVal { get; }`: Value of variable $VSMO_VAL
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## SysframeFile

`class SysframeFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file sysframe.va

- `SysframeFile()`
- `CartesianPositionVariable CellFloor { get; }`: Value of variable $CELL_FLOOR
- `CellGrpVariableType[] CellGrp { get; }`: Value of variable $CELL_GRP
- `CartesianPositionVariable[,] Mnuframe { get; }`: Value of variable $MNUFRAME
- `byte[] Mnuframenum { get; }`: Value of variable $MNUFRAMENUM
- `CartesianPositionVariable[,] Mnutool { get; }`: Value of variable $MNUTOOL
- `byte[] Mnutoolnum { get; }`: Value of variable $MNUTOOLNUM
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## SysfsacFile

`class SysfsacFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file sysfsac.va

- `SysfsacFile()`
- `int FsacDefLv { get; }`: Value of variable $FSAC_DEF_LV
- `int FsacEnable { get; }`: Value of variable $FSAC_ENABLE
- `FsacLstVariableType[] FsacList { get; }`: Value of variable $FSAC_LIST
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## SyshostFile

`class SyshostFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file syshost.va

- `SyshostFile()`
- `BinCfgVariableType BinCfg { get; }`: Value of variable $BIN_CFG
- `DhcpCtrlVariableType[] DhcpCtrl { get; }`: Value of variable $DHCP_CTRL
- `DnsCfgVariableType DnsCfg { get; }`: Value of variable $DNS_CFG
- `byte[] DnsLocDom { get; }`: Value of variable $DNS_LOC_DOM
- `DnssCfgVariableType DnssCfg { get; }`: Value of variable $DNSS_CFG
- `int[] EthFltr { get; }`: Value of variable $ETH_FLTR
- `FtpCtrlVariableType FtpCtrl { get; }`: Value of variable $FTP_CTRL
- `HostentVariableType[] HostShared { get; }`: Value of variable $HOST_SHARED
- `PppcfgLstVariableType[] PppList { get; }`: Value of variable $PPP_LIST
- `RcmcfgVariableType Rcmcfg { get; }`: Value of variable $RCMCFG
- `RdmCfgVariableType RdmCfg { get; }`: Value of variable $RDM_CFG
- `SmbVariableType Smb { get; }`: Value of variable $SMB
- `SmbClntVariableType[] SmbClnt { get; }`: Value of variable $SMB_CLNT
- `SmtpCtrlVariableType SmtpCtrl { get; }`: Value of variable $SMTP_CTRL
- `SntpCfgVariableType SntpCfg { get; }`: Value of variable $SNTP_CFG
- `SntpCustomVariableType SntpCustom { get; }`: Value of variable $SNTP_CUSTOM
- `TcpipcfgVariableType Tcpipcfg { get; }`: Value of variable $TCPIPCFG
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## SysmacroFile

`class SysmacroFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file sysmacro.va

- `SysmacroFile()`
- `int MacroMaxnu { get; }`: Value of variable $MACRO_MAXNU
- `bool Macrolduimt { get; }`: Value of variable $MACROLDUIMT
- `int Macromaxdri { get; }`: Value of variable $MACROMAXDRI
- `MnMcrTableVariableType[] Macrotable { get; }`: Value of variable $MACROTABLE
- `MnMcrSopVariableType Macrsopenbl { get; }`: Value of variable $MACRSOPENBL
- `int Macrspdimsk { get; }`: Value of variable $MACRSPDIMSK
- `int Macrspsumsk { get; }`: Value of variable $MACRSPSUMSK
- `bool Macrtpdsbex { get; }`: Value of variable $MACRTPDSBEX
- `MnMcrUopVariableType Macruopenbl { get; }`: Value of variable $MACRUOPENBL
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## SysmastFile

`class SysmastFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file sysmast.va

- `SysmastFile()`
- `DmrGrpVariableType[] DmrGrp { get; }`: Value of variable $DMR_GRP
- `FmsGrpVariableType[] FmsGrp { get; }`: Value of variable $FMS_GRP
- `PlclGrpVariableType[] PlclGrp { get; }`: Value of variable $PLCL_GRP
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## SyspassFile

`class SyspassFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file syspass.va

- `SyspassFile()`
- `PassnameVariableType[] Passname { get; }`: Value of variable $PASSNAME
- `PassnameVariableType Passsuper { get; }`: Value of variable $PASSSUPER
- `PasswordVariableType Password { get; }`: Value of variable $PASSWORD
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## SysservoFile

`class SysservoFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file sysservo.va

- `SysservoFile()`
- `SbrVariableType[] Sbr { get; }`: Value of variable $SBR
- `Sbr2VariableType[] Sbr2 { get; }`: Value of variable $SBR2
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## SystemFile

`class SystemFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file system.va

- `SystemFile()`
- `AavmWrkVariableType[] AavmWrk { get; }`: Value of variable $AAVM_WRK
- `AbsposGrpVariableType[] AbsposGrp { get; }`: Value of variable $ABSPOS_GRP
- `int AcUpdate { get; }`: Value of variable $AC_UPDATE
- `int AccMaxlmt { get; }`: Value of variable $ACC_MAXLMT
- `int AccMinlmt { get; }`: Value of variable $ACC_MINLMT
- `int AccPreExe { get; }`: Value of variable $ACC_PRE_EXE
- `AioCnvVariableType[] AioCnv { get; }`: Value of variable $AIO_CNV
- `int AiocnvNum { get; }`: Value of variable $AIOCNV_NUM
- `int AiocnvUse { get; }`: Value of variable $AIOCNV_USE
- `AlmIfVariableType AlmIf { get; }`: Value of variable $ALM_IF
- `AlmdgVariableType Almdg { get; }`: Value of variable $ALMDG
- `double[] Angtol { get; }`: Value of variable $ANGTOL
- `int ApActive { get; }`: Value of variable $AP_ACTIVE
- `bool ApAutomode { get; }`: Value of variable $AP_AUTOMODE
- `bool ApChgaponl { get; }`: Value of variable $AP_CHGAPONL
- `ApcoupledVariableType[] ApCoupled { get; }`: Value of variable $AP_COUPLED
- `ApcureqVariableType[] ApCureq { get; }`: Value of variable $AP_CUREQ
- `int ApCurtool { get; }`: Value of variable $AP_CURTOOL
- `bool ApDoClean { get; }`: Value of variable $AP_DO_CLEAN
- `bool[] ApDoClenm { get; }`: Value of variable $AP_DO_CLENM
- `bool ApDspdryrn { get; }`: Value of variable $AP_DSPDRYRN
- `bool[] ApHide { get; }`: Value of variable $AP_HIDE
- `int ApMaxapp { get; }`: Value of variable $AP_MAXAPP
- `int ApMaxax { get; }`: Value of variable $AP_MAXAX
- `int ApPlugged { get; }`: Value of variable $AP_PLUGGED
- `int[] ApPrcDsbm { get; }`: Value of variable $AP_PRC_DSBM
- `bool ApProcDsb { get; }`: Value of variable $AP_PROC_DSB
- `bool[] ApSegChkm { get; }`: Value of variable $AP_SEG_CHKM
- `bool ApSegfChk { get; }`: Value of variable $AP_SEGF_CHK
- `bool[] ApSelap { get; }`: Value of variable $AP_SELAP
- `int ApTotalax { get; }`: Value of variable $AP_TOTALAX
- `byte[] ApUsenum { get; }`: Value of variable $AP_USENUM
- `AppinfoVariableType Appinfo { get; }`: Value of variable $APPINFO
- `string[] Application { get; }`: Value of variable $APPLICATION
- `ArgStrVariableType[] ArgString { get; }`: Value of variable $ARG_STRING
- `string[] ArgWord { get; }`: Value of variable $ARG_WORD
- `double Argdispmmck { get; }`: Value of variable $ARGDISPMMCK
- `int Argdispmode { get; }`: Value of variable $ARGDISPMODE
- `AsbnCfgVariableType AsbnConfig { get; }`: Value of variable $ASBN_CONFIG
- `AtCellsetupVariableType Atcellsetup { get; }`: Value of variable $ATCELLSETUP
- `AutobackupVariableType Autobackup { get; }`: Value of variable $AUTOBACKUP
- `int Autoinit { get; }`: Value of variable $AUTOINIT
- `int Automessage { get; }`: Value of variable $AUTOMESSAGE
- `bool AutomodeDo { get; }`: Value of variable $AUTOMODE_DO
- `bool AutomodeOv { get; }`: Value of variable $AUTOMODE_OV
- `JointPositionVariable[] Autopauspos { get; }`: Value of variable $AUTOPAUSPOS
- `int[] Autoppostsk { get; }`: Value of variable $AUTOPPOSTSK
- `int Autoupdtmod { get; }`: Value of variable $AUTOUPDTMOD
- `int AuxwzdEnb { get; }`: Value of variable $AUXWZD_ENB
- `int AuxwzdStat { get; }`: Value of variable $AUXWZD_STAT
- `AxscrdcfgVariableType[] Axscrdcfg { get; }`: Value of variable $AXSCRDCFG
- `BackEditVariableType[] BackEdit { get; }`: Value of variable $BACK_EDIT
- `bool Background { get; }`: Value of variable $BACKGROUND
- `string BackupName { get; }`: Value of variable $BACKUP_NAME
- `bool BckNoDel { get; }`: Value of variable $BCK_NO_DEL
- `bool BgeUnusend { get; }`: Value of variable $BGE_UNUSEND
- `BigallowVariableType[] Bigallow { get; }`: Value of variable $BIGALLOW
- `BlalOutVariableType BlalOut { get; }`: Value of variable $BLAL_OUT
- `bool BwdAbort { get; }`: Value of variable $BWD_ABORT
- `int BwdItrRtn { get; }`: Value of variable $BWD_ITR_RTN
- `int BwdNonstop { get; }`: Value of variable $BWD_NONSTOP
- `int CeOption { get; }`: Value of variable $CE_OPTION
- `int CeRiaId { get; }`: Value of variable $CE_RIA_ID
- `CfcfgVariableType Cfcfg { get; }`: Value of variable $CFCFG
- `bool Checkconfig { get; }`: Value of variable $CHECKCONFIG
- `ChgPriVariableType[] ChgPri { get; }`: Value of variable $CHG_PRI
- `ChkposVariableType[] Chkpauspos { get; }`: Value of variable $CHKPAUSPOS
- `CmdInfoVariableType[] CmdInfo { get; }`: Value of variable $CMD_INFO
- `CoMorgrpVariableType[] CoMorgrp { get; }`: Value of variable $CO_MORGRP
- `CoParamgpVariableType[] CoParamgrp { get; }`: Value of variable $CO_PARAMGRP
- `CocfgVariableType Cocfg { get; }`: Value of variable $COCFG
- `CollectVariableType CollectCfg { get; }`: Value of variable $COLLECT_CFG
- `int CollectEnb { get; }`: Value of variable $COLLECT_ENB
- `CondetCfgVariableType CondetCfg { get; }`: Value of variable $CONDET_CFG
- `CondetGrpVariableType[] CondetGrp { get; }`: Value of variable $CONDET_GRP
- `CondetIoVariableType CondetIo { get; }`: Value of variable $CONDET_IO
- `CondetTrgpVariableType[] CondetTrgp { get; }`: Value of variable $CONDET_TRGP
- `CondetTrigVariableType CondetTrig { get; }`: Value of variable $CONDET_TRIG
- `CpMcrgrpVariableType[] CpMcrgrp { get; }`: Value of variable $CP_MCRGRP
- `CpMorgrpVariableType[] CpMorgrp { get; }`: Value of variable $CP_MORGRP
- `CpParamgpVariableType[] CpParamgrp { get; }`: Value of variable $CP_PARAMGRP
- `CpT1GrpVariableType[] CpT1Grp { get; }`: Value of variable $CP_T1_GRP
- `CpT1ModeVariableType CpT1Mode { get; }`: Value of variable $CP_T1_MODE
- `CpcfgVariableType Cpcfg { get; }`: Value of variable $CPCFG
- `CpdbgVariableType Cpdbg { get; }`: Value of variable $CPDBG
- `int CrAutoDo { get; }`: Value of variable $CR_AUTO_DO
- `bool CrIndtEnb { get; }`: Value of variable $CR_INDT_ENB
- `int CrT1Do { get; }`: Value of variable $CR_T1_DO
- `int CrT2Do { get; }`: Value of variable $CR_T2_DO
- `string CrtDefprog { get; }`: Value of variable $CRT_DEFPROG
- `bool CrtInuser { get; }`: Value of variable $CRT_INUSER
- `byte[] CrtKeyTbl { get; }`: Value of variable $CRT_KEY_TBL
- `bool CrtLckuser { get; }`: Value of variable $CRT_LCKUSER
- `bool CrtUsestat { get; }`: Value of variable $CRT_USESTAT
- `bool Cstop { get; }`: Value of variable $CSTOP
- `string CtScreen { get; }`: Value of variable $CT_SCREEN
- `int CtrlDelete { get; }`: Value of variable $CTRL_DELETE
- `bool CustManual { get; }`: Value of variable $CUST_MANUAL
- `CustommenuVariableType[] Custommenu { get; }`: Value of variable $CUSTOMMENU
- `bool DbAwayAlm { get; }`: Value of variable $DB_AWAY_ALM
- `double DbAwaytrig { get; }`: Value of variable $DB_AWAYTRIG
- `int DbCondtyp { get; }`: Value of variable $DB_CONDTYP
- `DbDbgVariableType[] DbDbg { get; }`: Value of variable $DB_DBG
- `double DbMindist { get; }`: Value of variable $DB_MINDIST
- `int DbMontime { get; }`: Value of variable $DB_MONTIME
- `int DbMontyp { get; }`: Value of variable $DB_MONTYP
- `bool DbMotnend { get; }`: Value of variable $DB_MOTNEND
- `DbRecordVariableType[] DbRecord { get; }`: Value of variable $DB_RECORD
- `double DbTolerenc { get; }`: Value of variable $DB_TOLERENC
- `int Dbcondtrig { get; }`: Value of variable $DBCONDTRIG
- `DbgErrlogVariableType DbgErrlog { get; }`: Value of variable $DBG_ERRLOG
- `int Dbnumlim { get; }`: Value of variable $DBNUMLIM
- `DbpxworkVariableType[] Dbpxwork { get; }`: Value of variable $DBPXWORK
- `DbtbCtrlVariableType DbtbCtrl { get; }`: Value of variable $DBTB_CTRL
- `DcsCfgVariableType DcsCfg { get; }`: Value of variable $DCS_CFG
- `DcsCrcOutVariableType DcsCrcOut { get; }`: Value of variable $DCS_CRC_OUT
- `DcsNocodeVariableType DcsNocode { get; }`: Value of variable $DCS_NOCODE
- `DcsSgnVariableType DcsSgn { get; }`: Value of variable $DCS_SGN
- `string DcsVersion { get; }`: Value of variable $DCS_VERSION
- `DcssCnstcyVariableType[] DcssCnstcy { get; }`: Value of variable $DCSS_CNSTCY
- `DcssDeviceVariableType[] DcssDevice { get; }`: Value of variable $DCSS_DEVICE
- `DcssHndgdVariableType DcssHndgd { get; }`: Value of variable $DCSS_HNDGD
- `DcssLsVariableType[] DcssLs { get; }`: Value of variable $DCSS_LS
- `DcssParamVariableType DcssParam { get; }`: Value of variable $DCSS_PARAM
- `DcssSlaveVariableType DcssSlave { get; }`: Value of variable $DCSS_SLAVE
- `int DefAcclim { get; }`: Value of variable $DEF_ACCLIM
- `int DefWrstjnt { get; }`: Value of variable $DEF_WRSTJNT
- `DeflogicVariableType[] Deflogic { get; }`: Value of variable $DEFLOGIC
- `bool DefprogEnb { get; }`: Value of variable $DEFPROG_ENB
- `int Defpulse { get; }`: Value of variable $DEFPULSE
- `DemoInitVariableType DemoInit { get; }`: Value of variable $DEMO_INIT
- `int DevIndex { get; }`: Value of variable $DEV_INDEX
- `string DevPath { get; }`: Value of variable $DEV_PATH
- `string[] DhcpClntid { get; }`: Value of variable $DHCP_CLNTID
- `DiagGrpVariableType[] DiagGrp { get; }`: Value of variable $DIAG_GRP
- `DictCfgVariableType DictConfig { get; }`: Value of variable $DICT_CONFIG
- `int DistbfTts { get; }`: Value of variable $DISTBF_TTS
- `int DistbfVer { get; }`: Value of variable $DISTBF_VER
- `bool Dmaurst { get; }`: Value of variable $DMAURST
- `DmswCfgVariableType DmswCfg { get; }`: Value of variable $DMSW_CFG
- `DocviewerVariableType Docviewer { get; }`: Value of variable $DOCVIEWER
- `DrcCfgVariableType DrcCfg { get; }`: Value of variable $DRC_CFG
- `DsblFaultVariableType DsblFault { get; }`: Value of variable $DSBL_FAULT
- `int DsblGpmsk { get; }`: Value of variable $DSBL_GPMSK
- `DtrecVariableType Dtdiag { get; }`: Value of variable $DTDIAG
- `DtrecVariableType Dtrecp { get; }`: Value of variable $DTRECP
- `int DumpOption { get; }`: Value of variable $DUMP_OPTION
- `int DutrCfg { get; }`: Value of variable $DUTR_CFG
- `int DutrCpmes { get; }`: Value of variable $DUTR_CPMES
- `double DutyTemp { get; }`: Value of variable $DUTY_TEMP
- `int DutyUnit { get; }`: Value of variable $DUTY_UNIT
- `DynBrkVariableType DynBrk { get; }`: Value of variable $DYN_BRK
- `int EStopDo { get; }`: Value of variable $E_STOP_DO
- `EdtRecentVariableType[] EditRecent { get; }`: Value of variable $EDIT_RECENT
- `int EditorOptn { get; }`: Value of variable $EDITOR_OPTN
- `int EmgdiStat { get; }`: Value of variable $EMGDI_STAT
- `EncInfoVariableType[] EncInfo { get; }`: Value of variable $ENC_INFO
- `EnetmodeVariableType[] Enetmode { get; }`: Value of variable $ENETMODE
- `EoatcfgVariableType Eoatcfg { get; }`: Value of variable $EOATCFG
- `EoatdataVariableType[] Eoatdata { get; }`: Value of variable $EOATDATA
- `bool ErAutoEnb { get; }`: Value of variable $ER_AUTO_ENB
- `ErNoalmVariableType[] ErNoAlm { get; }`: Value of variable $ER_NO_ALM
- `ErNoautoVariableType ErNoauto { get; }`: Value of variable $ER_NOAUTO
- `bool ErNofltr { get; }`: Value of variable $ER_NOFLTR
- `int ErNohis { get; }`: Value of variable $ER_NOHIS
- `bool[] ErSevNoau { get; }`: Value of variable $ER_SEV_NOAU
- `ErpostLogVariableType ErpostLog { get; }`: Value of variable $ERPOST_LOG
- `string ErrorProg { get; }`: Value of variable $ERROR_PROG
- `int[] ErrorTable { get; }`: Value of variable $ERROR_TABLE
- `int ErrsevNum { get; }`: Value of variable $ERRSEV_NUM
- `string EtcpVer { get; }`: Value of variable $ETCP_VER
- `bool ExtBwdSel { get; }`: Value of variable $EXT_BWD_SEL
- `ExtSetVariableType ExtDiBwd { get; }`: Value of variable $EXT_DI_BWD
- `ExtSetVariableType ExtDiStep { get; }`: Value of variable $EXT_DI_STEP
- `int ExtlogReq { get; }`: Value of variable $EXTLOG_REQ
- `int ExtlogSiz { get; }`: Value of variable $EXTLOG_SIZ
- `int Extstksiz { get; }`: Value of variable $EXTSTKSIZ
- `double Exttol { get; }`: Value of variable $EXTTOL
- `int FactoryTun { get; }`: Value of variable $FACTORY_TUN
- `FdrGrpVariableType[] FdrGrp { get; }`: Value of variable $FDR_GRP
- `string[] FeatAdd { get; }`: Value of variable $FEAT_ADD
- `FeatureVariableType FeatDemo { get; }`: Value of variable $FEAT_DEMO
- `int FeatDemoin { get; }`: Value of variable $FEAT_DEMOIN
- `int FeatIndex { get; }`: Value of variable $FEAT_INDEX
- `FeatureVariableType Feature { get; }`: Value of variable $FEATURE
- `FileBackVariableType[] FileAp2bck { get; }`: Value of variable $FILE_AP2BCK
- `FileBackVariableType[] FileAppbck { get; }`: Value of variable $FILE_APPBCK
- `FileBackVariableType[] FileDgbck { get; }`: Value of variable $FILE_DGBCK
- `bool FileFrsprt { get; }`: Value of variable $FILE_FRSPRT
- `FileBackVariableType[] FileVisbck { get; }`: Value of variable $FILE_VISBCK
- `FilecompVariableType Filecomp { get; }`: Value of variable $FILECOMP
- `FileSetup2VariableType Filesetup2 { get; }`: Value of variable $FILESETUP2
- `FluiCfgVariableType FluiConfig { get; }`: Value of variable $FLUI_CONFIG
- `FluiDataVariableType FluiData { get; }`: Value of variable $FLUI_DATA
- `FluiResVariableType[] FluiResult { get; }`: Value of variable $FLUI_RESULT
- `FmrCfgVariableType FmrCfg { get; }`: Value of variable $FMR_CFG
- `string Fno { get; }`: Value of variable $FNO
- `int FrmChktyp { get; }`: Value of variable $FRM_CHKTYP
- `int FromchkMin { get; }`: Value of variable $FROMCHK_MIN
- `FssbCfgVariableType FssbCfg { get; }`: Value of variable $FSSB_CFG
- `bool FtpDefOw { get; }`: Value of variable $FTP_DEF_OW
- `bool FtpDircomp { get; }`: Value of variable $FTP_DIRCOMP
- `bool GenovEnb { get; }`: Value of variable $GENOV_ENB
- `GravcGrpVariableType[] GravcGrp { get; }`: Value of variable $GRAVC_GRP
- `GrsmtGrpVariableType[] GrsmtGrp { get; }`: Value of variable $GRSMT_GRP
- `ErrMaskVariableType HostErr { get; }`: Value of variable $HOST_ERR
- `int HostPdusiz { get; }`: Value of variable $HOST_PDUSIZ
- `HostCfgVariableType[] HostcCfg { get; }`: Value of variable $HOSTC_CFG
- `HostentVariableType[] Hostent { get; }`: Value of variable $HOSTENT
- `string Hostname { get; }`: Value of variable $HOSTNAME
- `HostCfgVariableType[] HostsCfg { get; }`: Value of variable $HOSTS_CFG
- `bool HscdQupd { get; }`: Value of variable $HSCD_QUPD
- `int HscdUpdtyp { get; }`: Value of variable $HSCD_UPDTYP
- `HscdMngVariableType[] Hscdmngrp { get; }`: Value of variable $HSCDMNGRP
- `HttpAuthVariableType[] HttpAuth { get; }`: Value of variable $HTTP_AUTH
- `HttpVariableType HttpCtrl { get; }`: Value of variable $HTTP_CTRL
- `HwrConfigVariableType HwrConfig { get; }`: Value of variable $HWR_CONFIG
- `double IdlCpuPct { get; }`: Value of variable $IDL_CPU_PCT
- `double IdlMinPct { get; }`: Value of variable $IDL_MIN_PCT
- `int IgnrIoerr { get; }`: Value of variable $IGNR_IOERR
- `int InptSimDo { get; }`: Value of variable $INPT_SIM_DO
- `int InstalScrn { get; }`: Value of variable $INSTAL_SCRN
- `int IntpPrty { get; }`: Value of variable $INTP_PRTY
- `int Intpmodntol { get; }`: Value of variable $INTPMODNTOL
- `int InvistpEnb { get; }`: Value of variable $INVISTP_ENB
- `bool IoAutoCfg { get; }`: Value of variable $IO_AUTO_CFG
- `bool IoAutoUop { get; }`: Value of variable $IO_AUTO_UOP
- `int IoCmtOpt { get; }`: Value of variable $IO_CMT_OPT
- `bool IoCycle { get; }`: Value of variable $IO_CYCLE
- `IoDefAsgVariableType[] IoDefAsg { get; }`: Value of variable $IO_DEF_ASG
- `int IoDefNum { get; }`: Value of variable $IO_DEF_NUM
- `bool IoIpche { get; }`: Value of variable $IO_IPCHE
- `int IoRtryCnt { get; }`: Value of variable $IO_RTRY_CNT
- `int IoScrnUpd { get; }`: Value of variable $IO_SCRN_UPD
- `IoUopCfgVariableType IoUopCfg { get; }`: Value of variable $IO_UOP_CFG
- `IolnkVariableType[] Iolnk { get; }`: Value of variable $IOLNK
- `bool Iomaster { get; }`: Value of variable $IOMASTER
- `IoslaveVariableType Ioslave { get; }`: Value of variable $IOSLAVE
- `bool Iosramcache { get; }`: Value of variable $IOSRAMCACHE
- `ItemAccVariableType[] IrcaAcc { get; }`: Value of variable $IRCA_ACC
- `ItemBuffElVariableType[] IrcaBuf001 { get; }`: Value of variable $IRCA_BUF001
- `ItemBuffElVariableType[] IrcaBuf002 { get; }`: Value of variable $IRCA_BUF002
- `ItemBuffElVariableType[] IrcaBuf003 { get; }`: Value of variable $IRCA_BUF003
- `IrcaCnfVariableType[] IrcaCfg { get; }`: Value of variable $IRCA_CFG
- `HistDayVariableType[] IrcaHis001 { get; }`: Value of variable $IRCA_HIS001
- `HistDayVariableType[] IrcaHis002 { get; }`: Value of variable $IRCA_HIS002
- `HistDayVariableType[] IrcaHis003 { get; }`: Value of variable $IRCA_HIS003
- `ItemNameVariableType[] IrcaICfg { get; }`: Value of variable $IRCA_I_CFG
- `IrprogCfgVariableType IrprogCfg { get; }`: Value of variable $IRPROG_CFG
- `int[] IsdtIsolc { get; }`: Value of variable $ISDT_ISOLC
- `bool J23DspEnb { get; }`: Value of variable $J23_DSP_ENB
- `JincVariableType Jinc { get; }`: Value of variable $JINC
- `int JobprocEnb { get; }`: Value of variable $JOBPROC_ENB
- `int JogInAuto { get; }`: Value of variable $JOG_IN_AUTO
- `int JposrecEnb { get; }`: Value of variable $JPOSREC_ENB
- `int KanjiMask { get; }`: Value of variable $KANJI_MASK
- `KarelCfgVariableType KarelCfg { get; }`: Value of variable $KAREL_CFG
- `int KarelEnb { get; }`: Value of variable $KAREL_ENB
- `KarelmonVariableType Karelmon { get; }`: Value of variable $KARELMON
- `bool KclLinNum { get; }`: Value of variable $KCL_LIN_NUM
- `int Keylogging { get; }`: Value of variable $KEYLOGGING
- `string Language { get; }`: Value of variable $LANGUAGE
- `LgcfgVariableType Lgcfg { get; }`: Value of variable $LGCFG
- `LnDispVariableType LnDisp { get; }`: Value of variable $LN_DISP
- `double Loctol { get; }`: Value of variable $LOCTOL
- `LogBuffVariableType[] LogBuff { get; }`: Value of variable $LOG_BUFF
- `LogDcsVariableType LogDcs { get; }`: Value of variable $LOG_DCS
- `LogDioVariableType[] LogDio { get; }`: Value of variable $LOG_DIO
- `int[] LogErItm { get; }`: Value of variable $LOG_ER_ITM
- `int LogErSev { get; }`: Value of variable $LOG_ER_SEV
- `int[] LogErTyp { get; }`: Value of variable $LOG_ER_TYP
- `bool LogRecRst { get; }`: Value of variable $LOG_REC_RST
- `LogScrnFlVariableType[] LogScrnFl { get; }`: Value of variable $LOG_SCRN_FL
- `int[] LogTpkey { get; }`: Value of variable $LOG_TPKEY
- `LogbookVariableType Logbook { get; }`: Value of variable $LOGBOOK
- `bool LongnamEnb { get; }`: Value of variable $LONGNAM_ENB
- `string LuLoadprog { get; }`: Value of variable $LU_LOADPROG
- `int LupsDigit { get; }`: Value of variable $LUPS_DIGIT
- `int MaxDigPrt { get; }`: Value of variable $MAX_DIG_PRT
- `int Maxualrmnum { get; }`: Value of variable $MAXUALRMNUM
- `McspVariableType Mcsp { get; }`: Value of variable $MCSP
- `McspGrpVariableType[] McspGrp { get; }`: Value of variable $MCSP_GRP
- `int MdLdxdisab { get; }`: Value of variable $MD_LDXDISAB
- `string[] MemoApname { get; }`: Value of variable $MEMO_APNAME
- `MfrqCfgVariableType MfrqCfg { get; }`: Value of variable $MFRQ_CFG
- `MfrqGrpVariableType[] MfrqGrp { get; }`: Value of variable $MFRQ_GRP
- `MiscMstrVariableType MiscMstr { get; }`: Value of variable $MISC_MSTR
- `MiscScdVariableType[] MiscScd { get; }`: Value of variable $MISC_SCD
- `MkcfgVariableType Mkcfg { get; }`: Value of variable $MKCFG
- `MltarmCfgVariableType MltarmCfg { get; }`: Value of variable $MLTARM_CFG
- `int Mmetpu { get; }`: Value of variable $MMETPU
- `int MndspAdcol { get; }`: Value of variable $MNDSP_ADCOL
- `int MndspCmnt { get; }`: Value of variable $MNDSP_CMNT
- `int MndspFncmn { get; }`: Value of variable $MNDSP_FNCMN
- `int MndspFstli { get; }`: Value of variable $MNDSP_FSTLI
- `MndspMstVariableType MndspMst { get; }`: Value of variable $MNDSP_MST
- `int MndspPoscf { get; }`: Value of variable $MNDSP_POSCF
- `int MndspPrpmt { get; }`: Value of variable $MNDSP_PRPMT
- `MndsppstlVariableType[] MndspPstol { get; }`: Value of variable $MNDSP_PSTOL
- `bool MnsingChk { get; }`: Value of variable $MNSING_CHK
- `ModaqCfgVariableType ModaqCfg { get; }`: Value of variable $MODAQ_CFG
- `string ModaqDev { get; }`: Value of variable $MODAQ_DEV
- `int ModaqHsize { get; }`: Value of variable $MODAQ_HSIZE
- `string ModaqTask { get; }`: Value of variable $MODAQ_TASK
- `FxTriggerVariableType[] ModaqTrig { get; }`: Value of variable $MODAQ_TRIG
- `int ModaqType { get; }`: Value of variable $MODAQ_TYPE
- `ModemInfVariableType[] ModemInf { get; }`: Value of variable $MODEM_INF
- `string[] MonitorMsg { get; }`: Value of variable $MONITOR_MSG
- `MorGrpSvVariableType[] MorGrpSv { get; }`: Value of variable $MOR_GRP_SV
- `MotionDbgVariableType MotionDbg { get; }`: Value of variable $MOTION_DBG
- `string MplName { get; }`: Value of variable $MPL_NAME
- `MrHistVariableType[] MrHist { get; }`: Value of variable $MR_HIST
- `MskCeGrpVariableType[] MskCeGrp { get; }`: Value of variable $MSK_CE_GRP
- `int[] Mskcfmap { get; }`: Value of variable $MSKCFMAP
- `int Mskconrel { get; }`: Value of variable $MSKCONREL
- `int Mskexcfenb { get; }`: Value of variable $MSKEXCFENB
- `int Mskexcffnc { get; }`: Value of variable $MSKEXCFFNC
- `int Mskjogovlim { get; }`: Value of variable $MSKJOGOVLIM
- `int Mskkey { get; }`: Value of variable $MSKKEY
- `int MskkeyPanl { get; }`: Value of variable $MSKKEY_PANL
- `int Mskrunovlim { get; }`: Value of variable $MSKRUNOVLIM
- `int Msksfspdtyp { get; }`: Value of variable $MSKSFSPDTYP
- `int Msksign { get; }`: Value of variable $MSKSIGN
- `int Mskt1motlim { get; }`: Value of variable $MSKT1MOTLIM
- `int MsqzEdit { get; }`: Value of variable $MSQZ_EDIT
- `bool MtArcEnb { get; }`: Value of variable $MT_ARC_ENB
- `int MtMnMode { get; }`: Value of variable $MT_MN_MODE
- `bool MtSplEnb { get; }`: Value of variable $MT_SPL_ENB
- `MtcomCfgVariableType[] MtcomCfg { get; }`: Value of variable $MTCOM_CFG
- `bool MuapCplenb { get; }`: Value of variable $MUAP_CPLENB
- `int NoWaitLn { get; }`: Value of variable $NO_WAIT_LN
- `string[] Nocheck { get; }`: Value of variable $NOCHECK
- `int[] NumRspace { get; }`: Value of variable $NUM_RSPACE
- `int OdrdspEnb { get; }`: Value of variable $ODRDSP_ENB
- `bool OffsetCart { get; }`: Value of variable $OFFSET_CART
- `bool OffsetDis { get; }`: Value of variable $OFFSET_DIS
- `int OfsAtMark { get; }`: Value of variable $OFS_AT_MARK
- `int OpenFiles { get; }`: Value of variable $OPEN_FILES
- `int OptionIo { get; }`: Value of variable $OPTION_IO
- `string OptmPrg { get; }`: Value of variable $OPTM_PRG
- `OpworkVariableType Opwork { get; }`: Value of variable $OPWORK
- `byte[] OrgDsbl { get; }`: Value of variable $ORG_DSBL
- `double Orienttol { get; }`: Value of variable $ORIENTTOL
- `int OutSimDo { get; }`: Value of variable $OUT_SIM_DO
- `bool OvrdPexe { get; }`: Value of variable $OVRD_PEXE
- `int OvrdRate { get; }`: Value of variable $OVRD_RATE
- `OvrdSetupVariableType OvrdSetup { get; }`: Value of variable $OVRD_SETUP
- `OvrdslctVariableType Ovrdslct { get; }`: Value of variable $OVRDSLCT
- `bool PalPosChk { get; }`: Value of variable $PAL_POS_CHK
- `PlcfgVariableType Palcfg { get; }`: Value of variable $PALCFG
- `string[] ParamMenu { get; }`: Value of variable $PARAM_MENU
- `string PauseProg { get; }`: Value of variable $PAUSE_PROG
- `int PcTimeout { get; }`: Value of variable $PC_TIMEOUT
- `int Pccrt { get; }`: Value of variable $PCCRT
- `string PccrtHost { get; }`: Value of variable $PCCRT_HOST
- `int Pctp { get; }`: Value of variable $PCTP
- `string PctpHost { get; }`: Value of variable $PCTP_HOST
- `PgCfgVariableType PgCfg { get; }`: Value of variable $PG_CFG
- `PgDefspdVariableType PgDefspd { get; }`: Value of variable $PG_DEFSPD
- `int Pgdebug { get; }`: Value of variable $PGDEBUG
- `int PginpFlmsk { get; }`: Value of variable $PGINP_FLMSK
- `int PginpFltr { get; }`: Value of variable $PGINP_FLTR
- `int[] PginpPgatr { get; }`: Value of variable $PGINP_PGATR
- `int PginpPgchk { get; }`: Value of variable $PGINP_PGCHK
- `string[] PginpType { get; }`: Value of variable $PGINP_TYPE
- `string[] PginpWord { get; }`: Value of variable $PGINP_WORD
- `int Pglog { get; }`: Value of variable $PGLOG
- `TraceupVariableType PgtraceUp { get; }`: Value of variable $PGTRACE_UP
- `TracectlVariableType[] Pgtracectl { get; }`: Value of variable $PGTRACECTL
- `TracedtVariableType[,] Pgtracedt { get; }`: Value of variable $PGTRACEDT
- `int Pgtracelen { get; }`: Value of variable $PGTRACELEN
- `PingVariableType PingCtrl { get; }`: Value of variable $PING_CTRL
- `PipeCfgVariableType PipeConfig { get; }`: Value of variable $PIPE_CONFIG
- `bool PlMod { get; }`: Value of variable $PL_MOD
- `bool PlModSt { get; }`: Value of variable $PL_MOD_ST
- `PlResGVariableType[] PlResG1 { get; }`: Value of variable $PL_RES_G1
- `PlResGVariableType[] PlResG2 { get; }`: Value of variable $PL_RES_G2
- `PlResGVariableType[] PlResG3 { get; }`: Value of variable $PL_RES_G3
- `PlResGVariableType[] PlResG4 { get; }`: Value of variable $PL_RES_G4
- `PlResGVariableType[] PlResG5 { get; }`: Value of variable $PL_RES_G5
- `PlResGVariableType[] PlResG6 { get; }`: Value of variable $PL_RES_G6
- `PlResGVariableType[] PlResG7 { get; }`: Value of variable $PL_RES_G7
- `PlResGVariableType[] PlResG8 { get; }`: Value of variable $PL_RES_G8
- `int PlThrInrt { get; }`: Value of variable $PL_THR_INRT
- `int PlThrMass { get; }`: Value of variable $PL_THR_MASS
- `int PlThrMmnt { get; }`: Value of variable $PL_THR_MMNT
- `PlidCfgVariableType PlidCfg { get; }`: Value of variable $PLID_CFG
- `PlidCllbVariableType[] PlidCllb { get; }`: Value of variable $PLID_CLLB
- `bool PlidKnowM { get; }`: Value of variable $PLID_KNOW_M
- `PlimGrpVariableType[] PlimGrp { get; }`: Value of variable $PLIM_GRP
- `PlmrGrpVariableType[] PlmrGrp { get; }`: Value of variable $PLMR_GRP
- `bool Ploadbanfwd { get; }`: Value of variable $PLOADBANFWD
- `int PlsCmpLim { get; }`: Value of variable $PLS_CMP_LIM
- `int PlsErChk { get; }`: Value of variable $PLS_ER_CHK
- `int PlsErLim { get; }`: Value of variable $PLS_ER_LIM
- `bool PlsErRst { get; }`: Value of variable $PLS_ER_RST
- `PlstGrpVariableType[] PlstGrp6 { get; }`: Value of variable $PLST_GRP6
- `PlstGrpVariableType[] PlstGrp7 { get; }`: Value of variable $PLST_GRP7
- `PlstGrpVariableType[] PlstGrp8 { get; }`: Value of variable $PLST_GRP8
- `bool[] PlstOvld { get; }`: Value of variable $PLST_OVLD
- `PmonQueVariableType PmonQueue { get; }`: Value of variable $PMON_QUEUE
- `int PnsCurLin { get; }`: Value of variable $PNS_CUR_LIN
- `bool PnsEndCur { get; }`: Value of variable $PNS_END_CUR
- `bool PnsEndExe { get; }`: Value of variable $PNS_END_EXE
- `int PnsNumber { get; }`: Value of variable $PNS_NUMBER
- `int PnsOption { get; }`: Value of variable $PNS_OPTION
- `string PnsProgram { get; }`: Value of variable $PNS_PROGRAM
- `int PnsTaskId { get; }`: Value of variable $PNS_TASK_ID
- `PocfgVariableType Pocfg { get; }`: Value of variable $POCFG
- `PosEditVariableType PosEdit { get; }`: Value of variable $POS_EDIT
- `bool PrCartrep { get; }`: Value of variable $PR_CARTREP
- `PrgadjVariableType Prgadj { get; }`: Value of variable $PRGADJ
- `PrgnsCfgVariableType PrgnsCfg { get; }`: Value of variable $PRGNS_CFG
- `PrgnsGrpVariableType[] PrgnsGrp { get; }`: Value of variable $PRGNS_GRP
- `PrgnsPrefVariableType PrgnsPref { get; }`: Value of variable $PRGNS_PREF
- `int Priority { get; }`: Value of variable $PRIORITY
- `PfCfgVariableType ProCfg { get; }`: Value of variable $PRO_CFG
- `PfEnhanceVariableType ProEnhance { get; }`: Value of variable $PRO_ENHANCE
- `PfPrefVariableType ProPref { get; }`: Value of variable $PRO_PREF
- `string ProductId { get; }`: Value of variable $PRODUCT_ID
- `int ProggrpTgl { get; }`: Value of variable $PROGGRP_TGL
- `bool ProhibitDo { get; }`: Value of variable $PROHIBIT_DO
- `ProtoentVariableType[] Protoent { get; }`: Value of variable $PROTOENT
- `ProxyCfgVariableType ProxyCfg { get; }`: Value of variable $PROXY_CFG
- `int PrportNum { get; }`: Value of variable $PRPORT_NUM
- `int Pskstat { get; }`: Value of variable $PSKSTAT
- `PslgsetVariableType Pslgset { get; }`: Value of variable $PSLGSET
- `PslgtempVariableType Pslgtemp { get; }`: Value of variable $PSLGTEMP
- `string Pslgversion { get; }`: Value of variable $PSLGVERSION
- `PssaveVariableType Pssave { get; }`: Value of variable $PSSAVE
- `bool PurgeEnbl { get; }`: Value of variable $PURGE_ENBL
- `int PwfIo { get; }`: Value of variable $PWF_IO
- `string PwrNormal { get; }`: Value of variable $PWR_NORMAL
- `string PwrSemi { get; }`: Value of variable $PWR_SEMI
- `PwrupDlyVariableType PwrupDelay { get; }`: Value of variable $PWRUP_DELAY
- `QskipGrpVariableType[] QskipGrp { get; }`: Value of variable $QSKIP_GRP
- `int Rbtif { get; }`: Value of variable $RBTIF
- `int Rcvtmout { get; }`: Value of variable $RCVTMOUT
- `RdcrGrpVariableType[] RdcrGrp { get; }`: Value of variable $RDCR_GRP
- `int[] RdioType { get; }`: Value of variable $RDIO_TYPE
- `bool ReExecEnb { get; }`: Value of variable $RE_EXEC_ENB
- `RedprotCfgVariableType RedprotCfg { get; }`: Value of variable $REDPROT_CFG
- `RedprotGrpVariableType[] RedprotGrp { get; }`: Value of variable $REDPROT_GRP
- `Refpos11VariableType[] Refpos1 { get; }`: Value of variable $REFPOS1
- `Refpos21VariableType[] Refpos2 { get; }`: Value of variable $REFPOS2
- `Refpos31VariableType[] Refpos3 { get; }`: Value of variable $REFPOS3
- `Refpos41VariableType[] Refpos4 { get; }`: Value of variable $REFPOS4
- `Refpos51VariableType[] Refpos5 { get; }`: Value of variable $REFPOS5
- `Refpos61VariableType[] Refpos6 { get; }`: Value of variable $REFPOS6
- `Refpos71VariableType[] Refpos7 { get; }`: Value of variable $REFPOS7
- `Refpos81VariableType[] Refpos8 { get; }`: Value of variable $REFPOS8
- `RefpsmskVariableType[] Refposmask { get; }`: Value of variable $REFPOSMASK
- `int[] Refposmaxno { get; }`: Value of variable $REFPOSMAXNO
- `int Remote { get; }`: Value of variable $REMOTE
- `RemoteCfgVariableType RemoteCfg { get; }`: Value of variable $REMOTE_CFG
- `int ReplRange { get; }`: Value of variable $REPL_RANGE
- `RepowerVariableType Repower { get; }`: Value of variable $REPOWER
- `string ResmDryprg { get; }`: Value of variable $RESM_DRYPRG
- `RestartVariableType Restart { get; }`: Value of variable $RESTART
- `string ResumeProg { get; }`: Value of variable $RESUME_PROG
- `bool RgspdPrexe { get; }`: Value of variable $RGSPD_PREXE
- `bool RgtdbPrexe { get; }`: Value of variable $RGTDB_PREXE
- `bool RgtrmPrexe { get; }`: Value of variable $RGTRM_PREXE
- `bool[] RiAirpurge { get; }`: Value of variable $RI_AIRPURGE
- `int RmtMaster { get; }`: Value of variable $RMT_MASTER
- `int[] RobCateg { get; }`: Value of variable $ROB_CATEG
- `string[] RobOrdNum { get; }`: Value of variable $ROB_ORD_NUM
- `int[] RobotIsolc { get; }`: Value of variable $ROBOT_ISOLC
- `string RobotName { get; }`: Value of variable $ROBOT_NAME
- `int RpcTimeout { get; }`: Value of variable $RPC_TIMEOUT
- `Rs232CfgVariableType[] Rs232Cfg { get; }`: Value of variable $RS232_CFG
- `int Rs232Nport { get; }`: Value of variable $RS232_NPORT
- `RschVariableType RschLog { get; }`: Value of variable $RSCH_LOG
- `int Rsmavailnum { get; }`: Value of variable $RSMAVAILNUM
- `RspaceVariableType[] Rspace1 { get; }`: Value of variable $RSPACE1
- `RspaceVariableType[] Rspace2 { get; }`: Value of variable $RSPACE2
- `RspaceVariableType[] Rspace3 { get; }`: Value of variable $RSPACE3
- `RspaceVariableType[] Rspace4 { get; }`: Value of variable $RSPACE4
- `RspaceVariableType[] Rspace5 { get; }`: Value of variable $RSPACE5
- `RspaceVariableType[] Rspace6 { get; }`: Value of variable $RSPACE6
- `RspaceVariableType[] Rspace7 { get; }`: Value of variable $RSPACE7
- `RspaceVariableType[] Rspace8 { get; }`: Value of variable $RSPACE8
- `int RspaceMode { get; }`: Value of variable $RSPACE_MODE
- `RspacesrVariableType RspaceS { get; }`: Value of variable $RSPACE_S
- `RspacegVariableType Rspaceg { get; }`: Value of variable $RSPACEG
- `int RspcworkAd { get; }`: Value of variable $RSPCWORK_AD
- `byte[] Rsr { get; }`: Value of variable $RSR
- `int RsrIntval { get; }`: Value of variable $RSR_INTVAL
- `int RsrOption { get; }`: Value of variable $RSR_OPTION
- `int SafDoPuls { get; }`: Value of variable $SAF_DO_PULS
- `int ScanTime { get; }`: Value of variable $SCAN_TIME
- `int SelDefault { get; }`: Value of variable $SEL_DEFAULT
- `int SelHotstrt { get; }`: Value of variable $SEL_HOTSTRT
- `bool Semipowerfl { get; }`: Value of variable $SEMIPOWERFL
- `int Semipwfdo { get; }`: Value of variable $SEMIPWFDO
- `string ServDev { get; }`: Value of variable $SERV_DEV
- `int ServMail { get; }`: Value of variable $SERV_MAIL
- `int ServOutput { get; }`: Value of variable $SERV_OUTPUT
- `int ServSave { get; }`: Value of variable $SERV_SAVE
- `int ServType { get; }`: Value of variable $SERV_TYPE
- `ServentVariableType[] Servent { get; }`: Value of variable $SERVENT
- `string[] ServiceKl { get; }`: Value of variable $SERVICE_KL
- `string[] ServicePrg { get; }`: Value of variable $SERVICE_PRG
- `SfznCfgVariableType SfznCfg { get; }`: Value of variable $SFZN_CFG
- `SfznGrpVariableType[] SfznGrp { get; }`: Value of variable $SFZN_GRP
- `ShellCfgVariableType ShellCfg { get; }`: Value of variable $SHELL_CFG
- `ShellChkVariableType[] ShellChk { get; }`: Value of variable $SHELL_CHK
- `ShellCommVariableType ShellComm { get; }`: Value of variable $SHELL_COMM
- `int ShftovEnb { get; }`: Value of variable $SHFTOV_ENB
- `int ShowRegUi { get; }`: Value of variable $SHOW_REG_UI
- `bool SiUnitEnb { get; }`: Value of variable $SI_UNIT_ENB
- `SimiofwdlmVariableType Simiofwdlm { get; }`: Value of variable $SIMIOFWDLM
- `int SlcRetry { get; }`: Value of variable $SLC_RETRY
- `string[] SmonAlias { get; }`: Value of variable $SMON_ALIAS
- `string SmonDefprog { get; }`: Value of variable $SMON_DEFPROG
- `string[] SmonRecall { get; }`: Value of variable $SMON_RECALL
- `SnpxAsgVariableType[] SnpxAsg { get; }`: Value of variable $SNPX_ASG
- `SnpxParamVariableType SnpxParam { get; }`: Value of variable $SNPX_PARAM
- `int SoftKbCfg { get; }`: Value of variable $SOFT_KB_CFG
- `int[] SopinSim { get; }`: Value of variable $SOPIN_SIM
- `bool SrvnordyDo { get; }`: Value of variable $SRVNORDY_DO
- `int[] SrvqstpDsb { get; }`: Value of variable $SRVQSTP_DSB
- `SsrVariableType Ssr { get; }`: Value of variable $SSR
- `bool StopOnErr { get; }`: Value of variable $STOP_ON_ERR
- `string StopPtn { get; }`: Value of variable $STOP_PTN
- `bool StringPrm { get; }`: Value of variable $STRING_PRM
- `SvInfoVariableType[] SvInfo { get; }`: Value of variable $SV_INFO
- `SvdtGrpVariableType[] SvdtGrp { get; }`: Value of variable $SVDT_GRP
- `int SvprgCount { get; }`: Value of variable $SVPRG_COUNT
- `bool SvprgEnb { get; }`: Value of variable $SVPRG_ENB
- `int SvprmEnb { get; }`: Value of variable $SVPRM_ENB
- `SvprmUpdVariableType[] SvprmUpd { get; }`: Value of variable $SVPRM_UPD
- `int Sysdebug { get; }`: Value of variable $SYSDEBUG
- `int SysdspPass { get; }`: Value of variable $SYSDSP_PASS
- `SyslogVariableType Syslog { get; }`: Value of variable $SYSLOG
- `SyslogVariableType SyslogMpc { get; }`: Value of variable $SYSLOG_MPC
- `SyslogSavVariableType SyslogSav { get; }`: Value of variable $SYSLOG_SAV
- `SystemTimerVariableType[] SystemTime { get; }`: Value of variable $SYSTEM_TIME
- `short[] Systskmem { get; }`: Value of variable $SYSTSKMEM
- `int T1svgunspd { get; }`: Value of variable $T1SVGUNSPD
- `T2modeLimVariableType T2modeLim { get; }`: Value of variable $T2MODE_LIM
- `T2spdlimVariableType T2spdlim { get; }`: Value of variable $T2SPDLIM
- `bool TaDispEnb { get; }`: Value of variable $TA_DISP_ENB
- `Tbc2GrpVariableType[] Tbc2Grp { get; }`: Value of variable $TBC2_GRP
- `TbcsgGrpVariableType[] TbcsgGrp { get; }`: Value of variable $TBCSG_GRP
- `Tbj2GrpVariableType[] Tbj2Grp { get; }`: Value of variable $TBJ2_GRP
- `TbjopGrpVariableType[] TbjopGrp { get; }`: Value of variable $TBJOP_GRP
- `ThrCfgVariableType ThrCfg { get; }`: Value of variable $THR_CFG
- `TpThrTableVariableType[] Threstable { get; }`: Value of variable $THRESTABLE
- `TpThrTableVariableType[] Thrrditable { get; }`: Value of variable $THRRDITABLE
- `TpThrTableVariableType[] Thrrdotable { get; }`: Value of variable $THRRDOTABLE
- `TpThrTableVariableType[] Thrsditable { get; }`: Value of variable $THRSDITABLE
- `TpThrTableVariableType[] Thrsitable { get; }`: Value of variable $THRSITABLE
- `short[] Thrtablenum { get; }`: Value of variable $THRTABLENUM
- `int TimebfTts { get; }`: Value of variable $TIMEBF_TTS
- `int TimebfVer { get; }`: Value of variable $TIMEBF_VER
- `TimerVariableType[] Timer { get; }`: Value of variable $TIMER
- `int TimerNum { get; }`: Value of variable $TIMER_NUM
- `int TmiChan { get; }`: Value of variable $TMI_CHAN
- `int TmiDbglvl { get; }`: Value of variable $TMI_DBGLVL
- `string[] TmiEtherad { get; }`: Value of variable $TMI_ETHERAD
- `string TmiRouter { get; }`: Value of variable $TMI_ROUTER
- `string[] TmiSnmask { get; }`: Value of variable $TMI_SNMASK
- `bool ToolofsDis { get; }`: Value of variable $TOOLOFS_DIS
- `string TpDefprog { get; }`: Value of variable $TP_DEFPROG
- `int TpDisplay { get; }`: Value of variable $TP_DISPLAY
- `int[] TpInstMsk { get; }`: Value of variable $TP_INST_MSK
- `bool TpInuser { get; }`: Value of variable $TP_INUSER
- `bool TpLckuser { get; }`: Value of variable $TP_LCKUSER
- `bool TpQuickmen { get; }`: Value of variable $TP_QUICKMEN
- `string TpScreen { get; }`: Value of variable $TP_SCREEN
- `string TpUserscrn { get; }`: Value of variable $TP_USERSCRN
- `bool TpUsestat { get; }`: Value of variable $TP_USESTAT
- `int TpeDetail { get; }`: Value of variable $TPE_DETAIL
- `TpglConfVariableType TpglConfig { get; }`: Value of variable $TPGL_CONFIG
- `TpglOutVariableType TpglOutput { get; }`: Value of variable $TPGL_OUTPUT
- `int TpoffLim { get; }`: Value of variable $TPOFF_LIM
- `bool TponSvoff { get; }`: Value of variable $TPON_SVOFF
- `TppMonVariableType TppMon { get; }`: Value of variable $TPP_MON
- `TpstrtchkVariableType Tpstrtchk { get; }`: Value of variable $TPSTRTCHK
- `bool Tpvtcompat { get; }`: Value of variable $TPVTCOMPAT
- `TpvwvarVariableType Tpvwvar { get; }`: Value of variable $TPVWVAR
- `TraceCfgVariableType TraceCfg { get; }`: Value of variable $TRACE_CFG
- `TraceChnlVariableType[] TraceChnl { get; }`: Value of variable $TRACE_CHNL
- `TraceItemVariableType[] TraceItem { get; }`: Value of variable $TRACE_ITEM
- `TscfgVariableType Tscfg { get; }`: Value of variable $TSCFG
- `TsscbVariableType[] Tsscb { get; }`: Value of variable $TSSCB
- `TutorialVariableType Tutorial { get; }`: Value of variable $TUTORIAL
- `TvConfigVariableType TvConfig { get; }`: Value of variable $TV_CONFIG
- `TvOutputVariableType TvOutput { get; }`: Value of variable $TV_OUTPUT
- `TxscreenVariableType[] TxScreen { get; }`: Value of variable $TX_SCREEN
- `string[] UalrmMsg { get; }`: Value of variable $UALRM_MSG
- `byte[] UalrmSev { get; }`: Value of variable $UALRM_SEV
- `UecfgVariableType Uecfg { get; }`: Value of variable $UECFG
- `UegrpVariableType[] Uegrp { get; }`: Value of variable $UEGRP
- `BblNtWndVariableType UiBblNote { get; }`: Value of variable $UI_BBL_NOTE
- `string[] UiDefprog { get; }`: Value of variable $UI_DEFPROG
- `UiFkeydatVariableType[] UiFkeydata { get; }`: Value of variable $UI_FKEYDATA
- `bool[] UiInuser { get; }`: Value of variable $UI_INUSER
- `UiMenhisVariableType[] UiMenhist { get; }`: Value of variable $UI_MENHIST
- `UiPanedatVariableType[] UiPanedata { get; }`: Value of variable $UI_PANEDATA
- `int[] UiPostype { get; }`: Value of variable $UI_POSTYPE
- `bool[] UiQuickmen { get; }`: Value of variable $UI_QUICKMEN
- `UiUsrviewVariableType[] UiRestore { get; }`: Value of variable $UI_RESTORE
- `string[] UiScreen { get; }`: Value of variable $UI_SCREEN
- `int[] UiState { get; }`: Value of variable $UI_STATE
- `string[] UiUserscrn { get; }`: Value of variable $UI_USERSCRN
- `UndoCfgVariableType UndoCfg { get; }`: Value of variable $UNDO_CFG
- `bool UopCrm5 { get; }`: Value of variable $UOP_CRM5
- `string Update { get; }`: Value of variable $UPDATE
- `UserInfoVariableType[] UserInfo { get; }`: Value of variable $USER_INFO
- `UserOffstVariableType UserOffset { get; }`: Value of variable $USER_OFFSET
- `UserWorkVariableType UserWork { get; }`: Value of variable $USER_WORK
- `bool Useuframe { get; }`: Value of variable $USEUFRAME
- `UsrEvCfgVariableType[] UsrEvCfg { get; }`: Value of variable $USR_EV_CFG
- `UsrEvWrkVariableType[] UsrEvWrk { get; }`: Value of variable $USR_EV_WRK
- `int UsrEvnt { get; }`: Value of variable $USR_EVNT
- `bool UsrtolAbrt { get; }`: Value of variable $USRTOL_ABRT
- `bool UsrtolEnb { get; }`: Value of variable $USRTOL_ENB
- `UsrtolGrpVariableType[] UsrtolGrp { get; }`: Value of variable $USRTOL_GRP
- `int UsrtolMsk { get; }`: Value of variable $USRTOL_MSK
- `string UsrtolName { get; }`: Value of variable $USRTOL_NAME
- `VarsConfigVariableType VarsConfig { get; }`: Value of variable $VARS_CONFIG
- `VcmrGrpVariableType[] VcmrGrp { get; }`: Value of variable $VCMR_GRP
- `ViaWorkVariableType ViaWork { get; }`: Value of variable $VIA_WORK
- `VisGeCfgVariableType VisGeCfg { get; }`: Value of variable $VIS_GE_CFG
- `VisLogregVariableType VisLogreg { get; }`: Value of variable $VIS_LOGREG
- `VisionCfgVariableType VisionCfg { get; }`: Value of variable $VISION_CFG
- `VisionGrpVariableType[] VisionGrp { get; }`: Value of variable $VISION_GRP
- `int Visiontmout { get; }`: Value of variable $VISIONTMOUT
- `VlexeCfgVariableType VlexeCfg { get; }`: Value of variable $VLEXE_CFG
- `VrtdFiltVariableType[] VrtdFilter { get; }`: Value of variable $VRTD_FILTER
- `VsftCfgVariableType VshiftCfg { get; }`: Value of variable $VSHIFT_CFG
- `CustommenuVariableType[] Vshiftmenu { get; }`: Value of variable $VSHIFTMENU
- `VsmoCfgVariableType VsmoCfg { get; }`: Value of variable $VSMO_CFG
- `VzdtCfgVariableType VzdtCfg { get; }`: Value of variable $VZDT_CFG
- `bool WaitActive { get; }`: Value of variable $WAIT_ACTIVE
- `WaitDataVariableType WaitData { get; }`: Value of variable $WAIT_DATA
- `bool WaitRdisp { get; }`: Value of variable $WAIT_RDISP
- `bool Waitrelease { get; }`: Value of variable $WAITRELEASE
- `int Waittmout { get; }`: Value of variable $WAITTMOUT
- `XvrcfgVariableType Xvrcfg { get; }`: Value of variable $XVRCFG
- `ZabcGrpVariableType[] ZabcGrp { get; }`: Value of variable $ZABC_GRP
- `ZdtActvsptVariableType ZdtActvspt { get; }`: Value of variable $ZDT_ACTVSPT
- `ZdtDcschgVariableType ZdtDcschg { get; }`: Value of variable $ZDT_DCSCHG
- `ZipCfgVariableType ZipCfg { get; }`: Value of variable $ZIP_CFG
- `ZmposGrpVariableType[] ZmpGrp { get; }`: Value of variable $ZMP_GRP
- `ZmpcfGrpVariableType[] ZmpcfG { get; }`: Value of variable $ZMPCF_G
- `ZpCylinderVariableType[] ZpCylinder { get; }`: Value of variable $ZP_CYLINDER
- `ZpGrpVariableType[] ZpGrp { get; }`: Value of variable $ZP_GRP
- `ZpSphereVariableType[] ZpSphere { get; }`: Value of variable $ZP_SPHERE
- `ZpCfgVariableType Zpcfg { get; }`: Value of variable $ZPCFG
- `int Zzz { get; }`: Value of variable $ZZZ
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## SysuifFile

`class SysuifFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file sysuif.va

- `SysuifFile()`
- `UiConfigVariableType UiConfig { get; }`: Value of variable $UI_CONFIG
- `UiCustomVariableType[] UiCustom { get; }`: Value of variable $UI_CUSTOM
- `UiTopmenuVariableType[] UiTopmenu { get; }`: Value of variable $UI_TOPMENU
- `UiUsrviewVariableType[] UiUserview { get; }`: Value of variable $UI_USERVIEW
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## TpsnapFile

`class TpsnapFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file tpsnap.va

- `TpsnapFile()`
- `int Day { get; }`: Value of variable DAY
- `string DayStr { get; }`: Value of variable DAY_STR
- `string DevPathStr { get; }`: Value of variable DEV_PATH_STR
- `string DevStr { get; }`: Value of variable DEV_STR
- `int Entry { get; }`: Value of variable ENTRY
- `int Hour { get; }`: Value of variable HOUR
- `string HourStr { get; }`: Value of variable HOUR_STR
- `string LangStr { get; }`: Value of variable LANG_STR
- `int Min { get; }`: Value of variable MIN
- `string MinStr { get; }`: Value of variable MIN_STR
- `int Month { get; }`: Value of variable MONTH
- `string MonthStr { get; }`: Value of variable MONTH_STR
- `string PngStr { get; }`: Value of variable PNG_STR
- `int Sec { get; }`: Value of variable SEC
- `string SecStr { get; }`: Value of variable SEC_STR
- `int Status { get; }`: Value of variable STATUS
- `int TInt { get; }`: Value of variable T_INT
- `string TStr { get; }`: Value of variable T_STR
- `int TimeInt { get; }`: Value of variable TIME_INT
- `string TimeStr { get; }`: Value of variable TIME_STR
- `string TimeStr2 { get; }`: Value of variable TIME_STR2
- `int Year { get; }`: Value of variable YEAR
- `string YearStr { get; }`: Value of variable YEAR_STR
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`

## ValueKind

`enum ValueKind`

Describes the kind of a variable value

- Array: An array of values
- File: A file-level container
- Structure: A structured type with named fields
- Value: A single scalar value

## VariableFile

`abstract class VariableFile`

Abstract base class for typed variable file readers

- `string FileName { get; protected set; }`: Name of the variable file

## VariableFileList

`class VariableFileList : Collection<GenericVariableFile>, IList<GenericVariableFile>, ICollection<GenericVariableFile>, IEnumerable<GenericVariableFile>, IList, ICollection, IEnumerable, IGenericVariableType`

Collection of variable files that aggregates all variables from the controller

- `VariableFileList()`
- `string Name { get; set; }`: Name of this variable file list
- `IGenericVariableType Parent { get; set; }`: Parent container

## VariableReader<T>

`class VariableReader<T> : FileReader<T>, IFileReader<T>, IFileReader where T : GenericVariableFile, new()`

Typed variable file reader for specific variable file types

- `T ReadFile(Stream fileStream, Languages language, string fileName)`: Read and decode the file stream
- Inherited from [FileReader](UnderAutomation.Fanuc.Common.Files.md#filereader): `FileName`

## VariableReader

`class VariableReader : FileReader<GenericVariableFile>, IFileReader<GenericVariableFile>, IFileReader`

Reader for Fanuc variable files (*.va)

- `static readonly VariableReader<AavmmainFile> AavmmainFile`
- `static readonly VariableReader<BicsetupFile> BicsetupFile`
- `static readonly VariableReader<CbparamFile> CbparamFile`
- `static readonly VariableReader<CellioFile> CellioFile`
- `static readonly VariableReader<ComsetFile> ComsetFile`
- `static readonly VariableReader<DiocfgsvFile> DiocfgsvFile`
- `static readonly VariableReader<GemdataFile> GemdataFile`
- `static readonly VariableReader<HtcolrecFile> HtcolrecFile`
- `static readonly VariableReader<HttpkclFile> HttpkclFile`
- `static readonly VariableReader<IrcCounterFile> IrcCounterFile`
- `static readonly VariableReader<IrcMsgFile> IrcMsgFile`
- `static readonly VariableReader<IrcStatusFile> IrcStatusFile`
- `static readonly VariableReader<IrcStlabelFile> IrcStlabelFile`
- `static readonly VariableReader<KlactionFile> KlactionFile`
- `static readonly VariableReader<MixlogicFile> MixlogicFile`
- `static readonly VariableReader<MtparamFile> MtparamFile`
- `static readonly VariableReader<NumregFile> NumregFile`
- `static readonly VariableReader<PalregFile> PalregFile`
- `static GenericVariable[] ParseVariableFile(Stream stream, Languages language)`: Parses all variables from a stream
- `static readonly VariableReader<PosregFile> PosregFile`
- `GenericVariableFile ReadFile(Stream fileStream, Languages language, string fileName)`: Read and decode the file stream
- `static GenericVariableFile ReadVariableFile(Stream fileStream, string fileName, Languages language)`: Reads and parses a variable file from a stream
- `static GenericVariableFile ReadVariableFile(string fileName, Languages language)`: Reads and parses a variable file from a file path
- `static readonly VariableReader<StrregFile> StrregFile`
- `static readonly VariableReader<SwiupdtFile> SwiupdtFile`
- `static readonly VariableReader<SycldintFile> SycldintFile`
- `static readonly VariableReader<SymotnFile> SymotnFile`
- `static readonly VariableReader<SynosaveFile> SynosaveFile`
- `static readonly VariableReader<SysframeFile> SysframeFile`
- `static readonly VariableReader<SysfsacFile> SysfsacFile`
- `static readonly VariableReader<SyshostFile> SyshostFile`
- `static readonly VariableReader<SysmacroFile> SysmacroFile`
- `static readonly VariableReader<SysmastFile> SysmastFile`
- `static readonly VariableReader<SyspassFile> SyspassFile`
- `static readonly VariableReader<SysservoFile> SysservoFile`
- `static readonly VariableReader<SystemFile> SystemFile`
- `static readonly VariableReader<SysuifFile> SysuifFile`
- `static readonly VariableReader<TpsnapFile> TpsnapFile`
- `static readonly VariableReader<VcmrinitFile> VcmrinitFile`
- Inherited from [FileReader](UnderAutomation.Fanuc.Common.Files.md#filereader): `FileName`

## VcmrinitFile

`class VcmrinitFile : GenericVariableFile, IGenericVariableType, IFanucContent`

Describes the Fanuc variable file vcmrinit.va

- `VcmrinitFile()`
- `string ArgStr { get; }`: Value of variable ARG_STR
- `int DataType { get; }`: Value of variable DATA_TYPE
- `int DmyInt { get; }`: Value of variable DMY_INT
- `double DmyReal { get; }`: Value of variable DMY_REAL
- `int DmyStat { get; }`: Value of variable DMY_STAT
- `string DmyStr { get; }`: Value of variable DMY_STR
- `VcalMvVariableType MoveVar { get; }`: Value of variable MOVE_VAR
- `string ParamVal { get; }`: Value of variable PARAM_VAL
- `bool PrmSetDone { get; }`: Value of variable PRM_SET_DONE
- `int SelectGrp { get; }`: Value of variable SELECT_GRP
- `VcalVdVariableType VdetectVar { get; }`: Value of variable VDETECT_VAR
- `VcalVfVariableType VfbVar { get; }`: Value of variable VFB_VAR
- `VtcpsetVariableType VtcpVar { get; }`: Value of variable VTCP_VAR
- Inherited from [GenericVariableFile](UnderAutomation.Fanuc.Common.Files.Variables.md#genericvariablefile): `GetField`, `GenerateVa`, `GeneratedVa`, `Variables`, `Name`, `Parent`
