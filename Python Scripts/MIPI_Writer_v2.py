# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 16:32:28 2019.

@author: joslaton
"""
# %%

# MIPI SPEC DEPENDENT Constants
PM_TRIG = 28
ID_REGS = [29, 30, 31, 32]
REV_ID = 33
GSID = 34
UDR_RST = 35
ERR_SUM = 36
INT_MAP1 = 37
INT_MAP2 = 38
INT_EN0 = 39
INT_EN1 = 40
INT_CLR0 = 41
INT_CLR1 = 42
BUS_LD = 43
TEST_PATT = 44
EXT_TRIGGER_MASK = 45
EXT_TRIGGER = 46
TEMP_SENSOR = 67
FB_READBACK = [128, 129, 130, 131]
FUSE = 160
BANK = 161
DIENUM = 163
SIREV_ID = 164
MIM_SELECT = 165
MIM_COUNT1 = 166
MIM_COUNT2 = 167
trig_dict = {'TRIGGER0': 0,
             'TRIGGER1': 1,
             'TRIGGER2': 2,
             'EXT_TRIGGER_3': 3,
             'EXT_TRIGGER_4': 4,
             'EXT_TRIGGER_5': 5,
             'EXT_TRIGGER_6': 6,
             'EXT_TRIGGER_7': 7,
             'EXT_TRIGGER_8': 8,
             'EXT_TRIGGER_9': 9,
             'EXT_TRIGGER_10': 10}
# MMC NOTE
# UDR Registers with reserved bits should be populated in this dict.
# For example, if bits 7:4 of register 0x0E are the only reserved bits,
# the following declaration would be correct:
# res_dict = {14:15}
res_dict = {0: 15}

control_reg_lst = [PM_TRIG,
                   GSID,
                   UDR_RST,
                   ERR_SUM,
                   BUS_LD,
                   EXT_TRIGGER_MASK,
                   EXT_TRIGGER,
                   SIREV_ID,
                   TEMP_SENSOR,
                   TEST_PATT,
                   FUSE,
                   BANK,
                   DIENUM,
                   MIM_SELECT,
                   MIM_COUNT1,
                   MIM_COUNT2]

control_reg_lst += ID_REGS
control_reg_lst += FB_READBACK
has_bits_reserved_lst = list(res_dict.keys())
trg_cntr_reg_lst = []
# MMC NOTE
# rw_change_lst is used to exempt registers from testing.
# This is used for register's whose usage will alter the part's behavior.
rw_change_lst = []
exclude_lst = control_reg_lst + trg_cntr_reg_lst + rw_change_lst
exclude_lst += has_bits_reserved_lst


class register:
    """register class represents a register in the DUT."""

    def __init__(self, line):
        """
        Instantiate a member of the register class.

        Parameters
        ----------
        line : String
            line is a line from the PRD.

        Returns
        -------
        None.

        """
        self.ireq = line[0]
        self.address = int(line[1])
        self.address_hex = line[2]
        if 'x' in line[3]:
            self.default = int(line[3], 16)
        else:
            self.default = int(line[3])
        self.trig_sup = line[4]
        self.trigger = line[5]
        self.ext_rw = line[6]
        self.mask_rw = line[7]
        self.r_w = line[8]

    def __repr__(self):
        """
        Override print form.

        Returns
        -------
        rep_str : String
            DESCRIPTION.

        """
        rep_str = 'ireq : ' + self.ireq + '\n'
        rep_str += 'address : ' + str(self.address) + '\n'
        rep_str += 'address_hex : ' + self.address_hex + '\n'
        rep_str += 'default : ' + str(self.default) + '\n'
        rep_str += 'trig_sup : ' + self.trig_sup + '\n'
        rep_str += 'trigger : ' + self.trigger + '\n'
        rep_str += 'ext_rw : ' + self.ext_rw + '\n'
        rep_str += 'mask_rw : ' + self.mask_rw + '\n'
        rep_str += 'r_w : ' + self.r_w + '\n'
        return rep_str


def register_pack_generator(indir, in1, in2):
    """
    Create a pack of registers by passing csv files.

    Parameters
    ----------
    indir : string
        Path to directory holding Machine Readable PRD's.
    in1 : string
        Filename of standard Machine Readable PRD.
    in2 : string
        Filename of extended Machine Readable PRD.

    Returns
    -------
    b : list
        List packed with registers.

    """
    a = []

    with open(indir + in1, 'r') as f:
        f.readline()
        for line in f.readlines():
            a += [register(line.strip('\n').split(','))]
    with open(indir + in2, 'r') as f:
        f.readline()
        for line in f.readlines():
            a += [register(line.strip('\n').split(','))]
    b = [False for _ in range(a[-1].address+1)]
    for el in a:
        b[el.address] = el
    return b


def cmd_str_generator(enabled, typ, usid, regaddr, wrt_msk, reg_wrt_data,
                      exp_rd_data, regwrary=[]):
    """
    Send a Command.

    Parameters
    ----------
    enabled : int
        Toggle bit to determine if Command is sent.
    typ : int
        Controls the type of Command.
        1 => Standard Write Command
        2 => Standard Read Command
        3 => Extended Write Command
        4 => Extended Read Command
        5 => Masked Write Command
    usid : int
        Sets the USID for the Command.
    regaddr : int
        Sets the address for the Command.
    wrt_msk : int
        Sets the write mask for a Masked Write Command.
    reg_wrt_data : int
        Sets the data for a Write Command.
    exp_rd_data : int
        Sets the expected data for a Read Command.
    regwrary : list, optional
        Sets the data for an Extended Write Array Command. The default is [].

    Returns
    -------
    list
        DESCRIPTION.

    """
    cmd_str = str(enabled) + ','
    cmd_str += str(typ) + ','
    cmd_str += str(usid) + ','
    cmd_str += str(regaddr) + ','
    cmd_str += str(wrt_msk) + ','
    cmd_str += str(reg_wrt_data) + ','
    cmd_str += str(exp_rd_data) + '\n'
    if regwrary:
        assert type(regwrary) == list
        assert len(regwrary) < 5
        cmd_str = cmd_str.strip('\n') + ','
        for val in regwrary:
            cmd_str += str(val) + ','
        cmd_str += '\n'
    return [cmd_str]


def read_cmd_generator(reg, usid, erd):
    """
    Send a Standard Read Command .

    Parameters
    ----------
    reg : int
        Set the Address for the command.
    usid : int
        Set the USID for the command.
    erd : int
        Expected read data in decimal.

    Returns
    -------
    list
        list contains a command string.

    """
    return cmd_str_generator(1, 2, usid, reg.address, 0, 0, erd)


def extend_read_cmd_generator(reg, usid, erd):
    """
    Send an Extended Read Command.

    Parameters
    ----------
    reg : int
        Set the Address for the command.
    usid : int
        Set the USID for the command.
    erd : int
        Expected read data in decimal.

    Returns
    -------
    list
        list contains a command string.

    """
    return cmd_str_generator(1, 4, usid, reg.address, 0, 0, erd)


def write_cmd_generator(reg, usid, wrt):
    """
    Send a Standard Write Command.

    Parameters
    ----------
    reg : int
        Set the Address for the command.
    usid : int
        Set the USID for the command.
    wrt : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    return cmd_str_generator(1, 1, usid, reg.address, 0, wrt, 0)


