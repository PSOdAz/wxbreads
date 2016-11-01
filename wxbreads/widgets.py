#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
import wx
import wx.richtext as rt
import wx.lib.dialogs
try:
    from agw import genericmessagedialog as gmd
except ImportError:
    import wx.lib.agw.genericmessagedialog as gmd

try:
    import agw.flatnotebook as fnb
except ImportError:
    import wx.lib.agw.flatnotebook as fnb

import wx.lib.masked as masked
import wxbreads.utils as wxu
import windbreads.utils as wdu

'''Remark:
fsize/fstyle: 1st widget size/style
ssize/sstyle: 2nd widget size/sstyle
tsize/tstyle: 3rd widget size/tstyle
'''

ICONS = dict(info=wx.ICON_INFORMATION,
             i=wx.ICON_INFORMATION,
             warn=wx.ICON_WARNING,
             warning=wx.ICON_WARNING,
             w=wx.ICON_WARNING,
             error=wx.ICON_ERROR,
             e=wx.ICON_ERROR,
             question=wx.ICON_QUESTION,
             q=wx.ICON_QUESTION,
             exclamation=wx.ICON_EXCLAMATION,
             ex=wx.ICON_EXCLAMATION,
             )
DEFAULT_WILDCARD = 'All files|*'
HIGHLIGHT_RED = '#F75D59'


def set_tooltip(wgt, tooltip='', t=None):
    if tooltip:
        wgt.SetToolTipString(wdu.ttt(tooltip, t=t))


def set_fg(wgt, fg=None):
    if fg:
        wgt.SetForegroundColour(fg)


def set_bg(wgt, bg=None):
    if bg:
        wgt.SetBackgroundColour(bg)


def set_font(wgt, font=None):
    if font:
        wgt.SetFont(font)


def popup(parent=None, caption='caption', **kwargs):
    t = kwargs.get('t')
    btn = kwargs.pop('btn', wx.OK)
    need_return = kwargs.pop('need_return', False)
    size = kwargs.pop('size', (-1, -1))
    icon = kwargs.pop('icon', 'i')
    msg = kwargs.pop('msg', '')
    icon = ICONS.get(icon, ICONS['i'])
    if isinstance(msg, basestring):
        if not isinstance(msg, unicode):
            umsg = msg.decode(wdu.detect_encoding(msg)['encoding'])
        else:
            umsg = msg

    else:
        umsg = '{}'.format(msg)

    if t:
        umsg = wdu.ttt(umsg, t)
        title = wdu.ttt(caption, t)
    else:
        title = caption

    dlg = gmd.GenericMessageDialog(parent, umsg, title, btn | icon, size=size)
    help_label = kwargs.get('help_label', 'Help')
    ok_label = kwargs.get('ok_label', 'OK')
    cancel_label = kwargs.get('cancel_label', 'Cancel')
    yes_label = kwargs.get('yes_label', 'Yes')
    no_label = kwargs.get('no_label', 'No')
    if t:
        help_label = wdu.ttt(help_label, t)
        ok_label = wdu.ttt(ok_label, t)
        cancel_label = wdu.ttt(cancel_label, t)
        yes_label = wdu.ttt(yes_label, t)
        no_label = wdu.ttt(no_label, t)

    dlg.SetHelpLabel(help_label)
    dlg.SetOKLabel(ok_label)
    dlg.SetOKCancelLabels(ok_label, cancel_label)
    dlg.SetYesNoLabels(yes_label, no_label)
    dlg.SetYesNoCancelLabels(yes_label, no_label, cancel_label)
    dlg.SetMessage(umsg)

    if need_return:
        return dlg

    dlg.CenterOnParent()
    result = dlg.ShowModal()
    dlg.Destroy()
    return result


def popup_smd(parent=None, msg='', caption='Message', **kwargs):
    t = kwargs.get('t')
    btn_label = kwargs.get('btn_label', 'OK')
    if isinstance(msg, basestring):
        if not isinstance(msg, unicode):
            umsg = msg.decode(wdu.detect_encoding(msg)['encoding'])
        else:
            umsg = msg

    else:
        umsg = '{}'.format(msg)

    if t:
        btn_label = wdu.ttt(btn_label, t)
        umsg = wdu.ttt(umsg, t)
        title = wdu.ttt(caption, t)
    else:
        title = caption

    dlg = wx.lib.dialogs.ScrolledMessageDialog(parent, umsg, title)
    try:
        dlg.GetChildren()[1].SetLabel(btn_label)
    except:
        pass

    dlg.ShowModal()
    dlg.Destroy()


def add_button(parent, id=-1, **kwargs):
    t = kwargs.pop('t', None)
    label = kwargs.pop('label', 'Button')
    size = kwargs.pop('size', (-1, -1))
    tooltip = kwargs.pop('tooltip', '')
    font = kwargs.pop('font', None)
    fg = kwargs.pop('fg', None)
    bg = kwargs.pop('bg', None)
    icon = kwargs.pop('icon', None)
    style = kwargs.pop('style', wx.NO_BORDER)
    btn = wx.Button(parent, id, wdu.ttt(label, t), size=size,
                    name=kwargs.get('name', 'wxButton'), style=style)
    set_tooltip(btn, tooltip, t=t)
    set_font(btn, font)
    set_fg(btn, fg)
    set_bg(btn, bg)
    if icon:
        btn.SetBitmap(icon, kwargs.get('side', wx.LEFT))
        btn.SetBitmapMargins(kwargs.get('margins', (2, 2)))

    return btn


