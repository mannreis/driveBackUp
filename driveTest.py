from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import GoogleDriveFile

from os import mkdir
# Authenticate the client.
gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)

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
					file.content.close()
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
	