def extend_write_cmd_generator(reg, usid, wrt, ary=[]):
    """
    Send an Extended Write Command.

    Parameters
    ----------
    reg : int
        Set the Address for the command.
    usid : int
        Set the USID for the command.
    wrt : TYPE
        DESCRIPTION.
    ary : TYPE, optional
        DESCRIPTION. The default is [].

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    typ = 3
    if ary:
        typ = '1' + str(len(ary))
    return cmd_str_generator(1, typ, usid, reg.address, 0, wrt, 0,
                             regwrary=ary)


def msk_wrt_cmd_generator(reg, usid, msk, wrt):
    """
    Send a Masked Write Command.

    Parameters
    ----------
    reg : int
        Set the Address for the command.
    usid : int
        Set the USID for the command.
    msk : TYPE
        DESCRIPTION.
    wrt : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    return cmd_str_generator(1, 5, usid, reg.address, msk, wrt, 0)


def check_err_cmd_generator(usid, exp_read_err=False):
    """
    Read the ERROR SUM Register.

    Parameters
    ----------
    usid : int
        Set the USID for the command.
    exp_read_err : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    if exp_read_err:
        return cmd_str_generator(1, 2, usid, ERR_SUM, 0, 0, 4)
    return cmd_str_generator(1, 2, usid, ERR_SUM, 0, 0, -1)


def pwr_rst_cmd_generator(usid, useusid=False):
    """
    Send a Powered Reset Command.

    Parameters
    ----------
    usid : int
        Set the USID for the command.
    useusid : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    if useusid:
        return write_cmd_generator(a[PM_TRIG], usid, 64)
    return write_cmd_generator(a[PM_TRIG], 0, 64)


def udr_rst_cmd_generator(usid):
    """
    Send a UDR Reset Command.

    Parameters
    ----------
    usid : int
        Set the USID for the command.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    return write_cmd_generator(a[UDR_RST], usid, 128)


def trig_all(usid):
    """
    Send a Trigger All command.

    Parameters
    ----------
    usid : int
        Set the USID for the command.

    Returns
    -------
    cmd_lst : TYPE
        DESCRIPTION.

    """
    cmd_lst = write_cmd_generator(a[PM_TRIG], usid, 7)
    cmd_lst += write_cmd_generator(a[EXT_TRIGGER], usid, 255)
    return cmd_lst


def pm_trig_trigger_cmd_generator(usid, trigger):
    """
    Send a PM Trigger command to the specified trigger.

    Parameters
    ----------
    usid : int
        Set the USID for the command.
    trigger : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    return write_cmd_generator(a[PM_TRIG], usid, 2**trigger)