def add_label(parent, id=-1, **kwargs):
    t = kwargs.get('t')
    label = kwargs.pop('label', '')
    font = kwargs.pop('font', None)
    size = kwargs.pop('size', (-1, -1))
    tooltip = kwargs.pop('tooltip', '')
    fg = kwargs.pop('fg', None)
    bg = kwargs.pop('bg', None)
    style = kwargs.pop('style', None)
    nargs = dict(size=size, name=kwargs.get('name', 'wxStaticText'))
    if style:
        nargs.update(style=style)

    lbl = wx.StaticText(parent, id, wdu.ttt(label, t), **nargs)
    set_tooltip(lbl, tooltip, t)
    set_font(lbl, font)
    set_fg(lbl, fg)
    set_bg(lbl, bg)

    return lbl


def add_textctrl(parent, id=-1, **kwargs):
    t = kwargs.pop('t', None)
    value = kwargs.pop('value', '')
    size = kwargs.pop('size', (-1, -1))
    style = kwargs.pop('style', None)
    fg = kwargs.pop('fg', None)
    bg = kwargs.pop('bg', None)
    font = kwargs.pop('font', None)
    tooltip = kwargs.pop('tooltip', '')
    multiline = kwargs.pop('multiline', False)

    nargs = dict(size=size, name=kwargs.get('name', 'wxTextCtrl'))
    sty = wx.TE_MULTILINE if multiline else None
    if style and sty is not None:
        nargs.update(style=style | sty)
    elif style:
        nargs.update(style=style)
    elif sty is not None:
        nargs.update(style=sty)

    wgt = wx.TextCtrl(parent, id, '{}'.format(value), **nargs)
    set_tooltip(wgt, tooltip, t)
    set_font(wgt, font)
    set_fg(wgt, fg)
    set_bg(wgt, bg)
    return wgt


def add_spinctrl(parent, id=-1, **kwargs):
    value = kwargs.pop('value', '')
    size = kwargs.pop('size', (-1, -1))
    min_value = kwargs.pop('min_value', 0)
    max_value = kwargs.pop('max_value', 100)
    init_value = kwargs.pop('init_value', 0)
    tooltip = kwargs.pop('tooltip', '')
    t = kwargs.pop('t', None)

    sc = wx.SpinCtrl(parent, id, value, size=size,
                     name=kwargs.pop('name', 'wxSpinCtrl'))
    sc.SetRange(min_value, max_value)
    sc.SetValue(init_value)
    set_tooltip(sc, tooltip, t)
    return sc


def add_spinctrl_double(parent, id=-1, **kwargs):
    value = kwargs.pop('value', '')
    size = kwargs.pop('size', (-1, -1))
    inc = kwargs.pop('inc', 1)
    min_value = kwargs.pop('min_value', 0.0)
    max_value = kwargs.pop('max_value', 100.0)
    init_value = kwargs.pop('init_value', 0)
    sc = wx.SpinCtrlDouble(parent, id, value, size=size, inc=inc,
                           name=kwargs.pop('name', 'wxSpinCtrlDouble'))
    sc.SetRange(min_value, max_value)
    sc.SetValue(init_value)
    return sc


def add_richtext(parent, id=-1, **kwargs):
    value = kwargs.pop('value', '')
    size = kwargs.pop('size', (-1, -1))
    readonly = kwargs.pop('readonly', True)
    style = kwargs.pop('style', wx.TE_MULTILINE)
    fg = kwargs.pop('fg', None)
    bg = kwargs.pop('bg', None)
    font = kwargs.pop('font', None)
    if readonly:
        style |= wx.TE_READONLY

    kw = dict(size=size, name=kwargs.pop('name', 'wxRichText'), style=style)
    rtc = rt.RichTextCtrl(parent, id, value, **kw)
    set_font(rtc, font)
    set_fg(rtc, fg)
    set_bg(rtc, bg)
    return rtc


def add_checkbox(parent, id=-1, **kwargs):
    t = kwargs.pop('t', None)
    label = kwargs.pop('label', '')
    size = kwargs.pop('size', (-1, -1))
    value = kwargs.pop('value', True)
    font = kwargs.pop('font', None)
    tooltip = kwargs.pop('tooltip', '')
    fg = kwargs.pop('fg', None)
    bg = kwargs.pop('bg', None)
    wgt = wx.CheckBox(parent, id, wdu.ttt(label, t), size=size,
                      name=kwargs.pop('name', 'wxCheckBox'))
    set_tooltip(wgt, tooltip, t)
    set_font(wgt, font)
    set_fg(wgt, fg)
    set_bg(wgt, bg)
    wgt.SetValue(value)
    return wgt


