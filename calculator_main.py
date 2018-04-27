from calculator import *
from validator import CalcValidator
from asteval import Interpreter
from converter import *


class CalcBuilder:
    ENTER_ID, NUM_ENTER_ID = wx.NewId(), wx.NewId()
    CLEAR_ID = wx.NewId()
    curr_conv = CurrencyConverter()
    dist_conv = DistanceConverter()
    speed_conv = SpeedConverter()
    frm = None

    def build_frame(self):
        self.frm = CalcMainFrame(None)
        self.frm.Bind(wx.EVT_MENU, lambda e: self.frm.Close(), id=self.frm.mb_main.mi_quit.GetId())
        self.frm.Bind(wx.EVT_MENU, lambda e: self.swap_panel_calc(), id=self.frm.mb_main.mi_calc.GetId())
        self.frm.Bind(wx.EVT_MENU, lambda e: self.swap_panel_conv(), id=self.frm.mb_main.mi_conv.GetId())
        accelerator_tbl = wx.AcceleratorTable([
            (wx.ACCEL_NORMAL, wx.WXK_RETURN, self.ENTER_ID), (wx.ACCEL_NORMAL, wx.WXK_NUMPAD_ENTER, self.NUM_ENTER_ID),
            (wx.ACCEL_NORMAL, wx.WXK_DELETE, self.CLEAR_ID)
        ])
        self.frm.SetAcceleratorTable(accelerator_tbl)
        self.bind_calc(self.frm.calc_panel)
        self.bind_conv(self.frm.conv_panel)
        return self.frm

    def swap_panel_calc(self):
        if self.frm.conv_panel.IsShown():
            self.frm.SetTitle("wxCalculator")
            self.frm.SetSize((400, 300))
            self.frm.calc_panel.Show()
            self.frm.conv_panel.Hide()
            self.frm.Layout()

    def swap_panel_conv(self):
        if self.frm.calc_panel.IsShown():
            self.frm.SetTitle("wxCalculator [Converter]")
            self.frm.SetSize((600, 200))
            self.frm.calc_panel.Hide()
            self.frm.conv_panel.Show()
            self.frm.Layout()

    def bind_calc(self, calc: CalcPanel):
        display = calc.tctrl_calc_in
        display.Validator = CalcValidator()

        def handle_key_press(this, event):
            if event.GetId() == this.ENTER_ID or event.GetId() == this.NUM_ENTER_ID:
                exec_calc()
            elif event.GetId() == this.CLEAR_ID:
                update_screen()

        # Number buttons
        self.frm.Bind(wx.EVT_BUTTON, lambda e: update_screen('0'), id=calc.btn_zero.GetId())
        self.frm.Bind(wx.EVT_BUTTON, lambda e: update_screen('1'), id=calc.btn_one.GetId())
        self.frm.Bind(wx.EVT_BUTTON, lambda e: update_screen('2'), id=calc.btn_two.GetId())
        self.frm.Bind(wx.EVT_BUTTON, lambda e: update_screen('3'), id=calc.btn_three.GetId())
        self.frm.Bind(wx.EVT_BUTTON, lambda e: update_screen('4'), id=calc.btn_four.GetId())
        self.frm.Bind(wx.EVT_BUTTON, lambda e: update_screen('5'), id=calc.btn_five.GetId())
        self.frm.Bind(wx.EVT_BUTTON, lambda e: update_screen('6'), id=calc.btn_six.GetId())
        self.frm.Bind(wx.EVT_BUTTON, lambda e: update_screen('7'), id=calc.btn_seven.GetId())
        self.frm.Bind(wx.EVT_BUTTON, lambda e: update_screen('8'), id=calc.btn_eight.GetId())
        self.frm.Bind(wx.EVT_BUTTON, lambda e: update_screen('9'), id=calc.btn_nine.GetId())

        # Function buttons
        self.frm.Bind(wx.EVT_BUTTON, lambda e: update_screen('.'), id=calc.btn_comma.GetId())
        self.frm.Bind(wx.EVT_BUTTON, lambda e: update_screen('+'), id=calc.btn_add.GetId())
        self.frm.Bind(wx.EVT_BUTTON, lambda e: update_screen('-'), id=calc.btn_sub.GetId())
        self.frm.Bind(wx.EVT_BUTTON, lambda e: update_screen('*'), id=calc.btn_mult.GetId())
        self.frm.Bind(wx.EVT_BUTTON, lambda e: update_screen('/'), id=calc.btn_div.GetId())
        self.frm.Bind(wx.EVT_BUTTON, lambda e: update_screen('**'), id=calc.btn_pow.GetId())
        self.frm.Bind(wx.EVT_BUTTON, lambda e: update_screen('sqrt(x)'), id=calc.btn_sqrt.GetId())
        self.frm.Bind(wx.EVT_BUTTON, lambda e: update_screen('(x+y)'), id=calc.btn_brackets.GetId())
        self.frm.Bind(wx.EVT_BUTTON, lambda e: update_screen(), id=calc.btn_ca.GetId())
        self.frm.Bind(wx.EVT_BUTTON, lambda e: exec_calc(), id=calc.btn_equals.GetId())
        self.frm.Bind(wx.EVT_MENU, lambda e: handle_key_press(self, e), id=self.ENTER_ID, id2=self.NUM_ENTER_ID)
        self.frm.Bind(wx.EVT_MENU, lambda e: handle_key_press(self, e), id=self.CLEAR_ID)

        def update_screen(symbol=None):
            if not display.IsEmpty() and symbol == 'sqrt(x)':
                content = display.GetLineText(0)
                display.Clear()
                display.AppendText('sqrt({0})'.format(content))
            elif not display.IsEmpty() and symbol == '(x+y)':
                content = display.GetLineText(0)
                display.Clear()
                display.AppendText('({0})'.format(content))
            elif symbol:
                display.AppendText(symbol)
            else:
                display.Clear()

        def exec_calc():
            if not display.IsEmpty():
                a_eval = Interpreter()
                res = str(a_eval(display.GetLineText(0)))

                if len(a_eval.error) > 0:
                    err = a_eval.error[0].get_error()
                    err_box = wx.RichMessageDialog(
                        self.frm, 'An {0} occurred. Pleas check below for details.'.format(err[0]),
                        'Evaluation Error', wx.OK | wx.ICON_ERROR
                    )
                    err_list = [str(e.get_error()[1]).strip() + '\n' for e in a_eval.error]
                    err_box.ShowDetailedText(' '.join(err_list))
                    err_box.ShowModal()
                    display.SetBackgroundColour("pink")
                    display.SetFocus()
                    display.Refresh()
                else:
                    display.SetBackgroundColour(
                        wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
                    display.Refresh()
                    display.Clear()
                    display.AppendText(res)

    def bind_conv(self, conv: ConvPanel):
        curr_a, curr_b = conv.cmb_curr_a, conv.cmb_curr_b
        curr_av, curr_bv = conv.tctrl_curr_a, conv.tctrl_curr_b
        dist_a, dist_b = conv.cmb_dist_a, conv.cmb_dist_b
        dist_av, dist_bv = conv.tctrl_dist_a, conv.tctrl_dist_b
        speed_a, speed_b = conv.cmb_speed_a, conv.cmb_speed_b
        speed_av, speed_bv = conv.tctrl_speed_a, conv.tctrl_speed_b
        currencies = list(
            ['{0}, {1} ({2})'.format(k.ljust(4), v['Country'], v['Symbol']) for k, v in
             self.curr_conv.get_supported().items()]
        )
        distances = list(['{0} ({1})'.format(k.ljust(4), v['Name'])
                          for k, v in self.dist_conv.get_supported().items()])
        speeds = list(['{0} ({1})'.format(k.ljust(4), v['Name'])
                       for k, v in self.speed_conv.get_supported().items()])

        curr_a.SetItems(currencies)
        curr_a.Select(0)
        curr_b.SetItems(currencies)
        curr_b.Select(1)

        dist_a.SetItems(distances)
        dist_a.Select(0)
        dist_b.SetItems(distances)
        dist_b.Select(1)

        speed_a.SetItems(speeds)
        speed_a.Select(0)
        speed_b.SetItems(speeds)
        speed_b.Select(1)

        def ltr_convert(cmb_a, cmb_b, tctrl_a, tctrl_b, converter: ConverterBase):
            unit_a = cmb_a.GetValue().split(' ', 1)[0]
            unit_b = cmb_b.GetValue().split(' ', 1)[0]
            try:
                value = float(tctrl_a.GetValue())
                tctrl_b.ChangeValue(str(round(converter.convert(unit_a, unit_b, value), 4)))
            except ValueError as e:
                print(e)

        def rtl_convert(cmb_a, cmb_b, tctrl_a, tctrl_b, converter: ConverterBase):
            unit_a = cmb_a.GetValue().split(' ', 1)[0]
            unit_b = cmb_b.GetValue().split(' ', 1)[0]
            try:
                value = float(tctrl_b.GetValue())
                tctrl_a.ChangeValue(str(round(converter.convert(unit_b, unit_a, value), 4)))
            except ValueError as e:
                print(e)

        def l_curr_cmb_ch(converter: ConverterBase):
            unit_a = curr_a.GetValue()[0:3]
            unit_b = curr_b.GetValue()[0:3]
            try:
                conv.tctrl_exchange.ChangeValue(str(round(converter.conversion_rate(unit_a, unit_b), 4)))
            except ValueError:
                pass

        def r_curr_cmb_ch(converter: ConverterBase):
            unit_a = curr_a.GetValue()[0:3]
            unit_b = curr_b.GetValue()[0:3]
            try:
                conv.tctrl_exchange.ChangeValue(str(round(converter.conversion_rate(unit_b, unit_a), 4)))
            except ValueError:
                pass

        l_curr_cmb_ch(self.curr_conv)
        curr_a.Bind(wx.EVT_COMBOBOX, lambda e: l_curr_cmb_ch(self.curr_conv))
        curr_b.Bind(wx.EVT_COMBOBOX, lambda e: r_curr_cmb_ch(self.curr_conv))
        curr_av.Bind(wx.EVT_TEXT, lambda e: ltr_convert(curr_a, curr_b, curr_av, curr_bv, self.curr_conv))
        curr_bv.Bind(wx.EVT_TEXT, lambda e: rtl_convert(curr_a, curr_b, curr_av, curr_bv, self.curr_conv))
        self.frm.Bind(wx.EVT_BUTTON, lambda e: ltr_convert(curr_a, curr_b, curr_av, curr_bv, self.curr_conv),
                      id=conv.btn_convert.GetId())
        self.frm.Bind(wx.EVT_BUTTON, lambda e: self.curr_conv.try_update_exchange(), id=conv.btn_refresh.GetId())

        dist_a.Bind(wx.EVT_COMBOBOX, lambda e: ltr_convert(dist_a, dist_b, dist_av, dist_bv, self.dist_conv))
        dist_b.Bind(wx.EVT_COMBOBOX, lambda e: ltr_convert(dist_a, dist_b, dist_av, dist_bv, self.dist_conv))
        dist_av.Bind(wx.EVT_TEXT, lambda e: ltr_convert(dist_a, dist_b, dist_av, dist_bv, self.dist_conv))
        dist_bv.Bind(wx.EVT_TEXT, lambda e: rtl_convert(dist_a, dist_b, dist_av, dist_bv, self.dist_conv))

        speed_a.Bind(wx.EVT_COMBOBOX, lambda e: ltr_convert(speed_a, speed_b, speed_av, speed_bv, self.speed_conv))
        speed_b.Bind(wx.EVT_COMBOBOX, lambda e: ltr_convert(speed_a, speed_b, speed_av, speed_bv, self.speed_conv))
        speed_av.Bind(wx.EVT_TEXT, lambda e: ltr_convert(speed_a, speed_b, speed_av, speed_bv, self.speed_conv))
        speed_bv.Bind(wx.EVT_TEXT, lambda e: rtl_convert(speed_a, speed_b, speed_av, speed_bv, self.speed_conv))


if __name__ == "__main__":
    app = wx.App(False)
    builder = CalcBuilder()
    frame = builder.build_frame()
    frame.Show()
    app.MainLoop()
