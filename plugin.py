import irc
import threading
import time
import imp

class plugin_thread( threading.Thread ):
	plist = []
	trusted = []
	def __init__( self, server, plugins, trusted ):
		threading.Thread.__init__(self)
		self.server = server;
		self.trusted = trusted
		for plug in plugins:
			loaded = self.load_plugin( plug )
			if loaded:
				print( "        loaded plugin " + plug )
			
	def run( self ):
		while True:
			time.sleep(10)

	def load_plugin( self, name ):
		try:
			fp, pathname, description = imp.find_module( name )
			plugin = imp.load_module( name, fp, pathname, description )
			self.plist.append( plugin )
			if plugin.plugin.do_init:
				plugin.plugin.init(plugin)
			return True
		except Exception as e:
			print( "Could not load module " + name + ":", e )
			return False

	def unload_plugin( self, plug ):
		if plug in self.plist:
			self.plist.remove( plug )
			return True
		else:
			return False

	def unload_plugin_handle( self, name ):
		for plug in self.plist:
			if plug.plugin.handle == name:
				self.unload_plugin( plug )
				return True
				break
		return False

	def exec_cmd( self, message ):
		args = message["message"].split()
		command = args[0][1:]
		
		for plug in self.plist:
			if plug.plugin.handle == command:
				try:
					if plug.plugin.method == "string":
						plug.plugin.run( plug.plugin, self, self.server, 
							message["nick"], message["channel"], message["message"] );
					elif plug.plugin.method == "args":
						plug.plugin.run( plug.plugin, self, self.server, message["nick"], message["channel"], args );
				except Exception as ie:
					print( "Error in " + str(plug) + ", unloading.\nError:", ie )
					self.unload_plugin( plug )

	def get_trusted( self ):
		return self.trusted

	def get_handles( self ):
		handles = []
		for plug in self.plist:
			handles.append( plug.plugin.handle );
		return handles

	def add_trusted( self, name ):
		self.trusted.append( name )

	def remove_trusted( self, name ):
		if name in self.trusted:
			self.trusted.remove( name )