def add_path_picker(parent, id=-1, msg='Select a directory', **kwargs):
    t = kwargs.pop('t', None)
    kind = kwargs.pop('kind', 'dir')
    tooltip = kwargs.pop('tooltip', '')
    multiline = kwargs.pop('multiline', False)
    btn_label = kwargs.pop('btn_label', '')
    size = kwargs.pop('size', (-1, -1))
    prop = kwargs.pop('prop', 2)
    use_tc = kwargs.pop('use_tc', True)
    value = kwargs.pop('value', '')
    text_editable = kwargs.pop('text_editable', False)
    btn_enable = kwargs.pop('btn_enable', True)
    tc_bg = kwargs.pop('tc_bg', 'white')
    tc_name = kwargs.pop('tc_name', 'wxTextCtrl')
    btn_name = kwargs.pop('btn_name', 'wxButton')
    wgt_cls = wx.DirPickerCtrl if kind == 'dir' else wx.FilePickerCtrl
    if use_tc:
        kwargs.update(style=wx.DIRP_USE_TEXTCTRL)

    pc = wgt_cls(parent, id, message=wdu.ttt(msg, t), size=size, path=value,
                 name=kwargs.pop('name', 'wxDirPickerCtrl'), **kwargs)
    if pc.HasTextCtrl():
        pc.SetTextCtrlProportion(prop)

    tc, btn = pc.Sizer.GetChildren()
    tc = tc.GetWindow()
    btn = btn.GetWindow()
    if multiline:
        tc.SetWindowStyle(wx.TE_MULTILINE)

    btn.SetLabel(wdu.ttt(btn_label or btn.GetLabel(), t))
    if tooltip:
        tooltip = wdu.ttt(tooltip, t)
        set_tooltip(tc, tooltip)
        set_tooltip(btn, tooltip)

    tc.SetEditable(text_editable)
    set_bg(tc, tc_bg)

    btn.Enable(btn_enable)
    tc.SetName(tc_name)
    btn.SetName(btn_name)
    return pc, tc, btn


def add_dir_picker(parent, id=-1, msg='Select a directory', **kwargs):
    kwargs.setdefault('name', 'wxDirPickerCtrl')
    return add_path_picker(parent, id, kind='dir', msg=msg, **kwargs)


def add_file_picker(parent, id=-1, msg='Select a file', **kwargs):
    kwargs.setdefault('name', 'wxFilePickerCtrl')
    return add_path_picker(parent, id, kind='file', msg=msg, **kwargs)


def select_open_dir(parent, title='Select a directory', **kwargs):
    t = kwargs.pop('t', None)
    style = kwargs.pop('style', wx.DD_DEFAULT_STYLE)
    dlg = wx.DirDialog(parent, wdu.ttt(title, t), style=style, **kwargs)
    folder = dlg.GetPath() if dlg.ShowModal() == wx.ID_OK else None
    dlg.Destroy()
    return folder


def select_open_file(parent, msg='Select a file', **kwargs):
    wildcard = kwargs.pop('wildcard', DEFAULT_WILDCARD)
    style = kwargs.pop('style', wx.OPEN)
    multi = kwargs.pop('multi', False)
    if multi:
        style |= wx.MULTIPLE

    if kwargs.pop('exist', True):
        style |= wx.FILE_MUST_EXIST

    if kwargs.pop('change_dir', False):
        style |= wx.CHANGE_DIR

    t = kwargs.pop('t', None)
    dlg = wx.FileDialog(parent, message=wdu.ttt(msg, t),
                        defaultDir=kwargs.pop('default_dir', ''),
                        defaultFile=kwargs.pop('default_file', ''),
                        wildcard=wdu.ttt(wildcard, t),
                        style=style, name=kwargs.pop('name', 'wxFileDialog'),
                        **kwargs)

    paths = dlg.GetPaths() if dlg.ShowModal() == wx.ID_OK else []
    dlg.Destroy()
    if paths:
        return paths if multi else paths[0]

    return None


def select_save_file(parent, msg='Save file as...', **kwargs):
    wildcard = kwargs.pop('wildcard', DEFAULT_WILDCARD)
    style = kwargs.pop('style', wx.SAVE)
    if kwargs.pop('overwrite_prompt', True):
        style |= wx.OVERWRITE_PROMPT

    if kwargs.pop('change_dir', False):
        style |= wx.CHANGE_DIR

    t = kwargs.pop('t', None)
    dlg = wx.FileDialog(parent, message=wdu.ttt(msg, t),
                        defaultDir=kwargs.pop('default_dir', ''),
                        defaultFile=kwargs.pop('default_file', ''),
                        wildcard=wdu.ttt(wildcard, t),
                        style=style, **kwargs)
    path = dlg.GetPath() if dlg.ShowModal() == wx.ID_OK else None
    dlg.Destroy()
    return path


def add_staticbox(parent, id=-1, label='', orient='v', **kwargs):
    sbox = wx.StaticBox(parent, id, wdu.ttt(label, kwargs.pop('t', None)),
                        name=kwargs.pop('name', 'wxStaticBox'))
    style = wx.VERTICAL if orient == 'v' else wx.HORIZONTAL
    sbsizer = wx.StaticBoxSizer(sbox, style)
    return sbox, sbsizer


