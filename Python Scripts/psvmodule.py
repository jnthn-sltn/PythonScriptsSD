# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 11:43:33 2020.

@author: joslaton
"""

import pandas as pd
import sys

rffe_dict = {
    'PM_TRIG': 28,
    'PRODUCT_ID': 29,
    'MANUFACTURER_ID': 30,
    'MAN_USID': 31,
    'EXT_PRODUCT_ID': 32,
    'REV_ID': 33,
    'GSID': 34,
    'UDR_RST': 35,
    'ERR_SUM': 36,
    'INT_MAP1': 37,
    'INT_MAP2': 38,
    'INT_EN0': 39,
    'INT_EN1': 40,
    'INT_CLR0': 41,
    'INT_CLR1': 42,
    'BUS_LD': 43,
    'TEST_PATT': 44,
    'EXT_TRIG_MASK_A': 45,
    'EXT_TRIG_REG_A': 46,
    'EXT_TRIG_REG_B': 47,
    'EXT_TRIG_MASK_B': 48,
    'EXT_TRIG_CNT_11_H': 49,
    'EXT_TRIG_CNT_12_H': 50,
    'EXT_TRIG_CNT_13_H': 51,
    'EXT_TRIG_CNT_14_H': 52,
    'EXT_TRIG_CNT_15_H': 53,
    'EXT_TRIG_CNT_16_H': 54,
    'EXT_TRIG_CNT_17_H': 55,
    'EXT_TRIG_CNT_3_H': 56,
    'EXT_TRIG_CNT_4_H': 57,
    'EXT_TRIG_CNT_5_H': 58,
    'EXT_TRIG_CNT_6_H': 59,
    'EXT_TRIG_CNT_7_H': 60,
    'EXT_TRIG_CNT_8_H': 61,
    'EXT_TRIG_CNT_9_H': 62,
    'EXT_TRIG_CNT_10_H': 63,
    'SIREV_ID': 164}

import_cols = {'standard': ['Register Class',
                            'Implementation Required',
                            'Register Address (Hex.)',
                            'Register name',
                            'Data Bits',
                            'Bit Name',
                            'Default',
                            'Broadcast Slave ID and'
                            ' Group Slave ID Support',
                            'Trigger Support',
                            'Active Trigger ',
                            'Extended Register R/W',
                            'Masked Write Support',
                            'R/W'],
               'extended': ['Register Address (Hex.)',
                            'Register Name',
                            'No. Bits',
                            'Data Bits',
                            'Function',
                            'Default',
                            'Triggered',
                            'Mask-Write Support',
                            'TBYB']}

# %% Class Definition


class Register:
    """
    The Register class holds all information needed for a register.

    Parameters
    ----------
    None

    """

    def __init__(self, address):
        """
        Instantiate the Register class.

        Parameters
        ----------
        address : STRING
            HEX STRING with the format '0x01', '0x0A' etc.

        Returns
        -------
        None.

        """
        self.d = {}
        self.d['Name'] = ''
        self.d['Address'] = address
        self.d['Value'] = '---'
        self.d['D7'] = '-'
        self.d['D6'] = '-'
        self.d['D5'] = '-'
        self.d['D4'] = '-'
        self.d['D3'] = '-'
        self.d['D2'] = '-'
        self.d['D1'] = '-'
        self.d['D0'] = '-'
        self.d['Trig N'] = '-'
        self.d['RZW'] = '-' if address != '0x00' else 'O'
        self.d['RW'] = '-'
        self.d['ERW'] = '-'
        self.d['MRW'] = '-'
        self.d['RR'] = '-'
        self.d['ERR'] = '-'
        self.d['RST'] = '-'
        self.d['BSID'] = '-'
        self.d['GSID1'] = '-'
        self.d['GSID2'] = '-'

    def set_name(self, df_slice):
        """
        Set the register name.

        Parameters
        ----------
        df_slice : dataframe
            A dataframe limited to the current address.

        Returns
        -------
        None.

        """
        if self.d['Address'] < '0x80':
            a = [el for el in df_slice['Register name'].tolist() if
                 type(el) == str]
            if a:
                self.d['Name'] = a[0]
        else:
            a = [el for el in df_slice['Register Name'].tolist() if
                 type(el) == str]
            if a:
                self.d['Name'] = a[0]

    def set_dv(self, df_slice):
        """
        Set the Value.

        Parameters
        ----------
        df_slice : dataframe
            A dataframe limited to the current address.

        Returns
        -------
        None.

        """
        dv = ''.join([el for el in df_slice['Default'].tolist() if
                      type(el) == str])
        if self.d['Address'] < '0x80':
            try:
                if dv[1] in ['x', 'X']:
                    self.d['Value'] = dv.replace('X', 'x')
                else:
                    dv = int(dv, 2)
                    self.d['Value'] = f'0x{dv:2X}'.replace(' ', '0')
            except ValueError:
                print(f"Register {self.d['Address']} has an invalid"
                      f" default value of \"{dv}\".")
                print("Only numeric values are accepted."
                      " Please change the value in Excel and try again.")
                sys.exit(0)
        else:
            try:
                assert len(dv) == 4
                self.d['Value'] = dv.replace('X', 'x')
            except AssertionError:
                print(f"Register {self.d['Address']} has an invalid"
                      f" default value of \"{dv}\".")
                print("Only numeric values are accepted."
                      " Please change the value in Excel and try again.")
                sys.exit(0)

    def set_trign(self, df_slice):
        """
        Set the trigger.

        Parameters
        ----------
        df_slice : dataframe
            A dataframe limited to the current address.

        Returns
        -------
        None.

        """
        if self.d['Address'] < '0x80':
            a = [el for el in df_slice['Active Trigger '].tolist() if
                 type(el) == str]
            if a:
                a = a[0]
                a = a[0] + a[-1] if a[0] != 'E' else 'T' + a[-1]
                self.d['Trig N'] = a
        else:
            a = [el for el in df_slice['Triggered'].tolist() if
                 type(el) == str]
            if a:
                if a[0] not in ['N', 'n', 'No']:
                    a = a[0]
                    a = a[0] + a[-1] if a[0] != 'E' else 'T' + a[-1]
                    self.d['Trig N'] = a

    def set_rw(self, df_slice):
        """
        Set the register write field.

        Parameters
        ----------
        df_slice : dataframe
            A dataframe limited to the current address.

        Returns
        -------
        None.

        """
        if self.d['Address'] < '0x80':
            a = [el for el in df_slice['R/W'].tolist() if type(el) == str]
            if all([any(['R/W' in a, 'W' in a]), self.d['Address'] < '0x20']):
                self.d['RW'] = 'O'
        else:
            pass

    def set_rr(self, df_slice):
        """
        Set the register read field.

        Parameters
        ----------
        df_slice : dataframe
            A dataframe limited to the current address.

        Returns
        -------
        None.

        """
        if self.d['Address'] < '0x20':
            a = [el for el in df_slice['R/W'].tolist() if type(el) == str]
            if any(['R/W' in a, 'R' in a]):
                self.d['RR'] = 'O'
        else:
            pass

    def set_erw(self, df_slice):
        """
        Set the extended register write field.

        Parameters
        ----------
        df_slice : dataframe
            A dataframe limited to the current address.

        Returns
        -------
        None.

        """
        if self.d['Address'] < '0x80':
            a = [el for el in df_slice['R/W'].tolist() if type(el) == str]
            b = [el for el in df_slice['Extended Register R/W'].tolist() if
                 type(el) == str]
            if all([any(['R/W' in a, 'W' in a]), 'Yes' in b]):
                self.d['ERW'] = 'O'
        else:
            a = [el for el in df_slice['TBYB'].tolist() if type(el) == str]
            b = list(set([el for el in df_slice['Register Name'].tolist() if
                          type(el) == str]))
            if all([a, b]):
                if all([a[0] in ['N', 'No'],
                        b[0].lower() not in ['sirev_id']]):
                    self.d['ERW'] = 'O'

    def set_err(self, df_slice):
        """
        Set the extended register read field.

        Parameters
        ----------
        df_slice : dataframe
            A dataframe limited to the current address.

        Returns
        -------
        None.

        """
        if self.d['Address'] < '0x80':
            a = [el for el in df_slice['R/W'].tolist() if type(el) == str]
            b = [el for el in df_slice['Extended Register R/W'].tolist() if
                 type(el) == str]
            if all([any(['R/W' in a, 'R' in a]), 'Yes' in b]):
                self.d['ERR'] = 'O'
        else:
            self.d['ERR'] = 'O'

    def set_mrw(self, df_slice):
        """
        Set the extended register write field.

        Parameters
        ----------
        df_slice : dataframe
            A dataframe limited to the current address.

        Returns
        -------
        None.

        """
        if self.d['Address'] < '0x80':
            a = [el for el in df_slice['R/W'].tolist() if type(el) == str]
            b = [el for el in df_slice['Masked Write Support'].tolist() if
                 type(el) == str]
            if all([any(['R/W' in a, 'W' in a]), 'Yes' in b]):
                self.d['MRW'] = 'O'
        else:
            a = [el for el in df_slice['TBYB'].tolist() if type(el) == str]
            if a:
                if a[0] in ['N', 'No']:
                    b = [el for el in df_slice['Mask-Write Support'] if
                         type(el) == str]
                    if b:
                        if b[0] not in ['N', 'No']:
                            self.d['MRW'] = 'O'

    def set_bgg(self, df_slice):
        """
        Set the BSID/GSID1/GSID2 write field.

        Parameters
        ----------
        df_slice : dataframe
            A dataframe limited to the current address.

        Returns
        -------
        None.

        """
        if self.d['Address'] < '0x80':
            a = [el for el in df_slice['R/W'].tolist() if type(el) == str]
            b = [el for el in df_slice[
                'Broadcast Slave ID and Group Slave ID Support'] if
                type(el) == str]
            if all([any(['R/W' in a, 'W' in a]), 'Yes' in b]):
                self.d['BSID'] = 'O'
                self.d['GSID1'] = 'O'
                self.d['GSID2'] = 'O'
        else:
            pass

    def set_rst(self, df_slice):
        """
        Set the RST field.

        Parameters
        ----------
        df_slice : dataframe
            A dataframe limited to the current address.

        Returns
        -------
        None.

        """
        if self.d['Address'] < '0x80':
            a = self.d['ERW'] == 'O'
            b = self.d['ERR'] == 'O'
            c = [el for el in df_slice['Register Class'].tolist() if
                 type(el) == str]
            d = 'RFFE Reserved'
            if all([a, b, d not in c]):
                self.d['RST'] = 'O'
        else:
            if self.d['ERW'] == 'O':
                self.d['RST'] = 'O'

    def set_bits(self, df_slice):
        """
        Set the DX fields.

        Parameters
        ----------
        df_slice : dataframe
            A dataframe limited to the current address.

        Returns
        -------
        None.

        """
        for i in range(8):
            self.d[f'D{i}'] = 'R'
        a = [el.strip('[]') for el in df_slice['Data Bits'].tolist() if
             type(el) == str]
        if self.d['Address'] < '0x80':
            b = [el for el in df_slice['Bit Name'].tolist() if
                 type(el) == str]
            c = [el for el in df_slice['R/W'].tolist() if type(el) == str]
            sb_dict = dict(zip(a, b))
            reserved_dict = {}
            # Expand the '7:5' style data bits until each bit is represented.
            for k in sb_dict.keys():
                if ':' in k:
                    hi_dex = int(k[0]) + 1
                    lo_dex = int(k[-1])
                    for i in range(lo_dex, hi_dex):
                        reserved_dict[f"{i}"] = sb_dict[k]
                else:
                    reserved_dict[k] = sb_dict[k]
            # Now must become boolean
            for k in reserved_dict.keys():
                reserved_dict[k] = 'reserved' in reserved_dict[k].lower()
                if 'R' in c:
                    reserved_dict[k] = True
                if reserved_dict[k]:
                    try:
                        val = int(self.d['Value'], 16)
                    except ValueError:
                        print(f"Default value at Register {self.d['Address']}"
                              " is invalid.\n")
                        sys.exit(1)
                    self.d[f'D{k}'] += f'{val:008b}'[-1::-1][int(k)]
                else:
                    self.d[f'D{k}'] += '/W'
        else:
            b = [el for el in df_slice['Function'].tolist() if
                 type(el) == str]
            c = [el for el in df_slice['TBYB'].tolist() if type(el) == str]
            sb_dict = dict(zip(a, b))
            # Need to expand because sometimes not all bits are implemented.
            reserved_dict = {'0': 'RESERVED', '1': 'RESERVED',
                             '2': 'RESERVED', '3': 'RESERVED',
                             '4': 'RESERVED', '5': 'RESERVED',
                             '6': 'RESERVED', '7': 'RESERVED'}
            # Expand the '7:5' style data bits until each bit is represented.
            for k in sb_dict.keys():
                if ':' in k:
                    hi_dex = int(k[0]) + 1
                    lo_dex = int(k[-1])
                    for i in range(lo_dex, hi_dex):
                        reserved_dict[f"{i}"] = sb_dict[k]
                else:
                    reserved_dict[k] = sb_dict[k]
            # Now must become boolean
            for k in reserved_dict.keys():
                reserved_dict[k] = any(['reserved' in reserved_dict[k].lower(),
                                        'y' in c[0].lower()])
                if reserved_dict[k]:
                    val = int(self.d['Value'], 16)
                    self.d[f'D{k}'] += f'{val:008b}'[-1::-1][int(k)]
                else:
                    self.d[f'D{k}'] += '/W'


# %% Function Definition

def condition_df(df, ext=False):
    """
    Condition the dataframe to enforce formatting.

    Parameters
    ----------
    df : DataFrame
        DataFrame containing raw, unconditioned data.
    ext : Boolean, optional
        Flag for pSemi extended register DataFrame. The default is False.

    Returns
    -------
    df : DataFrame
        DataFrame containing conditioned data.

    """
    df.dropna(axis=0, how='all', inplace=True)
    df.reset_index(drop=True)
    if ext:
        df[
           ['Register Address (Hex.)', 'Register Name']
          ] = df[
                 ['Register Address (Hex.)', 'Register Name']
                ].fillna(method='ffill')
    else:
        df[
           ['Register Address (Hex.)', 'Bit Name']
          ] = df[
                 ['Register Address (Hex.)', 'Bit Name']
                ].fillna(method='ffill')
    return df


def get_implemented_registers(s_df, e_df):
    """
    Collect the implemented registers.

    Parameters
    ----------
    s_df : DataFrame
        DataFrame containing information on the standard registers.
    e_df : DataFrame
        DataFrame containing information on the extended registers.

    Returns
    -------
    implemented_registers : list
        List containing the addresses of implemented registers.

    """
    standard_registers = list(sorted(set(
        s_df.query('`Implementation Required` == "Yes"'
                   ' or `Implementation Required` == "Optional"')[
                            'Register Address (Hex.)'])))
    standard_registers = [address for address in
                          standard_registers if len(address) == 4]

    extended_registers = list(sorted(set(e_df['Register Address (Hex.)'])))
    extended_registers = [address for address in
                          extended_registers if len(address) == 4]
    # Want to remove all of the registers that use N/A as default value.
    tmp_reg_lst = []
    for address in extended_registers:
        tmp_list = e_df['Default'][
            e_df['Register Address (Hex.)'] == address].tolist()
        tmp_list = [n for n in tmp_list if type(n) == str]
        if tmp_list:
            tmp_reg_lst += [address]
    extended_registers = tmp_reg_lst
    # Get all implemented registers
    implemented_registers = standard_registers + extended_registers
    return implemented_registers


def populate_register_fields(s_df, e_df, implemented_registers, register_pack):
    """
    Populate the register fields for implemented registers.

    Parameters
    ----------
    s_df : DataFrame
        DataFrame containing information on the standard registers.
    e_df : DataFrame
        DataFrame containing information on the extended registers.
    implemented_registers : list
        List containing the addresses of implemented registers.
    register_pack : list
        List containing Register objects for all registers.

    Returns
    -------
    register_pack : list
        List containing Register objects for all registers.

    """
    for address in implemented_registers:
        if address < '0x80':
            df_slice = s_df[
                s_df['Register Address (Hex.)'] == address
                ]
        else:
            df_slice = e_df[
                e_df['Register Address (Hex.)'] == address
                ]
        register_pack[address].set_name(df_slice)
        register_pack[address].set_dv(df_slice)
        register_pack[address].set_trign(df_slice)
        register_pack[address].set_rw(df_slice)
        register_pack[address].set_rr(df_slice)
        register_pack[address].set_erw(df_slice)
        register_pack[address].set_err(df_slice)
        register_pack[address].set_mrw(df_slice)
        register_pack[address].set_bgg(df_slice)
        register_pack[address].set_rst(df_slice)
        register_pack[address].set_bits(df_slice)
    return register_pack


def get_register_df(prd_file, standard_sheet, extended_sheet):
    """
    Import the register maps and construct the MRD DataFrame.

    Parameters
    ----------
    prd_file : str
        string path to file containing register map sheets.
    standard_sheet : str
        string name of standard register map sheet.
    extended_sheet : str
        string name of extended register map sheet.

    Returns
    -------
    register_df : DataFrame
        DataFrame containing MRD.
    usid : int
        Base 10 integer value of device USID.

    """
    # Import the PRD Register Maps.
    s_df = pd.read_excel(prd_file,
                         sheet_name=standard_sheet,
                         header=0,
                         usecols=import_cols['standard'])

    e_df = pd.read_excel(prd_file,
                         sheet_name=extended_sheet,
                         header=0,
                         usecols=import_cols['extended'])
    s_df = condition_df(s_df)
    e_df = condition_df(e_df, ext=True)
    implemented_registers = get_implemented_registers(s_df, e_df)
    # Initialize reg_lst
    reg_lst = [f'0x{el:02X}' for el in range(256)]
    # Create empty register dict
    register_pack = {el: Register(el) for el in reg_lst}
    # Populate register fields
    register_pack = populate_register_fields(s_df,
                                             e_df,
                                             implemented_registers,
                                             register_pack)
    # Construct output from register pack dictionaries
    register_df = pd.DataFrame([register.d for register
                                in register_pack.values()])
    # usid sets the USID used during testing.
    usid = register_df.query('Address == "0x1F"')['Value'].values.tolist()
    usid = usid[0][3]
    usid = int(usid, 16)
    return register_df, usid


def save_mrd(df, output_file):
    """
    Save the MRD DataFrame to the output_file path.

    Parameters
    ----------
    df : DataFrame
        DataFrame containing the MRD.
    output_file : str
        String path to which MRD will be saved.

    Returns
    -------
    None.

    """
    df.to_csv(path_or_buf=output_file, index=False)


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


def read_cmd_generator(adrs, usid, erd):
    """
    Send a Standard Read Command .

    Parameters
    ----------
    adrs : int
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
    return cmd_str_generator(1, 2, usid, adrs, 0, 0, erd)


