#!/usr/bin/env python

from bwi_msgs.srv import QuestionDialog
import rospy
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))
from agent.simulator import Simulator
import time


class DialogManager(Simulator):
    def __init__(self):
        super(DialogManager,self).__init__()
        self.logfile = open("log.txt", w)
        self.counter = 0

    def get_string(self, question):
        rospy.wait_for_service('question_dialog')
        handle = rospy.ServiceProxy('question_dialog', QuestionDialog)
        response = handle(2, question, [], 200)
        self.logfile.write("QUESTION: "+question+"\n")
        self.logfile.write("ANSWER: "+response+"\n")
        self.counter += 1
        return response.text

    def print_message(self, message):
        rospy.wait_for_service('question_dialog')
        handle = rospy.ServiceProxy('question_dialog', QuestionDialog)
        response = handle(0, message, [], 200)
        self.logfile.write("MESSAGE: "+message+"\n")

    def close_log(self):
        self.logfile.write("\n Conversation Length: "+str(self.counter))
        self.logfile.close()

    def check_success(self):
        rospy.wait_for_service('question_dialog')
        handle = rospy.ServiceProxy('question_dialog', QuestionDialog)
        response = handle(1, "The Experiment is now over.  Thank you for participating. Please choose whether the robot chose the correct task to execute.",
                    ['Yes', 'No'], 200)
        self.logfile.write("SUCCESS: "+response+"\n")


def main():
    # the number of variables are stored in this file for now
    f = open("../agent/data/num_config.txt")
    num = f.readline().split()

    s = DialogManager(uniform_init_belief = True, 
        auto_state = True, 
        auto_observations = False, # was true
        print_flag = False, 
        policy_file = 'main_new.policy', 
        pomdp_file =  'main_new.pomdp',
        policy_file_plus = 'main_plus_new.policy',
        pomdp_file_plus = 'main_plus_new.pomdp',
        trials_num = 1,
        num_task = int(num[0]), 
        num_patient = int(num[1]), 
        num_recipient = int(num[2]),
        belief_threshold = 0.4,
        ent_threshold = 2)
 
    if not s.uniform_init_belief:   
        print('note that initial belief is not uniform\n')

    ##s.run_numbers_of_trials()
    s.run()
    time.sleep(5)
    s.check_success()
    s.close_log()

if __name__ == '__main__':
    main()