def add_text_row(parent, sizer=None, **kwargs):
    t = kwargs.pop('t', None)
    label = kwargs.pop('label', '')
    fsize = kwargs.pop('fsize', (-1, -1))
    ssize = kwargs.pop('ssize', (-1, -1))
    value = kwargs.pop('value', '')
    fg = kwargs.pop('fg', None)
    bg = kwargs.pop('bg', None)
    font = kwargs.pop('font', None)
    tooltip = kwargs.pop('tooltip', '')
    multiline = kwargs.pop('multiline', False)

    nargs = dict(tooltip=tooltip, font=font, fg=fg, bg=bg, t=t)
    lbl = add_label(parent, label=label, size=fsize,
                    style=kwargs.pop('fstyle', None),
                    name=kwargs.pop('fname', 'wxStaticText'), **nargs)
    wgt = add_textctrl(parent, value=value, multiline=multiline,
                       style=kwargs.pop('sstyle', None), size=ssize,
                       name=kwargs.pop('sname', 'wxTextCtrl'), **nargs)
    quick_pack(sizer, wgts=[lbl, wgt], **kwargs)

    return lbl, wgt


def add_checkbox_row(parent, sizer=None, **kwargs):
    t = kwargs.pop('t', None)
    label = kwargs.pop('label', '')
    cb_label = kwargs.pop('cb_label', '')
    fsize = kwargs.pop('fsize', (-1, -1))
    ssize = kwargs.pop('ssize', (-1, -1))
    value = kwargs.pop('value', True)
    fg = kwargs.pop('fg', None)
    bg = kwargs.pop('bg', None)
    font = kwargs.pop('font', None)
    tooltip = kwargs.pop('tooltip', '')

    nargs = dict(tooltip=tooltip, font=font, fg=fg, bg=bg, t=t)
    lbl = add_label(parent, label=label, size=fsize,
                    name=kwargs.pop('fname', 'wxStaticText'), **nargs)
    wgt = add_checkbox(parent, label=cb_label, value=value, size=ssize,
                       name=kwargs.pop('sname', 'wxCheckBox'), **nargs)
    quick_pack(sizer, wgts=[lbl, wgt], **kwargs)

    return lbl, wgt


def add_combobox(parent, sizer=None, **kwargs):
    t = kwargs.pop('t', None)
    label = kwargs.pop('label', '')
    fsize = kwargs.pop('fsize', (-1, -1))
    ssize = kwargs.pop('ssize', (-1, -1))
    fstyle = kwargs.pop('fstyle', None)
    sstyle = kwargs.pop('sstyle', wx.CB_DROPDOWN | wx.CB_SORT)
    fg = kwargs.pop('fg', None)
    font = kwargs.pop('font', None)
    value = kwargs.pop('value', '')
    choices = kwargs.pop('choices', [])
    readonly = kwargs.pop('readonly', False)
    tooltip = kwargs.pop('tooltip', '')
    if readonly and sstyle:
        sstyle = sstyle | wx.CB_READONLY

    lbl = None
    if label is not None:
        lbl = add_label(parent, label=label, size=fsize, font=font, fg=fg,
                        style=fstyle, t=t,
                        name=kwargs.pop('fname', 'wxStaticText'))

    wgt = wx.ComboBox(parent, -1, '{}'.format(value), choices=choices,
                      size=ssize, style=sstyle,
                      name=kwargs.pop('sname', 'wxComboBox'))
    set_tooltip(wgt, tooltip, t=t)
    quick_pack(sizer, wgts=[lbl, wgt], **kwargs)
    return lbl, wgt


def add_choice(parent, sizer=None, **kwargs):
    t = kwargs.pop('t', None)
    label = kwargs.pop('label', '')
    fsize = kwargs.pop('fsize', (-1, -1))
    ssize = kwargs.pop('ssize', (-1, -1))
    fstyle = kwargs.pop('fstyle', None)
    fg = kwargs.pop('fg', None)
    font = kwargs.pop('font', None)
    value = kwargs.pop('value', '')
    choices = kwargs.pop('choices', [])
    tooltip = kwargs.pop('tooltip', '')
    lbl = None
    if label is not None:
        lbl = add_label(parent, label=label, size=fsize, font=font, fg=fg,
                        style=fstyle, t=t,
                        name=kwargs.pop('fname', 'wxStaticText'))

    wgt = wx.Choice(parent, -1, choices=choices, size=ssize,
                    name=kwargs.pop('sname', 'wxChoice'))
    wgt.SetSelection(choices.index(value) if value in choices else 0)
    set_tooltip(wgt, tooltip, t)
    wgts = [lbl, wgt] if lbl else [wgt]
    quick_pack(sizer, wgts=wgts, **kwargs)

    return lbl, wgt


def add_radio_box(parent, sizer=None, **kwargs):
    t = kwargs.pop('t', None)
    label = kwargs.pop('label', '')
    size = kwargs.pop('size', (-1, -1))
    style = kwargs.pop('style', wx.RA_SPECIFY_COLS)
    choices = kwargs.pop('choices', [])
    cols = kwargs.pop('cols', 0)
    tooltip = kwargs.pop('tooltip', '')
    value = kwargs.pop('value', 0)
    wgt = wx.RadioBox(parent, -1, wdu.ttt(label, t), size=size,
                      choices=choices, majorDimension=cols, style=style,
                      name=kwargs.pop('name', 'wxRadioBox'))
    wgt.SetSelection(int(value))
    set_tooltip(wgt, tooltip, t)
    pack(wgt, sizer, **kwargs)
    return wgt


