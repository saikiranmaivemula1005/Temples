import wx
import difflib
import wx.richtext as rt


MENU_FILE_EXIT = wx.NewId()
DRAG_SOURCE = wx.NewId()

text_before_edit = ""


class TextDropTarget(wx.TextDropTarget):
        def __init__(self, obj):
            """ Initialize the Drop Target, passing in the Object Reference to
                indicate what should receive the dropped text """

        # Initialize the wx.TextDropTarget Object

            wx.TextDropTarget.__init__(self)

        # Store the Object Reference for dropped text

            self.obj = obj
        def OnDropText(self, x, y, data):
            # source = self.obj.GetValue() + data
            # print (source)

        # When text is dropped, write it into the object specified

            self.obj.WriteText(data + "\n")
            global text_before_edit
            text_before_edit = self.obj.GetValue()

class MainWindow(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(1200, 600),
			style=wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE,)
		self.SetBackgroundColour(wx.WHITE)
		menuBar = wx.MenuBar()

		menu1 = wx.Menu()
		menu1.Append(MENU_FILE_EXIT, 'E&xit', 'Quit Application')
		menuBar.Append(menu1, '&File')

		self.SetMenuBar(menuBar)
		# Events for menu items
		wx.EVT_MENU(self, MENU_FILE_EXIT, self.CloseWindow)
		wx.StaticText(self, -1,
                                    'Text Drag Source  (left-click to select, right-click to drag)'
                                    , (10, 1))
		 # Text Control
		self.text = wx.TextCtrl(
                self,
                DRAG_SOURCE,
                '',
                pos=(10, 15),
                size=(350, 500),
                style=wx.TE_MULTILINE | wx.HSCROLL | wx.TE_READONLY,
                )
		 # Text Drop Target
		dt1 = TextDropTarget(self.text)
		self.text.SetDropTarget(dt1)

		# text in control to copy 
		f = open("sample.txt")
		input = f.read()
		input.split()
		print(input)
		self.text.WriteText(input)
		wx.EVT_RIGHT_DOWN(self.text, self.OnDragInit)

        # Read only text control
		self.text2 = wx.TextCtrl(
                self,
                -1,
                '',
                pos=(370, 15),
                size=(410, 470),
                style=wx.TE_MULTILINE | wx.HSCROLL,
                )
        # Making this control a text drop target
		dt2 = TextDropTarget(self.text2)
		self.text2.SetDropTarget(dt2)
		self.button = wx.Button(self, wx.ID_ANY, pos=(680, 490), label='Compare')

        # setting event hadlers
		self.button.Bind(wx.EVT_BUTTON, self.OnButton)
		wx.StaticText(self, -1,
                            'Text Drag Source  (left-click to select, right-click to drag)'
                            , (10, 1))

        # creating a text control
		self.text3 = rt.RichTextCtrl(
                self,
                -1,
                '',
                pos=(800, 15),
                size=(350, 500),
                style=wx.TE_MULTILINE | wx.HSCROLL | wx.TE_READONLY,
                )
        # display the window
		self.Show(True)


	def OnButton(self, e):
		d = difflib.Differ()
		text_first = self.text.GetValue()
		for line in text_first:
			print(line)

		text_after_edit = self.text2.GetValue()

		global text_before_edit

		for i in text_first:
			if i in text_after_edit:
				self.text3.BeginTextColour('black')
				self.text3.WriteText(i)
			else:
				self.text3.BeginTextColour('green')
				self.text3.WriteText(i)
		# else:

	def CloseWindow(self, event):
		self.Close()

	def OnDragInit(self, event):
		#create a text data object to hold the text that is to be dragged

		tdo = wx.PyTextDataObject(self, text.GetStringSelection())

		#Create a Drop Source Object, which enables the Drag operation 

		tds = wx.DropSource(self.text)

		#Associate the Data to be dragged with the Drop Source Object

		tds.SetData(tdo)

		# Initiate the drag operation

		tds.DoDragDrop(True)
		

class MyApp(wx.App):
	def OnInit(self):
		frame = MainWindow(None, -1, 'Telugu Wiki')

		self.SetTopWindow(frame)
		return True




app = MyApp(0)
app.MainLoop()