def extend_read_cmd_generator(adrs, usid, erd):
    """
    Send an Extended Read Command.

    Parameters
    ----------
    adrs : int
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
    return cmd_str_generator(1, 4, usid, adrs, 0, 0, erd)


def write_cmd_generator(adrs, usid, wrt):
    """
    Send a Standard Write Command.

    Parameters
    ----------
    adrs : int
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
    return cmd_str_generator(1, 1, usid, adrs, 0, wrt, 0)


def extend_write_cmd_generator(adrs, usid, wrt, ary=[]):
    """
    Send an Extended Write Command.

    Parameters
    ----------
    adrs : int
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
    return cmd_str_generator(1, typ, usid, adrs, 0, wrt, 0,
                             regwrary=ary)


def msk_wrt_cmd_generator(adrs, usid, msk, wrt):
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
    return cmd_str_generator(1, 5, usid, adrs, msk, wrt, 0)


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
        return cmd_str_generator(1, 2, usid, rffe_dict['ERR_SUM'], 0, 0, 4)
    return cmd_str_generator(1, 2, usid, rffe_dict['ERR_SUM'], 0, 0, -1)


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
        return write_cmd_generator(rffe_dict['PM_TRIG'], usid, 64)
    return write_cmd_generator(rffe_dict['PM_TRIG'], 0, 64)


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
    return write_cmd_generator(rffe_dict['UDR_RST'], usid, 128)


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
    cmd_lst = write_cmd_generator(rffe_dict['PM_TRIG'], usid, 7)
    cmd_lst += write_cmd_generator(rffe_dict['EXT_TRIG_REG_A'], usid, 255)
    cmd_lst += write_cmd_generator(rffe_dict['EXT_TRIG_REG_B'], usid, 255)
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
    return write_cmd_generator(rffe_dict['PM_TRIG'], usid, 2**trigger)


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
    if trigger < 11:
        ext_trig_reg = 'EXT_TRIG_REG_A'
        trigger = 2**(trigger-3)
    else:
        ext_trig_reg = 'EXT_TRIG_REG_B'
        trigger = 2**(trigger-11)
    return write_cmd_generator(rffe_dict[ext_trig_reg], usid, trigger)


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
    return write_cmd_generator(rffe_dict['PM_TRIG'], usid, 0)


def rm_ext_trig_msk_a_cmd_generator(usid):
    """
    Set the Extended Trigger A Mask to 0.

    Parameters
    ----------
    usid : int
        Set the USID for the command.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    return write_cmd_generator(rffe_dict['EXT_TRIG_MASK_A'], usid, 0)


