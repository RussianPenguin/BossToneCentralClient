import requests
import wx
import wx.html2

_define_models = {
        'GT-100 v2/GT-001': 'gt.json',
        'GT-1': 'gt-1.json',
        'Katana': 'katana.json',
        'Katana Air': 'katana-air.json',
        'GT-1000': 'gt-1000.json',
        'GP-10': 'gp-10.json',
        'ME-80': 'me-80.json',
        'ME-25': 'me-25.json',
        }

class MainApplication(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(
                self,
                None,
                wx.ID_ANY,
                "Boss ToneCentral Downloader",
                size=wx.Size(640, 480),
        )
        panel = wx.Panel(self, wx.ID_ANY)
        choises = []
        self.cb_model_select = wx.ComboBox(panel)
        self.cb_genre_select = wx.ComboBox(panel)
        self.cb_preset_select = wx.ComboBox(panel)
        self.load_model_list()
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.cb_model_select, 1, wx.ALL)
        sizer.Add(self.cb_genre_select, 1, wx.ALL)
        sizer.Add(self.cb_preset_select, 1, wx.ALL)

        sizer_out = wx.BoxSizer(wx.VERTICAL)
        sizer_out.Add(sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT)

        sizer_browser = wx.BoxSizer(wx.HORIZONTAL)
        self.browser = wx.html2.WebView.New(panel)
        sizer_browser.Add(self.browser, 1, wx.EXPAND | wx.LEFT | wx.RIGHT)
        sizer_out.Add(sizer_browser, 1, wx.EXPAND | wx.LEFT | wx.RIGHT)

        self.btn_download = wx.Button(panel)
        sizer_out.Add(self.btn_download, 0, wx.EXPAND | wx.LEFT | wx.RIGHT)
        self.btn_download.SetBackgroundColour(wx.Colour(0, 144, 0))
        panel.SetSizer(sizer_out)
        self.model = None
        self.define = None
        self.apps = None
        self.cb_genre_select.Bind(wx.EVT_COMBOBOX, self.change_genre)
        self.cb_preset_select.Bind(wx.EVT_COMBOBOX, self.change_preset)
        self.btn_download.Bind(wx.EVT_BUTTON, self.download)
    
    def load_model_list(self) -> None:
        self.cb_model_select.Clear()
        for model in _define_models:
            self.cb_model_select.Append(model, _define_models[model])
        self.cb_model_select.Bind(wx.EVT_COMBOBOX, self.change_model)

    def load_genre_list(self) -> None:
        self.cb_genre_select.Clear()
        genres = set()
        for item in self.apps['items']:
            genres = genres.union(set(item['tags']))
        for genre in genres:
            self.cb_genre_select.Append(genre, genre)

    def change_genre(self, event):
        genre = self.cb_genre_select.GetClientData(
                self.cb_genre_select.GetSelection())
        self.load_preset_list(genre)
    
    def change_preset(self, event):
        preset = self.cb_preset_select.GetClientData(
                self.cb_preset_select.GetSelection())
        self.load_preset(preset)

    def download(self, event):
        basename = self.cb_preset_select.GetClientData(
                self.cb_preset_select.GetSelection())[0]
        content = requests.get(
                self.define['btc']['domain'] + self.define['btc']['liveset_file'] + basename + '.tsl'
            )
        open(basename + '.tsl', 'wb').write(content.content)

    def load_preset(self, preset):
        self.browser.LoadURL(preset[1])
        self.btn_download.SetLabel('Download ' + preset[2])

    def load_preset_list(self, genre: str):
        self.cb_preset_select.Clear()
        for item in self.apps['items']:
            if genre in item['tags']:
                self.cb_preset_select.Append(
                        item['title'], 
                        (
                            item['basename'], 
                            item['permalink'],
                            item['title']
                        ),
                    )

    def change_model(self, event):
        model = self.cb_model_select.GetClientData(
                self.cb_model_select.GetSelection())
        self.define = requests.get(
                'http://api.roland.com/app/btc/define/' + model,
                ).json()
        self.apps = requests.get(
                (
                    self.define['btc']['domain'] + 
                    self.define['btc']['dataapi']
                ),
                ).json()
        self.load_genre_list()


if __name__ == '__main__':
    app = wx.App(False)
    frame = MainApplication()
    frame.Show()
    app.MainLoop()

