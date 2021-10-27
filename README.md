# ActivityPlanningApp
 A small, toy app for planning activities with a Tkinter GUI and multiple options of data storage, including SQLite DBs


****************************************************DISCLAIMER****************************************************

This is the very first more "complex" project that I did in my first semester of university, having little to no prior programming experience. As such, the code is by no means perfect, there are many things that could have been done better, more elegantly or more efficently. However, this little app is still very near and dear to my heart because I learnt a lot while working on it, making it a milestone in my skill development.

****************************************************END DISCLAIMER****************************************************


This app follows the basic layered architecture with:
        -a domain for the entities (people, activities)
        -a repository which stores them and deals with the CRUD operations. Objects can be stored either in memory or in files of different types, each having their respective repository structure: text, binary, JSON and SQLite databases. The option is selected in the settings.properties file.
        -a controller/service where object creation and validation is performed and where the CRUD operations on the repository are recorded in order to allow undos/redos
        -a view/ui package for displaying data and allowing user interaction. User interaction can be done either via console or the GUI. The option is selected in the settings.properties file.