def rm_ext_trig_msk_b_cmd_generator(usid):
    """
    Set the Extended Trigger B Mask to 0.

    Parameters
    ----------
    usid : int
        Set the USID for the command.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    return write_cmd_generator(rffe_dict['EXT_TRIG_MASK_B'], usid, 0)


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
    return write_cmd_generator(rffe_dict['PM_TRIG'], usid, 56)


def set_ext_trig_mask_a_cmd_generator(usid):
    """
    Set the Extended Trigger A Mask to mask.

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
    return write_cmd_generator(rffe_dict['EXT_TRIG_MASK_A'], usid, 255)


def set_ext_trig_mask_b_cmd_generator(usid):
    """
    Set the Extended Trigger B Mask to mask.

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
    return write_cmd_generator(rffe_dict['EXT_TRIG_MASK_B'], usid, 255)


def trigger_cmd_generator(usid, trigger):
    """
    Catch all trigger command generator.

    Parameters
    ----------
    usid : int
        Set the USID for the command.
    trigger : TYPE
        DESCRIPTION.

    Returns
    -------
    function
        Passthrough function.

    """
    if trigger < 3:
        return pm_trig_trigger_cmd_generator(usid, trigger)
    else:
        return ext_trig_trigger_cmd_generator(usid, trigger)

# %%


def triggered_write_test(usid, adrs_lst, dv_lst, mtrig=False):
    """
    Test PM and Extended Triggers with this function.

    Parameters
    ----------
    usid : int
        Set the USID for the test.
    adrs_lst : list of ints
        Addresses to test.
    dv_lst : list of ints
        Default values list.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    cmd_lst = []
    for i in range(len(adrs_lst)):
        # Send address change header.
        cmd_lst += extend_write_cmd_generator(255, usid, 0)
        for trig in range(19):
            # Send trigger change header.
            cmd_lst += extend_write_cmd_generator(255, usid, 1)
            # Perform UDR Reset if not mtrig.
            if not mtrig:
                cmd_lst += udr_rst_cmd_generator(usid)
            # Set all trigger masking.
            cmd_lst += set_pm_trig_mask_cmd_generator(usid)
            cmd_lst += set_ext_trig_mask_a_cmd_generator(usid)
            cmd_lst += set_ext_trig_mask_b_cmd_generator(usid)
            # Verify default value is correct.
            cmd_lst += extend_read_cmd_generator(adrs_lst[i], usid, dv_lst[i])
            # Write 0xFF to the register.
            cmd_lst += extend_write_cmd_generator(adrs_lst[i], usid, 255)
            # Verify write occured.
            cmd_lst += extend_read_cmd_generator(adrs_lst[i], usid, 255)
            # Clear all trigger masks.
            cmd_lst += rm_pm_trig_msk_cmd_generator(usid)
            cmd_lst += rm_ext_trig_msk_a_cmd_generator(usid)
            cmd_lst += rm_ext_trig_msk_b_cmd_generator(usid)
            # Write 0x00 to the register.
            cmd_lst += extend_write_cmd_generator(adrs_lst[i], usid, 0)
            # Verify write hasnt occurred.
            cmd_lst += extend_read_cmd_generator(adrs_lst[i], usid, 0)
            # Trigger
            cmd_lst += trigger_cmd_generator(usid, trig)
            # Verify write has occurred.
            cmd_lst += extend_read_cmd_generator(adrs_lst[i], usid, 0)
    return cmd_lst