def add_datepicker(parent, sizer=None, **kwargs):
    t = kwargs.pop('t', None)
    label = kwargs.pop('label', '')
    fsize = kwargs.pop('fsize', (-1, -1))
    ssize = kwargs.pop('ssize', (-1, -1))
    value = kwargs.pop('value', '')
    tooltip = kwargs.pop('tooltip', '')
    fg = kwargs.pop('fg', None)
    bg = kwargs.pop('bg', None)
    font = kwargs.pop('font', None)
    style = kwargs.pop('style', None)
    tooltip = kwargs.pop('tooltip', '')
    if not style:
        dropdown = kwargs.pop('dropdown', True)
        sty1 = wx.DP_DROPDOWN if dropdown else None

        show_century = kwargs.pop('show_century', True)
        sty2 = wx.DP_SHOWCENTURY if show_century else None

        if sty1 or sty2:
            if sty1:
                style = sty1
                if sty2:
                    style |= sty2

            else:
                style = sty2
        else:
            style = wx.DP_DEFAULT | wx.DP_SHOWCENTURY

    allow_none = kwargs.pop('allow_none', False)
    if allow_none:
        style |= wx.DP_ALLOWNONE

    nargs = dict(size=fsize, tooltip=tooltip, font=font, fg=fg, bg=bg, t=t)
    lbl = add_label(parent, label=label,
                    name=kwargs.pop('fname', 'wxStaticText'), **nargs)
    kw = dict(size=ssize, style=style,
              name=kwargs.pop('sname', 'wxDatePickerCtrl'))
    if value:
        if isinstance(value, basestring):
            try:
                from dateutil.parser import parse
                value = wxu.pydate2wxdate(parse(value))
                kw.update(dt=value)
            except:
                pass

        else:
            kw.update(dt=value)

    wgt = wx.DatePickerCtrl(parent, **kw)
    set_tooltip(wgt, tooltip, t)
    quick_pack(sizer, wgts=[lbl, wgt], **kwargs)

    return lbl, wgt


def add_timectrl(parent, **kwargs):
    kwargs['min'] = kwargs.pop('min_value', None)
    kwargs['max'] = kwargs.pop('max_value', None)
    kwargs['spinButton'] = kwargs.pop('spin_btn', None)
    kwargs['fmt24hr'] = kwargs.pop('format_24', True)
    wgt = masked.TimeCtrl(parent, **kwargs)
    return wgt


def add_open_dialog(parent, sizer, label='Select folder', **kwargs):
    t = kwargs.pop('t', None)
    fsize = kwargs.pop('fsize', (-1, -1))
    ssize = kwargs.pop('ssize', (-1, -1))
    tsize = kwargs.pop('tsize', (-1, -1))
    value = kwargs.pop('value', '')
    tooltip = kwargs.pop('tooltip', '')
    fg = kwargs.pop('fg', None)
    multiline = kwargs.pop('multiline', False)
    btn_label = kwargs.pop('btn_label', 'Browse')
    btn_id = kwargs.pop('btn_id', None)
    lbl = add_label(parent, label=label, size=fsize, t=t, fg=fg)
    txt = add_textctrl(parent, value=value, size=ssize, multiline=multiline,
                       t=t)
    set_tooltip(txt, tooltip, t)
    nargs = dict(label=btn_label, size=tsize, t=t)
    if btn_id:
        nargs.update(id=btn_id)

    btn = add_button(parent, **nargs)
    set_tooltip(btn, tooltip, t)
    quick_pack(sizer, wgts=[(lbl, 0), (txt, 1), (btn, 0)], **kwargs)
    return lbl, txt, btn


def add_line(parent, id=-1, size=(-1, -1), orient='h'):
    style = wx.LI_HORIZONTAL if orient == 'h' else wx.LI_VERTICAL
    return wx.StaticLine(parent, id, size=(-1, -1), style=style)


def add_ok_buttons(parent, sizer, id=-1, size=(100, 40), border=5, **kwargs):
    t = kwargs.pop('t', None)
    ok_text = kwargs.pop('ok_text', '&OK')
    cancel_text = kwargs.pop('cancel_text', '&Cancel')
    pack_line = kwargs.pop('pack_line', True)
    if pack_line:
        sl = add_line(parent, id)

    ok_btn = add_button(parent, wx.ID_OK, label=ok_text, size=size, t=t,
                        name=kwargs.pop('fname', 'wxButton'))
    ok_btn.SetDefault()
    cancel_btn = add_button(parent, wx.ID_CANCEL, label=cancel_text,
                            size=size, t=t,
                            name=kwargs.pop('sname', 'wxButton'))

    btn_sizer = wx.StdDialogButtonSizer()
    btn_sizer.AddButton(ok_btn)
    btn_sizer.AddButton(cancel_btn)
    btn_sizer.Realize()

    if pack_line:
        pack(sl, sizer, flag='e,t', border=15)

    pack(btn_sizer, sizer, prop=1, flag='ac,a', border=border)
    return ok_btn, cancel_btn


