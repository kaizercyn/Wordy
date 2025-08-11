**Saint Louis University**  

**SCHOOL OF ACCOUNTANCY, MANAGEMENT, COMPUTING, and INFORMATION STUDIES**

` `**Computer Science and Computer Applications Department**



**Computer Programming 3** 

**CS222L 07:30-09:00 THF**

**CIS-2022-2-9328**


**Documentation for Final Lab Project**



**Group 5**



***Submitted by*:**

Austria, Jocel 

Emocling, Maria Sheena Shield

Gura, Kaizer Cyn 

Samson, Mik iris 

Solano, Xanthe Nicole 

Vanzuela, Ron Andrei 




**Submitted to:**

Roderick Makil

**Process of creating the Python Client**

**Setting up the Environment For Python**

**Introduction:**

This section provides the step-by-step instructions on how to set up Python, including setting up the necessary environment variables, choosing which version and adding the interpreter.

*Basic Steps to Set Up Python on Windows*

1. Install Python.
1. Set up the environment variables.
1. Install PyCharm.

*Assumptions*

- You are using a 64-bit Windows operating system.
- You have a license for a JetBrains product, such as PyCharm.

*Instructions*

1. Download the Python installer from the official Python website.
1. Run the installer to install Python on your computer.
1. Open a command prompt and type "python". This will verify that Python is installed correctly.
1. Open the environment variables window.
1. Add the following entries to the environment variables:
1. PYTHON\_HOME: The path to the Python installation directory.
1. PATH: Add the path to the Python installation directory to the PATH environment variable, the path to the OMNIORB installation directory, and the path to the OMNIpy installation directory.
1. Close the environment variables window.
1. Download and install PyCharm from the JetBrains website.
1. Open PyCharm and create a new project.
1. You are now ready to start coding in Python!

*Here are some additional tips for setting up Python on Windows:*

- Make sure you install the latest version of Python.
- Use a 64-bit version of Python if you are using a 64-bit Windows operating system.
- Add Python to your environment variables so that you can easily access it from the command prompt.
- Install a Python IDE, such as PyCharm or Visual Studio Code, to help you write and debug Python code.

**Detailed procedure for setting up Python:**

***Installing Python 3.10***

Download and install Python from the official website (<https://www.python.org>)


**BE SURE** that the version of Python that you will be using is Python 3.10 because that is the version that supports CORBA.

To verify that Python is installed correctly, open the command prompt and type "python."




Take note of the location where the.exe file is located; we are going to use that later when setting up the environment variables.















***Setting Up Environment Variables (Python)***

To create an environment variable, open the System search window and search for "environment variable". Then, select Edit the system environment variables from the results.











In the Environment Variables window, select the User variables tab if you want to create an environment variable for your current user account, or select the System variables tab if you want to create an environment variable for all users on the computer. In this case, we want to create an environment variable for all users.

We are now going to create a new environment variable **PYTHON\_HOME.** Press “New…”. This will open a dialogue box where we can fill in the necessary information and values. In the Variable name field, enter **PYTHON\_HOME.** In the Variable value field, enter the path to the Python installation directory. For example, if Python is installed in the C:\Users\andre\AppData\Local\Programs\Python\Python310 directory, you would enter C:\Users\andre\AppData\Local\Programs\Python\Python310. Then click OK.

The new environment variable will now be added to the list of environment variables.

To verify that the environment variable has been created correctly, open a command prompt and type the following command: 

***echo %PYTHON\_HOME%***

If the environment variable has been created correctly, you should see the path to the Python installation directory displayed on the command prompt.

Once you have created the **PYTHON\_HOME** environment variable, you need to modify the existing **PATH** environment variable to include the path to the Python bin directory. To do this, Scroll down the list of environment variables until you find the **PATH** variable. Click edit and In the Variable value field, Click New and enter the value to be inserted, which is **%PYTHON\_HOME%.**

To check if your device has been configured correctly, follow these steps:

1. Open a command prompt by searching for "cmd" in the Windows taskbar.
1. Type the following command:

**python --version**

1. If Python is installed and configured correctly, you should see a response similar to the following:

If you do not see a response similar to the above, Python is not installed or configured correctly. You may need to reinstall Python or modify your environment variables.




***Setting Up Environment Variables (OmniORB)***

To download the omniORBpy-4.3.0-win64-python310 file, follow these steps:

1. Open a web browser and navigate to the following URL:

<https://sourceforge.net/projects/omniorb/files/omniORB/omniORB-4.3.0/>

1. Scroll down to the "Files" section and click on the link for the omniORBpy-4.3.0-win64-python310.zip file.
1. The file will be downloaded to your computer.
1. Once the file has been downloaded, extract the contents to a directory of your choice.

The omniORBpy-4.3.0-win64-python310 file contains the necessary Python bindings for the omniORB object request broker. These bindings allow you to use omniORB from Python.











Open the extracted  File and follow this path: 

\omniORB-4.3.0\bin\x86\_win32

\omniORBpy-4.3.0-win64-python310\omniORBpy-4.3.0\bin\x86\_win32.




\omniORBpy-4.3.0-win64-python310\omniORBpy-4.3.0\lib\x86\_win32.


\omniORBpy-4.3.0-win64-python310\omniORBpy-4.3.0\lib\python.

Add the mentioned directories to the same PATH Variable inside the Environment Variables.


***Installing PyCharm IDE from JetBrains***

Go to this site and download PyCharm:

<https://www.jetbrains.com/pycharm/download/#section=windows>

Once the download finishes, Go ahead and open the Setup.



After the setup has finished, you should have PyCharm in your terminal.






***Difficulties encountered with Python***

1. **Syntax and Structure**

We've never written code in a language other than Java before. We may have needed to clarify the overall syntax at first. Nonetheless, we got through it by consulting online tutorials and asking friends who had already learned the language and were in the same field for help. Because we are accustomed to brackets, using proper colons and indentation is the most challenging aspect of learning the programming language. PS. Thank you very much, Robbie, Vlad, and Tintin 

1. **Environment Setup**

Teaching Python configuration has been difficult due to the numerous steps required and the number of times you have to do this due to the number of groupmates to teach, especially with version 3.10.9. Using an IDE like PyCharm, which has Python extensions and automatically sets up the environment, has been extremely helpful, and teaching the majority of them all at once was a wise decision.














***How to run the program***

`	`After following the steps above on how to download and set up your Python, the following steps are provided on how to run Python.

**STEP 1: Check the Servers Parameter**
**
`	`Use the following as parameters for the Java server, changing the port and host accordingly.

`	`-ORBInitialHost **HOST** - ORBInitialPort **PORT**


**STEP 2: Run the Server**



**STEP 3: Check the Python Clients Parameter**
**
`	`Use the following as parameters for the Python client, changing the port and host accordingly.

`	`-ORBInitRef NameService=corbaname::**HOST**:**PORT**


***STEP 4: Run the Client***

***	