def ext_trig_trigger_cmd_generator(usid, trigger):
    """
    Send an Extended Trigger command to the specified trigger.

    Parameters
    ----------
    usid : int
        Set the USID for the command.
    trigger : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    return write_cmd_generator(a[EXT_TRIGGER], usid, 2**(trigger-3))


def rm_pm_trig_msk_cmd_generator(usid):
    """
    Set the PM Trigger Mask to 0.

    Parameters
    ----------
    usid : int
        Set the USID for the command.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    return write_cmd_generator(a[PM_TRIG], usid, 0)


def rm_ext_trig_msk_cmd_generator(usid):
    """
    Set the Extended Trigger Mask to 0.

    Parameters
    ----------
    usid : int
        Set the USID for the command.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    return write_cmd_generator(a[EXT_TRIGGER_MASK], usid, 0)


def set_pm_trig_mask_cmd_generator(usid, mask='all'):
    """
    Set the PM Trig Mask.

    Parameters
    ----------
    usid : int
        Set the USID for the command.
    mask : TYPE, optional
        DESCRIPTION. The default is 'all'.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    if (mask == 'all'):
        return write_cmd_generator(a[PM_TRIG], usid, 56)
    else:
        assert type(int(mask)) == int
        return write_cmd_generator(a[PM_TRIG], usid, 2**(mask+3))


