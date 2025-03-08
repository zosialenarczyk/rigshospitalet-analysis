# rigshospitalet-analysis

Variable description

Descriptions of variables in “Case Rigshospitalet”  
Patientkontakt ID: ID for each appointment a patient has. Please count the number of unique 
ID’s when needing to find the sum of appointments.  
Kontakttype: the type of appointment – there are three types of appointments: 
• Fysisk fremmøde: the patient is physically present at the hospital  
• Virtuel pt.kt.: the patient is at home having a virtual appointment (either by video or 
phone)  
• Udekontakt: one or more clinical personnel is visiting the patient for an appointment at 
home  
Patientkontakttype: the type of outpatient activity the appointment is: 
• 2 Ambulant: regular outpatient activity 
• 3 Akut ambulant: Acute ambulatory activity 
• 4 Ambulant Us/Op: Outpatient activity where the patient is under observation – can 
often change into an admission (but admissions is not part of the dataset available to 
you)  
Indlæggelsesmåde: indicating the urgency of the appointment: planned or acute  
Patientkontakt start: The date and time of when the appointment started  
Patientkontakt slut: the date and time of when the appointment ended  
Kontakt varighed (timer): the duration of the appointment shown in number of hours. It’s just a 
simple calculation between the start and end of the appointment (the two variables before) to 
help some initiate navigation, but you are more than welcome to make your own calculations 
in minutes/other time measures using the same two variables.  
Behandlingsansvarlig afdeling: the name of the department responsible for the examination/ 
treatment/ care of the patient during their appointment. A patient can easily have interactions 
with personnel from different departments during their visit, but this variable indicates the 
department with the overall responsibility for the patient.  
Aktionsdiagnose: code that indicates the primary diagnosis related to the appointment (is the 
patient visiting because of a broken leg or cancer in their lungs for instance). If connected to 
the diagnosis dimension table, it is possible to use the diagnosis groups as a variable instead 
of each single code that is very specific.  
Bidiagnose: code that indicates the secondary diagnosis related to the appointment (e.g. if 
the cancer patient also has a burn on their hand while visiting). These codes function in the 
same way as describes regarding the primary diagnoses above.  
Procedurekode: code that indicates what primary procedure has been done during the 
appointment.  
Tillægskode: code that indicates the second (and sometimes third) procedure related to the 
primary procedure of the appointment.  
Behandlingskontakt ID: ID for each treatment contact a patient has during their appointment. 
One appointment can include one or more treatment contacts if the patient has one visit to 
the hospital regarding a disease, but while at the hospital both has a meeting with first a nurse 
and then a physician; that would be two treatment contacts. Please count the number of 
unique ID’s when needing to find the sum of meetings during an appointment. 
Besøgstype: type of meeting that the patient has (connected to treatment contact). This string 
indicates if the meeting is a control, examination, phone meeting etc.  
Patient ID: ID for each patient (function instead of a CPR number). Please count the number of 
unique ID’s when needing to find the sum of patients. 
Patient køn: the biological gender of the patient  
Patient alder på kontaktstart tidspunkt: the age of the patient at the time of their appointment  
Patient civilstand: describes if the patient is married or not 
Patient oprettet på Min SP (J/N): Boolean (J = Yes, N = No) describing weather or not the 
patient has downloaded and activated the app “Min SP” that allows them to see their hospital 
information and have video consultation via the app (only apply to Danish citizens).   
Patient land: the patient’s current/latest country of residence 
Patient region: the patient’s current/latest region of residence (only apply to Danish 
addresses)  
Patient postnummer: the municipality code of the patient’s current/latest residence (only 
apply to Danish addresses) 
Patient kommune: the municipality name of the patient’s current/latest residence (only apply 
to Danish addresses)
