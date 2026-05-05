from flask import render_template

def home():
    return render_template('home.html')

def pet_plan():
    return render_template('pet-plan.html')

def care_cost_support():
    return render_template('care_cost_support.html')

def about():
    return render_template('about.html')

def sign_in():
    return render_template('sign-in.html')
