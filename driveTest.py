from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import GoogleDriveFile
from subprocess import Popen, PIPE

from os import mkdir
# Authenticate the client.
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

sp = Popen(['bash'], shell=True, stdin=PIPE)

def cmd(i):
	sp.stdin.write((i +'\n').encode())


def mimeType(file):
	if file.metadata.get('mimeType') == 'application/vnd.google-apps.folder':
		return 'folder'
	else :
		return 'file'

def inOrder(path, id):
	file_list = drive.ListFile({'q': "'{}' in parents".format(id)}).GetList()
	for file in file_list:
		tipo=mimeType(file)
		if tipo != 'folder':
			fname = file['title'].replace(' ', '_')
			with open('/'.join(path)+'/'+fname, 'wb') as f:
				try:
					s = file.GetContentString(mimetype="application/pdf")
				except:
					s = file.content.read()
				f.write(s)
				
		else:
			d = str(file['title']).replace(" ", "_")
			path.append(d)
			try:
				mkdir('/'.join(path))
			except:
				pass
			inOrder( path , file['id'])
	
	path.pop()


if __name__=="__main__":
	try:
		mkdir('driveTest')
	except:
		pass
	#----------vvvvv DriveTest folder id  vvvvvv
	inOrder(['driveTest'],"1q7NWIY51qf0k2PNMwZ8Z2kioLV6xquv8")
	