import traceback
import sys

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = self.get_detalied_error_message(error_message,error_detail) # Initialize the base Exception class with the error message

    @staticmethod # Static method to get detailed error message
    def get_detalied_error_message(error_message, error_detail:sys):
        _,_, exc_tb = traceback.sys.exc_info() # Get the traceback information
        file_name = exc_tb.tb_frame.f_code.co_filename # Get the file name where the exception occurred
        line_number = exc_tb.tb_lineno # Get the line number where the exception occurred
        return f"Error in {file_name}, line {line_number}:{error_message}"  # Format the detailed error message
    
    def __str__(self):
        return self.error_message
    
# This code defines a custom exception class that captures detailed error information including the file name and line number where the exception occurred.