def add_statusbar(obj, widths=[-1, 170, 160], values=['', '', ''], **kwargs):
    t = kwargs.pop('t', None)
    sbar = obj.CreateStatusBar(len(widths))
    sbar.SetStatusWidths(widths)
    for i, v in enumerate(values):
        if v is None:
            continue

        sbar.SetStatusText(wdu.ttt(v, t), i)

    return sbar


def add_timer(self, timer_id, timer_func, miliseconds=-1, one_shot=False):
    timer = wx.Timer(self, timer_id)
    self.Bind(wx.EVT_TIMER, timer_func, id=timer_id)
    if miliseconds > 0:
        wxu.start_timer(timer, miliseconds, one_shot)

    return timer


def add_fnb(parent, id=-1, **kwargs):
    style = kwargs.pop('style', None)
    active_color = kwargs.pop('active_color', None)
    if style is None:
        # I prefer this style
        style = fnb.FNB_NODRAG | fnb.FNB_NO_X_BUTTON | fnb.FNB_NO_NAV_BUTTONS
        style |= fnb.FNB_VC8 | fnb.FNB_BACKGROUND_GRADIENT

    if kwargs.pop('bottom', False):
        style |= fnb.FNB_BOTTOM

    if active_color is None:
        # and this color
        active_color = wx.Colour(0, 128, 255, 255)

    nb = fnb.FlatNotebook(parent, id, agwStyle=style)
    nb.SetActiveTabColour(active_color)
    return nb


def get_sizer_flags(flags=''):
    flag = None
    for text in (flags or '').replace(' ', '').lower().split(','):
        if text in ('e', 'exp', 'expand'):
            f = wx.EXPAND
        elif text in ('l', 'left'):
            f = wx.LEFT
        elif text in ('r', 'right'):
            f = wx.RIGHT
        elif text in ('t', 'top'):
            f = wx.TOP
        elif text in ('b', 'bot', 'bottom'):
            f = wx.BOTTOM
        elif text in ('a', 'all'):
            f = wx.ALL
        elif text in ('sh', 'shaped'):
            f = wx.SHAPED
        elif text in ('fix', 'fixed'):
            f = wx.FIXED_MINSIZE
        elif text in ('hide', 'hidden'):
            f = wx.RESERVE_SPACE_EVEN_IF_HIDDEN
        elif text in ('ac', 'center', 'centre'):
            f = wx.ALIGN_CENTER
        elif text in ('al', 'a_left'):
            f = wx.ALIGN_LEFT
        elif text in ('ar', 'a_right'):
            f = wx.ALIGN_RIGHT
        elif text in ('at', 'a_top'):
            f = wx.ALIGN_TOP
        elif text in ('ab', 'a_bot', 'a_bottom'):
            f = wx.ALIGN_BOTTOM
        elif text in ('acv', 'a_center_v', 'a_centre_v'):
            f = wx.ALIGN_CENTER_VERTICAL
        elif text in ('ach', 'a_center_h', 'a_centre_h'):
            f = wx.ALIGN_CENTER_HORIZONTAL
        else:
            continue

        if flag is None:
            flag = f
        else:
            flag = flag | f

    if flag is None:
        flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP

    return flag


def pack(wgt, sizer='h', **kwargs):
    if sizer == 'h':
        sizer = wx.BoxSizer(wx.HORIZONTAL)
    elif sizer == 'v':
        sizer = wx.BoxSizer(wx.VERTICAL)
    elif not sizer:
        return

    kargs = dict(flag=get_sizer_flags(kwargs.get('flag')))
    border = kwargs.get('border', 3)
    if border:
        kargs.update(border=border)

    sizer.Add(wgt, kwargs.get('prop', 0), **kargs)
    return sizer


def sort_wgts(wgts=[], **kwargs):
    lst = []
    last_prop = kwargs.get('last_prop', 1)
    size = len(wgts)
    for i, wgt in enumerate(wgts, 1):
        if isinstance(wgt, (tuple, list)):
            lst.append(wgt)
        else:
            lst.append((wgt, last_prop if i == size else 0))

    return lst


def about_box(**kwargs):
    t = kwargs.pop('t', None)
    info = wx.AboutDialogInfo()
    icon = kwargs.pop('icon', None)
    icon_fmt = kwargs.pop('icon_fmt', None)
    if icon:
        if isinstance(icon, basestring):
            args = [icon]
            if icon_fmt:
                args.append(icon_fmt)

            info.SetIcon(wx.Icon(*args))
        else:
            info.SetIcon(icon)  # may be PyEmbeddedImage

    name = kwargs.pop('name', 'app name')
    version = kwargs.pop('version', '0.1')
    description = kwargs.pop('description', 'description')
    copyright = kwargs.pop('copyright', 'copyright')
    info.SetName(wdu.ttt(name, t))
    info.SetVersion(wdu.ttt(version, t))
    info.SetDescription(wdu.ttt(description, t))
    info.SetCopyright(wdu.ttt(copyright, t))
    website = kwargs.pop('website', '')
    if website:
        info.SetWebSite(website)

    licence = kwargs.pop('licence', '')
    if licence:
        info.SetLicence(licence)

    developers = kwargs.pop('developers', [])
    doc_writers = kwargs.pop('doc_writers', [])
    artists = kwargs.pop('artists', [])
    tranlators = kwargs.pop('tranlators', [])
    [info.AddDeveloper(developer) for developer in developers]
    [info.AddDocWriter(writer) for writer in doc_writers]
    [info.AddArtist(artist) for artist in artists]
    [info.AddTranslator(tranlator) for tranlator in tranlators]
    wx.AboutBox(info)


