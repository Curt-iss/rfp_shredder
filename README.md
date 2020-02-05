RFP_Shredder
===============================================================================
Highlight Search Terms and Analyze Request For Proposals (RFPs)

Contents
-------------------------------------------------------------------------------
- [RFP_Shredder](#rfp_shredder)
  - [Contents](#contents)
  - [Project Success and End Goal](#project-success-and-end-goal)
  - [Unknowns](#unknowns)
  - [Gallery](#gallery)
  - [Features](#features)
  - [Usage](#usage)
    - [Windows](#windows)
      - [Crap to Install](#crap-to-install)
      - [Crap To Do](#crap-to-do)
    - [MacOS](#macos)
      - [Crap to Install](#crap-to-install-1)
      - [Crap to Do](#crap-to-do-1)
  - [TODO List](#todo-list)
    - [Backlog](#backlog)
    - [Weekly Sprints](#weekly-sprints)


Project Success and End Goal
-------------------------------------------------------------------------------


Unknowns
-------------------------------------------------------------------------------


Gallery
-------------------------------------------------------------------------------

![Application's Home Page](./images/Screenshot_Main_Page.png)


Features
-------------------------------------------------------------------------------

Usage
-------------------------------------------------------------------------------

### Windows

#### Crap to Install

1. [Node.js](https://nodejs.org/en/download/)
   1. I have the 'Current' versions installed on Ubuntu, but which version you install here won't really matter.
2. [WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
   1. __WARNING:__ I haven't been able to get electron to run in WSL, yet. It seems like WSL doesn't support GUI applications, and electron needs a version of chromium to run. But, installing the WSL is still the Windows recommended way to develop Node.js on Windows.
   2. Dr. Brown's Lab actually has some [Bash tutorials](https://docs.google.com/document/d/1RamTOnZqMghshHrruyBtOo_gDqxQ8DrCzV1SlGbCDJQ/edit) if you're unfamiliar with a command line. Skip the setting up a Linux VM, and try using VS Code to connect to the WSL. In VS Code, you can pull up a terminal (type CTRL+` (Right next to the '1')). Let me know what you think of the tutorial if you try it out, so I can give feedback.
   3.  When your picking your version of linux to install, I'd pick Ubuntu.
3. [Visual Studio (Code?)](https://code.visualstudio.com/Download)
   1. [How to install extensions in VS Code](https://code.visualstudio.com/docs/editor/extension-gallery)
   2. Recommended Plugins for Node + Python development
      1. Python by Microsoft
      2. Prettier by Esben Petersen
      3. ESLint by Dirk Baeumer
      4. WSL extension by Microsoft (I forgot the exact name)

#### Crap To Do

1. Cloning the repo 
   1. With VS Code connected to the WSL, pull up a terminal
   2. Commands:
```bash
cd # Change directory to home
git clone https://github.com/Curt-iss/rfp_shredder # Clone our repo
cd rfp_shredder
```
2. Congrats, you're stuck at the same point as me.
   1. I think the next thing to do is symlink to the node.js executable you installed. Instructions coming when I figure it out.


### MacOS

I honestly don't have a Mac, so I'm not 100% sure. These are more general Unix steps to follow.

#### Crap to Install

1. [Homebrew](https://brew.sh/)
2.  Node.js 
    1.  If you installed Homebrew, open a terminal and enter: `brew install node`
    2. If you didn't install Homebrew, [nodejs.org](https://nodejs.org/en/download/) 
3. [Visual Studio Code](https://code.visualstudio.com/Download)
   1. [How to install extensions in VS Code](https://code.visualstudio.com/docs/editor/extension-gallery)
   2. One time, I heard VS Code is already installed on MacOS?
   3. Recommended Plugins for Node + Python development
      1. Python by Microsoft
      2. Prettier by Esben Petersen
      3. ESLint by Dirk Baeumer

#### Crap to Do

1.  Brush up on Bash, if you're unfamiliar
    1.  Dr. Brown's Lab actually has some [Bash tutorials](https://docs.google.com/document/d/1RamTOnZqMghshHrruyBtOo_gDqxQ8DrCzV1SlGbCDJQ/edit) if you're unfamiliar with a command line. Skip the setting up a Linux VM. In VS Code, you can pull up a terminal (type CTRL+` (Right next to the '1')). Let me know what you think of the tutorial if you try it out, so I can give feedback.
2. Cloning the repo 
   1. With VS Code open, pull up a terminal
   2. Commands:
```bash
  cd # Change directory to home, maybe change to a directory where you 
     # always put your school work?
  git clone https://github.com/Curt-iss/rfp_shredder # Clone our repo
  cd rfp_shredder
```
3. Starting Electron
   1. Theoretically, `npm` and `node` got installed together, so this should work
   2. In a terminal enter: `npm i && npm start`
      1. Did a pretty box open up?

TODO List
-------------------------------------------------------------------------------

### Backlog

- Learn how to exchange work with GitHub
- Propose electron to TeraThink contacts
- Figure out File upload to electron
- Packaging application and distribution 
- PDF conversion software
- Do we have access to Adobe?
- Annotate RFP document
- Search for keywords
- Highlight and capitalize words
- Maintain page numbers
- Figure out how to export a file from the application


### Weekly Sprints

Sprint 1: File upload 

Sprint 2: Conversion to text file

Sprint 3: RFP keyword search, highlight, capitalization (maintain page numbers

Sprint 4: Exporting and cleaning up final project
