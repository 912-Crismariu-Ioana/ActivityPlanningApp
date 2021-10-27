from ui.console import Console
from ui.consoleGUI import ConsoleGUI
from service.activity_service import ActivityService
from service.person_service import PersonService, PersonValidator
from repository.database_people_repo import DatabasePeopleRepo
from repository.person_text_repo import PersonTextFileRepository
from repository.database_activity_repo import DatabaseActivityRepo
from repository.activity_text_repo import ActivityTextFileRepository
from repository.activity_binary_repo import ActivityBinaryRepo
from repository.person_binary_repo import PersonBinaryRepo
from repository.person_json_repo import PersonJsonRepo
from repository.activity_json_repo import ActivityJsonRepo
from repository.test_inits import *
from service.undo import *
from settings import Settings
from tkinter import *
if __name__ ==  "__main__":
    settings = Settings()
    p_val = PersonValidator()
    a_val = ActivityValidator()
    u = Undo()
    if settings.typeofrepo == 'inmemory':
        p_repo = CustomPersonRepo()
        populated_people_repo = PopulatedPeopleRepo()
        updated_people_repo = populated_people_repo.test_init_person()
        a_repo = CustomActivityRepo()
        populated_activity_repo = PopulatedActivityRepo(populated_people_repo)
        updated_activity_repo = populated_activity_repo.test_init_activity()
        p_service = PersonService(updated_people_repo, p_val, u)
        a_service = ActivityService(a_val,updated_activity_repo,updated_people_repo,u)
    elif settings.typeofrepo == 'text file':
        p_repo = PersonTextFileRepository(settings.people_repo)
        a_repo = ActivityTextFileRepository(settings.activity_repo)
        p_service = PersonService(p_repo, p_val, u)
        a_service = ActivityService(a_val, a_repo, p_repo, u)
    elif settings.typeofrepo == 'binary file':
        p_repo = PersonBinaryRepo(settings.people_repo)
        a_repo = ActivityBinaryRepo(settings.activity_repo)
        p_service = PersonService(p_repo, p_val, u)
        a_service = ActivityService(a_val, a_repo, p_repo, u)
    elif settings.typeofrepo == 'json file':
        p_repo = PersonJsonRepo(settings.people_repo)
        a_repo = ActivityJsonRepo(settings.activity_repo)
        p_service = PersonService(p_repo, p_val, u)
        a_service = ActivityService(a_val, a_repo, p_repo, u)
    elif settings.typeofrepo == 'database':
        p_repo = DatabasePeopleRepo()
        a_repo = DatabaseActivityRepo()
        p_service = PersonService(p_repo,p_val,u)
        a_service = ActivityService(a_val,a_repo,p_repo,u)
    if settings.menu == 'gui':
        win = Tk()
        consolegui = ConsoleGUI(p_service, a_service, u, win)
        consolegui.butttons()
        win.mainloop()
    elif settings.menu == 'menu':
        console = Console(p_service,a_service,u)
        console.console()

