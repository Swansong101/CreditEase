import pymysql
import logging
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import decimal 

# Initialize logger
logger = logging.getLogger(__name__)

# Database connection helper function
def get_db_connection():
    try:
        return pymysql.connect(
            host="localhost",
            user="mysqlUser",
            password="mysqlPassword",
            database="rasa_db",
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.MySQLError as e:
        logger.exception("Database connection failed")  # Log full exception with traceback
        return None  # Explicitly return None if connection fails


class ActionCheckUser(Action):
    def name(self) -> str:
        return "action_check_user"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        user_id = tracker.get_slot("id_number")

        # Clean the ID number input
        if user_id:
            user_id = user_id.replace("My ID is ", "").strip()
        else:
            dispatcher.utter_message("Please provide a valid ID.")
            return []

        try:
            connection = get_db_connection()
            if connection is None:
                dispatcher.utter_message("Could not establish a connection to the database.")
                return []

            with connection:
                with connection.cursor() as cursor:
                    sql_query = "SELECT full_name FROM credit_ease_users WHERE id_number = %s"
                    cursor.execute(sql_query, (user_id,))
                    result = cursor.fetchone()

                    if result:
                        full_name = result["full_name"]
                        # Set the slot and respond once
                        dispatcher.utter_message(text=f"Hello, {full_name}! Welcome back!")
                        return [SlotSet("full_name", full_name)]
                    
                    else:
                        dispatcher.utter_message("It seems you are not registered in our system. Would you like to register?")
                        return []

        except pymysql.MySQLError as e:
            logger.exception("Error fetching user from database.")
            dispatcher.utter_message(text="A database error occurred. Please try again later.")
            return []


class ActionCreateUser(Action):
    def name(self) -> str:
        return "action_create_user"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        user_id = tracker.get_slot("id_number")
        full_name = tracker.get_slot("full_name")
        employment_status = tracker.get_slot("employment_status")
        monthly_income = tracker.get_slot("monthly_income")
        additional_income = tracker.get_slot("additional_income")

        # Input validation
        if not user_id or len(user_id) > 50:
            dispatcher.utter_message("Invalid ID number. Please provide a valid ID.")
            return []
        if not full_name or len(full_name) > 255:
            dispatcher.utter_message("Invalid name. Please provide a valid full name.")
            return []
        try:
            monthly_income = float(monthly_income)
            additional_income = str(additional_income) if additional_income else ""
        except (ValueError, TypeError):
            dispatcher.utter_message("Invalid income values. Please provide valid numeric values.")
            return []

        try:
            connection = get_db_connection()
            if connection is None:
                dispatcher.utter_message("Could not establish a connection to the database.")
                return []

            with connection:  # Manage database connection
                with connection.cursor() as cursor:
                    sql_query = """
                    INSERT INTO credit_ease_users (full_name, id_number, employment_status, monthly_income, additional_income)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    # Debugging: Log the data being inserted
                    logger.debug(f"Inserting user with details: {full_name}, {user_id}, {employment_status}, {monthly_income}, {additional_income}")

                    cursor.execute(sql_query, (full_name, user_id, employment_status, monthly_income, additional_income))
                    connection.commit()

                    dispatcher.utter_message(text=f"User {full_name} has been successfully registered.")
                    return [SlotSet("full_name", full_name)]

        except pymysql.MySQLError as e:
            logger.exception("Error creating user in the database.")  # Log full exception with traceback
            dispatcher.utter_message(text="A database error occurred while creating your profile. Please try again later.")
            return []

class ActionEvaluateLoanEligibility(Action):
    def name(self) -> str:
        return "action_evaluate_loan_eligibility"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        # Get the id_number slot value
        user_id = tracker.get_slot("id_number")

        logger.debug(f"Evaluating loan eligibility for ID: {user_id}")

        # Validate ID number
        if not user_id or not user_id.startswith("ID"):
            dispatcher.utter_message("Invalid ID number. Please provide a valid ID to proceed.")
            return []

        try:
            connection = get_db_connection()
            if connection is None:
                dispatcher.utter_message("Could not establish a connection to the database.")
                return []

            with connection.cursor() as cursor:
                # Fetch user details from the database
                sql_query = """
                SELECT full_name, monthly_income, additional_income, delinquency_status, 
                       existing_loans, loan_amount, repayment_period
                FROM credit_ease_loans
                WHERE id_number = %s
                """
                cursor.execute(sql_query, (user_id,))
                user_data = cursor.fetchone()

                if not user_data:
                    dispatcher.utter_message("User not found in the system.")
                    return []

                # Extract user data and ensure proper casting
                full_name = user_data["full_name"]  # VARCHAR
                monthly_income = float(user_data["monthly_income"] or 0)  # DECIMAL
                additional_income_description = user_data["additional_income"] or "None"  # VARCHAR
                delinquency_status = int(user_data["delinquency_status"])  # TINYINT
                existing_loans_description = user_data["existing_loans"] or "None"  # TEXT
                loan_amount = float(user_data["loan_amount"] or 0)  # DECIMAL
                repayment_period = user_data["repayment_period"]
                if isinstance(repayment_period, decimal.Decimal):
                    repayment_period= float(repayment_period)

                # Evaluate eligibility
                total_income = monthly_income  # Only using monthly_income for numeric evaluation

                if delinquency_status == 1:
                    dispatcher.utter_message(
                        f"Unfortunately, {full_name}, we cannot approve your loan application due to a delinquency on your account."
                    )
                    return []

                # Example decision logic for loan eligibility
                if loan_amount > (total_income * repayment_period) / 12:
                    dispatcher.utter_message(
                        f"Unfortunately, {full_name}, the requested loan amount of Ksh. {loan_amount} exceeds the maximum allowable limit based on your income."
                    )
                    return []

                # If all conditions are met
                dispatcher.utter_message(
                    f"Congratulations, {full_name}! Your loan application for Ksh. {loan_amount} has been approved. "
                    f"Based on your income of Ksh. {monthly_income} and a repayment period of {repayment_period} months, you meet the eligibility criteria. "
                    f"Additional income source noted as '{additional_income_description}', and existing loans include '{existing_loans_description}'."
                )
                return []

        except pymysql.MySQLError as e:
            logger.exception("Error evaluating loan eligibility.")
            dispatcher.utter_message("A database error occurred. Please try again later.")
            return []
