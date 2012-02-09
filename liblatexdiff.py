import os, os.path, subprocess, tempfile, glob

def showHelp(argv):
  ''' Determine whether or not to shows the usage to the user '''
  try:
    old_fileloc = argv[1]
  except IndexError:
    printHelp()    
  if old_fileloc in ["-h","h","--help","help","--h"]:
    printHelp()    

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
  ''' Print usage information and quit the program '''
  print """A command line tool to create diff pdf's from git and mercurial repos.
The script will automatically detect if the repo is git or hg. The 
result is a pdf with the differences between the revisions, diff.pdf.
  
Usage:
  scm-latexdiff OLD:FILE [NEW:FILE]
  
where:
  OLD:    old revision id, local for non-commited
  NEW:    new revision id, local for non-commited
  FILE:   filename of the file you want to diff
  
examples:
 # for hg
 scm-latexdiff 4:spam.tex
 scm-latexdiff 4:spam.tex 6:spam.tex
 # for git
 scm-latexdiff 87213:spam.tex
 scm-latexdiff 87213:spam.tex 97123:spam.tex
 # You can also diff against non-commited (local) files
 scm-latexdiff local:spam.tex
 scm-latexdiff 2:spam.tex local:spam.tex

Notes:
The NEW:FILE argument is optional, default NEW is 'HEAD' when using git, 
and 'tip' when using hg. When referring to a git revision, not the whole
sha1 key is needed, you can just provide the first few numbers.

Paul Hiemstra, paul AT numbertheory.nl"""
  exit()
  
def gitOrHg():
  ''' Determine whether we are in a git or mercurial repository'''
  if os.path.exists(".hg"):
    print "Detected Mercurial repository..."
    git = False
  elif os.path.exists(".git"):
    print "Detected Git repository..."
    git = True
  else:
    print "Error, no Git or Mercurial repository present."
    exit()    
  return git

def dumpLocalFile(f, output_fileobj = None):
  ''' Do not dump from the repository, but dump a local file. '''
  print "Dumping a local file %s: %s" % (f, runCommand(("cat", f), stdout = output_fileobj))

def dumpGitFile(git_fileloc, output_fileobj = None):
  ''' Dumping the file in 'git_fileloc' to a file open at 'output_fileobj' '''
  gitfile_split = git_fileloc.split(":")
  rev = gitfile_split[0]
  gitfile = hgfile_split[1]
  if rev == "local":
    dumpLocalFile(gitfile, output_fileobj)
  else:
    print "Dumping %s: %s" % (git_fileloc, runCommand(("git","show", git_fileloc), stdout = output_fileobj))

def dumpHgFile(hg_fileloc, output_fileobj = None):
  ''' Dumping the file in 'git_fileloc' to a file open at 'output_fileobj' '''
  hgfile_split = hg_fileloc.split(":")
  rev = hgfile_split[0]
  hgfile = hgfile_split[1]
  if rev == "local":
    dumpLocalFile(hgfile, output_fileobj)
  else:
    print "Dumping %s: %s" % (hg_fileloc, runCommand(("hg","cat", "-r %s" % rev, hgfile), stdout = output_fileobj))

def bibtex(aux_file, log_file = None):
  ''' Run bibtex on the diff.aux file to get working citations '''
  print "Running bibtex: %s" % runCommand(("bibtex", aux_file), stdout = log_file)

def compileDiffPdf(log_file = None):
  ''' Compile diff.pdf based on diff.tex '''
  if not log_file is None:
    log_file = open(log_file, "w")
  pdflatex("diff.tex", log_file)
  bibtex("diff.aux", log_file)
  pdflatex("diff.tex", log_file)
  pdflatex("diff.tex", log_file)
  if not log_file is None:
    log_file.close()


def processCmdlineArgs(argv, git):
  ''' Process the command line arguments given by the user '''
  old_fileloc = argv[1]
  try:
    new_fileloc = argv[2]
  except IndexError:
    if git:
      new_fileloc = "HEAD:" + old_fileloc.split(":")[1]  
    else:
      new_fileloc = "tip:" + old_fileloc.split(":")[1]  
  return old_fileloc, new_fileloc

def dumpFiles2tmp(old_fileloc, new_fileloc, git):
  ''' Create the requested two files, and put them in a temp file. '''
  old_fo = open(tempfile.mkstemp()[1], "w")
  new_fo = open(tempfile.mkstemp()[1], "w")
  if git:
    dumpGitFile(old_fileloc, old_fo)
    dumpGitFile(new_fileloc, new_fo)  
  else:
    dumpHgFile(old_fileloc, old_fo)
    dumpHgFile(new_fileloc, new_fo)
  old_fo.close()
  new_fo.close()
  return old_fo, new_fo
  
def createDiffTex(oldfile, newfile, diff_output = "diff.tex", swaplocal = False):
  ''' Produce diff.tex based on the two files in "oldfile" and "newfile" '''
  diff_tex = open(diff_output, "w")
  if swaplocal:
    latexdiff(newfile, oldfile, diff_tex)
  else:
    latexdiff(oldfile, newfile, diff_tex)
  diff_tex.close()
  
def cleanAllNonePDF():
  ''' Delete all diff files that are not a .pdf file '''
  for filename in glob.glob('diff*') :
    if not "pdf" in filename:
      os.remove(filename)   
