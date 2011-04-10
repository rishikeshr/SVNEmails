#!/usr/bin/env python

"""
This code sends email to the specified list of subscribers. 
The email contains the information about latest code thats checked into 
the subversion repository.

Change History
=======================================
Version No | Details | Date
=======================================
1.0 | Base Version | 08-Apr-2011
=======================================
"""

__author__ = "Rishikesh R"
__copyright__ = "Copyright 2011."
__license__ = "All Rights Reserved."
__version__ = "version 1.0"
__email__ = "r.rishikesh@gmail.com"



import ConfigParser
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
import os

config = ConfigParser.ConfigParser()
DELIMITER = ','
retVal = 0
SERVER = ""
PORT = ""
EMAILUSER = ""
EMAILPWD = ""
MAILCONTENT = ""
SMTPServer = ""

def loadConfigFile( configFilePath ):
    config.read( configFilePath )


def command_output( cmd ):
    " Capture a command's standard output. "
    import subprocess
    return subprocess.Popen( 
      cmd.split(), stdout = subprocess.PIPE ).communicate()[0]

def sendPostCommitEmail( configObj, toaddrs, fromaddr, subject, message ):
    """
        This method sends the email to the user.
    """
    '''  Server Details '''
    SERVER = configObj.get( "SERVERCONFIG", "SMTPSERVER" )
    PORT = configObj.get( "SERVERCONFIG", "SMTPSERVERPORT" )
    EMAILUSER = configObj.get( "SVNEMAILUSERCONFIG", "SVNUSER" )
    EMAILPWD = configObj.get( "SVNEMAILUSERCONFIG", "SVNUSERPWD" )

    ''' Email Contents '''
    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddrs
    msg['Subject'] = subject

    msg.attach( MIMEText( message ) )

    """ 
    Sending the emails 
    
    """
    emailserver = smtplib.SMTP( SERVER, PORT );
    emailserver.set_debuglevel( 1 )
    emailserver.starttls();
    emailserver.login( EMAILUSER, EMAILPWD );
    emailserver.sendmail( fromaddr, toaddrs, msg.as_string() );
    emailserver.quit();


def getSVNCommitInformation( repositoryPath, revVersion ):
    svnlookString = '/usr/bin/svnlook author -r {0} {1}'.format( revVersion, repositoryPath )
    commitAuthorName = command_output( svnlookString )
    svnlookString = '/usr/bin/svnlook date -r {0} {1}'.format( revVersion, repositoryPath )
    commitDate = command_output( svnlookString )
    informationString = 'Code Committed to {0} by {1} on {2}'.format( repositoryPath, commitAuthorName, commitDate )
    return informationString


def getSVNCommitDiffInformation( repositoryPath, revVersion ):
    svnlookString = '/usr/bin/svnlook diff -r {0} {1}'.format( revVersion, repositoryPath )
    commitDiff = command_output( svnlookString )
    return commitDiff


def processEmailContent( configObj, subject, content ):
    ''' Email Details '''
    toList = configObj.get( "MAILERLIST", "TOLIST" )
    frmAddr = configObj.get( "MAILERLIST", "FROMID" )
    message = content
    ''' Sending Email '''
    sendPostCommitEmail( configObj , toList , frmAddr, subject, message )

if __name__ == "__main__":
    import sys
    repository = sys.argv[1]
    rev = sys.argv[2]
    configFile = sys.argv[3]
    loadConfigFile( configFile )
    msgContent = getSVNCommitDiffInformation( repository, rev )
    msgSubject = getSVNCommitInformation( repository , rev )
    processEmailContent( config, msgSubject, msgContent )