def set_ext_trig_mask_cmd_generator(usid, mask='all'):
    """
    Set the Extended Trigger Mask to mask.

    Parameters
    ----------
    usid : int
        Set the USID for the command.
    mask : TYPE, optional
        DESCRIPTION. The default is 'all'.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    if (mask == 'all'):
        return write_cmd_generator(a[EXT_TRIGGER_MASK], usid, 255)
    else:
        assert type(int(mask)) == int
        return write_cmd_generator(a[EXT_TRIGGER_MASK], usid, 2**(mask-3))


def usid_prog_cmd_generator(usid, v1, v2, v3):
    """
    Perform a USID Program command.

    Parameters
    ----------
    usid : int
        Set the USID for the command.
    v1 : TYPE
        DESCRIPTION.
    v2 : TYPE
        DESCRIPTION.
    v3 : TYPE
        DESCRIPTION.

    Returns
    -------
    cmd_lst : TYPE
        DESCRIPTION.

    """
    cmd_lst = write_cmd_generator(a[29], usid, v1)
    cmd_lst += write_cmd_generator(a[30], usid, v2)
    cmd_lst += write_cmd_generator(a[31], usid, v3)
    return cmd_lst


def reg_zero_write(usid):
    """
    Test Reg0 Write functionality. (Deprecated).

    Parameters
    ----------
    usid : int
        Set the USID for the test.

    Returns
    -------
    cmd_lst : TYPE
        DESCRIPTION.

    """
    if 0 in has_bits_reserved_lst:
        val = res_dict[0]
    else:
        val = 255
    cmd_lst = pwr_rst_cmd_generator(usid)
    cmd_lst += set_pm_trig_mask_cmd_generator(usid)
    cmd_lst += read_cmd_generator(a[PM_TRIG], usid, 56)
    # cmd_lst += cmd_str_generator(1,4,usid,SIREV_ID,0,0,-1)
    cmd_lst += cmd_str_generator(1, 0, usid, 0, 0, 255, 0)
    cmd_lst += read_cmd_generator(a[0], usid, val)
    cmd_lst += rm_pm_trig_msk_cmd_generator(usid)
    cmd_lst += cmd_str_generator(1, 0, usid, 0, 0, 0, 0)
    cmd_lst += read_cmd_generator(a[0], usid, val)
    cmd_lst += pm_trig_trigger_cmd_generator(usid, trig_dict[a[0].trigger])
    cmd_lst += read_cmd_generator(a[0], usid, 0)
    return cmd_lst


def prog_USID(usid_initial):
    """
    Test programmable USID using 3 methods.

    Parameters
    ----------
    usid : int
        Set the initial USID for the test.

    Returns
    -------
    cmd_lst : TYPE
        DESCRIPTION.

    """
    def priv_prog_usid_read_block(usid):
        cmd_lst = check_err_cmd_generator(usid)
        cmd_lst += read_cmd_generator(a[ID_REGS[0]], usid,
                                      a[ID_REGS[0]].default)
        cmd_lst += check_err_cmd_generator(usid)
        cmd_lst += read_cmd_generator(a[ID_REGS[1]], usid,
                                      a[ID_REGS[1]].default)
        cmd_lst += check_err_cmd_generator(usid)
        cmd_lst += read_cmd_generator(a[ID_REGS[2]], usid,
                                      man_id_sans_usid+usid)
        cmd_lst += check_err_cmd_generator(usid)
        cmd_lst += read_cmd_generator(a[ID_REGS[3]], usid,
                                      a[ID_REGS[3]].default)
        cmd_lst += check_err_cmd_generator(usid)
        return cmd_lst

    def priv_prog_usid_method_1(usid_prev, usid_next):
        cmd_lst = write_cmd_generator(a[ID_REGS[0]], usid_prev,
                                      a[ID_REGS[0]].default)
        cmd_lst += write_cmd_generator(a[ID_REGS[1]], usid_prev,
                                       a[ID_REGS[1]].default)
        cmd_lst += write_cmd_generator(a[ID_REGS[2]], usid_prev,
                                       man_id_sans_usid+usid_next)
        return cmd_lst

    def priv_prog_usid_method_2(usid_prev, usid_next):
        val_ary = [a[ID_REGS[0]].default,
                   a[ID_REGS[1]].default,
                   man_id_sans_usid+usid_next]
        cmd_lst = extend_write_cmd_generator(a[ID_REGS[0]], usid_prev, 0,
                                             ary=val_ary)
        return cmd_lst

    def priv_prog_usid_method_3(usid_prev, usid_next):
        val_ary = [a[ID_REGS[0]].default,
                   a[ID_REGS[1]].default,
                   man_id_sans_usid+usid_next,
                   a[ID_REGS[3]].default]
        cmd_lst = extend_write_cmd_generator(a[ID_REGS[0]], usid_prev, 0,
                                             ary=val_ary)
        return cmd_lst

    man_id_sans_usid = a[ID_REGS[2]].default - usid_initial
    cmd_lst = []
    for usid2 in range(16):
        if usid2 != usid_initial:
            for fun in (priv_prog_usid_method_1,
                        priv_prog_usid_method_2,
                        priv_prog_usid_method_3):
                cmd_lst += pwr_rst_cmd_generator(usid_initial)
                cmd_lst += priv_prog_usid_read_block(usid_initial)
                cmd_lst += fun(usid_initial, usid2)
                cmd_lst += priv_prog_usid_read_block(usid2)

    return cmd_lst


def mask_write_tester(usid):
    """
    Test Masked Write functionality. (Deprecated).

    Parameters
    ----------
    usid : int
        Set the USID for the test.

    Returns
    -------
    cmd_lst : TYPE
        DESCRIPTION.

    """
    b = [reg for reg in a if type(reg) != bool]
    b = [reg for reg in b if reg.ireq == 'Yes']
    b = [reg.address for reg in b if reg.mask_rw == 'Yes']
    cmd_lst = []
    for addrs in b:
        cmd_lst += pwr_rst_cmd_generator(usid)
        cmd_lst += read_cmd_generator(a[PM_TRIG], usid, 128)
        cmd_lst += set_pm_trig_mask_cmd_generator(usid)
        cmd_lst += set_ext_trig_mask_cmd_generator(usid)
        cmd_lst += read_cmd_generator(a[PM_TRIG], usid, 56)
        cmd_lst += check_err_cmd_generator(usid)
        if addrs in has_bits_reserved_lst:
            cmd_lst += write_cmd_generator(a[addrs], usid, 0)
            cmd_lst += read_cmd_generator(a[addrs], usid, 0)
            cmd_lst += check_err_cmd_generator(usid)
            cmd_lst += msk_wrt_cmd_generator(a[addrs], usid,
                                             res_dict[addrs] ^ 255, 255)
            cmd_lst += check_err_cmd_generator(usid)
            cmd_lst += read_cmd_generator(a[addrs], usid, res_dict[addrs])
            cmd_lst += check_err_cmd_generator(usid)

        else:
            cmd_lst += write_cmd_generator(a[addrs], usid, 4)
            cmd_lst += read_cmd_generator(a[addrs], usid, 4)
            cmd_lst += check_err_cmd_generator(usid)
            cmd_lst += msk_wrt_cmd_generator(a[addrs], usid, 247, 255)
            cmd_lst += check_err_cmd_generator(usid)
            cmd_lst += read_cmd_generator(a[addrs], usid, 12)
            cmd_lst += check_err_cmd_generator(usid)
    return cmd_lst


def timed_triggers(usid):
    """
    Test the timed triggers.

    Parameters
    ----------
    usid : int
        Set the USID for the test.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    def set_clk_top_cmd_gen(usid, clk):
        return write_cmd_generator(clk, usid, 255)

    def read_clk_mult_cmd_gen(usid, clk):
        c = [244, 228, 211, 195, 178, 162, 145, 129, 112, 96,
             79, 63, 46, 30, 13, 0]
        cmd_lst = []
        for el in c:
            cmd_lst += read_cmd_generator(a[clk], usid, el)
        return cmd_lst

    b = [reg for reg in a if type(reg) != bool]
    b = [reg for reg in b if reg.ireq == 'Yes']
    b = [reg.address for reg in b if 'EXT_TRIGGER' in reg.trigger]
    cmd_lst = []
    for addrs in b:
        trig_cnt_addrs = trig_dict[a[addrs].trigger]+53
        cmd_lst += pwr_rst_cmd_generator(usid)
        cmd_lst += rm_pm_trig_msk_cmd_generator(usid)
        cmd_lst += read_cmd_generator(a[addrs], usid, a[addrs].default)
        cmd_lst += rm_ext_trig_msk_cmd_generator(usid)
        cmd_lst += write_cmd_generator(a[addrs], usid, 255)
        cmd_lst += read_cmd_generator(a[addrs], usid, a[addrs].default)
        cmd_lst += set_clk_top_cmd_gen(usid, a[trig_cnt_addrs])
        cmd_lst += read_cmd_generator(a[addrs], usid, a[addrs].default)*21
        if addrs in has_bits_reserved_lst:
            cmd_lst += read_cmd_generator(a[addrs], usid, res_dict[addrs])*5
        else:
            cmd_lst += read_cmd_generator(a[addrs], usid, 255)*5
    trig_cnt_addrs = trig_dict[a[b[0]].trigger]+53
    cmd_lst += pwr_rst_cmd_generator(usid)
    cmd_lst += rm_pm_trig_msk_cmd_generator(usid)
    cmd_lst += read_cmd_generator(a[b[0]], usid, a[b[0]].default)
    cmd_lst += rm_ext_trig_msk_cmd_generator(usid)
    cmd_lst += write_cmd_generator(a[b[0]], usid, 255)
    cmd_lst += read_cmd_generator(a[b[0]], usid, a[b[0]].default)
    cmd_lst += set_clk_top_cmd_gen(usid, a[trig_cnt_addrs])
    cmd_lst += read_clk_mult_cmd_gen(usid, trig_cnt_addrs)
    if b[0] in has_bits_reserved_lst:
        cmd_lst += read_cmd_generator(a[b[0]], usid, res_dict[b[0]])*2
    else:
        cmd_lst += read_cmd_generator(a[b[0]], usid, 255)*2
    return cmd_lst


