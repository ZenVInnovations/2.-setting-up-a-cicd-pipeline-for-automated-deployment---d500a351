# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and app code
COPY . /app

RUN apt-get update

# Install libraries
RUN pip install streamlit
RUN pip install pandas
RUN pip install numpy
RUN pip install pillow
RUN pip install scipy
RUN pip install scikit-learn

# Expose the port the app runs on
EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "stream_app.py"]