def quick_quit(self, **kwargs):
    """Quick handy method to ask for quit."""
    need_confirm = kwargs.pop('need_confirm', True)
    other_clean_work = kwargs.pop('other_clean_work', None)
    if hasattr(self, 'is_running') and self.is_running:
        caption = kwargs.pop('running_caption', 'Warning')
        msg = kwargs.pop('running_msg', 'Please stop current running task')
        icon = kwargs.pop('running_icon', 'w')
        popup(self, caption=caption, msg=msg, icon=icon, **kwargs)
        return

    if hasattr(self, 'opened_dlg') and self.opened_dlg > 0:
        caption = kwargs.pop('opened_caption', 'Warning')
        msg = kwargs.pop('opened_msg', 'Please close other dialogs')
        icon = kwargs.pop('opened_icon', 'w')
        popup(self, caption=caption, msg=msg, icon=icon, **kwargs)
        return

    if need_confirm:
        answer = popup(self,
                       caption=kwargs.pop('ask_caption', 'Confirmation'),
                       msg=kwargs.pop('ask_msg', 'Are you sure to quit?'),
                       icon=kwargs.pop('ask_icon', 'q'),
                       btn=kwargs.pop('btn', wx.YES_NO | wx.NO_DEFAULT),
                       **kwargs)
        if answer == wx.ID_NO:
            return

    self.Hide()
    if hasattr(self, 'hm'):
        try:
            self.hm.UnhookKeyboard()
        except:
            pass

        try:
            self.hm.UnhookMouse()
        except:
            pass

    if hasattr(self, 'stop_timers'):
        self.stop_timers()

    if hasattr(self, 'tbicon') and self.tbicon is not None:
        self.tbicon.Destroy()

    if other_clean_work:
        other_clean_work()
    elif hasattr(self, 'other_clean_work'):
        self.other_clean_work()

    self.Destroy()
    return True


def quick_about(*args, **kwargs):
    fmt = kwargs.pop('fmt',
                     '{}\n\nPlatform:\nPython {}\nwxPython {} ({})\n{}\n\n')
    t = kwargs.get('t', None)
    copyright = kwargs.pop('copyright', wdu.get_copy_right())
    author = kwargs.pop('author', '')
    remark = kwargs.pop('remark', 'about this tool')
    description = fmt.format(wdu.ttt(remark, t), sys.version.split()[0],
                             wx.VERSION_STRING, ', '.join(wx.PlatformInfo[1:]),
                             wdu.get_platform_info())
    if author:
        kwargs.update(developers=[author], doc_writers=[author])

    about_info = dict(description=description,
                      copyright=copyright.replace('&', '&&'), **kwargs)
    about_box(**about_info)


def quick_pack(sizer=None, wgts=[], orient='h', **kwargs):
    if not sizer:
        return

    ws = sort_wgts(wgts, **kwargs)
    kargs = dict(flag=kwargs.get('flag'), border=kwargs.get('border', 3))
    box = pack(ws[0][0], sizer=orient, prop=ws[0][1], **kargs)
    for wgt, pr in ws[1:]:
        pack(wgt, box, prop=pr, **kargs)

    pack(box, sizer, **kwargs)
    return box


def quick_open_file(parent, sizer=None, label='Select File', **kwargs):
    value = kwargs.pop('value', '')
    fg = kwargs.pop('fg', None)
    fsize = kwargs.pop('fsize', (-1, -1))
    ssize = kwargs.pop('ssize', (-1, -1))
    lbl = add_label(parent, label=label, size=fsize, fg=fg, t=kwargs.get('t'),
                    name=kwargs.pop('fname', 'wxStaticText'))
    kwargs.update(size=ssize)
    fp, tc, btn = add_file_picker(parent, value=value, **kwargs)
    quick_pack(sizer, wgts=[lbl, fp])
    return lbl, fp, tc, btn


def quick_open_folder(parent, sizer=None, label='Select Folder', **kwargs):
    value = kwargs.pop('value', '')
    fg = kwargs.pop('fg', None)
    fsize = kwargs.pop('fsize', (-1, -1))
    ssize = kwargs.pop('ssize', (-1, -1))
    lbl = add_label(parent, label=label, size=fsize, fg=fg, t=kwargs.get('t'),
                    name=kwargs.pop('fname', 'wxStaticText'))
    kwargs.update(size=ssize)
    fp, tc, btn = add_dir_picker(parent, value=value, **kwargs)
    quick_pack(sizer, wgts=[lbl, fp])
    return lbl, fp, tc, btn


