#  Test Cases

This Readme  provides an overview of the test cases implemented in the FastAPI application. The application offers an endpoint `/identify` for identifying contacts based on email and phone number inputs.

## Test Cases

In this section, we explore various scenarios based on the presence or absence of email and phone numbers in the POST request.

| Email | Phone Number | Description                                 | Handling                                                    |
|-------|--------------|---------------------------------------------|-------------------------------------------------------------|
|   0   |      0       | Neither email nor phone number is present. | Return a `400 Bad Request` response.                       |
|   0   |      1       | Email is absent, but phone number is present. | Lookup contact using phone number and return relevant information. |
|   1   |      0       | Email is present, but phone number is absent. | Lookup contact using email and return relevant information.    |
|   1   |      1       | Both email and phone number are present.   | Handle the sub-cases. |

### When Email and Phone Number Both are Present in the POST Request:

When both email and phone number are present in the POST request (`1 1`), we'll further divide based on whether an entry[a row] of the email or phoneNumber is present in the database.

#### Email List [row entries containing `email`] and Phone List [row entries containing `phoneNumber`] Presence:

| Email List | Phone List | Description                                            | Handling                                                           |
|------------|------------|--------------------------------------------------------|--------------------------------------------------------------------|
|     0      |      0     | Entry for both email and phone number not in the DB.   | Add a new primary entry for both email and phone number.  |
|     0      |      1     | Entry for email is not in the DB, but phone number is.| Create new secondary entry with phone number and return relevant information. |
|     1      |      0     | Entry for email is in the DB, but phone number isn't.| Create new secondary entry with email and return relevant information.       |
|     1      |      1     | Entries for both email and phone number are in the DB.| Handle the sub-cases.    |

#### Entries For Both Phone Number and Email are Also Present in the Database:

In this scenario, we have three sub-cases:

1. **Case 1:** Only 1 entry is present in the DB which exactly matches both the phone number and email. We update its `updatedAt` column and return its corresponding response.

2. **Case 2:** All rows resulting from the query have the same `linkedId` column values. We add a new secondary entry using the provided information and return its corresponding response.

3. **Case 3:** All rows resulting from the query have different `linkedId` column values. In this scenario, we need to merge the entries to ensure the contacts are properly linked. Here's how we handle it:

   - Identify the linked IDs from the query results.
   - Determine which primary contact corresponding to all the linked IDs was created first.
   - Update the linked IDs and link precedence accordingly:
     - Change the primary contact which is linked to the linked ID which is not the first one to secondary.
     - Change the linked IDs of its corresponding secondary rows to point to the first created linked ID.
   - Return the relevant response based on the merged entries.

## Running the Application

To run the application, follow these steps:

1. Install the required packages by running the following command in your terminal:

    ```shell
    $ pip install -r requirements.txt
    ```

2. Run the `load_db_data.py` script to create the database and load initial data:

    ```shell
    $ python load_db_data.py
    ```

   This will set up the SQLite database with initial data for testing.

3. Start the FastAPI server using the following `uvicorn` command:

    ```shell
    $ uvicorn main:app --reload
    ```


4. Open your web browser and go to the following URL to explore the API documentation and test the endpoints:

   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

   This interactive documentation provides details about the endpoints and allows you to send test requests.
