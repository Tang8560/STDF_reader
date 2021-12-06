# -*- coding: utf-8 -*-
#==========================================================================
# Parse STDF data
#--------------------------------------------------------------------------
# Redistribution and use of this file in source and binary forms, with
# or without modification, are permitted.
#==========================================================================

#==========================================================================
# IMPORTS
#==========================================================================
import os
import sys
import struct
import xlsxwriter

#==========================================================================
# PARAMETER
#==========================================================================

# filepath = "main_Lot_1_Wafer_1_Oct_13_09h33m41s_STDF.stdf"

STDF_TYPE ={
    # Information about the STDF file
    "010":"FAR",                       # File Attributes Record
    "020":"ATR",                       # Audit Trail Record
    # Data collected on a per lot basis
    "110":"MIR",                       # Master Information Record
    "120":"MRR",                       # Master Results Record
    "130":"PCR",                       # Part Count Record
    "140":"HBR",                       # Hardware Bin Record
    "150":"SBR",                       # Software Bin Record
    "160":"PMR",                       # Pin Map Record
    "162":"PGR",                       # Pin Group Record
    "163":"PLR",                       # Pin List Record
    "170":"RDR",                       # Retest Data Record
    "180":"SDR",                       # Retest Data Record
    # Data collected per wafer
    "210":"WIR",                       # Wafer Information Record
    "220":"WRR",                       # Wafer Results Record
    "230":"WCR",                       # Wafer Configuration Record
    # Data collected on a per part basis
    "510":"PIR",                       # Part Information Record
    "520":"PRR",                       # Part Results Record
    # Data collected per test in the test program
    "1030":"TSR",                      # Test Synopsis Record
    # Data collected per test execution
    "1510":"PTR",                      # Parametric Test Record
    "1515":"MPR",                      # Multiple-Result Parametric Record
    "1520":"FTR",                      # Functional Test Record
    # Data collected per program segment
    "2010":"BPS",                      # Begin Program Section Record
    "2020":"EPS",                      # End Program Section Record
    # Generic Data
    "5010":"GDR",                      # Generic Data Record
    "5030":"DTR",                      # Datalog Text Record
}

