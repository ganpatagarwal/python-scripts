import subprocess as sp

psResult = sp.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',
'Get-Module','-list'],stdout = sp.PIPE, stderr = sp.PIPE)

output, error = psResult.communicate()
rc = psResult.returncode

print "Return code given to Python script is: " + str(rc)
print "\n\nstdout:\n\n" + str(output)
print "\n\nstderr: " + str(error)