import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

def initialize_firestore():
    """
    Create database connection
    """

    # Setup Google Cloud Key - The json file is obtained by going to 
    # Project Settings, Service Accounts, Create Service Account, and then
    # Generate New Private Key
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]  = "courses-83e54-firebase-adminsdk-k5fn4-59e0612f71.json"

    # Use the application default credentials.  The projectID is obtianed 
    # by going to Project Settings and then General.
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'courses-83e54',
    })

    # Get reference to database
    db = firestore.client()
    return db

def get_course_code(db):

    if len(results) == 0:
        print("No courses in database")
        return None
    for i in range(len(results)):
        print(f"{i+1} - {results[i][0]}")
    choice = 0
    while choice < 1 or choice > len(results):
        choice = int(input("Select course: "))
    return results[choice-1][0]

def display_complete():
        # Display past courses and total courses completed

        print("{:>10}  {:>10}  {:>10} {:>10}  {:>10}".format("Year", "Semester", "Course Code", "Grade", "Credits"))

def display_planned():
        # Display planned courses and total courses planned

        print("{:>10}  {:>10}  {:>10} {:>10} {:>10}".format("Year", "Semester", "Course Code", "Grade", "Credits"))


def update_complete():
        # Update past courses
        year = input("Year: ")
        semester = input("Semester: ")
        course_code = input("Course code: ")
        grade = input("Grade: ")
        credits = int(input("Credits: "))

        data = {"year" : year, 
            "semester" : semester,
            "course code" : course_code,
            "grade" : grade,
            "credits" : credits}

        result = db.collection("courses").document(completed).get()
        data = result.to_dict()

        data["courses"] += add_courses
        db.collection("completed").document(course_code).set(data)


        # Save this in the log collection in Firestore
        log_completed(db, f"Added {course_code} to completed")

def update_planned():
        # Add planned courses
        year = input("Year: ")
        semester = input("Semester: ")
        course_code = input("Course code: ")
        grade = input("Grade ('P' for planned courses): ")
        credits = int(input("Credits: "))


        result = db.collection("courses").document(planned).get()
        data = result.to_dict()

        data["courses"] += add_courses
        db.collection("planned").document(course_code).set(data)

        
        # Save this in the log collection in Firestore
        log_planned(db, f"Added {course_code} to planned")

        
def remove_course():
      # Delete completed courses from planned 
        course_code = input("Course code: ")
        if course_code == None:
            continue
    data["course_code"] -= course_code
    db.collection("planned").document(course_code).set(data)

    # Save this in the log collection in Firestore
    log_change(db, f"Removed {course_code} from planned")
def total_credits():
        # Display total credits taken and total credits planned
        pass

def main():
  db = initialize_firestore()
  get_course_code(db)
  choice = None
  while choice != "7":
    print("1: View completed courses ")
    print("2: View planned courses ")
    print("3: Add completed courses ")
    print("4: Add planned courses")
    print("5: Delete courses you have completed from your planned courses")
    print("6: Show total credits taken / planned ")
    print("7: Quit ")
    choice = input("> ")
    print()

    if choice == "1":
        display_complete(db)
    elif choice == "2":
        display_planned(db)
    elif choice == "3":
        update_complete(db)
    elif choice == "4":
        update_planned(db)
    elif choice == "5":
        remove_course(db)
    elif choice == "6":
        total_credits(db)

   
if __name__ == "__main__":
    main()