def tbyb_test(usid, adrs_lst, dv_lst):
    """
    Test all TBYB registers with this function.

    Parameters
    ----------
    usid : int
        Set the USID for the test.
    adrs_lst : list of ints
        Addresses to test.
    dv_lst : list of ints
        Default values list.

    Returns
    -------
    cmd_lst

    """
    cmd_lst = []
    for i in range(len(adrs_lst)):
        # Send address change header.
        cmd_lst += extend_write_cmd_generator(255, usid, 2)
        # Perform PWR Reset.
        cmd_lst += pwr_rst_cmd_generator(usid)
        # Set all trigger masking.
        cmd_lst += set_pm_trig_mask_cmd_generator(usid)
        cmd_lst += set_ext_trig_mask_a_cmd_generator(usid)
        cmd_lst += set_ext_trig_mask_b_cmd_generator(usid)
        # Verify default value is correct.
        cmd_lst += extend_read_cmd_generator(adrs_lst[i], usid, dv_lst[i])
        # Write 0xFF to the register.
        cmd_lst += extend_write_cmd_generator(adrs_lst[i], usid, 255)
        # Verify no write occured.
        cmd_lst += extend_read_cmd_generator(adrs_lst[i], usid, dv_lst[i])
        # Set TBYB Mode to active.
        cmd_lst += extend_write_cmd_generator(rffe_dict['SIREV_ID'], usid, 238)
        # Write 0xFF to the register.
        cmd_lst += extend_write_cmd_generator(adrs_lst[i], usid, 255)
        # Verify write occured.
        cmd_lst += extend_read_cmd_generator(adrs_lst[i], usid, 255)
        # Write 0x00 to the register.
        cmd_lst += extend_write_cmd_generator(adrs_lst[i], usid, 0)
        # Verify write occured.
        cmd_lst += extend_read_cmd_generator(adrs_lst[i], usid, 0)
        # Set TBYB Mode to inactive.
        cmd_lst += extend_write_cmd_generator(rffe_dict['SIREV_ID'], usid, 239)
        # Write 0xFF to the register.
        cmd_lst += extend_write_cmd_generator(adrs_lst[i], usid, 255)
        # Verify write did not occur.
        cmd_lst += extend_read_cmd_generator(adrs_lst[i], usid, 0)
    return cmd_lst


