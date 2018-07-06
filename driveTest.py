from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from subprocess import Popen, PIPE
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

def inOrder(lvl, id):
	file_list = drive.ListFile({'q': "'{}' in parents".format(id)}).GetList()
	for file1 in file_list:
		tipo=mimeType(file1)
		print('{} {}: {}'.format(lvl*'\t', tipo ,file1['title']))#, file1['id']))
		if tipo != 'folder':
			print('{}Downloading'.format(lvl*'\t'))
			cmd('touch {}'.format(file1['title']))
		else:
			cmd('mkdir {}'.format(file1['title']))
			cmd('cd {}'.format(file1['title']))
			inOrder( lvl + 1 , file1['id'])
	
	cmd('cd ../')


if __name__=="__main__":
	cmd('mkdir driveTest')
	cmd('cd driveTest')
	#----------vvvvv DriveTest folder id  vvvvvv
	inOrder(0,"1q7NWIY51qf0k2PNMwZ8Z2kioLV6xquv8")
	cmd('exit')