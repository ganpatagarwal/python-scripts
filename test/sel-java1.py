import subprocess

escape_dict={'\a':r'\a',
           '\b':r'\b',
           '\c':r'\c',
           '\f':r'\f',
           '\n':r'\n',
           '\r':r'\r',
           '\t':r'\t',
           '\v':r'\v',
           '\'':r'\'',
           '\"':r'\"',
           '\0':r'\0',
           '\1':r'\1',
           '\2':r'\2',
           '\3':r'\3',
           '\4':r'\4',
           '\5':r'\5',
           '\6':r'\6',
           '\7':r'\7',
           '\8':r'\8',
           '\9':r'\9'}

def raw(text):
	"""Returns a raw string representation of text"""
	new_string=''
	for char in text:
		try: new_string+=escape_dict[char]
		except KeyError: new_string+=char
	return new_string

#arg = "C:\Program Files (x86)\Internet Explorer\iexplore.exe"
arg = "C:\Softwares\vCenterOrchestratorClient-64bit-5.5.0"
arg = raw(arg)
#subprocess.Popen(arg)
#subprocess.Popen("setx JAVA_HOME 'C:\Program Files\Java\jdk1.7.0_55'")
return_code = subprocess.call("setx JAVA_HOME 'C:\\Program Files\\Java\\jdk1.7.0_55'", shell=True)
print return_code