def default_values_test(usid, ctrl):
    """
    Test the Default value of registers. (Deprecated).

    Parameters
    ----------
    usid : int
        Set the USID for the test.
    ctrl : TYPE
        DESCRIPTION.

    Returns
    -------
    cmd_lst : TYPE
        DESCRIPTION.

    """
    def priv_dvt_write_all(usid, b):
        cmd_lst = []
        for adrs in b:
            cmd_lst += write_cmd_generator(a[adrs], usid, 255)
        return cmd_lst

    def priv_dvt_read_all(usid, c, d):
        cmd_lst = []
        for adrs in c:
            cmd_lst += read_cmd_generator(a[adrs], usid, a[adrs].default)
            cmd_lst += check_err_cmd_generator(usid)
        for adrs in d:
            cmd_lst += read_cmd_generator(a[adrs], usid, a[adrs].default)
            cmd_lst += check_err_cmd_generator(usid, exp_read_err=True)
        return cmd_lst

    def priv_dvt_write_sequence(usid, b):
        cmd_lst = set_pm_trig_mask_cmd_generator(usid)
        cmd_lst += set_ext_trig_mask_cmd_generator(usid)
        cmd_lst += write_cmd_generator(a[SIREV_ID], usid, 238)
        cmd_lst += priv_dvt_write_all(usid, b)
        return cmd_lst

    def priv_dvt_read_sequence_1(usid, c, d):
        cmd_lst = pwr_rst_cmd_generator(usid)
        cmd_lst += write_cmd_generator(a[SIREV_ID], usid, 64)
        cmd_lst += priv_dvt_read_all(usid, c, d)
        return cmd_lst

    def priv_dvt_read_sequence_2(usid, c, d):
        cmd_lst = pwr_rst_cmd_generator(usid)
        cmd_lst += write_cmd_generator(a[SIREV_ID], usid, 0)
        cmd_lst += priv_dvt_read_all(usid, c, d)
        return cmd_lst

    def priv_dvt_read_sequence_3(usid, c, d):
        # This line reflects the lack of GSID reset in seq3 and 4
        temp = a[34].default
        a[34].default = '255'
        cmd_lst = udr_rst_cmd_generator(usid)
        cmd_lst += write_cmd_generator(a[SIREV_ID], usid, 0)
        cmd_lst += priv_dvt_read_all(usid, c, d)
        a[34].default = temp
        return cmd_lst

    def priv_dvt_read_sequence_4(usid, c, d):
        # This line reflects the lack of GSID reset in seq3 and 4
        temp = a[34].default
        a[34].default = '255'
        cmd_lst = udr_rst_cmd_generator(usid)
        cmd_lst += rm_pm_trig_msk_cmd_generator(usid)
        cmd_lst += write_cmd_generator(a[SIREV_ID], usid, 0)
        cmd_lst += priv_dvt_read_all(usid, c, d)
        a[34].default = temp
        return cmd_lst

    b = [reg for reg in a if type(reg) != bool]
    b = [reg for reg in b if reg.address not in ctrl]
    # c contains all reg addresses that are not ctrl regs
    # and are implmnt req
    c = [reg.address for reg in b if reg.ireq == 'Yes']
    # d contains all reg addrs that are not ctrl reg
    # that are not implement req
    d = [reg.address for reg in b if reg.ireq == 'No']
    # b contains only addresses to r/w registers
    # that are not ctrl regs and are r/w.
    b = [reg.address for reg in b if reg.r_w == 'R/W']
    cmd_lst = priv_dvt_read_sequence_1(usid, c, d)
    cmd_lst += priv_dvt_write_sequence(usid, b)
    cmd_lst += priv_dvt_read_sequence_2(usid, c, d)
    cmd_lst += priv_dvt_write_sequence(usid, b)
    cmd_lst += priv_dvt_read_sequence_3(usid, c, d)
    cmd_lst += priv_dvt_write_sequence(usid, b)
    cmd_lst += priv_dvt_read_sequence_4(usid, c, d)
    return cmd_lst