def trig_counter_test(usid, adrs_lst, dv_lst, mtrig=False):
    """
    Test PM and Extended Triggers with this function.

    Parameters
    ----------
    usid : int
        Set the USID for the test.
    adrs_lst : list of ints
        Addresses to test.
    dv_lst : list of ints
        Default values list.

    Returns
    -------
    cmd_lst

    """
    def set_clk_top_cmd_gen(usid, clk):
        return write_cmd_generator(clk, usid, 255)

    def read_clk_mult_cmd_gen(usid, clk):
        c = [244, 228, 211, 195, 178, 162, 145, 129, 112, 96,
             79, 63, 46, 30, 13, 0]
        cmd_lst = []
        for el in c:
            cmd_lst += read_cmd_generator(clk, usid, el)
        return cmd_lst

    cmd_lst = []
    if len(adrs_lst) < 1:
        return cmd_lst
    for i in range(len(adrs_lst)):
        # Send address change header.
        cmd_lst += extend_write_cmd_generator(255, usid, 3)
        for trig in range(3, 18):
            # Send trigger change header.
            cmd_lst += extend_write_cmd_generator(255, usid, 4)
            # Perform UDR Reset if not mtrig.
            if not mtrig:
                cmd_lst += udr_rst_cmd_generator(usid)
            # Set all trigger masking.
            cmd_lst += set_pm_trig_mask_cmd_generator(usid)
            cmd_lst += set_ext_trig_mask_a_cmd_generator(usid)
            cmd_lst += set_ext_trig_mask_b_cmd_generator(usid)
            # Verify default value is correct.
            cmd_lst += extend_read_cmd_generator(adrs_lst[i], usid, dv_lst[i])
            # Write 0xFF to the register.
            cmd_lst += extend_write_cmd_generator(adrs_lst[i], usid, 255)
            # Verify write occured.
            cmd_lst += extend_read_cmd_generator(adrs_lst[i], usid, 255)
            # Clear all trigger masks.
            cmd_lst += rm_pm_trig_msk_cmd_generator(usid)
            cmd_lst += rm_ext_trig_msk_a_cmd_generator(usid)
            cmd_lst += rm_ext_trig_msk_b_cmd_generator(usid)
            # Write 0x00 to the register.
            cmd_lst += extend_write_cmd_generator(adrs_lst[i], usid, 0)
            # Verify write hasnt occurred.
            cmd_lst += extend_read_cmd_generator(adrs_lst[i], usid, 0)
            # Set the clk to top value.
            clk = rffe_dict[f'EXT_TRIG_CNT_{trig}_H']
            cmd_lst += set_clk_top_cmd_gen(usid, clk)
            # Verify clock readback.
            cmd_lst += read_clk_mult_cmd_gen(usid, clk)
            # Verify write has occurred.
            cmd_lst += extend_read_cmd_generator(adrs_lst[i], usid, 0)
    return cmd_lst


def mtrig_test(usid, mgroup_lst, mtrig_dict):
    """
    Test all available mtrig grouped registers.

    Parameters
    ----------
    usid : TYPE
        DESCRIPTION.
    mgroup_lst : TYPE
        DESCRIPTION.

    Returns
    -------
    cmd_lst : TYPE
        DESCRIPTION.

    """
    cmd_lst = []
    if len(mgroup_lst) < 1:
        print('No mappable triggers detected.')
        return cmd_lst
    a = list(set([el[2] for el in mgroup_lst]))
    b = [f'0x{el:02X}' for el in range(255)]
    for t in a:
        if t not in mtrig_dict.keys():
            print(f'No entry for mappable trigger {t[1]} ({t}) was found'
                  ' in mtrig_dict.\nPlease correct the issue and try again.')
            sys.exit(0)
        if mtrig_dict[t]['Reg'] not in b:
            print(f'There is an issue with the Reg field in mtrig_dict for'
                  f' mappable trigger {t[1]} ({t}). {mtrig_dict[t]["Reg"]} is'
                  ' not a valid input.'
                  '\nPlease correct the issue and try again.')
            sys.exit(0)
        if mtrig_dict[t]['U/L'] not in ['U', 'L']:
            print(f'There is an issue with the U/L field in mtrig_dict for')
    for reg in mgroup_lst:
        # Collect the register and mask for the mgroup
        mtrig_reg = mtrig_dict[reg[2]]['Reg']
        mtrig_mask = mtrig_dict[reg[2]]['U/L']
        mtrig_reg = int(mtrig_reg, 16)
        if mtrig_mask == 'L':
            mtrig_mask = 240
        elif mtrig_mask == 'U':
            mtrig_mask = 15
        # Send address change header
        cmd_lst += extend_write_cmd_generator(255, usid, 5)
        for i in range(15):
            # Send mtrig change header
            cmd_lst += extend_write_cmd_generator(255, usid, 6)
            if mtrig_mask == 240:
                val = i
            elif mtrig_mask == 15:
                val = i << 4
            # Change the mtrig group's trigger.
            cmd_lst += msk_wrt_cmd_generator(mtrig_reg, usid, mtrig_mask, val)
            cmd_lst += triggered_write_test(
                usid, [int(reg[0], 16)], [int(reg[1], 16)], mtrig=True)
            cmd_lst += trig_counter_test(
                usid, [int(reg[0], 16)], [int(reg[1], 16)], mtrig=True)
    return cmd_lst


def append_header():
    """
    Append the standard TestStand Sequence header.

    Returns
    -------
    hdr : list
        List of strings containing the standard header.

    """
    hdr = ['#,setup_header,test_system,Manual,,,\n']
    hdr += ['#,setup_header,version,1,,,\n']
    hdr += ['#,MipiVerification,clusters,,,,\n']
    hdr += ['enabled,type,usid,regAddr,writeMask,regWriteData,' +
            'expectedReadData,regWriteArrayItem0,regWriteArrayItem1,' +
            'regWriteArrayItem2,regWriteArrayItem3\n']
    return hdr


def get_trigger_registers(df, mtrig=False):
    """
    Get trigger enabled registers from the wider set.

    Parameters
    ----------
    df : DataFrame
        DataFrame containing the MRD.
    mtrig : Boolean, optional
        Boolean that determines whether mtrig registers are returned.
        The default is False.

    Returns
    -------
    t_lst : list
        List of lists pertaining to individual trigger registers.

    """
    t_lst = df[['Address', 'Value', 'Trig N']
               ][df['Trig N'] != '-'].values.tolist()
    if mtrig:
        t_lst = [el for el in t_lst if el[2]
                 in ['MA', 'MB', 'MC', 'MD', 'ME']]
    else:
        t_lst = [el for el in t_lst if el[2] not
                 in ['MA', 'MB', 'MC', 'MD', 'ME']]
    return t_lst


def get_tbyb_registers(df):
    """
    Get the TBYB registers from the wider set.

    Parameters
    ----------
    df : DataFrame
        DataFrame containing the MRD.

    Returns
    -------
    tbyb_lst : list
        List of lists pertaining to individual TBYB registers.

    """
    tbyb_lst = df.query(
        'ERW == "-" & ERR != "-" & Address > "0xA7"'
        )[['Address', 'Value']].values.tolist()
    return tbyb_lst


