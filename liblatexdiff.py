import os, os.path, subprocess

def runCommand(cmd, stdout = None):
    ''' Runs the command and returns an appropriate string '''
    try:
      retcode = subprocess.call(cmd, stdout = stdout)
      if retcode == 0:
          message = "OK"
      else:
          message = "failed (retcode: %s)" % retcode
    except OSError, e:
        message = "failed, %s" % e
    return(message)

def latexdiff(old_tex, new_tex, diff_tex = None):
  ''' Run latexdiff for the above input '''
  print "Running latexdiff: %s" % runCommand(("latexdiff", old_tex, new_tex), stdout = diff_tex)
  print "diff stored in %s" % diff_tex.name

def pdflatex(tex_file, log_file = None):
  ''' Run pdflatex on the resulting tex file '''
  print "Running pdflatex: %s" % runCommand(("pdflatex", tex_file), stdout = log_file)

def printHelp():
  print """A command line tool to create diff pdf's from git and mercurial repos.
The script will automatically detect if the repo is git or hg.
  
Usage:
  scm-latexdiff OLD:FILE [NEW:FILE]
  
The default NEW is HEAD

Paul Hiemstra, 2012
"""
  exit()
  
def gitOrHg():
  if os.path.exists(".hg"):
    git = False
  elif os.path.exists(".git"):
    git = True
  else:
    print "Error, no Git or Mercurial repository present."
    exit()    
  return git
  
def dumpGitFile(git_fileloc, output_fileobj = None):
  ''' Dumping the file in 'git_fileloc' to a file open at 'output_fileobj' '''
  print "Dumping %s: %s" % (git_fileloc, runCommand(("git","show", git_fileloc), stdout = output_fileobj))

def dumpHgFile(hg_fileloc, output_fileobj = None):
  hgfile_split = hg_fileloc.split(":")
  rev = hgfile_split[0]
  hgfile = hgfile_split[1]
  print "Dumping %s: %s" % (hg_fileloc, runCommand(("hg","cat", "-r %s" % rev, hgfile), stdout = output_fileobj))

def bibtex(aux_file, log_file = None):
  print "Running bibtex: %s" % runCommand(("bibtex", aux_file), stdout = log_file)

def compileDiffPdf(log_file = None):
  pdflatex("diff.tex", log_file)
  bibtex("diff.aux", log_file)
  pdflatex("diff.tex", log_file)
  pdflatex("diff.tex", log_file)

def processCmdlineArgs(argv, git):
  try:
    old_fileloc = argv[1]
  except IndexError:
    printHelp()    
  if old_fileloc in ["-h","h","--help","help","--h"]:
    printHelp()    
  try:
    new_fileloc = argv[2]
  except IndexError:
    if git:
      new_fileloc = "HEAD:" + old_fileloc.split(":")[1]  
    else:
      new_fileloc = "tip:" + old_fileloc.split(":")[1]  
  return old_fileloc, new_fileloc
