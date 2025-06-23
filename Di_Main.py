from subprocess import call
import tkinter as tk
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image, ImageTk
from tkinter import ttk
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score


root = tk.Tk()
root.title("Disease Detection System")


root.configure(background="purple")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))

image = Image.open('Images/3d.jpg')

image = image.resize((w, h))

background_image = ImageTk.PhotoImage(image)

background_image=ImageTk.PhotoImage(image)

background_label = tk.Label(root, image=background_image)

background_label.image = background_image

background_label.place(x=0, y=0) #, relwidth=1, relheight=1)

#img=ImageTk.PhotoImage(Image.open("s1.jpg"))

#img2=ImageTk.PhotoImage(Image.open("s2.jpg"))



logo_label=tk.Label()
logo_label.place(x=0,y=0)

x = 1




  # , relwidth=1, relheight=1)
lbl = tk.Label(root, text="Disease Detection System", font=('times', 35,' bold '), height=1, width=62,bg="purple",fg="white")
lbl.place(x=0, y=0)
# _+++++++++++++++++++++++++++++++++++++++++++++++++++++++

def Model_Training():
    data = pd.read_csv("database_csv_files/Disease.csv")
    data.head()
    data = data.dropna()

    """Feature Selection => Manual"""
    x = data.drop(['Disease'], axis=1)
    data = data.dropna()

    print(type(x))
    y = data['Disease']
    print(type(y))
    x.shape
    

    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.30,random_state=23)


    from sklearn.svm import SVC
    svcclassifier = SVC(kernel='linear')
    svcclassifier.fit(x_train, y_train)

    y_pred = svcclassifier.predict(x_test)
    print(y_pred)

    
    print("=" * 40)
    print("==========")
    print("Classification Report : ",(classification_report(y_test, y_pred)))
    print("Accuracy : ",accuracy_score(y_test,y_pred)*100)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy: %.2f%%" % (accuracy * 100.0))
    ACC = (accuracy_score(y_test, y_pred) * 100)
    repo = (classification_report(y_test, y_pred))
    from sklearn.metrics import ConfusionMatrixDisplay
    ConfusionMatrixDisplay.from_estimator(svcclassifier, x_test, y_test)
    plt.show()
    
    label4 = tk.Label(root,text =str(repo),width=45,height=10,bg='khaki',fg='black',font=("Tempus Sanc ITC",14))
    label4.place(x=205,y=200)
    
    label5 = tk.Label(root,text ="Accuracy : "+str(ACC)+"%\nModel saved as svm1.joblib",width=45,height=3,bg='khaki',fg='black',font=("Tempus Sanc ITC",14))
    label5.place(x=205,y=420)
    from joblib import dump
    dump (svcclassifier,"model_train_data/svm1.joblib")
    print("Model saved as svm1.joblib")


def Model_Training1():
    data = pd.read_csv("database_csv_files/Disease.csv")
    data = data.dropna()
    
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import classification_report, accuracy_score
    from joblib import dump


    x = data.drop(['Disease'], axis=1)
    y = data['Disease']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.30, random_state=42)

    # Create a Random Forest classifier
    rf_classifier = RandomForestClassifier(n_estimators=50,max_depth=5,random_state=23)
    
    # Train the Random Forest classifier
    rf_classifier.fit(x_train, y_train)

    # Make predictions on the test set
    y_pred = rf_classifier.predict(x_test)
    print(y_pred)

    print("=" * 40)
    print("==========")
    print("Classification Report: ", classification_report(y_test, y_pred))
    print("Accuracy: ", accuracy_score(y_test, y_pred) * 100)
    
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy: %.2f%%" % (accuracy * 100.0))
    ACC = (accuracy * 100)
    print(data['Disease'].value_counts())
    
    from sklearn.model_selection import cross_val_score
    scores = cross_val_score(rf_classifier, x, y, cv=5)
    print("CV Accuracy: %.2f%%" % (scores.mean() * 100))
    
    #from sklearn.metrics import ConfusionMatrixDisplay
    #ConfusionMatrixDisplay.from_estimator(rf_classifier, x_test, y_test)
    #plt.show()



    repo = (classification_report(y_test, y_pred))

    # Update the GUI code if needed
    label4 = tk.Label(root, text=str(repo), width=45, height=10, bg='khaki', fg='black', font=("Tempus Sanc ITC", 14))
    label4.place(x=785, y=200)
    
    label5 = tk.Label(root, text="Accuracy: " + str(ACC) + "%\nModel saved as random_forest1.joblib", width=45, height=3, bg='khaki', fg='black', font=("Tempus Sanc ITC", 14))
    label5.place(x=785, y=420)

    # Save the trained Random Forest model
    dump(rf_classifier, "model_train_data/random_forest1.joblib")
    print("Model saved as random_forest1.joblib")
        
    

#def call_file():
   # import Check_carrier
   # Check_carrier.Train()

def call_file():
   from subprocess import call
   call(['python','di_check.py'])



def window():
    root.destroy()

# button2 = tk.Button(root, foreground="white", background="black", font=("Tempus Sans ITC", 14, "bold"),
#                     text="Data_Preprocessing", command=Data_Preprocessing, width=15, height=2)
# button2.place(x=5, y=120)

button3 = tk.Button(root, foreground="white", background="#152238", font=("Tempus Sans ITC", 14, "bold"),
                    text="Model_SVM", command=Model_Training, width=15, height=2)
button3.place(x=355, y=100)

button5 = tk.Button(root, foreground="white", background="#152238", font=("Tempus Sans ITC", 14, "bold"),
                    text="Model_RF", command=Model_Training1, width=15, height=2)
button5.place(x=980, y=100)

#button6 = tk.Button(root, foreground="white", background="#152238", font=("Tempus Sans ITC", 14, "bold"),
#                    text="Model_DT", command=Model_Training2, width=15, height=2)
#button6.place(x=5, y=400)
3
button4 = tk.Button(root, foreground="white", background="#152238", font=("Tempus Sans ITC", 14, "bold"),
                    text="Check", command=call_file, width=15, height=2)
button4.place(x=355, y=600)

exit = tk.Button(root, text="Exit", command=window, width=15, height=2, font=('times', 15, ' bold '),bg="red",fg="white")
exit.place(x=980, y=600)

Model_Training()
Model_Training1()
root.mainloop()

'''+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'''