def get_register_info(registers):
    """
    Collect address and default value information.

    Parameters
    ----------
    registers : list
        List of lists pertaining to individual registers.

    Returns
    -------
    addresses : list
        List of integers containing the addresses of registers.
    default_values : list
        List of integers containing the default values of registers.

    """
    addresses = [int(el[0], 16) for el in registers]
    default_values = [int(el[1], 16) for el in registers]
    return addresses, default_values


def get_commands(df, mtrig_dict, usid):
    """
    Parse df and generate command sequence for Test Stand sequence.

    Parameters
    ----------
    df : DataFrame
        DataFrame containing the MRD.

    Returns
    -------
    cmd_lst : list
        List of strings containing commands to Test Stand sequence.

    """
    # Collect information from MRD
    trigger_regs = get_trigger_registers(df)
    tbyb_regs = get_tbyb_registers(df)
    mtrig_regs = get_trigger_registers(df, mtrig=True)
    # print(mtrig_regs)
    addresses, default_values = get_register_info(trigger_regs)
    tbyb_addresses, tbyb_default_values = get_register_info(tbyb_regs)
    # Construct command list
    cmd_lst = append_header()
    cmd_lst += triggered_write_test(usid, addresses, default_values)
    cmd_lst += tbyb_test(usid, tbyb_addresses, tbyb_default_values)
    cmd_lst += trig_counter_test(usid, addresses, default_values)
    cmd_lst += mtrig_test(usid, mtrig_regs, mtrig_dict)
    return cmd_lst


def save_commands(cmd_lst, output_file):
    """
    Save the command list to output_file.

    Parameters
    ----------
    cmd_lst : list
        List of strings containing commands to Test Stand sequence.
    output_file : list
        Path of file to save commands in.

    Returns
    -------
    None.

    """
    with open(output_file, 'w') as f:
        f.writelines(cmd_lst)