def quick_entry(parent=None, caption='', msg='Enter', password=True, **kwargs):
    entry_cls = wx.PasswordEntryDialog if password else wx.TextEntryDialog
    t = kwargs.pop('t', None)
    root_pass = kwargs.pop('root_pass', 'guess')
    ok_label = kwargs.pop('ok_label', None)
    cancel_label = kwargs.pop('cancel_label', None)
    dlg = entry_cls(parent, wdu.ttt(msg, t), wdu.ttt(caption, t))
    # update button labels for i18n
    try:
        btn_sizer = dlg.Sizer.GetChildren()[2].Sizer.GetChildren()[1].Sizer
        items = btn_sizer.GetChildren()
        ok_btn, c_btn = items[1].GetWindow(), items[2].GetWindow()
        ok_btn.SetLabel(wdu.ttt(ok_label or ok_btn.GetLabel(), t))
        c_btn.SetLabel(wdu.ttt(cancel_label or c_btn.GetLabel(), t))
    except:
        pass

    size = dlg.GetClientSize()
    dlg.SetMinClientSize(size)
    dlg.SetMaxClientSize(size)
    dlg.SetValue(kwargs.pop('value', ''))
    while 1:
        dlg.SetFocus()
        if dlg.ShowModal() == wx.ID_OK:
            text = dlg.GetValue()
            if password:
                if text == root_pass:
                    dlg.Destroy()
                    return True

            else:
                text = text.strip()
                if text:
                    dlg.Destroy()
                    return text

            dlg.SetValue('')
            dlg.SetFocus()
            continue

        dlg.Destroy()
        return False if password else ''


def quick_password_entry(parent=None, caption='Security Check', **kwargs):
    msg = kwargs.pop('msg', 'Please enter password:')
    return quick_entry(parent, caption=caption, msg=msg, **kwargs)


def quick_text_entry(parent=None, caption='Enter Something', **kwargs):
    msg = kwargs.pop('msg', 'Please enter something: ')
    return quick_entry(parent, caption=caption, msg=msg, password=False,
                       **kwargs)


def quick_choice(parent=None, msg='Please select', **kwargs):
    t = kwargs.pop('t', None)
    caption = kwargs.pop('caption', 'Please select')
    choices = kwargs.pop('choices', [])
    valid_choices = kwargs.pop('valid_choices', [])
    style = kwargs.pop('style', wx.CHOICEDLG_STYLE)
    dlg = wx.SingleChoiceDialog(parent, wdu.ttt(msg, t), wdu.ttt(caption, t),
                                choices, style)
    ok_label = kwargs.pop('ok_label', None)
    cancel_label = kwargs.pop('cancel_label', None)
    # update button labels for i18n
    try:
        btn_sizer = dlg.Sizer.GetChildren()[2].Sizer.GetChildren()[1].Sizer
        items = btn_sizer.GetChildren()
        ok_btn, c_btn = items[1].GetWindow(), items[2].GetWindow()
        ok_btn.SetLabel(wdu.ttt(ok_label or ok_btn.GetLabel(), t))
        c_btn.SetLabel(wdu.ttt(cancel_label or c_btn.GetLabel(), t))
    except:
        pass

    while 1:
        if dlg.ShowModal() == wx.ID_OK:
            selected = dlg.GetStringSelection()
            if selected in valid_choices:
                dlg.Destroy()
                return selected

            continue

        break

    dlg.Destroy()
    return None


def quick_big_buttons(self, parent, start=True, setting=True, hide=True,
                      changes=True, about=True):
    font = self.GetFont()
    font.SetWeight(wx.BOLD)
    kwargs = dict(size=(-1, 45), font=font)
    buttons = []
    if start:
        start_btn = add_button(parent, label='Start', **kwargs)
        start_btn.Bind(wx.EVT_BUTTON, self.on_start)
        buttons.append(start_btn)

    if setting:
        setting_btn = add_button(parent, label='Settings...', **kwargs)
        setting_btn.Bind(wx.EVT_BUTTON, self.on_setting)
        buttons.append(setting_btn)

    if hide:
        hide_btn = add_button(parent, label='Hide', **kwargs)
        hide_btn.Bind(wx.EVT_BUTTON, self.on_hide)
        buttons.append(hide_btn)

    if changes:
        changes_btn = add_button(parent, label='Changes', **kwargs)
        changes_btn.Bind(wx.EVT_BUTTON, self.on_changes)
        buttons.append(changes_btn)

    if about:
        about_btn = add_button(parent, label='About', **kwargs)
        about_btn.Bind(wx.EVT_BUTTON, self.on_about)
        buttons.append(about_btn)

    return buttons

add_rich_text = add_richtext
add_status_bar = add_statusbar
add_date_picker = add_datepicker
add_time_ctrl = add_timectrl
add_text_ctrl = add_textctrl
add_spin_ctrl = add_spinctrl
add_spin_ctrl_double = add_spinctrl_double
add_check_box = add_checkbox
add_static_box = add_staticbox
add_check_box_row = add_checkbox_row
add_combo_box = add_combobox
add_radiobox = add_radio_box

quick_textentry = quick_text_entry
quick_open_dir = quick_open_folder
