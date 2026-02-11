"""
Author: Dele Osuma
exam_scheduler.py
Description:
    reads exam and room CSV files and try to create a one-day schedule
    that assigns each exam to a room using recursive backtracking. The solution uses custom
    Time and TimeInterval classes along with Exam, Room, and Schedule classes.
    
    The scheduler checks that an exam is only assigned to a room if the room's availability
    interval contains the exam's time and if there is no conflict with other exams scheduled
    in that room. Recursive backtracking is used to try out different assignments until a valid
    schedule is found or if no schedule is possible.

    
"""


class Time:
    '''
    Represents a time in 24-hour format.
    '''
    def __init__(self, time_str):
        '''
        Initializes the Time object.

        Parameters:
        time_str (str): Time in 'HH:MM' format.
        '''
        time_parts = time_str.split(':')
        self.hour = int(time_parts[0])
        self.minute = int(time_parts[1])

    def __str__(self):
        '''
        Returns the string representation of the Time object in 'HH:MM' format.
        '''
        return f"{self.hour:02d}:{self.minute:02d}"

    def __eq__(self, other):
        return (self.hour, self.minute) == (other.hour, other.minute)

    def __lt__(self, other):
        return (self.hour, self.minute) < (other.hour, other.minute)

    def __le__(self, other):
        return (self.hour, self.minute) <= (other.hour, other.minute)

    def __gt__(self, other):
        return (self.hour, self.minute) > (other.hour, other.minute)

    def __ge__(self, other):
        return (self.hour, self.minute) >= (other.hour, other.minute)

    def __ne__(self, other):
        return not (self == other)


class TimeInterval:
    '''
    Represents a time interval between a start and an end time.
    '''
    def __init__(self, start, end):
        '''
        Initializes the TimeInterval object.

        Parameters:
        start (Time): Start time of the interval.
        end (Time): End time of the interval.
        '''
        self.start = start
        self.end = end

    def __str__(self):
        '''
        Returns the string representation of the TimeInterval in 'HH:MM - HH:MM' format.
        '''
        return f"{self.start} - {self.end}"

    def disjoint(self, other):
        '''
        Checks if two intervals are disjoint.

        Parameters:
        other (TimeInterval): Another time interval to compare.

        Returns:
        bool: True if intervals are disjoint, False otherwise.
        '''
        return self.end <= other.start or self.start >= other.end

    def contain(self, other):
        '''
        Checks if this interval contains another interval.

        Parameters:
        other (TimeInterval): Another time interval to check.

        Returns:
        bool: True if this interval contains the other, False otherwise.
        '''
        return self.start <= other.start and self.end >= other.end



class Exam:
    '''
    Represents an exam with a name and a time interval.
    '''
    def __init__(self, name, start_str, end_str):
        self.name = name
        self.interval = TimeInterval(Time(start_str), Time(end_str))
    
    def __str__(self):
        return f"{self.name}: {self.interval}"

class Room:
    '''
    Represents a room with a name, availability interval, and a list of scheduled exams.
    '''
    def __init__(self, name, avail_start, avail_end):
        self.name = name
        self.availability = TimeInterval(Time(avail_start), Time(avail_end))
        self.scheduled_exams = []  # list of Exam objects

    def can_schedule(self, exam):
        '''
        Checks if the exam can be scheduled in this room.
        
         - The room’s availability must contain the exam’s time interval.
         - The exam must not conflict with any already scheduled exam in this room.
        '''
        # Check room availability
        if not self.availability.contain(exam.interval):
            return False
        
        # Check for conflict with already scheduled exams (each exam in the room must not overlap)
        for scheduled in self.scheduled_exams:
            # If exam times are not disjoint, there is a conflict.
            if not exam.interval.disjoint(scheduled.interval):
                return False
        return True

    def schedule_exam(self, exam):
        '''
        Adds the exam to the scheduled_exams list.
        '''
        self.scheduled_exams.append(exam)
    
    def remove_exam(self, exam):
        '''
        Removes the exam from the scheduled_exams list.
        '''
        self.scheduled_exams.remove(exam)
    
    def __str__(self):
        if not self.scheduled_exams:
            return ""
        exams_str = "\n\t".join(str(exam) for exam in self.scheduled_exams)
        return f"{self.name} {self.availability}:\n\t{exams_str}"

class Schedule:
    '''
    Represents the exam schedule and contains methods to load data and solve the scheduling problem.
    '''
    def __init__(self):
        self.exams = []  # list of Exam objects
        self.rooms = []  # list of Room objects

    def load_exams(self, exam_file_name):
        '''
        Loads exams from a CSV file.
        file format: exam_name,start_time,end_time
        '''
        try:
            with open(exam_file_name, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(",")
                    if len(parts) != 3:
                        print("Skipping invalid line in exam file:", line)
                        continue
                    name = parts[0].strip()
                    start_time = parts[1].strip()
                    end_time = parts[2].strip()
                    exam = Exam(name, start_time, end_time)
                    self.exams.append(exam)
        except FileNotFoundError:
            print("Error: Exam file not found!")
            return False
        return True

    def load_rooms(self, room_file_name):
        '''
        Loads rooms from the CSV file.
        '''
        try:
            with open(room_file_name, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(",")
                    if len(parts) != 3:
                        print("Skipping invalid line in room file:", line)
                        continue
                    name = parts[0].strip()
                    avail_start = parts[1].strip()
                    avail_end = parts[2].strip()
                    room = Room(name, avail_start, avail_end)
                    self.rooms.append(room)
        except FileNotFoundError:
            print("Error: Room file not found!")
            return False
        return True

    def solve(self):
        '''
        Attempts to assign all exams to rooms using recursive backtracking.
        Returns True if a valid schedule is found, False otherwise.
        '''
        return self._assign_exam(0)

    def _assign_exam(self, exam_index):
        '''
        Recursive helper function to assign exams one by one.
        
        Parameters:
            exam_index (int): The index of the current exam to schedule.
        
        Returns:
            bool: True if a valid assignment is found 
        '''
        # Base Case: All exams have been scheduled
        if exam_index >= len(self.exams):
            return True
        
        exam = self.exams[exam_index]
        
        # Try to assign the exam to each room (in order)
        for room in self.rooms:
            if room.can_schedule(exam):
                room.schedule_exam(exam)
                # Recursively assign the next exam
                if self._assign_exam(exam_index + 1):
                    return True
                # Backtrack if the recursive call did not lead to a solution
                room.remove_exam(exam)
        
        # No valid room assignment found and backtrack
        return False

    def __str__(self):
        '''
        Returns a string representation of the final schedule.
        Only includes rooms with at least one scheduled exam.
        '''
        schedule_str = ""
        for room in self.rooms:
            room_str = str(room)
            if room_str:
                schedule_str += room_str + "\n"
        return schedule_str if schedule_str else "No valid schedule found."



def tester():
    '''
    Runs the scheduler on all provided exam and room files.
    '''
    # input for the file names
    exam_file = input("Enter the exam file name: ")
    room_file = input("Enter the room file name: ")
    
    schedule = Schedule()
    if not schedule.load_exams(exam_file):
        return
    if not schedule.load_rooms(room_file):
        return
    
    print("\nAttempting to create a schedule...")
    if schedule.solve():
        print("\nSchedule Found:")
        print(schedule)
    else:
        print("\nNo valid schedule is possible.")

def main():
    '''
    Main function to run the scheduler.
    '''
    
    # running the complete scheduler.
    tester()

if __name__ == "__main__":
    main()