def psv_save_excel(writer, output_path):
    """
    Save the excel output and use win32 to squash a format bug.

    Parameters
    ----------
    writer : TYPE
        DESCRIPTION.
    output_path : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    import win32com.client

    writer.save()
    xl = win32com.client.DispatchEx("Excel.Application")
    wb = xl.workbooks.open(output_path)
    xl.Visible = False
    wb.Close(SaveChanges=1)
    xl.Quit()


def process_tbyb(df, trig_reg_ddict):
    """
    Process the TBYB df to generate result list.

    Parameters
    ----------
    df : pandas dataframe
        Contains all TBYB tests.

    Returns
    -------
    res_dict : dict of results
        Dictionary containing result of all TBYB tests.

    """
    # Get indices of test starts.
    indices = df.query('Address == 255 & Write == 2').index.tolist()
    adrs_offset = 5
    dv_offset = 5
    dv2_offset = 7
    nv1_offset = 10
    nv2_offset = 12
    fv_offset = 15
    res_list = []
    for idx in indices:
        res_dict = {}
        adrs = int(df['Address'].iloc[idx + adrs_offset])
        adrs = f'Reg0x{adrs:02X}'
        res_dict['Address'] = adrs
        dv = int(df['Read'].iloc[idx + dv_offset])
        dv2 = int(df['Read'].iloc[idx + dv2_offset])
        nv1 = int(df['Read'].iloc[idx + nv1_offset])
        nv2 = int(df['Read'].iloc[idx + nv2_offset])
        fv = int(df['Read'].iloc[idx + fv_offset])
        check1 = dv == dv2
        check2 = nv1 != dv
        check3 = nv2 != dv
        check4 = fv == nv2
        if all([check1, any([check2, check3]), check4]):
            res_dict['TBYB Result'] = 'O'
        else:
            res_dict['TBYB Result'] = '---'
        res_list += [res_dict]
    res_df = pd.DataFrame(res_list)
    debug_df = pd.DataFrame(res_list)
    return debug_df, res_df


def process_counters(df, trig_reg_ddict, mtrig=False):
    """
    Process the Counter df to generate result list.

    Each test frame begins with a write of 0x03 to Reg0xFF.
    The test frame will contain the results of each counter
    register on the register address associated with the test frame.

    Parameters
    ----------
    df : pandas dataframe
        Contains all Counter test frames.

    Returns
    -------
    debug_df : pandas dataframe
        Dataframe containing result of timed trigger tests
        with debug information.

    result_df: pandas dataframe
        Dataframe containing condensed result of timed trigger tests.

    """
    # mtrig trigger test cant reset so we need to change the offset.
    # If not mtrig, add 1
    mtrig = int(not mtrig)
    # Get indices of test frame starts.
    indices = df.query('Address == 255 & Write == 3').index.tolist()
    indices += [len(df)]
    adrs_offset = 5 + mtrig
    # dv_offset = 4 + mtrig      Works but unnecessary.
    nv1_offset = 6 + mtrig
    nv2_offset = 11 + mtrig
    count_offset = 13 + mtrig
    fv_offset = 29 + mtrig
    debug_dicts = []
    result_dicts = []
    for i in range(len(indices)-1):
        sub_df = df.iloc[indices[i]:indices[i+1]]
        sub_indices = sub_df.query(
            'Address == 255 & Write == 4').index.tolist()
        # get the address
        adrs = sub_df['Address'].loc[indices[i] + adrs_offset]
        adrs = f"0x{adrs:02X}"
        for sub_idx in sub_indices:
            tmp_dict = {'Register Address': adrs}
            # get the dv Works but unneccesary.
            # dv = sub_df['Read'].loc[sub_idx + dv_offset]
            # get the first new value
            nv1 = sub_df['Read'].loc[sub_idx + nv1_offset]
            # get the second new value
            nv2 = sub_df['Read'].loc[sub_idx + nv2_offset]
            # get the trigger counter register
            count_reg = sub_df['Address'].loc[sub_idx + count_offset]
            # get the count pass fail value
            c = sub_df['Read'].loc[
                sub_idx + count_offset:sub_idx + count_offset + 15
                ].values.tolist()
            c_chk = sub_df['Pass'].loc[
                sub_idx + count_offset:sub_idx + count_offset + 15]
            c_chk = all(c_chk)
            # get final value
            fv = sub_df['Read'].loc[sub_idx + fv_offset]
            fv = int(fv)
            # Check 1: Verify nv1 not 0
            chk1 = nv1 != 0
            # Check 2: Verify nv2 == nv1
            chk2 = nv2 == nv1
            # Check 3: Verify final value == 0
            chk3 = fv == 0
            count_reg = trig_reg_ddict[f'0x{count_reg:02X}']
            tmp_dict['Trigger Register'] = count_reg
            tmp_dict['Counter Test'] = 'O' if c_chk else '---'
            tmp_dict['Trigger Test'] = 'O' if all([chk1, chk2, chk3]) \
                else '---'
            debug_string = count_reg + ':\t'
            if chk1:
                debug_string += ""
            else:
                debug_string += "Write failed with all triggers unmasked.\t"
            if chk2:
                debug_string += ""
            else:
                debug_string += "Write occurred with all triggers masked.\t"
            if chk3:
                debug_string += ""
            else:
                debug_string += f"Final value of 0x{fv:02X}" + \
                    " is unexpected with write value of 0x00\t"
            if c_chk:
                debug_string += ''
            else:
                debug_string += 'Count failure. Count reads: '
                debug_string += '; '.join([f'0x{int(el):02X}' for el in c])
            tmp_dict['Debug'] = debug_string
            debug_dicts += [tmp_dict]
    debug_df = pd.DataFrame(debug_dicts)
    addresses = list(set(debug_df['Register Address'].values.tolist()))
    addresses.sort()
    for adrs in addresses:
        success_tc = debug_df.query(
            '`Register Address` == ' + f'"{adrs}"' +
            ' & `Trigger Test` == "O"'
                                    ).index.tolist()
        success_tc = debug_df['Trigger Register'].loc[
            success_tc].values.tolist()
        success_cnt = debug_df.query(
            '`Register Address` == ' + f'"{adrs}"' +
            ' & `Counter Test` == "O"'
                                    ).index.tolist()
        success_cnt = debug_df['Trigger Register'
                               ].loc[success_cnt].values.tolist()
        result_dicts += [{'Register Address': adrs,
                          'Successful Timed Triggers': '; '.join(success_tc),
                          'Successful Counter Readback': '; '.join(success_cnt)
                          }]
    result_df = pd.DataFrame(result_dicts)
    return debug_df, result_df


def process_triggers(df, trig_reg_ddict, mtrig=False):
    """
    Process the trigger df to generate result list.

    Each test frame begins with a write of 0x00 to Reg0xFF.
    The test frame will contain the results of each trigger
    register on the register address associated with the test frame.

    Parameters
    ----------
    df : pandas dataframe
        Contains all trigger test frames.

    Returns
    -------
    debug_df : pandas dataframe
        Dataframe containing result of trigger tests with debug information.

    result_df: pandas dataframe
        Dataframe containing condensed result of trigger tests.

    """
    # Get indices of test frame starts.
    indices = df.query('Address == 255 & Write == 0').index.tolist()
    indices += [len(df)]
    # mtrig trigger test cant reset so we need to change the offset.
    # If not mtrig, add 1
    mtrig = int(not mtrig)
    adrs_offset = 5 + mtrig
    # Default value works but is unnecessary
    # dv_offset = 5
    nv1_offset = 6 + mtrig
    nv2_offset = 11 + mtrig
    trig_offset = 12 + mtrig
    fv_offset = 13 + mtrig
    debug_dicts = []
    result_dicts = []
    for i in range(len(indices)-1):
        sub_df = df.iloc[indices[i]:indices[i+1]]
        sub_indices = sub_df.query(
            'Address == 255 & Write == 1').index.tolist()
        # get the address
        adrs = sub_df['Address'].loc[indices[i] + adrs_offset]
        adrs = f"0x{adrs:02X}"
        for sub_idx in sub_indices:
            tmp_dict = {'Register Address': adrs}
            # get the dv
            # Default value works but is unnecessary
            # dv = sub_df['Read'].loc[sub_idx + dv_offset]
            # get the first new value
            nv1 = sub_df['Read'].loc[sub_idx + nv1_offset]
            # get the second new value
            nv2 = sub_df['Read'].loc[sub_idx + nv2_offset]
            # get the trigger register
            trig_reg = sub_df['Address'].loc[sub_idx + trig_offset]
            trig_reg = f'0x{int(trig_reg):02X}'
            # get the trig value
            trig_val = sub_df['Write'].loc[sub_idx + trig_offset]
            trig_val = f'0x{int(trig_val):02X}'
            # get the trig from the register and value
            trig = trig_reg_ddict[trig_reg][trig_val]
            # get final value
            fv = sub_df['Read'].loc[sub_idx + fv_offset]
            fv = int(fv)
            # Check 1: Verify nv1 not 0
            chk1 = nv1 != 0
            # Check 2: Verify nv2 == nv1
            chk2 = nv2 == nv1
            # Check 3: Verify final value == 0
            chk3 = fv == 0
            tmp_dict['Trigger Register'] = trig
            tmp_dict['Trigger Test'] = 'O' if all([chk1, chk2, chk3]) \
                else '---'
            debug_string = trig_reg + ':\t'
            if chk1:
                debug_string += ""
            else:
                debug_string += "Write failed with all triggers unmasked.\t"
            if chk2:
                debug_string += ""
            else:
                debug_string += "Write occurred with all triggers masked.\t"
            if chk3:
                debug_string += ""
            else:
                debug_string += f"Final value of 0x{fv:02X}" + \
                    " is unexpected with write value of 0x00\t"
            tmp_dict['Debug'] = debug_string
            debug_dicts += [tmp_dict]
    debug_df = pd.DataFrame(debug_dicts)
    addresses = list(set(debug_df['Register Address'].values.tolist()))
    addresses.sort()
    for adrs in addresses:
        success_tc = debug_df.query(
            '`Register Address` == ' + f'"{adrs}"' +
            ' & `Trigger Test` == "O"'
                                    ).index.tolist()
        success_tc = debug_df['Trigger Register'].loc[
            success_tc].values.tolist()
        result_dicts += [{'Register Address': adrs,
                          'Successful Triggers': '; '.join(success_tc)}]
    result_df = pd.DataFrame(result_dicts)
    return debug_df, result_df


def process_mtrigs(df, trig_reg_ddict):
    """
    Process the mtrig df to generate result list.

    Each test frame begins with a write of 0x05 to Reg0xFF.
    The test frame will contain the results of each trigger
    register and trigger counter on the register address associated
    with the test frame.

    Parameters
    ----------
    df : pandas dataframe
        Contains all mtrig test frames.

    Returns
    -------
    debug_df : pandas dataframe
        Dataframe containing result of mtrig tests with debug information.

    result_df: pandas dataframe
        Dataframe containing condensed result of mtrig tests.

    """
    # Get indices of test frame starts.
    indices = df.query('Address == 255 & Write == 5').index.tolist()
    indices += [len(df)]
    # Offsets referenced from indices
    adrs_offset = 8
    mtrig_offset = 2
    # Offsets referenced from sub_indices
    setting_offset = -1
    result_list = []
    debug_list = []
    for i in range(len(indices)-1):
        # Split off an mtrig frame
        # get the address
        adrs = df['Address'].loc[indices[i] + adrs_offset]
        adrs = f"0x{adrs:02X}"
        mtrig_adrs = df['Address'].loc[indices[i] + mtrig_offset]
        mtrig_adrs = f"0x{mtrig_adrs:02X}"
        msk = df['Mask'].loc[indices[i] + mtrig_offset]
        msk = f"0x{int(msk):02X}"
        mtrig_grp = trig_reg_ddict[mtrig_adrs][msk]
        # Get indices of each mtrig setting.
        sub_indices = df.iloc[indices[i]:indices[i+1]].query(
            'Address == 255 & Write == 6').index.tolist()
        sub_indices = [el+2 for el in sub_indices]
        sub_indices += [indices[i+1]]
        for j in range(len(sub_indices)-1):
            setting = df['Write'].loc[sub_indices[j] + setting_offset]
            if msk == '0xF0':
                setting = int(setting)
            else:
                setting = int(setting) >> 4
            setting = trig_reg_ddict['mtrig'][f'0x{setting:02X}']
            # print(df.iloc[sub_indices[j]:sub_indices[j+1]])
            trig_res_debug_df, trig_res_df = process_triggers(
                df.iloc[sub_indices[j]:sub_indices[j+1]
                        ].reset_index(drop=True), trig_reg_ddict, mtrig=True)
            tt_res_debug_df, tt_res_df = process_counters(
                df.iloc[sub_indices[j]:sub_indices[j+1]
                        ].reset_index(drop=True), trig_reg_ddict, mtrig=True)
            success_trigs = trig_res_df[
                'Successful Triggers'].values.tolist()[0]
            success_ttrigs = tt_res_df[
                'Successful Timed Triggers'].values.tolist()[0]
            success_count = tt_res_df[
                'Successful Counter Readback'].values.tolist()[0]
            tmp_dict = {'Register Address': adrs,
                        'mTrig Group': mtrig_grp,
                        'mTrig Setting': setting,
                        'Successful Triggers': success_trigs,
                        'Successful Timed Triggers': success_ttrigs,
                        'Successful Counter Readback': success_count}
            result_list += [tmp_dict]
            # Need to add mTrig group and mTrig setting
            trig_res_debug_df['mTrig Group'] = mtrig_grp
            tt_res_debug_df['mTrig Group'] = mtrig_grp
            trig_res_debug_df['mTrig Setting'] = setting
            tt_res_debug_df['mTrig Setting'] = setting
            trig_res_debug_df['Test Name'] = 'Trigger'
            tt_res_debug_df['Test Name'] = 'Timed Trigger'
            debug_list += [trig_res_debug_df]
            debug_list += [tt_res_debug_df]
    debug_df = pd.concat(debug_list, ignore_index=True, sort=False)
    debug_df = debug_df[['Register Address',
                         'mTrig Group',
                         'mTrig Setting',
                         'Trigger Register',
                         'Trigger Test',
                         'Counter Test',
                         'Debug',
                         'Test Name']]
    result_df = pd.DataFrame(result_list)
    # print(result_df)
    return debug_df, result_df


def psv_loadwriter(src_template_path, output_path):
    """
    Load the excel writer.

    Parameters
    ----------
    src_template_path : string
        Path to the excel template.
    output_path : string
        Path to which the output will be written.

    Returns
    -------
    writer : ExcelWriter object
        ExcelWriter object facilitates the writing of Excel documents.

    """
    from shutil import copyfile
    from openpyxl import load_workbook

    copyfile(src_template_path, output_path)
    writer = pd.ExcelWriter(output_path, engine='openpyxl')
    book = load_workbook(output_path)
    writer.book = book
    writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
    return writer


def psv_loadfile(input_file):
    """
    Load and condition the result of TestStand sequence.

    Parameters
    ----------
    input_file : string
        Path to the csv file containing the test results.

    Returns
    -------
    df : Pandas DataFrame
        Dataframe containing the conditioned output.

    """
    header_dict = {' COND_TYPE': 'Type',
                   ' COND_REG_ADDR': 'Address',
                   ' COND_WRITE_MASK': 'Mask',
                   ' COND_WRITE_DATA': 'Write',
                   ' COND_EXPECTED_DATA': 'Expected',
                   ' MEAS_READ_DATA': 'Read',
                   ' MEAS_PARITY_OK': 'Parity',
                   ' MEAS_PASS': 'Pass'}
    df = pd.read_csv(input_file, header=8,
                     usecols=[' COND_TYPE',
                              ' COND_REG_ADDR',
                              ' COND_WRITE_MASK',
                              ' COND_WRITE_DATA',
                              ' COND_EXPECTED_DATA',
                              ' MEAS_READ_DATA',
                              ' MEAS_PARITY_OK',
                              ' MEAS_PASS'])
    df = df.rename(mapper=header_dict, axis=1)
    return df


def psv_processfile(result_df, writer, trig_reg_ddict, rsa_file, mrd_file):
    """
    Process the results.

    Parameters
    ----------
    result_df : DataFrame
        Dataframe containing the conditioned test result.
    writer : ExcelWriter
        Writer used to write to the Excel Sheets.
    trig_reg_ddict : Dictionary
        Multlevel dictionary containing register information.
    rsa_file : string
        Path to Register Status Analyzer output csv.
    mrd_file : string
        Path to Machine Readable PRD csv.

    Returns
    -------
    None.

    """
    from copy import deepcopy

    df_dict = {'Trigger Test': {'Query': 'Address == 255 & Write == 0',
                                'Function': process_triggers,
                                'input DF': pd.DataFrame([]),
                                'Debug DF': pd.DataFrame([]),
                                'Result DF': pd.DataFrame([])},
               'Timed Trigger Test': {'Query': 'Address == 255 & Write == 3',
                                      'Function': process_counters,
                                      'input DF': pd.DataFrame([]),
                                      'Debug DF': pd.DataFrame([]),
                                      'Result DF': pd.DataFrame([])},
               'TBYB Test': {'Query': 'Address == 255 & Write == 2',
                             'Function': process_tbyb,
                             'input DF': pd.DataFrame([]),
                             'Debug DF': pd.DataFrame([]),
                             'Result DF': pd.DataFrame([])},
               'mTrig Test': {'Query': 'Address == 255 & Write == 5',
                              'Function': process_mtrigs,
                              'input DF': pd.DataFrame([]),
                              'Debug DF': pd.DataFrame([]),
                              'Result DF': pd.DataFrame([])}}
    test_list = ['mTrig Test', 'Timed Trigger Test',
                 'TBYB Test', 'Trigger Test']

    for k in test_list:
        index = result_df.query(df_dict[k]['Query']).head(n=1)
        if len(index) > 0:
            index = index.index.tolist()[0]
            df_dict[k]['input DF'] = deepcopy(result_df.iloc[index:])
            df_dict[k]['input DF'].reset_index(drop=True, inplace=True)
            result_df = result_df.truncate(after=index-1)
            df_dict[k]['Debug DF'], df_dict[k]['Result DF'] = df_dict[
                k]['Function'](df_dict[k]['input DF'], trig_reg_ddict)
            df_dict[k]['Result DF'].to_excel(writer, sheet_name=k, index=False)
            if k != 'TBYB Test':
                df_dict[k]['Debug DF'].to_excel(writer,
                                                sheet_name=k + ' Debug',
                                                index=False)
    rsa = pd.read_csv(rsa_file)
    rsa.rename(columns={'Unnamed: 0': 'Address'}, inplace=True)
    mrd = pd.read_csv(mrd_file)
    rsa.to_excel(writer, sheet_name='RSA', index=False)
    mrd.to_excel(writer, sheet_name='MR-PRD', index=False)
