import  threading,time,urllib2,urllib,os,re,gtk,pygtk,time

downloadlist=[]



class surf(threading.Thread):
	def __init__(self,url,level,filext):
		self.filext=filext
		self.finish=False
		self.depth=2
		self.url=url
		self.level=level
		if self.level==self.depth :
			self.finish=True
			return
		
		super(surf,self).__init__()
		self.start()
		
	def findextension(self,url):
		m=re.search(r'(.\w+$)',url)
		
		if m:	
			return m.group(1)
		else:
			return ''	
		
	def findurls(self,page):
		content=page.read()
		urllist= re.findall(r'(http://[\w+/.\-_\d+]+)',content)
		return urllist	
	def run(self):
		
		req = urllib2.Request(self.url, headers={'User-Agent' : "Dileeps Browser"}) 
		try:
			self.page = urllib2.urlopen( req )
		except:
			self.finish=True
			return

		if self.page.info().gettype()=='text/html':
			urllist=self.findurls(self.page)
			
			surfthrds=[surf(i,self.level+1,self.filext) for i in urllist]
			childfinish=False
			while not childfinish:
					
				childfinish=True
				for i in surfthrds:
					if not i.finish:
						childfinish=False
						break
				time.sleep(1)		
						
			
				
		else:			
			if self.findextension(self.url)==self.filext and self.url not in downloadlist:
				downloadlist.append(self.url)
				
		
		self.finish=True
		
		return
		




class appgui:
	def findefilename(self,url):
		m=re.search(r'(\w+.\w+$)',url)
		
		if m:	
			
			return m.group(1)
		else:
			return 'file'	
			
	def downloadfiles(self,widget,data):
		self.destpath=os.path.abspath('')+'/'+self.destpath
		try:
			os.mkdir(self.destpath)
			print 'creating folder ',self.destpath,':'
		except:
			print 'creating folder ',self.destpath,':already exist'	
		n=0
		for i in downloadlist :
			urllib.urlretrieve(i,self.destpath+'/'+self.findefilename(i))
			fraction=n/len(downloadlist)
			self.progressbar.set_fraction(fraction)
			
			
	def searchfiles(self,widget,data):
		
		keyword=self.keytextbox.get_text()
		filext=self.exttextbox.get_text()
		self.destpath=self.dirtextbox.get_text()
		
		
		qry=''
		for i in keyword.split(' '):
			qry=qry+'+'+i
		qry=qry+'+'+filext		
		
		s=surf('http://www.google.co.in/search?hl=en&q='+qry,0,filext)	
		
		while not s.finish:
			time.sleep(0.01)	
			
		print 'search result:',
		
		files=''
		for i in downloadlist :
			files=files+'\n'+self.findefilename(i)
			self.listoffiles.set_text(files)
			self.listoffiles.show()
			#urllib.urlretrieve(i,destpath+'/'+self.findefilename(i))
		#if len(downloadlist)>0:
				
		return
		
	def __init__(self):
		self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title("Tutfinder")
		self.window.show()
		self.box=gtk.VBox(False,0)
		self.window.add(self.box)
		self.searchbutton=gtk.Button("Search")
		self.searchbutton.connect("clicked",self.searchfiles,None)
		self.downloadbutton=gtk.Button("Download")
		self.downloadbutton.connect("clicked",self.downloadfiles,None)
		self.progressbar = gtk.ProgressBar(adjustment=None)
		
		
		self.keybox=gtk.VBox(False,0)
		self.extbox=gtk.VBox(False,0)
		self.dirbox=gtk.VBox(False,0)
		self.butbox=gtk.VBox(False,0)
		self.opbox=gtk.VBox(False,0)
		
		self.box.pack_start(self.keybox,False,False,0)
		self.box.pack_start(self.extbox,False,False,0)
		self.box.pack_start(self.dirbox,False,False,0)
		self.box.pack_start(self.butbox,False,False,0)
		self.box.pack_start(self.opbox,False,False,0)
		
		self.keytextbox = gtk.Entry(max=0)
		self.keylabel=gtk.Label("Search keywords")
		self.keybox.pack_start(self.keylabel,False,False,0)
		self.keybox.pack_start(self.keytextbox,False,False,0)
		
		self.exttextbox = gtk.Entry(max=0)
		self.extlabel=gtk.Label("file extension")
		self.extbox.pack_start(self.extlabel,False,False,0)
		self.extbox.pack_start(self.exttextbox,False,False,0)
		
		self.dirtextbox = gtk.Entry(max=0)
		self.dirlabel=gtk.Label("target folder")
		self.dirbox.pack_start(self.dirlabel,False,False,0)
		self.dirbox.pack_start(self.dirtextbox,False,False,0)
		
		self.butbox.pack_start(self.searchbutton,False,False,0)
		self.opframe=gtk.Frame("available files")
		self.listoffiles=gtk.Label("")
		self.opframe.add(self.listoffiles)
		self.opbox.pack_start(self.opframe,False,False,0)
		self.opbox.pack_start(self.downloadbutton,False,False,0)
		self.opbox.pack_start(self.progressbar,False,False,0)
		
		self.window.show_all()
		
		
		
		
		
		
		
		
		
		
		return
	def rungui(self):
		gtk.main()
		return
	

gui=appgui()
gui.rungui()