def standard_write_read_test(usid, ctrl, rb_lst):
    """
    Test Standard Write and Read functionality. (Deprecated).

    Parameters
    ----------
    usid : int
        Set the USID for the test.
    ctrl : TYPE
        DESCRIPTION.
    rb_lst : TYPE
        DESCRIPTION.

    Returns
    -------
    cmd_lst : TYPE
        DESCRIPTION.

    """
    def startup_sequence(usid):
        cmd_lst = pwr_rst_cmd_generator(usid)
        cmd_lst += write_cmd_generator(a[PM_TRIG], usid, 128)
        cmd_lst += set_pm_trig_mask_cmd_generator(usid)
        cmd_lst += write_cmd_generator(a[EXT_TRIGGER_MASK], usid, 255)
        cmd_lst += write_cmd_generator(a[SIREV_ID], usid, 238)
        return cmd_lst

    def r_w_all(usid, b, val):
        cmd_lst = check_err_cmd_generator(usid)
        for adrs in b:
            cmd_lst += write_cmd_generator(a[adrs], usid, val)
            cmd_lst += check_err_cmd_generator(usid)
        for adrs in b:
            cmd_lst += read_cmd_generator(a[adrs], usid, val)
            cmd_lst += check_err_cmd_generator(usid)
        return cmd_lst

    def r_w_rb(usid, rb_lst, val):
        cmd_lst = check_err_cmd_generator(usid)
        for adrs in rb_lst:
            cmd_lst += write_cmd_generator(a[adrs], usid, val)
            cmd_lst += check_err_cmd_generator(usid)
        if val == 0:
            for adrs in rb_lst:
                cmd_lst += read_cmd_generator(a[adrs], usid, val)
                cmd_lst += check_err_cmd_generator(usid)
            return cmd_lst
        for k in res_dict.keys():
            cmd_lst += read_cmd_generator(a[k], usid, res_dict[k])
            cmd_lst += check_err_cmd_generator(usid)
        return cmd_lst
    b = [reg for reg in a if type(reg) != bool]
    b = [reg for reg in b if reg.address not in ctrl]
    b = [reg.address for reg in b if reg.ireq == 'Yes' and reg.r_w == 'R/W']
    cmd_lst = startup_sequence(usid)
    cmd_lst += r_w_all(usid, b, 0)
    cmd_lst += r_w_all(usid, b, 255)
    cmd_lst += r_w_all(usid, b, 0)
    cmd_lst += r_w_rb(usid, rb_lst, 0)
    cmd_lst += r_w_rb(usid, rb_lst, 255)
    cmd_lst += r_w_rb(usid, rb_lst, 0)

    return cmd_lst


