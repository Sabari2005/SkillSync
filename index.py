
from bottle import Bottle,get,route,redirect, request, template, run, static_file
import pdfplumber
import pandas as pd
from bottle import static_file
import subprocess
import os
import csv
import os
import spacy
from spacy.tokens import DocBin
import pandas as pd
from fuzzywuzzy import fuzz
from load_modelbest import nlp
import shutil

app = Bottle()

@app.route('/')
def upload_form():
    return template('template/index')

@app.route('/company', method=['POST', 'GET'])
def company():
    if request.method=='POST':
        redirect('/company')
    else:
        return "this is comppany page"
@app.route('/company')
def individual():
    return template('template/company')

@app.route('/individual', method=['POST', 'GET'])
def company():
    if request.method=='POST':
        redirect('/individual_only')
    else:
        return template('template/individual')
@app.route('/individual_only')
def individual_only():
    return template('template/individual')

@app.route('/upload', method='POST')
def do_upload():
    csv_file = request.files.get('csv_file')
    pdf_file = request.files.get('pdf_file')
    def copy_file(upload,copy_path):
        try:
            with open(copy_path,'wb') as f:
                shutil.copyfileobj(upload.file,f)
            return True
        except Exception as e:
            return False
    if csv_file:
        copy_path=r'.\download\uploaded_file.csv'
        copy_file(csv_file,copy_path)
    if csv_file and pdf_file:
        # Process the PDF file
        with pdfplumber.open(pdf_file.file) as pdf:
            pdf_text = ''
            for page in pdf.pages:
                pdf_text += page.extract_text()
    else:
        return "Please upload both CSV and PDF files."

    def result(text,csv_file):
        text=text
        doc=nlp(text)
        my_dict={}
        for ent in doc.ents:
            key = ent.label_
            value = ent.text
            if key.strip() in my_dict:
                my_dict[key.strip()].append(value)
            else:
                my_dict[key.strip()] = [value]
        name=[]
        my_dict =my_dict
        for key,value in my_dict.items():
                if key=="NAME":
                    print("\nNAME:",end=" ")
                    print(value[0])
                    name.append(value[0])
                else:
                    pass
        print("\nEDUCATION:\n")
        education=[]
        for key,value in my_dict.items():
                if key=="DEGREE":
                    for i in range(0,len(value)):
                        print("\t",value[i],end='\n')
                        education.append(value[i])
                if key=="EDUCATION":
                    for i in range(0,len(value)):
                        print("\t",value[i],end='\n')
                        education.append(value[i])
        a1=[]
        for key,value in my_dict.items():
                if (key=="WORKED AS"):
                    a1=value
        print("\n")
        def extract_skills(text, skills_list):
            text = text.lower()
            extracted_skills = []
            for skill in skills_list:
                skill = skill.lower()
                if skill in text:
                    extracted_skills.append(skill)
            return extracted_skills
        skills_list = ["Python", "Java", "C", "C++", "C#", "Ruby", "JavaScript", "TypeScript", "PHP", "Swift", "Kotlin", "Go", "Rust", "Dart", "Scala", "HTML", "CSS", "Ruby on Rails", "Django", "Flask", "Laravel", "ASP.NET", "Haskell", "Erlang", "Clojure", "Elixir", "F#", "Perl", "Lua", "Shell Scripting", "XML", "Markdown", "LaTeX", "R", "Julia", "MATLAB", "React Native", "Xamarin", "Assembly Language", "VHDL", "Verilog", "SQL", "PL/SQL", "T-SQL", "CQL", "Solidity", "Vyper", "Apex", "ABAP", "Prolog", "Lisp", "Smalltalk", "OCaml", "Scheme", "Groovy", "Objective-C", "Fortran", "Pascal", "Ada", "COBOL", "Assembly", "AWK", "Sed", "Logo", "Scratch", "SAS", "SPSS", "D", "Delphi", "LabVIEW", "Lisp", "Mercury", "Modula-2", "Nim", "Powershell", "Racket", "REXX", "Simula", "Tcl", "Visual Basic", "Wolfram Language", "XQuery", "YAML", "Zsh", "Algol", "APL", "BASIC", "ColdFusion", "Common Lisp", "Crystal", "Dylan", "Elm", "Emacs Lisp", "Erlang", "Factor", "Fantom", "Forth", "Hack", "Haxe", "Io", "J", "Janet", "Kotlin/Native", "KRL", "Leda", "LiveScript", "ML", "Modula-3", "Oak", "OCaml", "Pico", "Pike", "PostScript", "PowerShell", "PureScript", "Q#", "Raku (formerly Perl 6)", "REBOL", "Red", "Ring", "Rust", "Scala", "Scheme", "SNOBOL", "Swift", "TypeScript", "Vala", "Vimscript", "Visual Basic .NET"]
        advanced_technical_skills = ["Hadoop", "Apache Spark", "Apache Kafka", "HBase", "Apache Cassandra", "Apache Flink", "Apache Hive", "MapReduce", "Pig", "Apache Drill", "Continuous Integration/Continuous Deployment (CI/CD)", "Jenkins", "Ansible", "Docker", "Kubernetes", "Terraform", "Puppet", "Chef", "GitOps", "Infrastructure as Code (IaC)", "Ethereum", "Solidity", "Hyperledger Fabric", "Smart Contracts", "Cryptography", "Distributed Ledger Technology (DLT)", "Consensus Mechanisms (e.g., Proof of Work, Proof of Stake)", "Decentralized Applications (DApps)", "Tokenization", "Ethical Hacking", "Penetration Testing", "Network Security", "Cryptography", "Security Information and Event Management (SIEM)", "Intrusion Detection Systems (IDS)", "Security Operations Center (SOC)", "Incident Response", "Threat Intelligence", "Identity and Access Management (IAM)", "Amazon Web Services (AWS)", "Microsoft Azure", "Google Cloud Platform (GCP)", "Serverless Computing", "Microservices Architecture", "Multi-cloud Management", "Cloud Security", "Data Analysis", "Machine Learning Algorithms (e.g., Linear Regression, Decision Trees, Random Forest, SVM, Neural Networks)", "Deep Learning (e.g., Convolutional Neural Networks, Recurrent Neural Networks)", "Natural Language Processing (NLP)", "Computer Vision", "Reinforcement Learning", "Feature Engineering", "Model Evaluation and Validation", "Model Deployment", "TensorFlow", "PyTorch", "Scikit-learn", "Apache Spark MLlib"]
        general_skills = extract_skills(text, skills_list)
        predicted_skills = extract_skills(text,advanced_technical_skills)
        full_list=[]
        if len(general_skills)>0:
            print("\nGENERAL SKILLS:\n")
            for item in general_skills:
                if (len(general_skills)<=1):
                    print(item, end="")
                    full_list.append(item)
                else:
                    print(item, end=", ")
                    full_list.append(item)
                print("\n")
        else:
            pass
        if len(predicted_skills)>0:
            print("\nPREDICTED SKILLS:\n")
            for item in predicted_skills:
                if (len(predicted_skills)<=1):
                    print(item, end="")
                    full_list.append(item)
                else:
                    print(item, end=", ")
                    full_list.append(item)
                print("\n")
            else:
                pass
        import csv
        def get_text_lists_from_third_column(csv_file):
            text_lists = []
            with open(csv_file, newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if len(row) >= 3:
                        text_elements = [element.strip() for element in row[2].split(',')]
                        text_lists.append(text_elements)
            return text_lists
        csv_file_path = csv_file
        text_lists = get_text_lists_from_third_column(csv_file_path)
        your_list = full_list

        machlist=[]
        def count_matches_with_csv_lists(your_list,text_lists):
            for i, text_lists in enumerate(text_lists, 1):
                matched_count = sum(1 for element in your_list if element in text_lists)
                machlist.append(matched_count)
        count_matches_with_csv_lists(your_list, text_lists)
        intlist=[]
        def display_integers_from_fourth_column(csv_file):
            with open(csv_file, newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if len(row) >= 4:
                        try:
                            integer_value = int(row[3])
                            intlist.append(integer_value)
                        except ValueError:
                            pass
        display_integers_from_fourth_column(csv_file_path)
        over=[]
        for i in range(0,len(intlist)):
            if (machlist[i]>=intlist[i]):
                over.append(i)
            else:
                pass
        temp_list=[]
        def display_text_from_columns(csv_file, row_numbers):
            with open(csv_file, newline='') as csvfile:
                reader = csv.reader(csvfile)
                for i, row in enumerate(reader):
                    if i + 1 in row_numbers:
                        if len(row) >= 2:
                            print(row[0], row[1])
                            temp_list.append(row[1])
                        else:
                            print(f"Row {i+1} does not have enough columns")
            return temp_list
        row_numbers_to_display = over
        a=display_text_from_columns(csv_file_path, row_numbers_to_display)
        name=" ".join(name)
        full_list=",".join(full_list)
        a=" ".join(a)
        education=" ,".join(education)
        return name,education,full_list,a
    text=pdf_text
    csv_file=r".\download\uploaded_file.csv"
    nae,edu,skill_list,resut=result(text,csv_file)
    return template('template/output',pdf_text=resut,education=edu,naming=nae,skills=skill_list)
    
@app.route('/upload_individual', method='POST')
def do_upload():
    pdf_file = request.files.get('pdf_file')
    def result(text):
        text=text
        doc=nlp(text)
        my_dict={}
        for ent in doc.ents:
            key = ent.label_
            value = ent.text
            if key.strip() in my_dict:
                my_dict[key.strip()].append(value)
            else:
                my_dict[key.strip()] = [value]
        my_dict =my_dict
        name=[]
        for key,value in my_dict.items():
                if key=="NAME":
                    print("\nNAME:",end=" ")
                    print(value[0])
                    name.append(value[0])
                else:
                    pass
        education=[]
        print("\nEDUCATION:\n")
        for key,value in my_dict.items():
                if key=="DEGREE":
                    for i in range(0,len(value)):
                        print("\t",value[i],end='\n')
                        education.append(value[i])
                if key=="EDUCATION":
                    for i in range(0,len(value)):
                        print("\t",value[i],end='\n')
                        education.append(value[i])
        a1=[]
        for key,value in my_dict.items():
                if (key=="WORKED AS"):
                    a1=value
        print("\n")
        def extract_skills(text, skills_list):
            text = text.lower()
            extracted_skills = []
            for skill in skills_list:
                skill = skill.lower()
                if skill in text:
                    extracted_skills.append(skill)

            return extracted_skills
        skills_list = ["Python", "Java", "C", "C++", "C#", "Ruby", "JavaScript", "TypeScript", "PHP", "Swift", "Kotlin", "Go",
                    "Rust", "Dart", "Scala", "HTML", "CSS", "Ruby on Rails", "Django", "Flask", "Laravel", "ASP.NET",
                    "Haskell", "Erlang", "Clojure", "Elixir", "F#", "Perl", "Lua", "Shell Scripting", "XML", "Markdown",
                    "LaTeX", "R", "Julia", "MATLAB", "React Native",
                    "Xamarin", "Assembly Language", "VHDL", "Verilog", "SQL", "PL/SQL",
                    "T-SQL", "CQL", "Solidity", "Vyper", "Apex", "ABAP", "Prolog", "Lisp",
                    "Smalltalk", "OCaml", "Scheme", "Groovy", "Objective-C", "Fortran",
                    "Pascal", "Ada", "COBOL", "Assembly", "AWK", "Sed", "Logo", "Scratch",
                    "SAS", "SPSS", "D", "Delphi", "LabVIEW", "Lisp", "Mercury", "Modula-2",
                    "Nim", "Powershell", "Racket", "REXX", "Simula", "Tcl", "Visual Basic",
                    "Wolfram Language", "XQuery", "YAML", "Zsh", "Algol", "APL", "BASIC",
                    "ColdFusion", "Common Lisp", "Crystal", "Dylan", "Elm", "Emacs Lisp",
                    "Erlang", "Factor", "Fantom", "Forth", "Hack", "Haxe", "Io", "J",
                    "Janet", "Kotlin/Native", "KRL", "Leda", "LiveScript", "ML", "Modula-3",
                    "Oak", "OCaml", "Pico", "Pike", "PostScript", "PowerShell", "PureScript",
                    "Q#", "Raku (formerly Perl 6)", "REBOL", "Red", "Ring", "Rust", "Scala",
                    "Scheme", "SNOBOL", "Swift", "TypeScript", "Vala", "Vimscript", "Visual Basic .NET"]

        advanced_technical_skills = [
            # Big Data
            "Hadoop",
            "Apache Spark",
            "Apache Kafka",
            "HBase",
            "Apache Cassandra",
            "Apache Flink",
            "Apache Hive",
            "MapReduce",
            "Pig",
            "Apache Drill",

            # DevOps
            "Continuous Integration/Continuous Deployment (CI/CD)",
            "Jenkins",
            "Ansible",
            "Docker",
            "Kubernetes",
            "Terraform",
            "Puppet",
            "Chef",
            "GitOps",
            "Infrastructure as Code (IaC)",

            # Blockchain
            "Ethereum",
            "Solidity",
            "Hyperledger Fabric",
            "Smart Contracts",
            "Cryptography",
            "Distributed Ledger Technology (DLT)",
            "Consensus Mechanisms (e.g., Proof of Work, Proof of Stake)",
            "Decentralized Applications (DApps)",
            "Tokenization",

            # Cybersecurity
            "Ethical Hacking",
            "Penetration Testing",
            "Network Security",
            "Cryptography",
            "Security Information and Event Management (SIEM)",
            "Intrusion Detection Systems (IDS)",
            "Security Operations Center (SOC)",
            "Incident Response",
            "Threat Intelligence",
            "Identity and Access Management (IAM)",

            # Cloud Computing
            "Amazon Web Services (AWS)",
            "Microsoft Azure",
            "Google Cloud Platform (GCP)",
            "Serverless Computing",
            "Microservices Architecture",
            "Multi-cloud Management",
            "Cloud Security",

            # Data Science and Machine Learning
            "Data Analysis",
            "Machine Learning Algorithms (e.g., Linear Regression, Decision Trees, Random Forest, SVM, Neural Networks)",
            "Deep Learning (e.g., Convolutional Neural Networks, Recurrent Neural Networks)",
            "Natural Language Processing (NLP)",
            "Computer Vision",
            "Reinforcement Learning",
            "Feature Engineering",
            "Model Evaluation and Validation",
            "Model Deployment",
            "TensorFlow",
            "PyTorch",
            "Scikit-learn",
            "Apache Spark MLlib"
        ]
        general_skills = extract_skills(text, skills_list)
        predicted_skills = extract_skills(text,advanced_technical_skills)
        full_list=[]
        if len(general_skills)>0:
            print("\nGENERAL SKILLS:\n")
            for item in general_skills:
                if (len(general_skills)<=1):
                    print(item, end="")
                    full_list.append(item)
                else:
                    print(item, end=", ")
                    full_list.append(item)
                print("\n")
        else:
            pass
        if len(predicted_skills)>0:
            print("\nPREDICTED SKILLS:\n")
            for item in predicted_skills:
                if (len(predicted_skills)<=1):
                    print(item, end="")
                    full_list.append(item)
                else:
                    print(item, end=", ")
                    full_list.append(item)
                print("\n")
            else:
                pass
        import csv
        def get_text_lists_from_third_column(csv_file):
            text_lists = []
            with open(csv_file, newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if len(row) >= 3:
                        text_elements = [element.strip() for element in row[2].split(',')]
                        text_lists.append(text_elements) 
            return text_lists
        csv_file_path = r'.\onet_dataset\onet.csv'
        text_lists = get_text_lists_from_third_column(csv_file_path)
        your_list = full_list
        machlist=[]
        def count_matches_with_csv_lists(your_list,text_lists):
            for i, text_lists in enumerate(text_lists, 1):
                matched_count = sum(1 for element in your_list if element in text_lists)
                machlist.append(matched_count)
        count_matches_with_csv_lists(your_list, text_lists)
        intlist=[]
        def display_integers_from_fourth_column(csv_file):
            with open(csv_file, newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if len(row) >= 4:
                        try:
                            integer_value = int(row[3])
                            intlist.append(integer_value)
                        except ValueError:
                            pass
        display_integers_from_fourth_column(csv_file_path)
        over=[]
        for i in range(0,len(intlist)):
            if (machlist[i]>=intlist[i]):
                over.append(i)
            else:
                pass
        temp_list=[]
        def display_text_from_columns(csv_file, row_numbers):
            with open(csv_file, newline='') as csvfile:
                reader = csv.reader(csvfile)
                for i, row in enumerate(reader):
                    if i in row_numbers:
                        if len(row) >= 2:
                            print(row[0], row[1])
                            temp_list.append(row[1])
                        else:
                            print(f"Row {i} does not have enough columns")
            return temp_list
        row_numbers_to_display = over
        a=display_text_from_columns(csv_file_path, row_numbers_to_display)
        name=" ".join(name)
        full_list=",".join(full_list)
        a=" ,".join(a)
        education=" ,".join(education)
        return name,education,full_list,a

    if  pdf_file:
        # Process the PDF file
        with pdfplumber.open(pdf_file.file) as pdf:
            pdf_text = ''
            for page in pdf.pages:
                pdf_text += page.extract_text()

        # Process the CSV file
    
    nae,edu,skill_list,resut=result(pdf_text)
        # Render the index.html template with processed data
    return template('template/output',pdf_text=resut,education=edu,naming=nae,skills=skill_list)


if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)
