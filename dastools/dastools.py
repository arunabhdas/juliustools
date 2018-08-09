#!/usr/bin/env python3
import base64
import urllib
from bs4 import BeautifulSoup
import urllib.request
import json
import hashlib
import requests
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from PIL import Image, ImageFont, ImageDraw

icons = ["edit-cut", "edit-paste", "edit-copy"]
# dastools is a multi-purpose tool written in Python
# Simply launch dastools on the command line as follows :
# ./dastools.py
# Enter the dimensions you want the image to be and the enter the text you want on the image and click generate.
# An image with the filename image_generated_output.png will be generated.
# More documentation can be found here :
# http://confluence.knowroaming.com/display/AA/Android+%3A+Vsim+Apps+%3A+Offline+Activation+%3A+SecureVault%2C+Cromulent%2C+Kwijybo%2C+Garfield#Android:VsimApps:OfflineActivation:SecureVault,Cromulent,Kwijybo,Garfield-GarfieldGUI
# http://www.pygtk.org/pygtk2tutorial/sec-PackingUsingTables.html
# http://python-gtk-3-tutorial.readthedocs.io/en/latest/index.html
class DastoolsWindow(Gtk.Window):
	"""docstring for DastoolsWindow"""
	def __init__(self):
		Gtk.Window.__init__(self, title="DasTools is a GUI which provides common useful functionality from multiple tools")
		self.set_border_width(20)
		self.set_default_size(800, 300)

		hb = Gtk.HeaderBar()
		hb.set_show_close_button(True)
		hb.props.title = "DasTools"
		self.set_titlebar(hb)

		self.headerbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		Gtk.StyleContext.add_class(self.headerbox.get_style_context(), "linked")

		# buttonleft = Gtk.Button()
		# buttonleft.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
		# self.headerbox.add(buttonleft)

		# buttonright = Gtk.Button()
		# buttonright.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
		# self.headerbox.add(buttonright)

		hb.pack_start(self.headerbox)

		# self.hbox = Gtk.Box(spacing=7)
		# start stack

		self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.add(self.vbox)

		self.stack = Gtk.Stack()
		self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
		self.stack.set_transition_duration(1000)




		self.stack_switcher = Gtk.StackSwitcher()
		self.stack_switcher.set_stack(self.stack)
		self.vbox.pack_start(self.stack_switcher, True, True, 0)
		self.vbox.pack_start(self.stack, True, True, 0)


		# JuliusGenerator
		self.entry_width = Gtk.Entry()
		self.entry_width.set_placeholder_text("320")
		self.entry_height = Gtk.Entry()
		self.entry_height.set_placeholder_text("480")
		self.entry_displaytext = Gtk.Entry()
		self.entry_displaytext.set_placeholder_text("Lorem Ipsum")



		self.button_generate = Gtk.Button(label="Generate image")
		self.button_generate.connect("clicked", self.on_button_generate_clicked)

		self.button_save = Gtk.Button(label="Save")
		self.button_save.connect("clicked", self.on_button_save_clicked)

		self.label_width = Gtk.Label(label="Width", angle=0, halign=Gtk.Align.START)
		self.label_height = Gtk.Label(label="Height", angle=0, halign=Gtk.Align.START)
		self.label_displaytext = Gtk.Label(label="Display Text", angle=0, halign=Gtk.Align.START)



		julius_file_name = "julius_placeholder.jpg"
		self.frame_placeholder = Gtk.Frame(label="Preview")
		self.frame_placeholder.set_label_align(0.5, 0.5)
		self.frame_placeholder.set_shadow_type(Gtk.ShadowType.IN)
		self.image_placeholder = Gtk.Image.new_from_file(julius_file_name)
		self.frame_placeholder.add(self.image_placeholder)




		table = Gtk.Table(2,5)
		table.attach(self.label_width, 0, 1, 0, 1)
		table.attach(self.entry_width, 1, 2, 0, 1)
		table.attach(self.label_height, 0, 1, 1, 2)
		table.attach(self.entry_height, 1, 2, 1, 2)
		table.attach(self.label_displaytext, 0, 1, 2, 3)
		table.attach(self.entry_displaytext, 1, 2, 2, 3)
		table.attach(self.button_generate, 1, 2, 3, 4)
		table.attach(self.button_save, 0, 1, 3, 4)
		table.attach(self.frame_placeholder, 0, 2, 4, 5)


		# AugustusBase64Tools start
		table_base64 = Gtk.Table(2, 5)

		self.label_base64_plaintext = Gtk.Label(label="Plaintext", angle=0, halign=Gtk.Align.START)
		table_base64.attach(self.label_base64_plaintext, 0, 1, 0, 1)

		self.entry_base64_plaintext = Gtk.Entry()
		self.entry_base64_plaintext.set_placeholder_text("Plaintext")
		table_base64.attach(self.entry_base64_plaintext, 1, 2, 0, 1)

		self.label_base64_ciphertext = Gtk.Label(label="Ciphertext", angle=0, halign=Gtk.Align.START)
		table_base64.attach(self.label_base64_ciphertext, 0, 1, 1, 2)

		self.entry_base64_ciphertext = Gtk.Entry()
		self.entry_base64_ciphertext.set_placeholder_text("Ciphertext")
		table_base64.attach(self.entry_base64_ciphertext, 1, 2, 1, 2)

		self.frame_base64_placeholder = Gtk.Frame(label="Preview")
		self.frame_base64_placeholder.set_label_align(0.5, 0.5)
		self.frame_base64_placeholder.set_shadow_type(Gtk.ShadowType.IN)
		self.image_base64_placeholder = Gtk.Image.new_from_file('augustus_placeholder.png')
		self.frame_base64_placeholder.add(self.image_base64_placeholder)


		table_base64.attach(self.frame_base64_placeholder, 0, 2, 4, 5)

		self.button_to_base64 = Gtk.Button(label="Convert to base64")
		self.button_to_base64.connect("clicked", self.on_button_to_base64_clicked)

		self.button_from_base64 = Gtk.Button(label="Convert from base64")
		self.button_from_base64.connect("clicked", self.on_button_from_base64_clicked)

		table_base64.attach(self.button_from_base64, 1, 2, 3, 4)
		table_base64.attach(self.button_to_base64, 0, 1, 3, 4)

		# AugustusBase64Tools end


		# AureliusTools start

		table_aurelius = Gtk.Table(4, 21)

		##############################################################
		# Global Constants
		##############################################################
		self.ver = "3"
		self.vendorId = "168118"
		self.chipsetVendorId = "2"
		self.oemBrandingSelectorId = "106"
		self.appVersion = "2.30.9"
		self.phoneOS = "Android%207.1.2"
		self.phoneModel = "BlackBerry%20BBD100-1"
		##############################################################
		# BaseURL
		##############################################################
		# Label1
		self.label_aurelius_base_url = Gtk.Label(label="Select Environment : ", angle=0, halign=Gtk.Align.START)
		table_aurelius.attach(self.label_aurelius_base_url, 0, 2, 0, 1)

		# Entry1
		# self.entry_aurelius_base_url = Gtk.Entry()
		# self.entry_aurelius_base_url.set_text("http://10.27.74.20:9000/API_Handler_release_live/?")
		# table_aurelius.attach(self.entry_aurelius_base_url, 0, 2, 1, 2)

		environments = ["https://app.knowroaming.com/API_Handler_release_live/?", "http://10.27.74.20:9000/API_Handler_release_live/?"]
		self.environments_combo = Gtk.ComboBoxText()
		# self.environments_combo.set_entry_text_column(0)
		self.environments_combo.connect("changed", self.on_environments_combo_changed)
		for env in environments:
			self.environments_combo.append_text(env)
		table_aurelius.attach(self.environments_combo, 0, 2, 1, 2)


		self.label_aurelius_base_url_confirm = Gtk.Label(label="Click to login : ", angle=0, halign=Gtk.Align.START)
		table_aurelius.attach(self.label_aurelius_base_url_confirm, 2, 4, 0, 1)

		# Button12
		self.button_aurelius_do_login = Gtk.Button(label="Login")
		table_aurelius.attach(self.button_aurelius_do_login, 2, 4, 1, 2)
		self.button_aurelius_do_login.connect("clicked", self.on_button_aurelius_do_login_clicked)

		##############################################################
		# Commands
		##############################################################


		# Label2
		self.label_aurelius_command = Gtk.Label(label="Command", angle=0, halign=Gtk.Align.START)
		table_aurelius.attach(self.label_aurelius_command, 0, 2, 2, 3)

		commands = ["checkAppVersion", \
					"getBuyablePackages", \
					"getAlcatelCountries_n", \
					"getHistory_TODO", \
					"getPrivateNews", \
					"getPublicNews", \
					"updatePushNotificationDeviceToken", \
					"getCustomerInformation"]
		self.commands_combo = Gtk.ComboBoxText()
		# self.environments_combo.set_entry_text_column(0)
		self.commands_combo.set_active(0)
		self.commands_combo.connect("changed", self.on_commands_combo_changed)
		for command in commands:
			self.commands_combo.append_text(command)

		# Entry2
		# self.entry_aurelius_two = Gtk.Entry()
		# self.entry_aurelius_two.set_placeholder_text("Command")
		table_aurelius.attach(self.commands_combo, 0, 2, 3, 4)

		# LabelRight
		self.label_aurelius_save_command_confirm = Gtk.Label(label="Click to execute command : ", angle=0, halign=Gtk.Align.START)
		table_aurelius.attach(self.label_aurelius_save_command_confirm, 2, 4, 2, 3)

		# Button22
		self.button_aurelius_execute_command = Gtk.Button(label="Execute command")
		table_aurelius.attach(self.button_aurelius_execute_command, 2, 4, 3, 4)
		self.button_aurelius_execute_command.connect("clicked", self.on_button_aurelius_execute_command_clicked)

		##############################################################
		# Email
		##############################################################
		# Label3
		self.label_aurelius_three = Gtk.Label(label="email", angle=0, halign=Gtk.Align.START)
		table_aurelius.attach(self.label_aurelius_three, 0, 2, 4, 5)

		# Entry3
		self.entry_aurelius_current_email = Gtk.Entry()
		self.entry_aurelius_current_email.set_text("blackberry01@knowroaming.com")
		table_aurelius.attach(self.entry_aurelius_current_email, 0, 2, 5, 6)

		# Button31
		self.button_aurelius_save_email = Gtk.Button(label="Save Email")
		table_aurelius.attach(self.button_aurelius_save_email, 2, 4, 4, 5)
		self.button_aurelius_save_email.connect("clicked", self.on_button_aurelius_save_email_clicked)

		# Button32
		self.button_aurelius_saved_email = Gtk.Button(label="Saved Email : ")
		table_aurelius.attach(self.button_aurelius_saved_email, 2, 4, 5, 6)

		##############################################################
		# Password
		##############################################################
		# Label4
		self.label_aurelius_four = Gtk.Label(label="password", angle=0, halign=Gtk.Align.START)
		table_aurelius.attach(self.label_aurelius_four, 0, 2, 6, 7)

		# Entry4
		self.entry_aurelius_four = Gtk.Entry()
		self.entry_aurelius_four.set_text("qwerty")
		table_aurelius.attach(self.entry_aurelius_four, 0, 2, 7, 8)

		# Button41
		self.button_aurelius_save_password = Gtk.Button(label="Save Password")
		table_aurelius.attach(self.button_aurelius_save_password, 2, 4, 6, 7)

		# Button41
		self.button_aurelius_saved_password = Gtk.Button(label="Saved Password : ")
		table_aurelius.attach(self.button_aurelius_saved_password, 2, 4, 7, 8)

		##############################################################
		# Vendor
		##############################################################

		self.label_aurelius_vendor_select = Gtk.Label(label="Select Vendor : ", angle=0, halign=Gtk.Align.START)
		table_aurelius.attach(self.label_aurelius_vendor_select, 0, 2, 8, 9)

		vendor_store = Gtk.ListStore(int, str)
		vendor_store.append([168011, "ZTE"])
		vendor_store.append([2, "POP"])
		vendor_store.append([168121, "COOLPAD"])
		vendor_store.append([168118, "BLACKBERRY"])
		self.vendor_combo = Gtk.ComboBox.new_with_model_and_entry(vendor_store)
		self.vendor_combo.connect("changed", self.on_vendor_combo_changed)
		self.vendor_combo.set_entry_text_column(1)
		self.vendor_combo.set_active(0)
		table_aurelius.attach(self.vendor_combo, 0, 2, 9, 10)

		##############################################################
		# Output
		##############################################################
		# AureliusPreview
		# self.frame_aurelius_placeholder = Gtk.Frame(label="Preview")
		# self.frame_aurelius_placeholder.set_label_align(0.5, 0.5)
		# self.frame_aurelius_placeholder.set_shadow_type(Gtk.ShadowType.IN)
		# self.image_aurelius_placeholder = Gtk.Image.new_from_file('aurelius_placeholder.jpg')
		# self.frame_aurelius_placeholder.add(self.image_aurelius_placeholder)
		# table_aurelius.attach(self.frame_aurelius_placeholder, 0, 2, 11, 12)

		# aureliusTextViewOutput
		self.frame_aurelius_output_placeholder = Gtk.Frame(label="Output")
		self.frame_aurelius_output_placeholder.set_label_align(0.5, 0.5)
		self.frame_aurelius_output_placeholder.set_shadow_type(Gtk.ShadowType.IN)
		self.textbuffer_output = Gtk.TextBuffer()
		self.textview_output = Gtk.TextView(buffer=self.textbuffer_output)
		self.textview_output.set_wrap_mode(Gtk.WrapMode.WORD)

		self.frame_aurelius_output_placeholder.add(self.textview_output)
		table_aurelius.attach(self.frame_aurelius_output_placeholder, 0, 4, 16, 21)

		# JacksTools end


		# Continue stack
		self.resizer_button = Gtk.Button(label="AugustusBase64Tools")
		self.stack.add_titled(table_base64, "base64tools", "AugustusTools : Base64")
		self.stack.add_titled(table, "generator", "JuliusTools : Generator")
		self.stack.add_titled(table_aurelius, "aureliustools", "AureliusTools : Network Gym : API Exerciser")
	##############################################################
	def on_button_generate_clicked(self, widget):
		width_value = self.entry_width.get_text()
		width_value_int = int(width_value)
		print('Width %s' % width_value )
		height_value = self.entry_height.get_text()
		height_value_int = int(height_value)
		print('Height %s' % height_value)
		displaytext_value = self.entry_displaytext.get_text()
		print(displaytext_value)
		fontname = 'FreeMono.ttf'
		fontsize = 20

		color_text = 'black'
		color_outline = 'red'
		color_background = 'transparent'

		# self.image_generated = Image.new('RGBA', (width_value_int, height_value_int), color_background)
		self.image_generated = Image.new('RGBA', (width_value_int, height_value_int))
		self.image_draw_generated = ImageDraw.Draw(self.image_generated)
		font = ImageFont.truetype(fontname, fontsize)
		self.image_draw_generated.text((2, height_value_int/2), displaytext_value, fill=color_text, font=font)
		self.image_generated.save('image_generated_output.png')

	##############################################################
	def on_button_save_clicked(self, widget):
		print("Saving...")

	##############################################################
	def on_button_to_base64_clicked(self, widget):
		print("To base64...")
		plaintext_value = self.entry_base64_plaintext.get_text()
		print("Plaintext:")
		print(plaintext_value)
		ciphertext_value = base64.b64encode(bytes(plaintext_value, 'utf-8'))
		self.entry_base64_ciphertext.set_text(ciphertext_value)
		print(ciphertext_value)

	##############################################################
	def on_button_from_base64_clicked(self, widget):
		print("From base64...")

	##############################################################
	def on_button_aurelius_save_base_url_clicked(self, widget):
		# base_url_value = self.entry_aurelius_base_url.get_text()
		# self.label_aurelius_base_url.set_text("BaseURL : " + base_url_value)
		# self.textbuffer_output.set_text("Saved : " + base_url_value)
		print("on_button_aurelius_save_base_url_clicked")

	##############################################################
	def on_environments_combo_changed(self, combo):
		environments_entry_txt = combo.get_active_text()
		if environments_entry_txt != None:
			self.base_url_value = environments_entry_txt
			self.textbuffer_output.set_text("Changed... %s " % environments_entry_txt)

	##############################################################
	def on_commands_combo_changed(self, combo):
		commands_entry_txt = combo.get_active_text()
		if commands_entry_txt != None:
			self.selected_command = commands_entry_txt
			self.button_aurelius_execute_command.set_label("Execute command : %s " % commands_entry_txt)
			self.textbuffer_output.set_text("You are logged in as the following user : account_number : %s" % self.account_number)

	##############################################################
	def on_button_aurelius_do_login_clicked(self, widget):
			self.textbuffer_output.set_text("Login...")
			login_value = self.entry_aurelius_current_email.get_text()
			self.selected_command = "verifyLogin_n"
			# password_value = self.entry_aurelius_four.get_text()
			self.hashed_password = hashlib.md5(self.entry_aurelius_four.get_text().encode('utf-8')).hexdigest()
			password_value = self.hashed_password
			self.current_request = self.base_url_value \
			+ "login=" + login_value \
			+ "&password=" + password_value \
			+ "&cmd=" + self.selected_command \
			+ "&startTime=1499956971244&startingPosition=-2&intervalInDays=-1&phoneOS=iOS&phoneModel=iPad";
			print("Request \n" + self.current_request)
			response = urllib.request.urlopen(self.current_request)
			charset_encoding = response.info().get_content_charset()
			content = response.read()
			json_data = json.loads(content.decode(charset_encoding))
			# soup = BeautifulSoup(content.decode(charset_encoding))
			self.account_number = json_data['account_number']
			self.email = json_data['email']
			self.account_token = json_data['account_token']

			# self.textbuffer_output.set_text("Response ...account_number : %s" % soup)
			self.textbuffer_output.set_text("You are logged in as the following user : account_number : %(1)s : email : %(2)s" % {"1" : self.account_number, "2" : self.email})
	##############################################################
	def on_button_aurelius_execute_command_clicked(self, widget):
			self.current_request = self.base_url_value + "cmd=" \
			+ self.selected_command \
			+ "&account_number=" \
			+ self.account_number \
			+ "&account_token=" \
			+ self.account_token \
			+ "&ver=" \
			+ self.ver \
			+ "&vendorId=" \
			+ self.vendorId \
			+ "&chipsetVendorId=" \
			+ self.chipsetVendorId \
			+ "&oemBrandingSelectorId=" \
			+ self.oemBrandingSelectorId \
			+ "&appVersion=" \
			+ self.appVersion \
			+ "&phoneOS=" \
			+ self.phoneOS \
			+ "&phoneModel=" \
			+ self.phoneModel
			print("Request \n" + self.current_request)
			response = urllib.request.urlopen(self.current_request)
			charset_encoding = response.info().get_content_charset()
			content = response.read()
			json_data = json.loads(content.decode(charset_encoding))
			# soup = BeautifulSoup(content.decode(charset_encoding))
			self.status = json_data['status']
			self.textbuffer_output.set_text("status : %s" % self.status)
			# self.textbuffer_output.set_text("status : %s" % soup)
			# self.textbuffer_output.set_text("status : %s" % json_data)

	##############################################################
	def on_button_aurelius_save_email_clicked(self, widget):
		self.button_aurelius_saved_email.set_label(self.entry_aurelius_current_email.get_text())
		print("Saving " + self.entry_aurelius_current_email.get_text())
	##############################################################
	def on_vendor_combo_changed(self, combo):
		tree_iter = combo.get_active_iter()
		if tree_iter != None:
			model = combo.get_model()
			row_id, name = model[tree_iter][:2]
			print("Selected: ID=%d, name=%s" % (row_id, name))
			self.vendorId = str(row_id)
	##############################################################
win = DastoolsWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