def triggered_write_test(usid, val):
    """
    Test PM and Extended Triggers with this function.

    Parameters
    ----------
    usid : int
        Set the USID for the test.
    val : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    def priv_trig_meta_trigger(usid, trig):
        if (trig < 3):
            return pm_trig_trigger_cmd_generator(usid, trig)
        else:
            return ext_trig_trigger_cmd_generator(usid, trig)

    def priv_trig_cmd_generator(address, usid, val, trig, target_trig):
        if address in has_bits_reserved_lst:
            orval = res_dict[address]
        else:
            orval = 255
        assert orval != a[address].default
        cmd_lst = write_cmd_generator(a[address], usid, orval)
        cmd_lst += priv_trig_meta_trigger(usid, trig)
        if (trig == target_trig):
            cmd_lst += read_cmd_generator(a[address], usid, orval)
            cmd_lst += write_cmd_generator(a[address], usid,
                                           a[address].default)
            cmd_lst += priv_trig_meta_trigger(usid, trig)
        else:
            cmd_lst += read_cmd_generator(a[address], usid,
                                          a[address].default)
        return cmd_lst

    cmd_lst = []
    b = [reg for reg in a if type(reg) != bool]
    b = [reg for reg in b if reg.ireq == 'Yes']
    b = [reg.address for reg in b if reg.trig_sup == 'Yes']

    for adrs in b:
        target_trig = trig_dict[a[adrs].trigger]
        cmd_lst += pwr_rst_cmd_generator(usid)
        cmd_lst += read_cmd_generator(a[45], usid, 0)
        cmd_lst += set_ext_trig_mask_cmd_generator(usid)
        cmd_lst += read_cmd_generator(a[45], usid, 255)
        cmd_lst += rm_pm_trig_msk_cmd_generator(usid)
        cmd_lst += rm_ext_trig_msk_cmd_generator(usid)
        cmd_lst += write_cmd_generator(a[adrs], usid, val)
        cmd_lst += read_cmd_generator(a[adrs], usid, a[adrs].default)
        for trig in trig_dict.values():
            cmd_lst += priv_trig_cmd_generator(adrs, usid, val, trig,
                                               target_trig)
    return cmd_lst


def extended_write_test(usid, val, ctrl, rb_lst):
    """
    Test the Extended Write Command functionality of registers. (Deprecated).

    Parameters
    ----------
    usid : int
        Set the USID for the test.
    val : TYPE
        DESCRIPTION.
    ctrl : TYPE
        DESCRIPTION.
    rb_lst : TYPE
        DESCRIPTION.

    Returns
    -------
    cmd_lst : list
        Returns a list of commands.

    """
    def priv_test_sequence(reg, usid, vals):
        cmd_lst = pwr_rst_cmd_generator(usid)
        cmd_lst += set_pm_trig_mask_cmd_generator(usid)
        cmd_lst += set_ext_trig_mask_cmd_generator(usid)
        cmd_lst += write_cmd_generator(a[SIREV_ID], usid, 238)
        for val in vals:
            cmd_lst += extend_write_cmd_generator(reg, usid, val)
            cmd_lst += extend_read_cmd_generator(reg, usid, val)
        cmd_lst += check_err_cmd_generator(usid)
        return cmd_lst

    def priv_test_pm_trig(usid):
        cmd_lst = pwr_rst_cmd_generator(usid)
        cmd_lst += priv_test_sequence(a[PM_TRIG], usid, [56, 48, 56])
        return cmd_lst

    def priv_test_udr_rst(usid):
        if 0 in has_bits_reserved_lst:
            val = res_dict[0]
        else:
            val = 255
        cmd_lst = set_pm_trig_mask_cmd_generator(usid)
        cmd_lst += set_ext_trig_mask_cmd_generator(usid)
        cmd_lst += write_cmd_generator(a[0], usid, val)
        cmd_lst += read_cmd_generator(a[0], usid, val)
        cmd_lst += extend_write_cmd_generator(a[UDR_RST], usid, 128)
        cmd_lst += extend_read_cmd_generator(a[UDR_RST], usid, 0)
        cmd_lst += read_cmd_generator(a[0], usid, a[0].default)
        return cmd_lst

    def priv_test_err_sum(usid):
        cmd_lst = write_cmd_generator(a[20], usid, 255)
        cmd_lst += read_cmd_generator(a[20], usid, 0)
        cmd_lst += extend_read_cmd_generator(a[ERR_SUM], usid, 6)
        return cmd_lst

    def priv_test_bus_ld(usid):
        cmd_lst = extend_read_cmd_generator(a[BUS_LD], usid,
                                            a[BUS_LD].default)
        cmd_lst += extend_write_cmd_generator(a[BUS_LD], usid,
                                              a[BUS_LD].default+1)
        cmd_lst += extend_read_cmd_generator(a[BUS_LD], usid,
                                             a[BUS_LD].default+1)
        cmd_lst += extend_write_cmd_generator(a[BUS_LD], usid,
                                              a[BUS_LD].default)
        return cmd_lst

    def priv_test_ext_trig_mask(usid):
        cmd_lst = pwr_rst_cmd_generator(usid)
        cmd_lst += extend_read_cmd_generator(a[EXT_TRIGGER_MASK], usid,
                                             a[EXT_TRIGGER_MASK].default)
        cmd_lst += extend_write_cmd_generator(a[EXT_TRIGGER_MASK], usid, 255)
        cmd_lst += extend_read_cmd_generator(a[EXT_TRIGGER_MASK], usid, 255)
        cmd_lst += extend_write_cmd_generator(a[EXT_TRIGGER_MASK], usid, 0)
        return cmd_lst

    def priv_test_ext_trigger(usid, reg):
        cmd_lst = write_cmd_generator(reg, usid, 15)
        cmd_lst += read_cmd_generator(reg, usid, reg.default)
        cmd_lst += extend_write_cmd_generator(a[EXT_TRIGGER], usid, 255)
        cmd_lst += read_cmd_generator(reg, usid, 15)
        return cmd_lst

    def priv_test_test_patt(usid):
        return extend_read_cmd_generator(a[TEST_PATT], usid,
                                         a[TEST_PATT].default)

    b = [reg for reg in a if type(reg) != bool]
    b = [reg for reg in b if reg.ireq == 'Yes']
    b = [reg for reg in b if reg.address not in ctrl]
    trig_lst = [reg for reg in b if (type(reg) != bool and
                                     reg.trigger != 'N/A')]
    trig_lst = [reg for reg in trig_lst if 'EXT' in reg.trigger]
    b = [reg.address for reg in b if reg.ext_rw == 'Yes']
    rb_lst = [rb for rb in rb_lst if a[rb].ext_rw == 'Yes']
    cmd_lst = priv_test_pm_trig(usid)
    cmd_lst += priv_test_udr_rst(usid)
    cmd_lst += priv_test_err_sum(usid)
    cmd_lst += priv_test_bus_ld(usid)
    cmd_lst += priv_test_ext_trig_mask(usid)
    # Determine if there are any triggers in the chip
    # No reason to test if there arent any.
    if any(trig_lst):
        cmd_lst += priv_test_ext_trigger(usid, trig_lst[0])
    cmd_lst += priv_test_test_patt(usid)
    cmd_lst += pwr_rst_cmd_generator(usid)
    cmd_lst += set_pm_trig_mask_cmd_generator(usid)
    cmd_lst += write_cmd_generator(a[EXT_TRIGGER_MASK], usid, 255)
    cmd_lst += write_cmd_generator(a[SIREV_ID], usid, 238)
    for adrs in b:
        cmd_lst += priv_test_sequence(a[adrs], usid, [0, 255, 0])
    for adrs in rb_lst:
        orval = res_dict[adrs]  # val | a[adrs].default
        assert orval != a[adrs].default
        cmd_lst += priv_test_sequence(a[adrs], usid, [0, orval, 0])
    return cmd_lst


def fuseburn_readback(usid, num_banks=4):
    """
    Test the fuse readback registers with this test.

    Parameters
    ----------
    usid : int
        Set the USID for the test.
    num_banks : int, optional
        Set the number of fuse banks. The default is 4.

    Returns
    -------
    cmd_lst : list
        Returns a list of commands.

    """
    cmd_lst = pwr_rst_cmd_generator(usid)
    cmd_lst += set_pm_trig_mask_cmd_generator(usid)
    cmd_lst += set_ext_trig_mask_cmd_generator(usid)
    cmd_lst += write_cmd_generator(a[FUSE], usid, 0)
    # For every bank
    for i in range(num_banks):
        # Select a bank
        cmd_lst += write_cmd_generator(a[BANK], usid, 128+i)
        # NOP's to give the FBRB regs time to populate with values.
        for _ in range(5):
            # We've set the masks, so we should expect to see 56 in PM_TRIG.
            # Read five times for delay.
            cmd_lst += read_cmd_generator(a[PM_TRIG], usid, 56)
        # Read from the FBRB registers
        for adrs in FB_READBACK:
            cmd_lst += read_cmd_generator(a[adrs], usid, 0)
    return cmd_lst


hdr_str = ['#,setup_header,test_system,Manual,,,\n']
hdr_str += ['#,setup_header,version,1,,,\n']
hdr_str += ['#,MipiVerification,clusters,,,,\n']
hdr_str += ['enabled,type,usid,regAddr,writeMask,regWriteData,' +
            'expectedReadData,regWriteArrayItem0,regWriteArrayItem1,' +
            'regWriteArrayItem2,regWriteArrayItem3\n']

# %%
# MMC NOTE
# We should specify our input files below.
in_file_dir = 'C:\\Users\\joslaton\\Documents\\MIPI Demo\\'
# MMC NOTE
# in_file_stand is the standard machine readable register map file.
# Registers range from 0x00-0x63.
in_file_stand = 'SARGE_USID7.csv'
# MMC NOTE
# in_file_extended is the extended machine readable register map file.
# Registers range from 0x00-0x63.
in_file_extended = 'SARGE_EXTENDED.csv'
# MMC NOTE
# usid sets the USID used during testing.
usid = 7
a = register_pack_generator(in_file_dir, in_file_stand, in_file_extended)

# MMC NOTE
# An output directory must be specified
out_file_dir = 'C:\\Users\\joslaton\\Documents\\MIPI Demo\\Generated\\'
# MMC NOTE
# We should specify our required tests below.
# If, for instance, there are no timed triggers on the
# device, we should not attempt to run the timed
# triggers function. An error may result.
out_file_name = [  # 'Reg0Write.csv',
                 'Programmable_USID.csv',
                 # 'Masked_Write.csv',
                 # 'Timed_Triggers.csv',
                 # 'Default_Values.csv',
                 # 'Std_Write.csv',
                 'Triggered_Write_Test.csv',
                 # 'Extended_Write_Test.csv',
                 'Fuseburn_ReadBack_Test.csv']

# MMC NOTE
# Comment out any test you do not wish to have performed.
# Keep in mind that the output order is positional.
output = [hdr_str + prog_USID(usid)]
# output += [hdr_str + timed_triggers(usid)]
output += [hdr_str + triggered_write_test(usid, 255)]
# MMC NOTE
# num_banks is the number of Fuse Banks in the part.
output += [hdr_str + fuseburn_readback(usid, num_banks=8)]


for i in range(len(output)):
    with open(out_file_dir+out_file_name[i], 'w') as f:
        f.writelines(output[i])