class StdfParse(object):

    def __init__(self, filepath):
        # Build xlsx
        self.xlsx_filename = os.path.basename(filepath) + ".xlsx"
        self.wb = xlsxwriter.Workbook(self.xlsx_filename)
        bold = self.wb.add_format({
            'bold': 1,
            'fg_color': 'red',
            'font_color': 'white',
            'align': 'center',
            'valign': 'vcenter',
        })
        # Open stdf file
        self.binfile = open(filepath, "rb")
        # Make function array to get run times
        func_arr = []
        while True:
            REC_LEN, RET_TYP, RET_SUB = self.RecordHeader()
            STDF_func = STDF_TYPE.get(str(RET_TYP)+str(RET_SUB))
            func_arr.append(STDF_func)
            print(STDF_func,func_arr.count(STDF_func))
            if STDF_func:
                # Create worksheet
                globals()[STDF_func+"_WS"] = self.wb.get_worksheet_by_name(STDF_func)
                if globals()[STDF_func+"_WS"] is None:
                    globals()[STDF_func+"_WS"] = self.wb.add_worksheet(STDF_func)
                try:
                    func = getattr(StdfParse, format(STDF_func))
                    RET = func(self, REC_LEN)
                    print(RET)

                    # Set column size
                    if len(RET) > 26:
                        mod = len(RET)//26
                        rem = len(RET)%26
                        max_column = chr(ord('@')+mod)+chr(ord('@')+rem)
                    else:
                        max_column = chr(ord('@')+len(RET))
                    all_column = "A:%s" %max_column
                    globals()[STDF_func+"_WS"].set_column(all_column, 15)

                    self.row = 1
                    for i, v in enumerate(RET):
                        # Set label value
                        globals()[STDF_func+"_WS"].write(0, i, v, bold)
                        # Set value
                        try:
                            int_value = int(RET[v])
                            globals()[STDF_func+"_WS"].write_number(func_arr.count(STDF_func), i, int_value)
                        except ValueError:
                            str_value = RET[v].decode('utf-8')
                            globals()[STDF_func+"_WS"].write_string(func_arr.count(STDF_func), i, str_value)

                except Exception as e:
                    self.traceback(e)
            else:
                break
        self.binfile.close()
        self.wb.close()

    def RecordHeader(self):
        """
        RecordHeader
            -------------------------------------------------
            REC_LEN U*2 Bytes of data following header
            REC_TYP U*1 Record type (0)
            REC_SUB U*1 Record sub-type (20)
        """
        try:
            data = self.binfile.read(4)
            REC_LEN, RET_TYP, RET_SUB = struct.unpack("H2B", data)
            STDF_func = STDF_TYPE.get(str(RET_TYP)+str(RET_SUB))
            print("[INFO] %s(%d%d)  [REC_LEN]:%d" % (STDF_func, RET_TYP, RET_SUB, REC_LEN))
            return REC_LEN, RET_TYP, RET_SUB

        except struct.error as e:
            print("[INFO] error     [ERROR]:",e)
            REC_LEN = RET_TYP = RET_SUB = 0
            return REC_LEN, RET_TYP, RET_SUB

    def FAR(self,REC_LEN):
        """
        File Attributes Record (FAR)
            -------------------------------------------------
            REC_LEN U*2 Bytes of data following header
            REC_TYP U*1 Record type (0)
            REC_SUB U*1 Record sub-type (10)
            -------------------------------------------------
            CPU_TYPE U*1 CPU type that wrote this file
            STDF_VER U*1 STDF version number
        """
        FAR = {}
        data = self.binfile.read(REC_LEN)
        unpackType = "=2B"
        CPU_TYPE, STDF_VER = struct.unpack(unpackType, data)
        FAR["CPU_TYPE"] = CPU_TYPE
        FAR["STDF_VER"] = STDF_VER
        return FAR

    def ATR(self,REC_LEN):
        """
        Audit Trail Record (ATR)
            -------------------------------------------------
            REC_LEN U*2 Bytes of data following header
            REC_TYP U*1 Record type (0)
            REC_SUB U*1 Record sub-type (20)
            --------------------------------------------------
            MOD_TIM U*4 Date and time of STDF file modification
            CMD_LINE C*n Command line of program
        """
        ATR = {}
        data = self.binfile.read(REC_LEN)
        stringSize = REC_LEN - struct.calcsize("L")
        unpackType = "=L%ds" % stringSize
        MOD_TIM, CMD_LINE = struct.unpack(unpackType, data)
        ATR["MOD_TIM"] = MOD_TIM
        ATR["CMD_LINE"] = CMD_LINE
        return ATR

    def MIR(self,REC_LEN):
        """
        Master Information Record (MIR)
            -------------------------------------------------
            REC_LEN U*2 Bytes of data following header
            REC_TYP U*1 Record type (0)
            REC_SUB U*1 Record sub-type (20)
            --------------------------------------------------
            SETUP_T U*4 Date and time of job setup
            START_T U*4 Date and time first part tested
            STAT_NUM U*1 Tester station number
            MODE_COD C*1 Test mode code (e.g. prod, dev) space
            RTST_COD C*1 Lot retest code space
            PROT_COD C*1 Data protection code space
            BURN_TIM U*2 Burn-in time (in minutes) 65,535
            CMOD_COD C*1 Command mode code space
            LOT_ID C*n Lot ID (customer specified)
            PART_TYP C*n Part Type (or product ID)
            NODE_NAM C*n Name of node that generated data
            TSTR_TYP C*n Tester type
            JOB_NAM C*n Job name (test program name)
            JOB_REV C*n Job (test program) revision number length byte = 0
            SBLOT_ID C*n Sublot ID length byte = 0
            OPER_NAM C*n Operator name or ID (at setup time) length byte = 0
            EXEC_TYP C*n Tester executive software type length byte = 0
            EXEC_VER C*n Tester exec software version number length byte = 0
            TEST_COD C*n Test phase or step code length byte = 0
            TST_TEMP C*n Test temperature length byte = 0
            USER_TXT C*n Generic user text length byte = 0
            AUX_FILE C*n Name of auxiliary data file length byte = 0
            PKG_TYP C*n Package type length byte = 0
            FAMLY_ID C*n Product family ID length byte = 0
            DATE_COD C*n Date code length byte = 0
            FACIL_ID C*n Test facility ID length byte = 0
            FLOOR_ID C*n Test floor ID length byte = 0
            PROC_ID C*n Fabrication process ID length byte = 0
            OPER_FRQ C*n Operation frequency or step length byte = 0
            SPEC_NAM C*n Test specification name length byte = 0
            SPEC_VER C*n Test specification version number length byte = 0
            FLOW_ID C*n Test flow ID length byte = 0
            SETUP_ID C*n Test setup ID length byte = 0
            DSGN_REV C*n Device design revision length byte = 0
            ENG_ID C*n Engineering lot ID length byte = 0
            ROM_COD C*n ROM code ID length byte = 0
            SERL_NUM C*n Tester serial number length byte = 0
            SUPR_NAM C*n Supervisor name or ID length byte = 0
        """
        MIR = {}
        unpackType = "=2LB3cHc"
        data = self.binfile.read(struct.calcsize(unpackType))
        SETUP_T, START_T, STAT_NUM, MODE_COD, RTST_COD, PROT_COD, BURN_TIM, CMOD_COD = struct.unpack(unpackType, data)
        MIR["SETUP_T"]  = SETUP_T
        MIR["START_T"]  = START_T
        MIR["STAT_NUM"] = STAT_NUM
        MIR["MODE_COD"] = MODE_COD
        MIR["RTST_COD"] = RTST_COD
        MIR["PROT_COD"] = PROT_COD
        MIR["BURN_TIM"] = BURN_TIM
        MIR["CMOD_COD"] = CMOD_COD
        data = self.binfile.read(REC_LEN - struct.calcsize(unpackType))
        MIR_RET = data
        MIR_data = MIR_RET.decode('utf-8',"ignore")
        mapping  = dict.fromkeys(range(33), ",")
        MIR_arr  = MIR_data.translate(mapping)
        MIR_arr  = MIR_arr.split(",")
        MIR["LOT_ID"]   = MIR_arr[1]
        MIR["PART_TYP"] = MIR_arr[2]
        MIR["NODE_NAM"] = MIR_arr[3]
        MIR["TSTR_TYP"] = MIR_arr[4]
        MIR["JOB_NAM"]  = MIR_arr[5]
        MIR["JOB_REV"]  = MIR_arr[6]
        MIR["SBLOT_ID"] = MIR_arr[7]
        MIR["OPER_NAM"] = MIR_arr[8]
        MIR["EXEC_TYP"] = MIR_arr[9]
        MIR["EXEC_VER"] = MIR_arr[10]
        MIR["TEST_COD"] = MIR_arr[11]
        MIR["TST_TEMP"] = MIR_arr[12]
        MIR["USER_TXT"] = MIR_arr[13]
        MIR["AUX_FILE"] = MIR_arr[14]
        MIR["PKG_TYP"]  = MIR_arr[15]
        MIR["FAMLY_ID"] = MIR_arr[16]
        MIR["DATE_COD"] = MIR_arr[17]
        MIR["FACIL_ID"] = MIR_arr[18]
        MIR["FLOOR_ID"] = MIR_arr[19]
        MIR["PROC_ID"]  = MIR_arr[20]
        MIR["OPER_FRQ"] = MIR_arr[21]
        MIR["SPEC_NAM"] = MIR_arr[22]
        MIR["SPEC_VER"] = MIR_arr[23]
        MIR["FLOW_ID"]  = MIR_arr[24]
        MIR["SETUP_ID"] = MIR_arr[25]
        MIR["DSGN_REV"] = MIR_arr[26]
        MIR["ENG_ID"]   = MIR_arr[27]
        MIR["ROM_COD"]  = MIR_arr[28]
        MIR["SERL_NUM"] = MIR_arr[29]
        MIR["SUPR_NAM"] = MIR_arr[30]
        return MIR

    def SDR(self,REC_LEN):
        """
        Site Description Record (SDR)
            -------------------------------------------------
            REC_LEN U*2 Bytes of data following header
            REC_TYP U*1 Record type (1)
            REC_SUB U*1 Record sub-type (80)
            -------------------------------------------------
            HEAD_NUM U*1 Test head number
            SITE_GRP U*1 Site group number
            SITE_CNT U*1 Number (k) of test sites in site group
            SITE_NUM kxU*1 Array of test site numbers
            HAND_TYP C*n Handler or prober type length byte = 0
            HAND_ID C*n Handler or prober ID length byte = 0
            CARD_TYP C*n Probe card type length byte = 0
            CARD_ID C*n Probe card ID length byte = 0
            LOAD_TYP C*n Load board type length byte = 0
            LOAD_ID C*n Load board ID length byte = 0
            DIB_TYP C*n DIB board type length byte = 0
            DIB_ID C*n DIB board ID length byte = 0
            CABL_TYP C*n Interface cable type length byte = 0
            CABL_ID C*n Interface cable ID length byte = 0
            CONT_TYP C*n Handler contactor type length byte = 0
            CONT_ID C*n Handler contactor ID length byte = 0
            LASR_TYP C*n Laser type length byte = 0
            LASR_ID C*n Laser ID length byte = 0
            EXTR_TYP C*n Extra equipment type field length byte = 0
            EXTR_ID C*n Extra equipment ID length byte = 0
        """
        SDR = {}
        data = self.binfile.read(3)
        HEAD_NUM, SITE_GRP, SITE_CNT = struct.unpack("3B", data)
        data = self.binfile.read(REC_LEN-3)
        calcsizeString = "%dB" % SITE_CNT
        unpackType = "=%dB%ds" % (SITE_CNT, REC_LEN-3-struct.calcsize(calcsizeString))
        SDR_RET = struct.unpack(unpackType, data)
        print(SDR_RET)
        SDR["HEAD_NUM"] = HEAD_NUM
        SDR["SITE_GRP"] = SITE_GRP
        SDR["SITE_CNT"] = SITE_CNT
        SDR["SITE_NUM"] = SDR_RET[0]
        SDR_data = SDR_RET[1].decode('utf-8',"ignore")
        mapping  = dict.fromkeys(range(33), ",")
        SDR_arr  = SDR_data.translate(mapping)
        SDR_arr  = SDR_arr.split(",")
        SDR["HAND_TYP"] = SDR_arr[1]
        SDR["HAND_ID"]  = SDR_arr[2]
        SDR["CARD_TYP"] = SDR_arr[3]
        SDR["CARD_ID"]  = SDR_arr[4]
        SDR["LOAD_TYP"] = SDR_arr[5]
        SDR["LOAD_ID"]  = SDR_arr[6]
        SDR["DIB_TYP"]  = SDR_arr[7]
        SDR["DIB_ID"]   = SDR_arr[8]
        SDR["CABL_TYP"] = SDR_arr[9]
        SDR["CABL_ID"]  = SDR_arr[10]
        SDR["CONT_TYP"] = SDR_arr[11]
        SDR["CONT_ID"]  = SDR_arr[12]
        SDR["LASR_TYP"] = SDR_arr[13]
        SDR["LASR_ID"]  = SDR_arr[14]
        SDR["EXTR_TYP"] = SDR_arr[15]
        SDR["EXTR_ID"]  = SDR_arr[16]
        return SDR

    def PMR(self,REC_LEN):
        """
        Pin Map Record (PMR)
            -------------------------------------------------
            REC_LEN U*2 Bytes of data following header
            REC_TYP U*1 Record type (1)
            REC_SUB U*1 Record sub-type (60)
            -------------------------------------------------
            PMR_INDX U*2 Unique index associated with pin
            CHAN_TYP U*2 Channel type 0
            CHAN_NAM C*n Channel name length byte = 0
            PHY_NAM C*n Physical name of pin length byte = 0
            LOG_NAM C*n Logical name of pin length byte = 0
            HEAD_NUM U*1 Head number associated with channel 1
            SITE_NUM U*1 Site number associated with channel 1
        """
        PMR = {}
        data = self.binfile.read(REC_LEN)
        unpackType = "=2H%ds2B" % (REC_LEN-struct.calcsize("=2H2B"))
        PMR_INDX, CHAN_TYP, PMR_RET, HEAD_NUM, SITE_NUM= struct.unpack(unpackType, data)
        PMR["PMR_INDX"] = PMR_INDX
        PMR["CHAN_TYP"] = CHAN_TYP
        PMR_data = PMR_RET.decode('utf-8',"ignore")
        mapping  = dict.fromkeys(range(33), ",")
        PMR_arr  = PMR_data.translate(mapping)
        PMR_arr  = PMR_arr.split(",")
        PMR["CHAN_NAM"] = PMR_arr[1]
        PMR["PHY_NAM"]  = PMR_arr[2]
        PMR["LOG_NAM"]  = PMR_arr[3]
        PMR["HEAD_NUM"] = HEAD_NUM
        PMR["SITE_NUM"] = SITE_NUM
        return PMR

    def WCR(self,REC_LEN):
        """
        Wafer Configuration Record (WCR)
            -------------------------------------------------
            REC_LEN U*2 Bytes of data following header
            REC_TYP U*1 Record type (2)
            REC_SUB U*1 Record sub-type (30)
            -------------------------------------------------
            WAFR_SIZ R*4 Diameter of wafer in WF_UNITS 0
            DIE_HT R*4 Height of die in WF_UNITS 0
            DIE_WID R*4 Width of die in WF_UNITS 0
            WF_UNITS U*1 Units for wafer and die dimensions 0
            WF_FLAT C*1 Orientation of wafer flat space
            CENTER_X I*2 X coordinate of center die on wafer -32768
            CENTER_Y I*2 Y coordinate of center die on wafer -32768
            POS_X C*1 Positive X direction of wafer space
            POS_Y C*1 Positive Y direction of wafer space
        """
        WCR = {}
        data = self.binfile.read(REC_LEN)
        unpackType = "=3fBc2hcc"
        WAFR_SIZ, DIE_HT, DIE_WID, WF_UNITS, WF_FLAT, CENTER_X, CENTER_Y, POS_X, POS_Y = struct.unpack(unpackType, data)
        WCR["WAFR_SIZ"]  = WAFR_SIZ
        WCR["DIE_HT"]    = DIE_HT
        WCR["DIE_WID"]   = DIE_WID
        WCR["WF_UNITS"]  = WF_UNITS
        WCR["WF_FLAT"]   = WF_FLAT
        WCR["CENTER_X"]  = CENTER_X
        WCR["CENTER_Y"]  = CENTER_Y
        WCR["POS_X"]     = POS_X
        WCR["POS_Y"]     = POS_Y
        return WCR

    def WIR(self,REC_LEN):
        """
        Wafer Information Record (WIR)
            -------------------------------------------------
            REC_LEN U*2 Bytes of data following header
            REC_TYP U*1 Record type (2)
            REC_SUB U*1 Record sub-type (10)
            -------------------------------------------------
            HEAD_NUM U*1 Test head number
            SITE_GRP U*1 Site group number 255
            START_T U*4 Date and time first part tested
            WAFER_ID C*n Wafer ID length byte = 0
        """
        WIR = {}
        data = self.binfile.read(REC_LEN)
        # print("[INFO] WIR(210)  [initial]:", data)
        ## [Note]: https://stackoverflow.com/questions/48425462/python-struct-calsize-different-from-actual

        unpackType = "=2BL%ds" % (REC_LEN-struct.calcsize("=2BL"))
        HEAD_NUM, SITE_GRP, START_T, WAFER_ID = struct.unpack(unpackType, data)
        WIR["HEAD_NUM"] = HEAD_NUM
        WIR["SITE_GRP"] = SITE_GRP
        WIR["START_T"]  = START_T
        WIR["WAFER_ID"] = WAFER_ID
        return WIR

    def PIR(self,REC_LEN):
        """
        Part Information Record (PIR)
            -------------------------------------------------
            REC_LEN U*2 Bytes of data following header
            REC_TYP U*1 Record type (5)
            REC_SUB U*1 Record sub-type (10)
            -------------------------------------------------
            HEAD_NUM U*1 Test head number
            SITE_NUM U*1 Test site number
        """
        PIR = {}
        data = self.binfile.read(REC_LEN)
        unpackType = "=2B"
        HEAD_NUM, SITE_NUM = struct.unpack(unpackType, data)
        PIR["HEAD_NUM"] = HEAD_NUM
        PIR["SITE_NUM"] = SITE_NUM
        return PIR

    def PRR(self,REC_LEN):
        """
        Part Results Record (PRR)
            -------------------------------------------------
            REC_LEN U*2 Bytes of data following header
            REC_TYP U*1 Record type (5)
            REC_SUB U*1 Record sub-type (20)
            -------------------------------------------------
            HEAD_NUM U*1 Test head number
            SITE_NUM U*1 Test site number
            PART_FLG B*1 Part information flag
            NUM_TEST U*2 Number of tests executed
            HARD_BIN U*2 Hardware bin number
            SOFT_BIN U*2 Software bin number 65535
            X_COORD I*2 (Wafer) X coordinate -32768
            Y_COORD I*2 (Wafer) Y coordinate -32768
            TEST_T U*4 Elapsed test time in milliseconds 0
            PART_ID C*n Part identification length byte = 0
            PART_TXT C*n Part description text length byte = 0
            PART_FIX B*n Part repair information length byte = 0
        """
        PRR = {}
        data = self.binfile.read(REC_LEN)
        # print("[INFO] PRR(520)  [initial]:", data)
        unpackType = "=2Bp3H2hL%ds" % (REC_LEN-struct.calcsize("=2Bp3H2hL"))
        HEAD_NUM, SITE_NUM, PART_FLG, NUM_TEST, HARD_BIN, SOFT_BIN, X_COORD, Y_COORD, TEST_T, PRR_RET = struct.unpack(unpackType, data)
        PRR["HEAD_NUM"] = HEAD_NUM
        PRR["SITE_NUM"] = SITE_NUM
        PRR["PART_FLG"] = PART_FLG
        PRR["NUM_TEST"] = NUM_TEST
        PRR["HARD_BIN"] = HARD_BIN
        PRR["SOFT_BIN"] = SOFT_BIN
        PRR["X_COORD"]  = X_COORD
        PRR["Y_COORD"]  = Y_COORD
        PRR["TEST_T"]   = TEST_T
        PART_data = PRR_RET.decode('utf-8',"ignore")
        mapping   = dict.fromkeys(range(33), ",")
        PRR_arr  = PART_data.translate(mapping)
        PRR_arr  = PRR_arr.split(",")
        PRR["PART_ID"]  = PRR_arr[1]
        PRR["PART_TXT"] = PRR_arr[2]
        PRR["PART_FIX"] = PRR_arr[3]
        return PRR

    def WRR(self,REC_LEN):
        """
        Wafer Results Record (WRR)
            -------------------------------------------------
            REC_LEN U*2 Bytes of data following header
            REC_TYP U*1 Record type (2)
            REC_SUB U*1 Record sub-type (20)
            -------------------------------------------------
            HEAD_NUM U*1 Test head number
            SITE_GRP U*1 Site group number 255
            FINISH_T U*4 Date and time last part tested
            PART_CNT U*4 Number of parts tested
            RTST_CNT U*4 Number of parts retested 4,294,967,295
            ABRT_CNT U*4 Number of aborts during testing 4,294,967,295
            GOOD_CNT U*4 Number of good (passed) parts tested 4,294,967,295
            FUNC_CNT U*4 Number of functional parts tested 4,294,967,295
            WAFER_ID C*n Wafer ID length byte = 0
            FABWF_ID C*n Fab wafer ID length byte = 0
            FRAME_ID C*n Wafer frame ID length byte = 0
            MASK_ID  C*n Wafer mask ID length byte = 0
            USR_DESC C*n Wafer description supplied by user length byte = 0
            EXC_DESC C*n Wafer description supplied by exec length byte = 0
        """
        WRR = {}
        data = self.binfile.read(REC_LEN)
        unpackType = "=2B6L%ds" % (REC_LEN-struct.calcsize("=2B6L"))
        HEAD_NUM, SITE_GRP, FINISH_T, PART_CNT, RTST_CNT, ABRT_CNT, GOOD_CNT, FUNC_CNT, WRR_RET = struct.unpack(unpackType, data)
        WRR["HEAD_NUM"] = HEAD_NUM
        WRR["SITE_GRP"] = SITE_GRP
        WRR["FINISH_T"] = FINISH_T
        WRR["PART_CNT"] = PART_CNT
        WRR["RTST_CNT"] = RTST_CNT
        WRR["ABRT_CNT"] = ABRT_CNT
        WRR["GOOD_CNT"] = GOOD_CNT
        WRR["FUNC_CNT"] = FUNC_CNT
        ID_DESC = WRR_RET.decode('utf-8',"ignore")
        mapping   = dict.fromkeys(range(33), ",")
        WRR_arr  = ID_DESC.translate(mapping)
        WRR_arr  = WRR_arr.split(",")
        WRR["WAFER_ID"] = WRR_arr[1]
        WRR["FABWF_ID"] = WRR_arr[2]
        WRR["FRAME_ID"] = WRR_arr[3]
        WRR["MASK_ID"]  = WRR_arr[4]
        WRR["USR_DESC"] = WRR_arr[5]
        WRR["EXC_DESC"] = WRR_arr[6]
        return WRR

    def HBR(self,REC_LEN):
        """
        Hardware Bin Record (HBR)
            -------------------------------------------------
            REC_LEN U*2 Bytes of data following header
            REC_TYP U*1 Record type (1)
            REC_SUB U*1 Record sub-type (40)
            -------------------------------------------------
            HEAD_NUM U*1 Test head number See note
            SITE_NUM U*1 Test site number
            HBIN_NUM U*2 Hardware bin number
            HBIN_CNT U*4 Number of parts in bin
            HBIN_PF  C*1 Pass/fail indication space
            HBIN_NAM C*n Name of hardware bin length byte = 0
        """
        HBR = {}
        data = self.binfile.read(REC_LEN)
        unpackType = "=2BHLc%ds" % (REC_LEN-struct.calcsize("=2BHLc"))
        HEAD_NUM, SITE_NUM, HBIN_NUM, HBIN_CNT, HBIN_PF, HBIN_NAM = struct.unpack(unpackType, data)
        HBR["HEAD_NUM"] = HEAD_NUM
        HBR["SITE_NUM"] = SITE_NUM
        HBR["HBIN_NUM"] = HBIN_NUM
        HBR["HBIN_CNT"] = HBIN_CNT
        HBR["HBIN_PF"]  = HBIN_PF
        HBR["HBIN_NAM"]  = HBIN_NAM
        return HBR

    def SBR(self,REC_LEN):
        """
        Software Bin Record (SBR)
            -------------------------------------------------
            REC_LEN U*2 Bytes of data following header
            REC_TYP U*1 Record type (1)
            REC_SUB U*1 Record sub-type (50)
            -------------------------------------------------
            HEAD_NUM U*1 Test head number See note
            SITE_NUM U*1 Test site number
            SBIN_NUM U*2 Software bin number
            SBIN_CNT U*4 Number of parts in bin
            SBIN_PF C*1 Pass/fail indication space
            SBIN_NAM C*n Name of software bin length byte = 0
        """
        SBR = {}
        data = self.binfile.read(REC_LEN)
        unpackType = "=2BHLc%ds" % (REC_LEN-struct.calcsize("=2BHLc"))
        HEAD_NUM, SITE_NUM, SBIN_NUM, SBIN_CNT, SBIN_PF, SBIN_NAM = struct.unpack(unpackType, data)
        SBR["HEAD_NUM"] = HEAD_NUM
        SBR["SITE_NUM"] = SITE_NUM
        SBR["SBIN_NUM"] = SBIN_NUM
        SBR["SBIN_CNT"] = SBIN_CNT
        SBR["SBIN_PF"]  = SBIN_PF
        SBR["SBIN_NAM"] = SBIN_NAM
        return SBR

    def PCR(self,REC_LEN):
        """
        Part Count Record (PCR)
            -------------------------------------------------
            REC_LEN U*2 Bytes of data following header
            REC_TYP U*1 Record type (1)
            REC_SUB U*1 Record sub-type (30)
            -------------------------------------------------
            HEAD_NUM U*1 Test head number See note
            SITE_NUM U*1 Test site number
            PART_CNT U*4 Number of parts tested
            RTST_CNT U*4 Number of parts retested 4,294,967,295
            ABRT_CNT U*4 Number of aborts during testing 4,294,967,295
            GOOD_CNT U*4 Number of good (passed) parts tested 4,294,967,295
            FUNC_CNT U*4 Number of functional parts tested 4,294,967,295
        """
        PCR = {}
        data = self.binfile.read(REC_LEN)
        unpackType = "=2B5L"
        HEAD_NUM, SITE_NUM, PART_CNT, RTST_CNT, ABRT_CNT, GOOD_CNT, FUNC_CNT = struct.unpack(unpackType, data)
        PCR["HEAD_NUM"] = HEAD_NUM
        PCR["SITE_NUM"] = SITE_NUM
        PCR["PART_CNT"] = PART_CNT
        PCR["RTST_CNT"] = RTST_CNT
        PCR["ABRT_CNT"] = ABRT_CNT
        PCR["GOOD_CNT"] = GOOD_CNT
        PCR["FUNC_CNT"] = FUNC_CNT
        return PCR

    def MRR(self,REC_LEN):
        """
        Master Results Record (MRR)
            -------------------------------------------------
            REC_LEN U*2 Bytes of data following header
            REC_TYP U*1 Record type (1)
            REC_SUB U*1 Record sub-type (20)
            -------------------------------------------------
            FINISH_T U*4 Date and time last part tested
            DISP_COD C*1 Lot disposition code space
            USR_DESC C*n Lot description supplied by user length byte = 0
            EXC_DESC C*n Lot description supplied by exec length byte = 0
        """
        MRR = {}
        data = self.binfile.read(REC_LEN)
        unpackType = "=Lc%ds" % (REC_LEN-struct.calcsize("=Lc"))
        FINISH_T, DISP_COD, MRR_RET = struct.unpack(unpackType, data)
        MRR["FINISH_T"] = FINISH_T
        MRR["DISP_COD"] = DISP_COD
        MRR["MRR_RET"]  = MRR_RET
        return MRR

    def traceback(self, error):
        """ Error handling """
        traceback = sys.exc_info()[2]
        print (os.path.abspath(__file__) + ': ' ,error,'line '+ str(traceback.tb_lineno))

# StdfParse(filepath)




