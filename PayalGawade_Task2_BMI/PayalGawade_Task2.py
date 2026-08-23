# OIBSIP - Task 2 - BMI Calculator - Intern Payal Gawade
def calculate_bmi(weight, height):
    return weight / (height ** 2)

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi <= 24.9:
        return "Normal Weight"
    elif 25 <= bmi <= 29.9:
        return "Overweight"
    else:
        return "Obese"

def main():
    print("------ OIBSIP BMI Calculator ------")
    try:
        weight = float(input("Enter weight in kg: "))
        height = float(input("Enter height in meters: "))
        if weight <= 0 or height <= 0:
            print("Error: Weight and height must be positive.")
            return
        bmi = calculate_bmi(weight, height)
        category = classify_bmi(bmi)
        print(f"\nYour BMI is: {round(bmi, 2)}")
        print(f"Category: {category}")
    except ValueError:
        print("Error: Please enter numbers only.")

if __name__ == "__main__":
    main()
