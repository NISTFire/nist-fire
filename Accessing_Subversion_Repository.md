# Introduction #

[Google Code](http://code.google.com) uses [Subversion](http://subversion.tigris.org) (SVN) for version control.  Subversion is widely considered as an improved versioning method over CVS.  This Wiki page provides instructions on using a browser called _SmartSVN_ or the command line to obtain files from the NIST-FIRE SVN Repository.

# Using SVN via the Browser SmartSVN #

[SmartSVN](http://smartsvn.com) is available as freeware.  A for-purchase version of _SmartSVN_ is available that has additional capabilities, but for most users the free version will suffice.

## Checking out the Repository via SVN ##

### The First Time ###

  * After installing _SmartSVN_, launch the program.
  * The program will open with a _Welcome to SmartSVN_ window.  Select **Check out project from repository**.
  * A _Check Out Repository_ window will open.
  * In the **Server Name** box, for anonymous checkout, type

```
http://nist-fire.googlecode.com/svn/trunk/
```

> or if you have commit privileges, type

```
https://nist-fire.googlecode.com/svn/trunk/
```

  * Click **Next**
  * _SmartSVN_ will scan the repository in display a directory tree.
  * Click **Next**
  * Click **No** to avoid checking out files up to the project root.
  * Type in or browse to a **Local directory** where the files will be stored on your computer.
  * Ensure that the **Check Out: Directly into the above directory** and **Check out recursively** options are selected.
  * Click **Next**.
  * Enter a name for the new project, e.g., **NIST-FIRE**.
  * Click **Finish** to check out the files to your machine.

At this point, the entire NIST-FIRE project will be copied from the repository to your computer.

### After the First Time ###

  * After launching _SmartSVN_, select **Open Existing project(s):**
  * Select the **Project Name** you wish update
  * Click **OK**
  * You can now select either a file or a subdirectory and click the green arrow to update your local files from the repository.


# Using SVN at the Command Line #

If you have SVN command line client installed, you can check out the NIST-FIRE repository using the command line version of SVN.

You can download the command line client for your platform here:
http://subversion.tigris.org/project_packages.html

Open a terminal/shell session and change to the directory that you want the NIST-FIRE project folder to be placed within. We recommend that you be in your home directory.

## Anonymous Checkout ##

If you are not a member of the NIST-FIRE development team, then type:

```
svn co http://nist-fire.googlecode.com/svn/trunk/ NIST-FIRE
```

Note the use of "http" for an anonymous checkout. If you want to check out an older version of the repository or you want to only check out part of the repository, there are options for doing so. For example, to check out only the Projects folder for SVN number 200, do this:

```
svn co -r 200 http://nist-fire.googlecode.com/svn/trunk/Projects NIST-FIRE-Projects
```

Note that the new directory called `NIST-FIRE-Projects` will appear in the present working directory. There is nothing special about the name you choose, but it is recommended that you do not use blanks in the name.

## Developer Checkout ##

As a member of the NIST-FIRE development team with commit privileges, type:

```
svn co https://nist-fire.googlecode.com/svn/trunk/ NIST-FIRE --username [your developer username]
```

Note the use of "https" for a developer checkout. Also, your developer username is often the same as your gmail address.

You will be prompted for your password, but this is _**NOT**_ the password for your Google Account_, this is a special Google Code password that you can find through a link under the "Source" tab of the Google Code NIST-FIRE project site.  It will be a random bunch of numbers and letters and nothing that you can specify. NOTE: the link will not be available unless you are a Project Member or Owner._

Either way, a directory called NIST-FIRE will appear in the directory where you executed the checkout command (the 'co' part of the string), with the contents of the NIST-FIRE repository contained within.

## Updates ##

To update your local copy of the repository, go to the sub-directory that you want to update (NIST-FIRE in the example above) and type:

```
svn update
```

NOTE: This could be used to update any of the sub-directories under NIST-FIRE.  If you change down to a subdirectory, like 'Projects' and execute the svn update command, only that directory will be updated.

If you want to return to an older version, type:

```
svn update -r 1234
```

where 1234 is the SVN number you want to return to. If you want to get back to the latest, just redo the svn update without the -r.

## Excluding sub-directories from update ##

The NIST-FIRE repository is quite large in size. If you want to exclude certain sub-directory from your local version, you can use the '--set-depth exclude' option of the svn update command. For instance, to exclude the 'Training' sub-directory from your future updates type:

```
svn update --set-depth exclude NIST-FIRE /Equipment
```

## Commit Log ##

To obtain a log of transactions for that particular sub-directory, type:

```
svn log -r N:M > text_file.txt
```

Which will record all transactions from SVN revision N to M in the file text\_file.txt
By switching the order of the revision numbers you can sort the log in ascending or descending order by revision number.

## Status ##

To see which local files are different from those in the Repository, type:

```
svn status | grep -v '?'
```

This is a very useful command. If you first do an svn update and then the status command, you will know what is different on your system. It is a good habit to do this at the start and end of the day. Try to avoid having too many modified files on your system.

## Info ##

To find out repository details such as the revision number or who made the last change
use the `svn info` command.

For example, cd'ing into the `Equipment` directory and typing `svn info` results in the following output:

```
Path: .
Working Copy Root Path: /Users/koverholt/Repos/NIST-FIRE
URL: https://nist-fire.googlecode.com/svn/trunk/Equipment
Repository Root: https://nist-fire.googlecode.com/svn
Repository UUID: 0dc9d3fe-6b89-d991-a054-10efd4949ef8
Revision: 668
Node Kind: directory
Schedule: normal
Last Changed Author: koverholt
Last Changed Rev: 596
Last Changed Date: 2014-08-28 10:07:08 -0400 (Thu, 28 Aug 2014)
```


## Edit Existing Commit Log Entry ##

To edit an existing commit log entry (developers only):

```
svn propset -r N --revprop svn:log "[new log message]" https://nist-fire.googlecode.com/svn/trunk/ --username [dev. username]
```

This will replace the log entry for SVN revision N, with the text placed in quotes.  Note, this command will prompt for your GoogleCode password, which is the password in your profile, and **not** your Google Account password.